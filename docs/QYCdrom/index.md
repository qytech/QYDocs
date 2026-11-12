# QYCdrom Android SDK

[![Maven Central](https://img.shields.io/maven-central/v/io.github.qytech/qycdrom.svg)](https://central.sonatype.com/artifact/io.github.qytech/qycdrom)
[![Changelog](https://img.shields.io/badge/Changelog-CHANGELOG.md-blue.svg)](./CHANGELOG.md)

QYCdrom 是基于 Rust 与系统租约服务的 CD-ROM 驱动与播放 SDK（`io.github.qytech:qycdrom`），支持租约式光驱共享、FFmpeg PCM/DTS-CD 播放、原子 WAV 抓轨和 DiscID 元数据查询。

> 当前版本：`0.0.3`（2026-11-11）。与 C++ [Cdrom](../Cdrom/) 互斥，不依赖 Oboe，不要在同一应用中混用两个 CD SDK。版本变化见[更新日志](CHANGELOG.md)。

## 依赖与运行环境

```kotlin
dependencies {
    implementation("io.github.qytech:qycdrom:0.0.3")
}
```

- Android API 29+，仅提供 `arm64-v8a`（内置 `libqy_cdrom.so` 与 `libqy_cdrom_audio.so`）。
- 播放与租约客户端通过 `AudioTrack` 输出音频，不引入 Oboe 依赖；升级时 Kotlin 与 Native `.so` 须配套发布。
- 固件集成 `com.qytech.cdrom.ICdromService/default`（`cdromd` 与对应 SELinux/init 配置）时启用跨应用可撤销独占租约；无系统服务的旧固件允许回退到 Rust JNI 兼容路径（仅提供进程内互斥）。
- 库内置 `FOREGROUND_SERVICE` 与 `FOREGROUND_SERVICE_MEDIA_PLAYBACK` 权限及 `QYCDROMService` 清单声明，接入 AAR 时自动合并。

## 主要变更与能力（v0.0.3）

- **播放读盘缓存**：播放路径按 `16 → 10 → 1` 扇区预读缓存，严格限制在真实 lead-out 内，并在重读、seek、刷新与租约失效时清空缓存。
- **有界解码恢复与短尾排空**：已有有效输出后，短暂的 `INVALIDDATA` / `PATCHWELCOME` 解码失败在连续最长 100 ms 内按帧时长补静音恢复（首帧未知格式、连续超限与真实 IO 错误仍失败）；Android 12+ 短尾帧排空支持 5 s 有界等待并支持 HDMI DTS 同载体布局复用。
- **可撤销租约与硬件兼容**：`CdromDeviceClient` 在打开状态监听时不抢占光驱；播放和抓轨获取独占租约，被其他宿主或托盘操作抢占时触发回收回调并停止读取。

## 使用方法

### 1. DTS 与租约播放（推荐接入方式）

宿主负责队列、音频焦点与 MediaSession，注入生命周期长于会话的 `ownerScope` 与 `ioDispatcher`：

```kotlin
import com.qytech.cdrom.player.CdOutputCapabilities
import com.qytech.cdrom.player.CdPlayer
import com.qytech.cdrom.player.CdPlayerListener
import com.qytech.cdrom.player.CdPlaybackState

val cdPlayer = CdPlayer(
    outputDevice = { selectedAudioDevice },
    outputCapabilities = { device ->
        CdOutputCapabilities(
            maxPcmChannelsBySampleRate = mapOf(44100 to 2, 48000 to 6),
            maxDtsChannelsBySampleRate = mapOf(44100 to 6),
        )
    },
    ioDispatcher = Dispatchers.IO,
    ownerScope = applicationScope,
)

cdPlayer.addListener(playerListener)
cdPlayer.prepare(trackIndex = 1, positionMs = savedPositionMs, durationMs = knownDurationMs)
cdPlayer.play()

// 切源或销毁前等待原生输出与固件租约完全释放
cdPlayer.release { released ->
    if (released) {
        // 可安全切换到下一音源
    }
}
```

### 2. 设备监听、进出仓与抓轨

通过 `com.qytech.cdrom.compat.CdromController` 监听光驱状态、读取 TOC、控制托盘并执行原子 WAV 抓轨：

```kotlin
import com.qytech.cdrom.compat.CdromController

val controller = CdromController(io = Dispatchers.IO, scope = viewModelScope)
controller.init()

// 读取 TOC（suspend）
val toc = controller.getCdRomToc()

// 抓轨（suspend，内部先写临时文件并通过原子移动发布）
val code = controller.saveAudioTrackToFile(
    track = 1,
    outputPath = File(context.cacheDir, "track_01.wav").absolutePath,
    speed = 32,
    progress = callback,
)

// 页面销毁时释放监听与轮询
controller.release()
```

### 3. 兼容入口（`QYCDROM`）

沿用前台服务封装的旧宿主可继续使用 `QYCDROM.startService(context, config)`、`QYCDROM.state` 与 `QYCDROM.stopService(context)`；新接入多宿主或 DTS 透传场景优先使用上述 `CdPlayer` 与 `CdromDeviceClient`。

## 更新日志

完整变更记录见 [更新日志](CHANGELOG.md)，返回[文档首页](../../README.md)。
