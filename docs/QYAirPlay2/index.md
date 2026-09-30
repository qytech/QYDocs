# QYAirPlay2 Android SDK <img src="https://img.shields.io/badge/★_推荐-Recommended-success?style=flat-square" alt="推荐" style="vertical-align: middle;">

[![Maven Central](https://img.shields.io/maven-central/v/io.github.qytech/qyairplay2.svg)](https://central.sonatype.com/artifact/io.github.qytech/qyairplay2)

QYAirPlay2 为 Android 设备提供局域网 AirPlay 音频接收与播放、歌曲信息与封面，以及对手机的播放控制。接入入口为 `com.qytech.airplay.QYAirPlay2`。

> 当前版本：`0.1.0`（2026-09-30）。版本变化见[更新日志](CHANGELOG.md)。

## 1. 环境与依赖

- Android API 29+，当前仅提供 `arm64-v8a`。
- 手机与设备处于可互通的局域网。
- 默认接收端口为 `7000`；启用前确认端口未被其他服务占用。
- 设备须完成下方 UDP 319/320 配置；安装 AAR 或 APK 不会修改低端口权限。

```kotlin
dependencies {
    implementation("io.github.qytech:qyairplay2:0.1.0")
}
```

SDK 已声明以下权限，接入 AAR 时会自动合并到 App 清单：

- 网络访问：`INTERNET`、`ACCESS_NETWORK_STATE`、`CHANGE_WIFI_MULTICAST_STATE`。
- 前台播放服务：`FOREGROUND_SERVICE`、`FOREGROUND_SERVICE_MEDIA_PLAYBACK`。

## 2. 固件配置：允许 UDP 319/320

AirPlay 2 的时钟同步需要由接收 App 绑定 **UDP 319 和 320**。固件应将 `/proc/sys/net/ipv4/ip_unprivileged_port_start` 设为 `319`。

该设置调整整个网络命名空间的非特权端口起点，并非只放行两个 UDP 端口。普通 App 不能自行写入此值；system UID 本身也不等于具备低端口绑定能力。权限含义见 [Linux 内核文档](https://www.kernel.org/doc/html/latest/networking/ip-sysctl.html#ip-variables)。

### 固件永久配置

以下补丁适用于 RK356X 固件的 `device/rockchip/rk356x/init.rk356x.rc`，加到现有 `on init` 段：

```diff
--- a/device/rockchip/rk356x/init.rk356x.rc
+++ b/device/rockchip/rk356x/init.rk356x.rc
@@ -78,3 +78,5 @@
 on init
+    # AirPlay 2 PTP uses UDP ports 319 and 320.
+    write /proc/sys/net/ipv4/ip_unprivileged_port_start 319
     # Increased power consumption and CPU in exchange for memory
     write /proc/sys/vm/swappiness 100
```

该配置由 `device/rockchip/rk356x/device.mk` 安装到 `/vendor/etc/init/hw/init.rk356x.rc`。重新编译并烧录包含此文件的 vendor 镜像，重启后验证。其他平台应修改实际加载的 vendor init 文件，并确认后续启动脚本没有覆盖该值。

UDP 319/320 应由接收 App 独占；不要另外启动占用这两个端口的 `airplay2d` 或 NQPTP 服务。

### ADB 临时设置

以下命令用于支持 `adb root` 的调试固件。多设备连接时，在每条命令的 `adb` 后加 `-s <设备序列号>`。

```powershell
adb root
adb wait-for-device
adb shell cat /proc/sys/net/ipv4/ip_unprivileged_port_start
adb shell "echo 319 > /proc/sys/net/ipv4/ip_unprivileged_port_start"
adb shell cat /proc/sys/net/ipv4/ip_unprivileged_port_start
```

最后一条应输出 `319`。临时写入在重启后失效；若生产固件不允许 `adb root`，需由固件方集成永久配置。命令说明见 [ADB 官方文档](https://android.googlesource.com/platform/packages/modules/adb/+/refs/heads/main/docs/user/adb.1.md)。

### 重启与监听验证

安装永久配置后执行：

```powershell
adb reboot
adb wait-for-device
adb shell getprop sys.boot_completed
adb shell cat /proc/sys/net/ipv4/ip_unprivileged_port_start
```

待 `sys.boot_completed` 为 `1` 后，确认端口阈值仍为 `319`。启动 App 的 AirPlay 接收功能，再查看监听：

```powershell
adb shell ss -lunp
```

确认 `:319`、`:320` 均有 UDP 监听，且由接收 App 持有。无进程信息时，可在调试固件上先执行 `adb root` 再查看。

阈值正确但绑定失败时，检查端口占用与 SELinux 拒绝日志；已经监听但手机无法发现或播放时，检查局域网组播、设备防火墙及会话协商端口。上述 sysctl 不会自动放行防火墙或绕过 [SELinux 策略](https://source.android.com/docs/security/features/selinux)。

## 3. 启动、状态与停止

在 App 启用 AirPlay 功能时启动，`deviceName` 是手机 AirPlay 列表中显示的名称：

```kotlin
import com.qytech.airplay.QYAirPlay2

QYAirPlay2.start(
    context = context,
    deviceName = "HiFi AirPlay",
    port = 7000,
)
```

在 Activity 或 Fragment 中，使用已有的生命周期作用域观察状态：

```kotlin
import androidx.lifecycle.lifecycleScope
import kotlinx.coroutines.flow.collect
import kotlinx.coroutines.launch

lifecycleScope.launch {
    QYAirPlay2.state.collect { state ->
        println("连接: ${state.isConnected}, 播放: ${state.playbackStatus}")
        println("曲目: ${state.title} - ${state.artist}")
        println("进度: ${state.positionMs}/${state.durationMs} ms")
        println("音量: ${state.volumePercent}%")
        // 显示 state.coverBitmap；为 null 时清除旧封面。
    }
}
```

关闭 AirPlay 功能时停止接收：

```kotlin
QYAirPlay2.stop()
```

`start()`、`stop()` 可在主线程调用，均异步完成。用 `state.isRunning` 确认运行状态，用 `state.lastError` 查看错误；方法返回不表示发送端已经连接或开始播放。

运行期间更改设备名、端口或音量模式时，先调用 `stop()`，等待 `state.isRunning == false` 后再 `start()`。状态收集与监听器应随宿主页面或服务的生命周期释放。

### 前台服务模式

需要库自带的前台服务时，成对使用：

```kotlin
QYAirPlay2.startService(context, "HiFi AirPlay", 7000)

// 不再接收时
QYAirPlay2.stopService(context)
```

前台服务使用默认软件音量模式。由已有播放服务管理生命周期或硬件音量的宿主，直接使用 `start()` / `stop()`。宿主需按目标 Android 版本处理通知权限，并在系统允许的时机启动前台服务。

## 4. 手机音量控制设备音量

默认 `start(context, deviceName, port)` 使用软件音量。设备已有硬件音量控制时，关闭软件音量，并在三参数 `onVolumeChanged` 回调中设置设备音量：

```kotlin
import com.qytech.airplay.QYAirPlay2Listener
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.launch

val listener = object : QYAirPlay2Listener {
    override fun onVolumeChanged(
        volumeDb: Double,
        volumePercent: Float,
        isCurrent: () -> Boolean,
    ) {
        // hostScope 和 writeDeviceVolume 由宿主提供。
        hostScope.launch(Dispatchers.IO) {
            // 如需等待设备、队列或锁，先完成等待。
            if (!isCurrent()) return@launch
            writeDeviceVolume(volumePercent) // 在此处实际写入硬件。
        }
    }
}

// 在主线程注册。
QYAirPlay2.addListener(listener)
QYAirPlay2.start(
    context = context,
    deviceName = "HiFi AirPlay",
    port = 7000,
    softwareVolumeEnabled = false,
)

// 宿主关闭功能时：
QYAirPlay2.removeListener(listener)
QYAirPlay2.stop()
```

音量事件回调在主线程派发，硬件读写应放工作线程。**在真正写硬件前检查 `isCurrent()`**；若硬件接口内部还会排队、等待锁或先读取设备，必须在这些等待结束后、实际写入前再次检查，丢弃已断开或被另一手机接管的旧请求。该检查不能撤销已经开始的硬件写入。

关闭软件音量后，SDK 不代替宿主调节硬件音量。不要从注册时的初始状态或每次状态更新无条件写硬件；设备音量应跟随有效的 `onVolumeChanged` 事件。原双参数音量回调仍可用于界面显示。

## 5. 播放控制与回调

下列方法按需放入对应按钮操作中：

| 方法 | 用途 |
|---|---|
| `play()` / `pause()` | 请求手机恢复 / 暂停播放 |
| `togglePlayPause()` | 切换播放与暂停 |
| `next()` / `previous()` | 下一首 / 上一首 |
| `seekTo(30_000L)` | 跳转到 30 秒，参数单位为毫秒 |
| `setVolumePercent(60f)` | 音量百分比，范围 0..100 |
| `setVolume(-15.0)` | 音量分贝值，范围 -144.0..0.0 dB |
| `reannounce()` | 重新广播设备，供手机发现 |

以上方法通过 `QYAirPlay2` 调用。百分比 `0f` 或 `-144.0 dB` 表示静音；`0.0 dB` 表示无衰减。

通过 `state` 或 `currentState` 读取运行状态、连接状态、曲目信息、播放进度、音量和封面。手机控制请求失败通过 `state.lastError` 与 `events` 查看，不会触发 `onError` 或中断正在播放的音乐；`onError` 表示接收端运行异常。

需要传统回调时，实现 `QYAirPlay2Listener` 并调用 `addListener(listener)`。请在主线程注册：首次 `onStateChanged` 在注册调用线程同步执行，后续回调在主线程执行；不再使用时调用 `removeListener(listener)`。

播放、暂停、切歌、进度和音量控制的支持程度取决于手机系统与音乐 App。`reverseVolumeReady` 仅表示音量控制可用，不代表其他操作均受支持。

## 6. 升级与使用说明

- 从 `0.0.1-snapshot` 升级后，重新编译所有依赖 SDK 的模块。现有 `QYAirPlay2` 常用方法和双参数音量回调可继续使用。
- 多台手机使用同一设备时，后发起播放的手机会接管当前播放；仅浏览设备不会中断音乐。
- 关闭功能时停止接收端并移除监听，宿主自行创建的协程也应按其生命周期取消。
- [下载 API 文档（javadoc.jar）](https://repo.maven.apache.org/maven2/io/github/qytech/qyairplay2/0.1.0/qyairplay2-0.1.0-javadoc.jar)。解压后打开 `index.html` 查看公开 API、参数和状态说明；版本变化见[更新日志](CHANGELOG.md)。

返回[文档首页](../../README.md)。
