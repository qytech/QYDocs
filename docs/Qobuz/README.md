# Qobuz Connect Android 快速接入

## 适用范围

`qobuz` 是 Android 侧的 Qobuz Connect 接入库，对外统一入口为 `QobuzConnectManager`。

当前版本：

- `groupId`: `io.github.qytech`
- `artifactId`: `qobuz-connect`
- `version`: `0.0.2`

## 接入前提

接入方需要提前准备以下信息：

- `appId`
- `appSecret`
- `deviceName`
- `manufacturer`
- `model`
- `serialNumber`

当前库的构建条件：

- `minSdk 29`
- `compileSdk 36`
- Java/Kotlin 11
- 当前仅支持 `arm64-v8a`

## 依赖接入

接入依赖：

```kotlin
implementation("io.github.qytech:qobuz-connect:0.0.2")
```

## 必要权限

请在宿主应用中至少声明以下权限：

```xml
<uses-permission android:name="android.permission.INTERNET" />
<uses-permission android:name="android.permission.ACCESS_NETWORK_STATE" />
<uses-permission android:name="android.permission.ACCESS_WIFI_STATE" />
<uses-permission android:name="android.permission.ACCESS_FINE_LOCATION" />
<uses-permission android:name="android.permission.ACCESS_COARSE_LOCATION" />
<uses-permission android:name="android.permission.CHANGE_WIFI_MULTICAST_STATE" />
```

说明：

- Qobuz Connect 的设备发现依赖局域网和 NSD。
- 组播发现依赖 `CHANGE_WIFI_MULTICAST_STATE`。
- 运行时权限申请策略请按宿主应用自己的系统版本策略处理。

## 最小接入示例

### 1. 创建管理器

```kotlin
private lateinit var qobuzManager: QobuzConnectManager

override fun onCreate(savedInstanceState: Bundle?) {
    super.onCreate(savedInstanceState)
    qobuzManager = QobuzConnectManager(this)
}
```

### 2. 注册状态监听

```kotlin
qobuzManager.stateListener = object : QobuzStateListener {
    override fun onTrackInfoChanged(trackInfo: TrackInfo) {
        // 更新曲目信息
    }

    override fun onPlaybackStateChanged(state: QbzPlaybackState) {
        // 更新播放状态
    }

    override fun onPlaybackProgressChanged(progressMs: Long) {
        // 更新播放进度
    }

    override fun onVolumeChanged(volume: Int) {
        // 更新音量
    }

    override fun onMuteStateChanged(isMuted: Boolean) {
        // 更新静音状态
    }
}
```

### 3. 启动 Qobuz Connect

```kotlin
qobuzManager.startConnect(
    QobuzConnectManager.Config(
        appId = "your_app_id",
        appSecret = "your_app_secret",
        deviceName = "your_device_name",
        manufacturer = "your_manufacturer",
        model = "your_model",
        serialNumber = "your_serial_number",
        httpPort = 6789,
    )
)
```

### 4. 页面销毁时释放资源

```kotlin
override fun onDestroy() {
    qobuzManager.release()
    super.onDestroy()
}
```

## 播放控制接口

库当前提供以下控制能力：

```kotlin
qobuzManager.play()
qobuzManager.pause()
qobuzManager.resume()
qobuzManager.stop()
qobuzManager.skipToNext()
qobuzManager.skipToPrevious()
qobuzManager.seekTo(positionMs)
qobuzManager.setVolume(volume)
qobuzManager.setMute(muted)
```

参数说明：

- `seekTo(positionMs)`: 单位毫秒
- `setVolume(volume)`: 传入整型音量值
- `setMute(muted)`: `true` 为静音，`false` 为取消静音

## 状态模型

### 播放状态

```kotlin
QbzPlaybackState.QBZ_PLAYBACK_STATE_STOPPED
QbzPlaybackState.QBZ_PLAYBACK_STATE_PLAYING
QbzPlaybackState.QBZ_PLAYBACK_STATE_PAUSED
QbzPlaybackState.QBZ_PLAYBACK_STATE_SEEKING
```

### 曲目信息

`TrackInfo` 当前包含：

- `trackId`
- `title`
- `artist`
- `album`
- `coverUrl`
- `durationMs`
- `sampleRate`
- `channel`
- `bitPreSample`

## 推荐接入方式

建议在宿主侧采用以下模式：

1. 在 `ViewModel` 中持有 `QobuzConnectManager`。
2. 用 `StateFlow` 或等价状态容器承接 `QobuzStateListener` 回调。
3. UI 层只消费状态，不直接操作底层对象。
4. 在宿主生命周期结束时调用 `release()`。

## 接入注意事项

### 1. 设备发现依赖局域网能力

宿主设备需要满足：

- 网络可用
- Wi‑Fi 可用
- 允许组播

否则可能出现设备发现失败、注册失败或控制端无法看到设备。

### 2. 当前 ABI 仅支持 arm64-v8a

如果客户设备存在其他 ABI 需求，需要同步补充对应 native 二进制。

### 3. `release()` 必须调用

不调用 `release()` 可能导致：

- NSD 服务未注销
- Multicast Lock 未释放
- native 资源未释放

### 4. 密钥不要写死在代码中

正式项目建议通过配置中心、安全存储或设备初始化流程注入：

- `appId`
- `appSecret`

不要将正式凭据直接写入源码仓库。

## 常见接入顺序

推荐客户按以下顺序完成接入：

1. 引入依赖。
2. 补齐权限。
3. 创建 `QobuzConnectManager`。
4. 注册 `QobuzStateListener`。
5. 调用 `startConnect()`。
6. 将播放控制接口接到宿主播放器能力。
7. 在页面或进程结束时调用 `release()`。
