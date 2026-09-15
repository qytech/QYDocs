# QYDlna Android SDK

QYDlna 为 Android 提供局域网 DLNA/UPnP 接收能力：MediaRenderer（DMR）用于接收播放控制，MediaServer（DMS）用于浏览宿主提供的本地音乐目录。客户只需要使用 `com.qytech.dlna.QYDLNA`。

> `0.0.1-snapshot` 是预发布版本。正式接入前必须用目标发送端和真实局域网设备验证发现、播放、暂停、拖动、音量、连续播放、DMS 浏览和停止重启。

## 1. 环境与依赖

- Android API 29+
- 设备包含 `arm64-v8a` ABI
- 宿主和发送端处于同一 IPv4 局域网
- `uuid` 在设备生命周期内稳定且唯一
- 默认端口为 `8192`；多实例应使用不同端口，或将 `port` 设为 `0` 请求系统分配
- DMS 的 `roots` 必须是宿主进程可读取的本地绝对路径，SAF URI 不能直接作为曲库根目录

使用团队提供的 Maven Central 预发布源，然后添加依赖：

```kotlin
dependencies {
    implementation("io.github.qytech:qydlna:0.0.1-snapshot")
}
```

## 2. 选择运行模式

### 只接收播放（DMR）

```kotlin
val config = QYDLNAStartConfig(
    friendlyName = "HiFiPlayer",
    uuid = "uuid:player-1",
)

val started = QYDLNA.startRenderer(context, config)
// 页面退出或切换接收端时
QYDLNA.stopRenderer()
```

### 同时接收播放并提供曲库（DMR + DMS）

```kotlin
val config = QYDLNAStartConfig(
    friendlyName = "HiFiPlayer",
    uuid = "uuid:player-1",
    mediaServerName = "HiFi Library",
    mediaServerUuid = "uuid:player-1-dms",
    roots = listOf("/storage/emulated/0/Music"),
)

if (QYDLNA.start(context, config)) {
    // DMR 与 DMS 已在同一网络端点启动
}
QYDLNA.stop()
```

### 只提供曲库（DMS）

```kotlin
QYDLNA.startMediaServer(
    friendlyName = "HiFi Library",
    uuid = "uuid:player-1-dms",
    roots = listOf("/storage/emulated/0/Music"),
)
QYDLNA.stopMediaServer()
```

### 长时间后台运行

```kotlin
QYDLNA.startService(context, config)
// 不再接收时
QYDLNA.stopService(context)
```

库会启动前台服务并提供 `mediaPlayback` 服务类型。宿主仍需按目标 Android 版本完成通知权限、前台服务启动时机和电池策略配置。

## 3. 生命周期、状态与播放控制

```kotlin
QYDLNA.state.collect { renderer ->
    renderer.transport
    renderer.currentMetadata
    renderer.positionMs
    renderer.durationMs
    renderer.volumePercent
    renderer.muted
}

QYDLNA.mediaServerState.collect { server ->
    server.running
    server.roots
}

QYDLNA.play()
QYDLNA.pause()
QYDLNA.stopPlayback()
QYDLNA.next()
QYDLNA.previous()
QYDLNA.seekTo(30_000L) // 毫秒
QYDLNA.setVolume(60) // 0..100
QYDLNA.setMute(false)
```

`QYDLNA.start*` 返回 `false` 表示本地端点未启动成功，例如实例已运行、参数或端口不可用、原生库未加载；返回 `true` 只表示本地端点已创建，不代表发送端已经发现设备或播放成功。重复 `stop*` 安全。

## 4. 可选能力

- 在启动前传入 `QPlayConfig(psk, mid, did)` 可启用 QPlay。PSK 不要写入日志、崩溃报告或埋点。
- 使用 `QYDLNA.qplayState` 和 `QYDLNA.events` 观察 QPlay 鉴权、队列、音质和歌词事件。
- 需要自定义设备描述时，设置 `description` 或 `mediaServerDescription`。
- 不使用 Flow 时，可通过 `QYDLNA.setCallback(...)` 接收播放事件。

## 5. 诊断、验收与回退

```kotlin
val info = QYDLNA.libraryInfo
println("${info.version} (${info.buildDate})")
```

先检查宿主和发送端是否在同一 IPv4 局域网、端口是否被占用、`roots` 是否可读，再保存版本信息、端口、发送端型号和 `QYDLNA.state`。完整验收表和回退步骤见[客户接入与验收](customer-integration.md)。

## 6. API 文档

发布制品包含由 Dokka 生成的 `javadoc.jar`，可直接导入 Android Studio 查看公开 API、参数说明和状态模型。

版本变化见 [`CHANGELOG.md`](CHANGELOG.md)。
