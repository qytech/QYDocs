# AirPlay 模块

`airplay` 是面向 QYTech Android 音频设备的 AirPlay 接收与会话接入库。

## 依赖

```kotlin
implementation("io.github.qytech:airplay:0.0.10")
```

## 适用场景

- 设备端集成 AirPlay 接收能力
- 接入播放会话、远程控制与元数据同步
- 与现有播放器服务或 MediaSession 做桥接

## 功能特性

- AirPlay 接收与播放会话接入
- 多设备连接管理
- 远程控制与 DACP 会话
- 播放进度、音质信息和元数据同步
- JPEG、PNG 封面接收
- 网络状态处理与断线恢复

公开类型主要包括 `QYAirPlay`、`QYAirPlayService`、`QYAirPlayServiceImpl`、`AirplayCallback`、`PlaybackProgress` 及 DACP 远程控制相关类型。

## 使用方法

1. 在设备启动链路中初始化 AirPlay 服务。
2. 将播放、暂停、进度、元数据回调桥接到你的播放器控制层。
3. 统一由上层应用决定如何把 AirPlay 会话切换到内部播放器或其它播放后端。

### 封面与元数据

- 通过 `AirplayCallback.onCoverArtworkChanged` 接收 JPEG、PNG 图片字节，宿主负责解码及展示。
- QQ 音乐可能用曲名字段推送当前歌词。宿主应独立维护封面，避免每次曲名变化都清空图片；重复收到相同图片时可按字节内容去重。
- 封面可能先于歌曲元数据到达。宿主应暂存后合并展示，并在会话结束或切换来源时清理。

### 暂停与恢复

- 手机暂停可能关闭音频连接，但保留 DACP 控制服务。收到 `onAirplayDisconnected` 时，应结合 `onRemoteControlStatusChange` 判断是否仍可从设备恢复播放。
- 当前发送端控制信息仍有效时，库保留控制端点和令牌；新连接、控制服务消失及关闭服务时会清理。
- 使用 `RemoteControl.sendRequest(MediaAction.PLAY, requestCallback)` 恢复，使用 `MediaAction.PAUSE` 暂停。可为单次请求提供 `RemoteControlCallback`，根据成功或失败更新宿主状态，并忽略旧会话的迟到响应。
- HTTP 成功表示发送端接受命令，实际恢复仍依赖发送端应用重新输出音频。

## 兼容性

- `minSdk = 29`
- `compileSdk = 36`
- Java 17

## 调试与发布

- 仓库内部开发可启用本地源码模式
- 对外分发建议直接使用 Maven Central 坐标

根项目双模式说明见：
[README.md](../../README.md)

## 更新日志

### v0.0.10

- 修复暂停后恢复播放时可能无法重新启动音频输出的问题。
- 改善手机暂停后的设备端恢复控制，保留仍可用的发送端控制连接。
- 支持 JPEG、PNG 封面接收，修复封面数据读取不完整的问题。

### v0.0.9

- 修复部分 Apple Music、Spotify 投放时歌曲标题与专辑信息混淆的问题。
- 补充采样率、位深和声道信息上报，支持宿主展示接收流音质。
- 改善断开重连后的播放控制，避免继续控制旧设备。
- 增加音频输出异常通知，便于宿主及时提示播放失败。

### v0.0.8

- 修复多源切换时 `AudioTrack` 崩溃问题。
- 修复 DMAP 元数据错位与歌词、制作人信息冲刷歌曲标题的问题。

### v0.0.7

- 修复开关 AirPlay 可能出现的端口占用问题。
- 修复关闭 AirPlay 可能卡住的问题。
- 新增 `init` 和 `release` 方法，用于监听网络变化时自动处理 AirPlay 状态。

```kotlin
QYAirPlay.init(context)
QYAirPlay.release(context)
```

### v0.0.5

- 修复一个设备连接后另一个设备再次连接时的播放异常问题。
