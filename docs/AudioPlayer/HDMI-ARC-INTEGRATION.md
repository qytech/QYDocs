# HDMI ARC 开发者接入指南

更新日期：2026-10-23。适用于已适配 ARC 的配套 Android 设备与固件。

应用使用 `HdmiArcPlayer()` 接收并播放电视声音，无需查询设备信息或配置音频参数。

## 1. 运行前准备

- Android API 29 及以上，保留 SDK 的 `arm64-v8a` 库文件。
- 电视 ARC 端口连接设备 ARC 接收端口，启用电视的 ARC、HDMI-CEC 和外部音响输出。
- 首次使用先将电视音频格式设为 PCM；确认有声后再尝试自动模式。
- 停止其他播放器，选择可用的本地音频输出，确认音量正常且未静音。

**HDMI ARC 输入与用户选择的 HDMI 输出互斥，不能同时启用。** 设备及应用安装环境由设备方提供。

## 2. 添加依赖

工程仓库包含 Maven Central：

```kotlin
dependencyResolutionManagement {
    repositories {
        google()
        mavenCentral()
    }
}
```

应用模块添加：

```kotlin
dependencies {
    implementation("io.github.qytech:audioplayer:1.2.8")
}
```

Demo 还使用 Kotlin 协程和 AndroidX Lifecycle，依赖见 [Demo 第 2 节](HDMI-ARC-DEMO.md#2-添加依赖)。宿主已有兼容版本时直接复用。

## 3. 开始使用

1. 复制 [Demo 的两个 Kotlin 文件](HDMI-ARC-DEMO.md#3-核心示例hdmiarcdemokt) 到应用模块。
2. 按 [页面调用示例](HDMI-ARC-DEMO.md#4-接入页面生命周期hdmiarcdemolifecyclekt) 在 Activity 的 `onCreate()` 注册一次。
3. 电视持续播放有声内容，打开页面，按日志观察播放、暂停、恢复及停止；离开页面时自动释放。

播放器入口如下；完整的错误处理和释放直接沿用 Demo：

```kotlin
import com.qytech.audioplayer.player.HdmiArcPlayer

val player = HdmiArcPlayer()
```

调用顺序：

```text
创建 → 注册监听 → prepareAndCheck → playAndCheck → pauseAndCheck → playAndCheck → stop → release
```

| 方法 | 用法 |
|---|---|
| `prepareAndCheck()` | 准备播放，必须检查返回值 |
| `playAndCheck()` | 开始或恢复播放，必须检查返回值 |
| `pauseAndCheck()` | 短暂停，必须检查返回值 |
| `stop()` | 停止；再次播放前重新准备 |
| `release()` | 结束并释放会话，之后必须新建实例 |
| `getState()` | 查询状态，不能代替实际听音 |
| `addListener()` / `removeListener()` | 注册或移除 `PlayerListener` |

ARC 是实时输入，不需要 `MediaSource`，不支持歌曲进度、拖动或下一首操作。

## 4. 注意事项

- **串行调用**：在工作线程中，由同一个任务创建、控制和释放播放器；同一时间只保留一个 ARC 会话。
- **回调处理**：回调只记录日志或发送事件，不调用播放器的控制或状态查询方法；更新界面时切回主线程。
- **失败释放**：任何 `AndCheck` 返回 `false`，或收到 `onError`，都结束本次操作并在 `finally` 释放；重试时新建实例。
- **退出页面**：取消任务并等待释放完成，再切源或启动新会话。Demo 已处理页面退出；后台播放交由应用的播放服务管理。
- **暂停恢复**：恢复失败后释放并重新创建，不反复调用 `play()`。

切换输入输出时，由应用执行以下顺序；播放器和 Demo 不会自动切换设备输出：

| 操作 | 顺序 |
|---|---|
| 选择 ARC 输入 | 停止当前播放，退出 HDMI 输出并选择本地输出，再启动 ARC |
| 选择 HDMI 输出 | 取消 ARC 待恢复任务，停止并等待 ARC 释放完成，再启用 HDMI 输出；重连不能抢回 ARC |
| 断连或电视关闭 | 结束 ARC 会话；Demo 需退出页面，连接恢复后再进入，自动恢复由完整应用处理 |

未识别到可用 ARC 输入或输入不能启动时，接口返回失败，启动错误不会被 `PLAYING` 覆盖；持续输入错误会进入 `ERROR`。静音本身是合法输入，不能仅凭无声判断固件是否支持 ARC。

使用目标设备、固件和电视确认实际声音。出现噪声时停止播放；失败时保留错误码、消息与日志，联系设备方。电视自动模式、eARC 及其他音频格式的兼容范围以设备交付说明为准。
