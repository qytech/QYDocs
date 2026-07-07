# Changelog

本文档记录 `qobuz` 模块当前仓库内可确认的版本与改动信息。

## [0.0.2] - 2026-03

当前 `qobuz/build.gradle.kts` 中声明的发布版本为 `0.0.2`。

### Added

- 新增 `qobuz` Android Library 模块，用于集成 Qobuz Connect 能力。
- 新增 `QobuzConnectManager` 作为 Kotlin 层统一入口，负责生命周期、播放控制和状态分发。
- 新增 `QobuzStateListener` 回调接口。
- 新增 `TrackInfo` 与 `QbzPlaybackState` 数据模型。
- 新增 JNI 桥接层 `src/main/cpp/jni_main.cpp`。
- 新增基于 Oboe 的音频输出、HTTP 本地配置服务、设备信息与日志代理实现。
- 新增 `qobuzdemo` Compose 演示应用，用于验证模块接入与播放控制。
- 新增 Maven Publish 配置和 `jreleaser.yml`。

### Changed

- Kotlin 层已支持通过 `stateListener` 向 UI 同步：
  - 曲目信息
  - 播放状态
  - 播放进度
  - 音量
  - 静音状态
- Demo 侧采用 `ViewModel + StateFlow + Compose` 的方式包装底层 SDK。

### Fixed

- JNI 层缓存 `TrackInfo` 的 `Class` 与构造函数，避免在回调过程中重复动态查找类带来的问题。
- Demo 页面对 `Slider` 的 `valueRange` 做了兜底处理，避免曲目时长为 `0` 时触发崩溃。
- Demo 页面增加拖拽保护，避免用户拖动进度条时被底层高频进度更新覆盖。
- `PlayerViewModel` 的上一曲/下一曲调用已对应到 `QobuzConnectManager` 的 `skipToPrevious()` / `skipToNext()`。

### Notes

- 当前仓库 `git log -- qobuz` 可见的相关提交记录较少，能直接确认的历史信息有限。
- 现有可见提交包括：
  - `e57381b fix play issue`
  - `407b4f2 fix samba and player issue`
- 上述提交信息较宽泛，且不只针对 `qobuz`，因此本 changelog 主要依据当前代码状态整理，而不是逐条还原完整历史。

## [0.0.1] - Initial internal integration

由于仓库中缺少更早的正式版本标签与详细提交说明，`0.0.1` 仅作为内部初始集成阶段占位记录。

### Included

- 初步引入 Qobuz Connect Android 集成框架。
- 建立 Kotlin 与 Native 层的桥接结构。
- 接入基础播放控制和状态回调链路。
