# ScreenMirror 更新日志

本文档记录 `io.github.qytech:screenmirror` 各版本的变更内容。

## v0.1.0 - 2026-08-17

- 初始版本：提供 `ScreenMirrorController` 设备端投屏运行时，支持 `MediaProjection` 授权、主屏镜像（`MIRROR`）与独立扩展屏（`EXTENDED`）。
- 支持 H.264 低延迟视频流发布、动态分辨率/帧率（`FPS30`/`FPS60`）配置及几何信息同步。
- 支持基于会话所有权与几何版本校验的归一化单指触摸注入。
