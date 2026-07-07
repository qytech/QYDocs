# QYTech Android SDK 文档

QYTech Android Framework 公共底座相关 SDK 的文档与更新日志。

---

## 文档导航

| 模块 | 说明 | 最后更新 |
|------|------|------|
| **Roon** | Roon Raat 协议支持，DSD512 播放、封面同步 | 2026-07-07 |
| **Qobuz** | Qobuz Connect Android SDK，设备发现与播放控制 | 2026-07-07 |
| **NetworkStorage** | 网络存储（SMB/NFS/WebDAV）管理 | 2026-07-07 |
| **Cdrom** | USB 光驱控制库，CD 播放、抓轨、硬件控制 | 2026-07-07 |
| **Spectrum** | 音频频谱 & VU 表处理组件，FFT 分析 | 2026-07-07 |
| **AirPlay** | AirPlay 接收端实现，多设备连接管理 | 2026-07-07 |
| **DLNA/QPlay** | DLNA 媒体渲染器，QPlay 协议，歌词回调 | 2026-07-07 |
| **AudioPlayer** | Android 高保真音频播放框架，DSD、MQA、SACD | 2026-07-07 |

---

## 快速链接

- [Roon](docs/Roon/)
- [Qobuz](docs/Qobuz/) · [Changelog](docs/Qobuz/CHANGELOG.md)
- [NetworkStorage](docs/NetworkStorage/)
- [Cdrom](docs/Cdrom/)
- [Spectrum](docs/Spectrum/)
- [AirPlay](docs/Airplay/)
- [DLNA/QPlay](docs/DLNA/)
- [AudioPlayer](docs/AudioPlayer/)

---

## 技术栈

- Android Framework（minSdk 29）
- Kotlin / Java（JDK 11+）
- 音视频开发
- DLNA / AirPlay / QPlay / Roon / Qobuz 协议
- Google Oboe（Native 音频输出）

---

## 模块概览

### Roon（v0.1.0）

Roon Raat 协议支持，已更新至 Raat 1.1.47，修复 DSD512 卡顿，支持封面同步。

### Qobuz（v0.0.2）

Qobuz Connect Android SDK，基于 Oboe 的音频输出、设备发现与播放控制。

### NetworkStorage

网络存储管理，支持 SMB/NFS/WebDAV 等协议。

### Cdrom（v0.2.5）

USB 光驱控制库，支持 CD 播放（Native Oboe）、CDDB/FreeDB 元数据、抓轨、硬件控制（进出仓）。

### Spectrum（v0.1.8）

音频频谱分析与 VU 表，支持单声道/双声道分离处理、音量增益补偿、硬件回采/软件回采双策略。

### AirPlay（v0.0.7）

AirPlay 接收端实现，支持多设备连接管理与网络状态自动处理。

### DLNA/QPlay（v0.2.6）

DLNA DMR 媒体渲染器，QPlay 协议支持（队列管理、歌词回调、SQ 音质），手机-设备同步控制。

### AudioPlayer（v1.1.1）

Android 高保真音频播放框架，支持 DSD512、MQA 完整识别、SACD 整轨/分轨、CUE 分轨、无缝播放、网盘/WebDAV 播放。

---

## 项目说明

公司框架项目，其他客户项目基于此公共底座进行定制开发。核心能力：

- 高保真音频播放（DSD、MQA、SACD、PCM、FLAC、WAV 等格式）
- 网络播放（网盘、WebDAV、局域网 DLNA/AirPlay）
- 多设备音频分发与控制
- USB 光驱与外部设备支持

---

> 仓库最后更新：2026-07-07
