# QYTech Android SDK 文档

QYTech Android Framework 公共底座相关 SDK 的文档与更新日志。

---

## 文档导航

| 模块 | 说明 | 文档 |
|------|------|------|
| **AudioPlayer** | Android 音频播放框架，支持 DSD、MQA、SACD、CUE、网盘等 | [更新日志](docs/AudioPlayer/) |
| **DLNA/QPlay** | DLNA 媒体渲染器，支持 QPlay 协议 | [更新日志](docs/DLNA/) |
| **AirPlay** | AirPlay 接收端实现 | [更新日志](docs/Airplay/) |
| **Spectrum** | 音频频谱 & VU 表处理组件 | [更新日志](docs/Spectrum/) |

---

## 技术栈

- Android Framework
- Kotlin / Java
- 音视频开发
- DLNA / AirPlay / QPlay 协议

## 项目说明

公司框架项目，其他客户项目基于此公共底座进行定制开发。核心能力包括：

- 高保真音频播放（DSD、MQA、SACD、PCM、FLAC、WAV 等格式）
- 网络播放（网盘、WebDAV、局域网 DLNA/AirPlay）
- 多设备音频分发与控制

---

## 版本概览

### AudioPlayer（最新 v1.1.1）

- 支持 DSD512、MQA 完整识别、SACD 整轨/分轨播放
- 无缝播放、CUE 分轨、网盘/WebDAV 播放
- USB / DOP / D2P 硬件输出

### DLNA（最新 v0.2.6）

- DLNA DMR 媒体渲染器
- QPlay 协议支持（队列管理、歌词回调、SQ 音质）
- 手机-设备同步控制

### AirPlay（最新 v0.0.7）

- AirPlay 接收端
- 多设备连接管理
- 网络状态自动处理

### Spectrum（最新 v0.1.8）

- FFT 频谱分析与 VU 表
- 单声道 / 双声道分离处理
- 音量增益补偿

---

> 最后更新：2026-07-07
