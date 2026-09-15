# QYDlna 客户接入与验收

本文档面向把 QYDlna 集成到 Android 宿主的客户。`0.0.1-snapshot` 是预发布版本；接入时保留旧接收端开关，便于回退。

## 1. 接入前检查

- Android API 29+，目标设备包含 `arm64-v8a`。
- 宿主与发送端在同一 IPv4 局域网；先关闭会隔离局域网的 VPN、访客网络或热点选项。
- `uuid` 稳定且唯一；`friendlyName` 只用于展示。
- DMS 的 `roots` 是宿主进程可读的本地绝对路径。SAF URI 需要由宿主先处理，不能直接传入。
- 默认端口是 `8192`；多实例必须使用不同端口，或把 `port` 设为 `0` 请求系统分配。

## 2. 最小接入

```kotlin
val config = QYDLNAStartConfig(
    friendlyName = deviceName,
    uuid = stableUuid,
    mediaServerName = libraryName, // 省略则只启动 DMR
    mediaServerUuid = "$stableUuid-dms",
    roots = musicRoots,
)

if (!QYDLNA.start(context, config)) {
    // 保持旧接收端或提示用户检查端口、网络和本地目录
}
```

模式选择：

| 需求 | API | 停止 API |
| --- | --- | --- |
| 只接收播放 | `startRenderer` | `stopRenderer` |
| 播放 + 曲库 | `start` + `mediaServerName` | `stop` |
| 只提供曲库 | `startMediaServer` | `stopMediaServer` |
| 长时间后台运行 | `startService` | `stopService` |

页面或宿主生命周期结束时停止对应角色。重复停止安全；重复启动返回 `false`。

## 3. 宿主配置

库已声明前台服务及 `mediaPlayback` 类型。宿主仍需：

1. 在目标 Android 版本允许的时机启动前台服务。
2. 按产品策略申请通知权限并配置电池优化白名单。
3. 确保 `roots` 在启动前仍然可读；外置存储挂载变化后应停止并重新启动。
4. 不要把 QPlay PSK 写入 logcat、崩溃报告或埋点。

## 4. 状态、控制和回退

使用 `QYDLNA.state`、`mediaServerState` 观察运行状态，使用 `events` 或 `setCallback` 接收播放事件。`start*` 返回 `true` 只表示本地网络端点已创建，不表示发送端已经发现或播放成功。

出现端口占用、原生库加载失败、发现超时或播放异常时：

1. 保存 `QYDLNA.libraryInfo`、端口、`QYDLNA.state`、发送端型号和时间。
2. 调用对应的 `stop*`，确认旧接收端仍可用。
3. 切回旧接收端，保留同一时间窗口的宿主和发送端日志。

## 5. 真实设备验收

至少使用一个目标发送端和一个目标控制点，并保存宿主 logcat：

| 场景 | 通过条件 |
| --- | --- |
| DMR 发现 | 发送端看到设备，设备名和 UUID 正确 |
| DMS 发现 | 启用 DMS 时看到独立曲库设备 |
| 首次播放 | 有声音，标题、时长和封面正确或按预期缺省 |
| 暂停/继续 | `PausedPlayback` 与 `Playing` 状态正确切换 |
| 拖动 | 位置误差在产品允许范围内，越界请求不崩溃 |
| 音量/静音 | 发送端和状态流结果一致 |
| 连续播放 | 至少连续播放 3 首，无卡死、重复或错误下一首 |
| 曲库浏览 | 每个 root 可浏览，非法路径不会越界 |
| 停止/重启 | 停止后设备消失，再次启动可重新发现 |
| 异常客户端 | 断开或不读取响应时，服务可在有限时间内停止 |

只有所有目标对端通过，才把预发布版本升级为正式版本。

## 6. 支持信息

提交问题时附上：

- `QYDLNA.libraryInfo.version` 和 `buildDate`；
- `networkRunning`、`transport`、`currentUri`、`mediaServerState`；
- 监听端口、发送端/控制点型号、Android 版本和测试时间；
- 不包含 PSK 的完整相关 logcat。
