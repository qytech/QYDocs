# QYCdrom 更新日志

本文档记录 `io.github.qytech:qycdrom` 各版本的变更内容。

## v0.0.3 - 2026-11-11

- 播放读盘路径新增 `16 → 10 → 1` 扇区预读缓存，限制不越过真实 lead-out，并在 seek、刷新、重读及租约关闭/撤销时使缓存失效。
- 在已有有效输出后，将连续最长 100 ms 的短暂 `INVALIDDATA` / `PATCHWELCOME` 解码失败纳入按帧时长静音恢复，正常帧复位计数；首帧未知格式、连续超限及真实 IO 错误仍失败。
- 完善短尾帧排空（5 s 有界等待并支持 stop/seek 取消）以及 HDMI DTS 同载体声道布局复用。

## v0.0.2 - 2026-11-11

- 发布基于固件可撤销 Binder 租约的 `CdromDeviceClient`、`CdromController` 与 FFmpeg `CdPlayer`。
- 支持 `CdOutputCapabilities` 输出能力协商（DTS 透传 → 多声道 PCM → 立体声 PCM 回退）、三参 `prepare(trackIndex, positionMs, durationMs)` 恢复定位及异步 `release(complete)` 释放确认。
- 新增 `CdromMetadataStore` 及 `QYCDROM` 前台服务兼容入口。

## v0.0.1-snapshot - 2026-09-16

- 初始版本：基于 Rust 核心的 Linux CD-ROM 驱动控制、CDDA 播放、WAV 抓轨与 DiscID 元数据获取库。
