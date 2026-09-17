# QYTech Android SDK 文档

QYTech Android Framework 公共底座相关 SDK 的文档与更新日志。

---

## 文档导航

| 模块 | 说明 | 最后更新 |
|------|------|------|
| <a href="docs/AudioPlayer/"><img src="https://img.shields.io/maven-central/v/io.github.qytech/audioplayer.svg" alt="Maven Central" style="vertical-align: middle;"></a> [AudioPlayer](docs/AudioPlayer/) | Android 音频播放框架，支持 DSD、MQA、CUE、SACD ISO 相邻曲目无缝播放、内嵌歌词与可中断资源释放 | 2026-09-09 |
| <a href="docs/QYDlna/"><img src="https://img.shields.io/maven-central/v/io.github.qytech/qydlna.svg" alt="Maven Central" style="vertical-align: middle;"></a> [QYDlna](docs/QYDlna/) · [Changelog](docs/QYDlna/CHANGELOG.md) | Android 局域网 DLNA/UPnP 接收，支持 DMR、DMS 与 QPlay | 2026-09-15 |
| <a href="docs/DLNA/"><img src="https://img.shields.io/maven-central/v/io.github.qytech/dlna.svg" alt="Maven Central" style="vertical-align: middle;"></a> [DLNA/QPlay（Deprecated）](docs/DLNA/) | 旧版 DLNA/QPlay 媒体渲染器，已停止更新 | 2026-08-12 |
| <a href="docs/Airplay/"><img src="https://img.shields.io/maven-central/v/io.github.qytech/airplay.svg" alt="Maven Central" style="vertical-align: middle;"></a> [AirPlay](docs/Airplay/) | AirPlay 接收端与会话接入，支持远程控制、元数据同步、封面接收和断线恢复 | 2026-09-10 |
| <a href="docs/Spectrum/"><img src="https://img.shields.io/maven-central/v/io.github.qytech/spectrum.svg" alt="Maven Central" style="vertical-align: middle;"></a> [Spectrum](docs/Spectrum/) | 音频频谱与 VU 表组件，支持真实响度和峰值显示 | 2026-08-14 |
| <a href="docs/Cdrom/"><img src="https://img.shields.io/maven-central/v/io.github.qytech/cdrom.svg" alt="Maven Central" style="vertical-align: middle;"></a> [Cdrom](docs/Cdrom/) | USB 光驱控制库，支持 CD 播放、抓轨、硬件控制 | 2026-09-02 |
| <a href="docs/NetworkStorage/"><img src="https://img.shields.io/maven-central/v/io.github.qytech/networkstorage.svg" alt="Maven Central" style="vertical-align: middle;"></a> [NetworkStorage](docs/NetworkStorage/) | 网络存储（SMB/NFS/WebDAV）管理，支持卸载前资源清理协调 | 2026-08-07 |
| <a href="docs/Qobuz/"><img src="https://img.shields.io/maven-central/v/io.github.qytech/qobuz-connect.svg" alt="Maven Central" style="vertical-align: middle;"></a> [Qobuz](docs/Qobuz/) · [Changelog](docs/Qobuz/CHANGELOG.md) | Qobuz Connect Android SDK | 2026-07-07 |
| <a href="docs/Roon/"><img src="https://img.shields.io/maven-central/v/io.github.qytech/roon.svg" alt="Maven Central" style="vertical-align: middle;"></a> [Roon](docs/Roon/) | Roon Raat 协议支持 | 2026-07-07 |
| <a href="docs/SerialPort/"><img src="https://img.shields.io/maven-central/v/io.github.qytech/serialport.svg" alt="Maven Central" style="vertical-align: middle;"></a> [SerialPort](docs/SerialPort/) | Android 串口访问与硬件设备通信 | 2026-08-19 |
| <a href="docs/AudioProbe/"><img src="https://img.shields.io/maven-central/v/io.github.qytech/qyaudioprobe.svg" alt="Maven Central" style="vertical-align: middle;"></a> [AudioProbe](docs/AudioProbe/) · [Changelog](docs/AudioProbe/CHANGELOG.md) | 高性能音频格式嗅探与元数据提取，支持 DSD、SACD、CUE 智能分轨与 HTTP Range 局部嗅探 | 2026-09-17 |
| <a href="docs/MediaScanner/"><img src="https://img.shields.io/maven-central/v/io.github.qytech/qymediascanner.svg" alt="Maven Central" style="vertical-align: middle;"></a> [MediaScanner](docs/MediaScanner/) · [Changelog](docs/MediaScanner/CHANGELOG.md) | 多线程本地与外置存储媒体扫描引擎，支持增量秒级复扫与流式批量持久化分发 | 2026-09-17 |

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
- ✅ SACD ISO 整轨 / 分轨播放，支持相邻曲目连续无缝播放（RAW / DST，Native / DoP / D2P），保留专辑原有曲间间隔
- ✅ CUE 分轨解析与无缝切歌，兼容常见文本编码和多种音频文件关联方式
- ✅ 常见音频容器内嵌歌词解析
- ✅ 网盘 / WebDAV 网络播放
- ✅ 阻塞读写、预加载与 Seek 的快速中断请求
- ✅ USB / DOP / D2P 硬件输出

---

### DLNA/QPlay（Deprecated）

[![Maven Central](https://img.shields.io/maven-central/v/io.github.qytech/dlna.svg)](https://central.sonatype.com/artifact/io.github.qytech/dlna)

> Deprecated：旧版 `dlna` 模块已停止更新。新项目请迁移到 [QYDlna](docs/QYDlna/)。

Android DLNA 媒体渲染器（DMR），支持 QPlay 协议，实现手机 - 设备同步控制。

- ✅ DLNA DMR 媒体渲染器
- ✅ QPlay 协议支持
- ✅ 播放列表管理（支持超长歌单分片下发）
- ✅ 歌词回调
- ✅ 手机 - 设备同步控制
- ✅ SQ 音质支持

---

### QYDlna

[![Maven Central](https://img.shields.io/maven-central/v/io.github.qytech/qydlna.svg)](https://central.sonatype.com/artifact/io.github.qytech/qydlna)

Android 局域网 DLNA/UPnP 接收 SDK，提供 MediaRenderer（DMR）播放控制和可选 MediaServer（DMS）曲库浏览，统一入口为 `com.qytech.dlna.QYDLNA`。

- ✅ DMR 播放控制：播放、暂停、拖动、音量和静音
- ✅ 可选 DMS 本地音乐目录浏览
- ✅ QPlay、设备描述和状态回调
- ✅ 前台服务模式，支持长时间后台运行
- ✅ Android API 29+，当前仅提供 `arm64-v8a`
- ⚠️ `0.0.1-snapshot` 为预发布版本，需完成真实局域网设备互操作验收

---

### AirPlay

[![Maven Central](https://img.shields.io/maven-central/v/io.github.qytech/airplay.svg)](https://central.sonatype.com/artifact/io.github.qytech/airplay)

Android AirPlay 接收与会话接入库，支持多设备连接、远程控制、元数据同步、封面接收和断线恢复。

- ✅ AirPlay 接收端与播放会话接入
- ✅ 多设备连接管理
- ✅ 远程控制、元数据同步与封面接收
- ✅ 网络状态自动处理与断线恢复

---

### Spectrum

[![Maven Central](https://img.shields.io/maven-central/v/io.github.qytech/spectrum.svg)](https://central.sonatype.com/artifact/io.github.qytech/spectrum)

音频频谱分析与 VU 表处理组件，统一管理软件回采、硬件回采、频谱分析和左右声道 VU 显示。

- ✅ FFT 频谱分析（支持配置 FFT 大小）
- ✅ 单声道 `SpectrumVuProcessor`
- ✅ 双声道分离 `StereoSpectrumVuProcessor`
- ✅ `SpectrumCaptureRuntime` 统一管理回采模式与生命周期
- ✅ `AUTO` 默认硬件回采，支持用户指定软件、硬件或关闭模式
- ✅ 不同硬件设备固定参数适配
- ✅ VU 支持 `LOUDNESS` 真实响度与 `PEAK` 峰值显示
- ✅ 左右声道独立显示，不受硬件音量调节影响

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

网络存储管理，支持 SMB/NFS/WebDAV 等协议，并可在 SMB/NFS 卸载前协调播放器关闭相关文件句柄。

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

### AudioProbe

[![Maven Central](https://img.shields.io/maven-central/v/io.github.qytech/qyaudioprobe.svg)](https://central.sonatype.com/artifact/io.github.qytech/qyaudioprobe)

Android 高性能音频格式嗅探与元数据提取组件，面向本地与网络高保真音频场景。

- ✅ 全格式本地音频解码与深度元数据提取
- ✅ DSD（DSF/DFF）与 SACD ISO 格式识别
- ✅ 智能编码 CUE 分轨解析（GB18030 / Big5 / Shift-JIS / UTF-8）
- ✅ HTTP / WebDAV / 私有网盘 Range 局部流式嗅探，无需下载整首文件
- ✅ 内嵌封面与同级歌词快速抽取

---

### MediaScanner

[![Maven Central](https://img.shields.io/maven-central/v/io.github.qytech/qymediascanner.svg)](https://central.sonatype.com/artifact/io.github.qytech/qymediascanner)

Android 多线程本地与外置存储媒体扫描引擎，支持海量曲库流式批量分发与增量极速复扫。

- ✅ 多线程并发目录遍历与高性能元数据提取
- ✅ 流式批量回调机制（`scanDirectoryStreaming`），零内存堆积
- ✅ 增量扫描版本比对（`encodeVersionCache`），秒级完成海量曲库复扫
- ✅ 细粒度失败统计（`traversalFailures` / `probeFailedFiles`）与原子级任务取消
- ✅ 经过数播一体机真机万首高规格曲库压测验证（[查看性能报告](docs/MediaScanner/benchmark-report.md)）

---

## 技术栈

- Android Framework（minSdk 29）
- Kotlin / Java（JDK 11+）
- 音视频开发
- QYDlna（DLNA / UPnP）/ AirPlay / QPlay / Roon / Qobuz 协议
- Google Oboe（Native 音频输出）

---

## 项目说明

公司框架项目，其他客户项目基于此公共底座进行定制开发。核心能力：

- 高保真音频播放（DSD、MQA、SACD、PCM、FLAC、WAV 等格式）
- 网络播放（网盘、WebDAV、局域网 QYDlna/AirPlay）
- 多设备音频分发与控制
- USB 光驱与外部设备支持

---

> 仓库最后更新：2026-09-17
