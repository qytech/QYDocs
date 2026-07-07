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
| **Cdrom** | USB 光驱控制库，支持 CD 播放、抓轨、硬件控制 | [更新日志](docs/Cdrom/) |
| **NetworkStorage** | 网络存储（SMB/NFS/WebDAV）管理 | [更新日志](docs/NetworkStorage/) |
| **Qobuz** | Qobuz Connect Android SDK | [使用文档](docs/Qobuz/) / [Changelog](docs/Qobuz/CHANGELOG.md) |
| **Roon** | Roon Raat 协议支持 | [变更日志](docs/Roon/) |

---

## 技术栈

- Android Framework
- Kotlin / Java
- 音视频开发
- DLNA / AirPlay / QPlay / Roon 协议

## 项目说明

公司框架项目，其他客户项目基于此公共底座进行定制开发。核心能力包括：

- 高保真音频播放（DSD、MQA、SACD、PCM、FLAC、WAV 等格式）
- 网络播放（网盘、WebDAV、局域网 DLNA/AirPlay）
- 多设备音频分发与控制
- USB 光驱与外部设备支持

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

### Cdrom（最新 v0.2.5）

- USB 光驱控制，支持 CD 播放（Oboe Native）
- CDDB/FreeDB 元数据、抓轨、硬件控制
- Mixed Mode CD 处理、DTS CD 支持

### NetworkStorage（最新）

- 网络存储管理（SMB/NFS/WebDAV）

### Qobuz（最新 v0.0.2）

- Qobuz Connect 协议支持
- 基于 Oboe 的音频输出
- 设备发现与控制

### Roon（最新 v0.1.0）

- Roon Raat 协议支持（1.1.47）
- DSD512 播放、封面同步

---

> 最后更新：2026-07-07
