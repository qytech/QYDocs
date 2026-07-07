# Qobuz Connect Android SDK 使用文档

**Library:** `com.qytech:qobuz-connect`
**Repository:** [Maven Central](https://central.sonatype.com/search?q=qobuz-connect)
**Language:** Kotlin / Android

## 更新日志

```Plain Text
implementation("io.github.qytech:qobuz-connect:0.0.2")
```

### v0\.0\.2

1. 初始化`Qobuz-Connect`

## 概述

`qobuz-connect` 是一个面向 Android 平台的 Qobuz Connect 协议 SDK，允许您的 Android 设备作为 Qobuz Connect 播放目标（类似 Chromecast Audio / AirPlay 接收端），接受来自 Qobuz 应用的远程控制指令并同步播放状态。

SDK 核心类为 `QobuzConnectManager`，负责：

- 启动/停止 Qobuz Connect 原生服务（通过 JNI）

- 通过 mDNS/NSD 注册设备服务，使其在局域网中可被 Qobuz App 发现

- 接收并转发播放控制回调（曲目信息、播放状态、进度、音量等）

- 提供平滑的本地进度预估

---

## 添加依赖

在您的模块 `build.gradle`（或 `build.gradle.kts`）中添加：

```Kotlin
// build.gradle.kts
dependencies {
    implementation("com.qytech:qobuz-connect:<latest_version>")
}
```

```Groovy
// build.gradle (Groovy)
dependencies {
    implementation 'com.qytech:qobuz-connect:<latest_version>'
}
```

请前往 [Maven Central](https://central.sonatype.com/search?q=qobuz-connect) 查询最新版本号。

---

## 权限配置

在 `AndroidManifest.xml` 中添加以下权限（NSD 服务发现和多播支持所需）：

```XML
<uses-permission android:name="android.permission.INTERNET" />
<uses-permission android:name="android.permission.CHANGE_WIFI_MULTICAST_STATE" />
<uses-permission android:name="android.permission.ACCESS_WIFI_STATE" />
<uses-permission android:name="android.permission.ACCESS_NETWORK_STATE" />
```

---

## 快速开始

### 创建 QobuzConnectManager 实例

`QobuzConnectManager` 接收一个 `Context` 参数，建议在 `ViewModel` 或 `Application` 级别持有实例：

```Kotlin
val qobuzManager = QobuzConnectManager(context)
```

### 配置并启动 SDK

调用 `startConnect(config)` 初始化并启动 Qobuz Connect 服务：

```Kotlin
qobuzManager.startConnect(
    QobuzConnectManager.Config(
        appId       = "YOUR_APP_ID",
        appSecret   = "YOUR_APP_SECRET",
        deviceName  = "My Audio Device",   // 显示在 Qobuz App 中的设备名
        manufacturer = "YourCompany",
        model        = "ModelName",
        serialNumber = "SN123456",
        httpPort     = 6789               // 可选，默认 6789
    )
)
```

### 注册状态监听器

通过 `stateListener` 属性设置 `QobuzStateListener` 接口实现，接收来自 SDK 的播放状态回调：

```Kotlin
qobuzManager.stateListener = object : QobuzStateListener {
    override fun onTrackInfoChanged(trackInfo: TrackInfo) {
        // 曲目信息变更（标题、艺术家、专辑、封面等）
    }
    override fun onPlaybackStateChanged(state: QbzPlaybackState) {
        // 播放状态变更（Playing / Paused / Stopped 等）
    }
    override fun onPlaybackProgressChanged(progressMs: Long) {
        // 播放进度更新
    }
    override fun onVolumeChanged(volume: Int) {
        // 音量变更
    }
    override fun onMuteStateChanged(isMuted: Boolean) {
        // 静音状态变更
    }
}
```

### 释放资源

在组件销毁时（如 `ViewModel.onCleared()`、`Activity.onDestroy()`）调用 `release()`：

```Kotlin
qobuzManager.release()
```

`release()` 会自动注销 NSD 服务、释放多播锁、取消进度轮询并停止原生服务。

---

## 播放控制 API

---

## 状态模型

### QbzPlaybackState

SDK 通过 `onPlaybackStateChanged(state: QbzPlaybackState)` 回调当前播放状态，枚举值包括：

### TrackInfo

`onTrackInfoChanged(trackInfo: TrackInfo)` 回调包含当前曲目的元数据信息（如标题、艺术家、专辑封面 URL 等），具体字段请参考 `com.qytech.qobuz.model.TrackInfo` 类定义。

---

## 与 ViewModel / Jetpack Compose 集成

推荐将 `QobuzConnectManager` 封装在 `AndroidViewModel` 中，使用 `StateFlow` 向 UI 层暴露状态：

```Kotlin
class PlayerViewModel(application: Application) : AndroidViewModel(application) {

    private val qobuzManager = QobuzConnectManager(application)

    private val _trackInfoFlow = MutableStateFlow(TrackInfo())
    val trackInfoFlow: StateFlow<TrackInfo> = _trackInfoFlow.asStateFlow()

    private val _playbackStateFlow =
        MutableStateFlow(QbzPlaybackState.QBZ_PLAYBACK_STATE_STOPPED)
    val playbackStateFlow: StateFlow<QbzPlaybackState> = _playbackStateFlow.asStateFlow()

    private val _progressFlow = MutableStateFlow(0L)
    val progressFlow: StateFlow<Long> = _progressFlow.asStateFlow()

    private val _volumeFlow = MutableStateFlow(50)
    val volumeFlow: StateFlow<Int> = _volumeFlow.asStateFlow()

    private val _muteStateFlow = MutableStateFlow(false)
    val muteStateFlow: StateFlow<Boolean> = _muteStateFlow.asStateFlow()

    init {
        qobuzManager.stateListener = object : QobuzStateListener {
            override fun onTrackInfoChanged(trackInfo: TrackInfo) {
                _trackInfoFlow.value = trackInfo
            }
            override fun onPlaybackStateChanged(state: QbzPlaybackState) {
                _playbackStateFlow.value = state
            }
            override fun onPlaybackProgressChanged(progressMs: Long) {
                _progressFlow.value = progressMs
            }
            override fun onVolumeChanged(volume: Int) {
                _volumeFlow.value = volume
            }
            override fun onMuteStateChanged(isMuted: Boolean) {
                _muteStateFlow.value = isMuted
            }
        }
    }

    fun startSdk() {
        qobuzManager.startConnect(
            QobuzConnectManager.Config(
                appId        = "YOUR_APP_ID",
                appSecret    = "YOUR_APP_SECRET",
                deviceName   = "My Device",
                manufacturer = "YourCompany",
                model        = "ModelX",
                serialNumber = "SN000001"
            )
        )
    }

    fun stopSdk()       = qobuzManager.release()
    fun play()          = qobuzManager.play()
    fun pause()         = qobuzManager.pause()
    fun resume()        = qobuzManager.resume()
    fun next()          = qobuzManager.skipToNext()
    fun previous()      = qobuzManager.skipToPrevious()
    fun seekTo(ms: Long) = qobuzManager.seekTo(ms)

    override fun onCleared() {
        super.onCleared()
        stopSdk()
    }
}
```

在 Compose 界面中使用 `collectAsState()` 消费这些 Flow：

```Kotlin
val trackInfo by viewModel.trackInfoFlow.collectAsState()
val playbackState by viewModel.playbackStateFlow.collectAsState()
val progressMs by viewModel.progressFlow.collectAsState()
```

---

## 进度同步机制

SDK 内置了**本地进度预估**逻辑，无需完全依赖服务端推送：

- 收到 `onPlaybackProgressChanged` 时，记录当前时间戳与进度值作为同步基准点。

- 播放状态下，启动每 **50ms** 触发一次的本地定时器，根据 `SystemClock.elapsedRealtime()` 差值估算当前进度，并回调 `onPlaybackProgressChanged`。

- 暂停/停止时，定时器自动停止，仅服务端推送会触发进度回调。

- 调用 `seekTo()` 时，本地基准点立即更新，实现即时响应。

---

## NSD 服务发现说明

SDK 使用 Android `NsdManager` 通过 **DNS\-SD** 协议广播设备，使 Qobuz App 能在局域网中发现该设备：

- SDK 内部自动调用 `registerService()` 注册 mDNS 服务（该方法为 JNI 回调，无需手动调用）。

- 注册时 SDK 会自动申请 `WifiManager.MulticastLock`，以确保多播数据包可被正常接收。

- 调用 `release()` 或组件销毁时，SDK 会自动注销服务并释放多播锁。

---

## 注意事项

- `QobuzConnectManager` 使用 `Dispatchers.Main` \+ `SupervisorJob` 的 `CoroutineScope`，所有回调均在主线程触发，可直接更新 UI 状态。

- 请勿手动调用 `registerService()` / `unregisterService()` 等带有 `@Keep` 注解的方法，它们由 C\+\+ 层通过 JNI 自动调用。

- SDK 内部加载了原生库 `libqobuz.so`，请确保打包时包含目标 ABI 的 `.so` 文件。

- 建议在 Application 或 ViewModel 级别持有 `QobuzConnectManager` 实例，避免重复初始化。

---

## 常见问题

**Q: 设备在 Qobuz App 中不可见？**
 A: 检查设备是否连接同一 Wi\-Fi 网络；确认 `CHANGE_WIFI_MULTICAST_STATE` 权限已声明；部分路由器默认屏蔽多播，请检查路由器设置。

**Q: 调用 ****`play()`**** / ****`pause()`**** 无响应？**
 A: 这些方法内部有状态保护（例如 `play()` 仅在 `!isPlaying` 时执行）。请先确认当前 `playbackState` 是否符合调用前提条件。

**Q: 如何获取最新版本号？**
 A: 访问 [Maven Central 搜索页](https://central.sonatype.com/search?q=qobuz-connect) 查询 `com.qytech:qobuz-connect` 的最新发布版本。

