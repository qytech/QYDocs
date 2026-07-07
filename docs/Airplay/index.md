# AirPlay 模块

Android AirPlay 接收端实现，支持多设备连接管理和网络状态自动处理。

## 更新日志

### v0.0.7

```kotlin
implementation("io.github.qytech:airplay:0.0.7")
```

- 修复了开关 AirPlay 可能出现的端口占用问题
- 修复了关闭 AirPlay 可能会卡住的问题
- 新增 `init` 和 `release` 方法，用于监听网络变化时自动处理 AirPlay 状态

```kotlin
QYAirPlay.init(context)
QYAirPlay.release(context)
```

### v0.0.5

- 修复了一个设备连接后另一个设备再次连接时播放异常的问题

## TODO

- [x] 端口占用问题
- [x] 一个设备连接后另一个设备再次连接时播放异常
