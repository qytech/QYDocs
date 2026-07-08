# QYTech Android SDK 文档

QYTech Android Framework 公共底座相关 SDK 的文档与更新日志。

---

## 文档导航

| 模块 | 说明 | 最后更新 | 文档 |
|------|------|------|------|
| <a href="docs/AudioPlayer/"><img src="https://img.shields.io/maven-central/v/io.github.qytech/audioplayer.svg" alt="Maven Central" style="vertical-align: middle;"></a> [AudioPlayer](docs/AudioPlayer/) | Android 音频播放框架，支持 DSD、MQA、SACD、CUE、网盘等 | 2026-07-07 | [查看](docs/AudioPlayer/) |
| <a href="docs/DLNA/"><img src="https://img.shields.io/maven-central/v/io.github.qytech/dlna.svg" alt="Maven Central" style="vertical-align: middle;"></a> [DLNA/QPlay](docs/DLNA/) | DLNA 媒体渲染器，支持 QPlay 协议 | 2026-07-07 | [查看](docs/DLNA/) |
| <a href="docs/Airplay/"><img src="https://img.shields.io/maven-central/v/io.github.qytech/airplay.svg" alt="Maven Central" style="vertical-align: middle;"></a> [AirPlay](docs/Airplay/) | AirPlay 接收端实现 | 2026-07-07 | [查看](docs/Airplay/) |
| <a href="docs/Spectrum/"><img src="https://img.shields.io/maven-central/v/io.github.qytech/spectrum.svg" alt="Maven Central" style="vertical-align: middle;"></a> [Spectrum](docs/Spectrum/) | 音频频谱 & VU 表处理组件 | 2026-07-07 | [查看](docs/Spectrum/) |
| <a href="docs/Cdrom/"><img src="https://img.shields.io/maven-central/v/io.github.qytech/cdrom.svg" alt="Maven Central" style="vertical-align: middle;"></a> [Cdrom](docs/Cdrom/) | USB 光驱控制库，支持 CD 播放、抓轨、硬件控制 | 2026-07-07 | [查看](docs/Cdrom/) |
| <a href="docs/NetworkStorage/"><img src="https://img.shields.io/maven-central/v/io.github.qytech/networkstorage.svg" alt="Maven Central" style="vertical-align: middle;"></a> [NetworkStorage](docs/NetworkStorage/) | 网络存储（SMB/NFS/WebDAV）管理 | 2026-07-07 | [查看](docs/NetworkStorage/) |
| <a href="docs/Qobuz/"><img src="https://img.shields.io/maven-central/v/io.github.qytech/qobuz-connect.svg" alt="Maven Central" style="vertical-align: middle;"></a> [Qobuz](docs/Qobuz/) | Qobuz Connect Android SDK | 2026-07-07 | [查看](docs/Qobuz/) · [Changelog](docs/Qobuz/CHANGELOG.md) |
| <a href="docs/Roon/"><img src="https://img.shields.io/maven-central/v/io.github.qytech/roon.svg" alt="Maven Central" style="vertical-align: middle;"></a> [Roon](docs/Roon/) | Roon Raat 协议支持 | 2026-07-07 | [查看](docs/Roon/) |

---

## 快速链接

[文档中心](https://central.sonatype.com/namespace/io.github.qytech) · 
[Maven Central](https://central.sonatype.com/) · 
[GitHub Pages](https://qytech.github.io/QYDocs/)

---

### AudioPlayer

[![Maven Central](https://img.shields.io/maven-central/v/io.github.qytech/audioplayer.svg)](https://central.sonatype.com/artifact/io.github.qytech/audioplayer)

Android 高保真音频播放组件，支持 DSD、MQA、SACD、CUE 分轨、网盘 / WebDAV 等场景。

- ✅ DSD（DFF / DSF）原生播放
- ✅ MQA 完整识别与展开
- ✅ SACD ISO 整轨 / 分轨播放
- ✅ CUE 分轨解析与无缝切歌
- ✅ 网盘 / WebDAV 网络播放
- ✅ USB / DOP / D2P 硬件输出

---

### DLNA/QPlay

[![Maven Central](https://img.shields.io/maven-central/v/io.github.qytech/dlna.svg)](https://central.sonatype.com/artifact/io.github.qytech/dlna)

Android DLNA 媒体渲染器（DMR），支持 QPlay 协议，实现手机 - 设备同步控制。

- ✅ DLNA DMR 媒体渲染器
- ✅ QPlay 协议支持
- ✅ 播放列表管理（支持超长歌单分片下发）
- ✅ 歌词回调
- ✅ 手机 - 设备同步控制
- ✅ SQ 音质支持

---

### AirPlay

[![Maven Central](https://img.shields.io/maven-central/v/io.github.qytech/airplay.svg)](https://central.sonatype.com/artifact/io.github.qytech/airplay)

Android AirPlay 接收端实现，支持多设备连接管理和网络状态自动处理。

- ✅ AirPlay 接收端
- ✅ 多设备连接管理
- ✅ 网络状态自动处理

---

### Spectrum

[![Maven Central](https://img.shields.io/maven-central/v/io.github.qytech/spectrum.svg)](https://central.sonatype.com/artifact/io.github.qytech/spectrum)

音频频谱分析与 VU 表处理组件，支持单声道/双声道分离处理、音量增益补偿等功能。

- ✅ FFT 频谱分析（支持配置 FFT 大小）
- ✅ 单声道 `SpectrumVuProcessor`
- ✅ 双声道分离 `StereoSpectrumVuProcessor`
- ✅ 音量增益补偿
- ✅ 硬件回采 / 软件回采双策略

---

### Cdrom

[![Maven Central](https://img.shields.io/maven-central/v/io.github.qytech/cdrom.svg)](https://central.sonatype.com/artifact/io.github.qytech/cdrom)

Android 平台外部 USB 光驱控制库。支持 CD 播放（基于 Native Oboe）、光盘信息获取（CDDB/FreeDB）、抓轨以及硬件控制（进出仓）。

- ✅ 高性能播放：Google Oboe 实现 Native 层音频回放
- ✅ 硬件控制：支持光驱进仓、出仓、状态检测
- ✅ 元数据支持：支持计算 DiscID（FreeDB/GnuDB 标准）
- ✅ 混合模式支持：完美处理 Mixed Mode CD（数据 + 音频）
- ✅ 抓轨功能：支持将 CD 音频轨道提取保存为 WAV 文件

---

### NetworkStorage

网络存储管理，支持 SMB/NFS/WebDAV 等协议。

---

### Qobuz

[![Maven Central](https://img.shields.io/maven-central/v/io.github.qytech/qobuz-connect.svg)](https://central.sonatype.com/artifact/io.github.qytech/qobuz-connect)

Qobuz Connect Android SDK，基于 Oboe 的音频输出、设备发现与播放控制。

- ✅ Qobuz Connect 协议支持
- ✅ 基于 Oboe 的音频输出
- ✅ 设备发现与控制
- ✅ minSdk 29，仅支持 arm64-v8a

---

### Roon

Roon Raat 协议支持，已更新至 Raat 1.1.47，修复 DSD512 卡顿，支持封面同步。

- ✅ Roon Raat 协议支持（1.1.47）
- ✅ DSD512 播放
- ✅ 封面同步

---

## 技术栈

- Android Framework（minSdk 29）
- Kotlin / Java（JDK 11+）
- 音视频开发
- DLNA / AirPlay / QPlay / Roon / Qobuz 协议
- Google Oboe（Native 音频输出）

---

## 项目说明

公司框架项目，其他客户项目基于此公共底座进行定制开发。核心能力：

- 高保真音频播放（DSD、MQA、SACD、PCM、FLAC、WAV 等格式）
- 网络播放（网盘、WebDAV、局域网 DLNA/AirPlay）
- 多设备音频分发与控制
- USB 光驱与外部设备支持

---

> 仓库最后更新：2026-07-07
