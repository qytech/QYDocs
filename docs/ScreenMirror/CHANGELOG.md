# ScreenMirror 更新日志

本文档记录 `io.github.qytech:screenmirror` 各版本的变更内容。

## v0.1.2 - 2026-11-23

- 将投屏 SDK 的混淆类放入独立命名空间，修复与 `qymultiroom:0.0.5` 一同打包时出现的重复类错误。宿主沿用原有 `ScreenMirrorController` 接入方式。

## v0.1.1 - 2026-11-21

- 扩展屏请求新增可选的 `aspectRatio`，按客户端视图宽高比选择目标尺寸。保留 0.1.0 客户端使用的 JVM 构造及复制方法签名。

## v0.1.0 - 2026-08-17

- 初始版本：提供 `ScreenMirrorController` 设备端投屏运行时，支持 `MediaProjection` 授权、主屏镜像（`MIRROR`）与独立扩展屏（`EXTENDED`）。
- 支持 H.264 低延迟视频流发布、动态分辨率/帧率（`FPS30`/`FPS60`）配置及几何信息同步。
- 支持基于会话所有权与几何版本校验的归一化单指触摸注入。
