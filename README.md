# QYTech Android SDK 文档

QYTech Android Framework 公共底座相关 SDK 的文档与更新日志。

---

## 文档导航

| 模块 | 说明 | 最后更新 |
|------|------|------|
| [HiFiPlayer SDK 接入](docs/HiFiPlayer/) | 公开 Maven 仓库配置及播放、网络存储、投屏 SDK 坐标 | 2026-11-23 |
| [AudioPlayer](docs/AudioPlayer/) | 音频播放、USB Native DSD64、HDMI ARC 输入与多声道透传 | 2026-11-21 |
| <a href="docs/QYDlna/"><img src="https://img.shields.io/maven-central/v/io.github.qytech/qydlna.svg" alt="Maven Central" style="vertical-align: middle;"></a> <img src="https://img.shields.io/badge/★_推荐-Recommended-success?style=flat-square" alt="推荐" style="vertical-align: middle;"> [QYDlna](docs/QYDlna/) · [Changelog](docs/QYDlna/CHANGELOG.md) | Android 局域网 DLNA/UPnP 接收，支持 DMR、DMS、QPlay 及宿主播放前输出交接 | 2026-11-11 |
| <a href="docs/DLNA/"><img src="https://img.shields.io/maven-central/v/io.github.qytech/dlna.svg" alt="Maven Central" style="vertical-align: middle;"></a> [DLNA/QPlay（Deprecated）](docs/DLNA/) | 旧版 DLNA/QPlay 媒体渲染器（0.2.10 移除 `core` 依赖，新项目请使用 QYDlna） | 2026-11-21 |
| <a href="docs/Airplay/"><img src="https://img.shields.io/maven-central/v/io.github.qytech/airplay.svg" alt="Maven Central" style="vertical-align: middle;"></a> [AirPlay（Deprecated）](docs/Airplay/) | 旧版 AirPlay 接收与会话接入，新项目推荐使用 QYAirPlay2 | 2026-09-30 |
| <a href="docs/QYAirPlay2/"><img src="https://img.shields.io/maven-central/v/io.github.qytech/qyairplay2.svg" alt="Maven Central" style="vertical-align: middle;"></a> <img src="https://img.shields.io/badge/★_推荐-Recommended-success?style=flat-square" alt="推荐" style="vertical-align: middle;"> [QYAirPlay2](docs/QYAirPlay2/) · [Changelog](docs/QYAirPlay2/CHANGELOG.md) | AirPlay 音频接收与播放，支持多手机播放接管、歌曲信息与封面、硬件音量及输出释放回调 | 2026-11-21 |
| <a href="docs/Spectrum/"><img src="https://img.shields.io/maven-central/v/io.github.qytech/spectrum.svg" alt="Maven Central" style="vertical-align: middle;"></a> [Spectrum](docs/Spectrum/) | 音频频谱与 VU 表组件，支持真实响度和峰值显示 | 2026-11-21 |
| <a href="docs/QYSpectrum/"><img src="https://img.shields.io/maven-central/v/io.github.qytech/qyspectrum.svg" alt="Maven Central" style="vertical-align: middle;"></a> [QYSpectrum](docs/QYSpectrum/) · [Changelog](docs/QYSpectrum/CHANGELOG.md) | 基于 ARM NEON SIMD 与 Rust JNI 的实时频谱与弹道 VU 表引擎（`0.0.1-snapshot` 预发布） | 2026-09-16 |
| <a href="docs/Cdrom/"><img src="https://img.shields.io/maven-central/v/io.github.qytech/cdrom.svg" alt="Maven Central" style="vertical-align: middle;"></a> [Cdrom](docs/Cdrom/) · [Changelog](docs/Cdrom/CHANGELOG.md) | USB 光驱控制库（C++/Oboe），支持 CD 播放、DTS 能力协商与有界恢复、原子抓轨及硬件控制 | 2026-11-21 |
| <a href="docs/QYCdrom/"><img src="https://img.shields.io/maven-central/v/io.github.qytech/qycdrom.svg" alt="Maven Central" style="vertical-align: middle;"></a> [QYCdrom](docs/QYCdrom/) · [Changelog](docs/QYCdrom/CHANGELOG.md) | 基于 Rust 与系统租约的 CD-ROM 驱动与播放 SDK（不依赖 Oboe），支持 DTS 透传回退与原子抓轨 | 2026-11-11 |
| [NetworkStorage](docs/NetworkStorage/) | SMB/NFS 发现、连接、卸载协调和普通 Android 应用的用户态后端 | 2026-11-21 |
| <a href="docs/Qobuz/"><img src="https://img.shields.io/maven-central/v/io.github.qytech/qobuz-connect.svg" alt="Maven Central" style="vertical-align: middle;"></a> [Qobuz](docs/Qobuz/) · [Changelog](docs/Qobuz/CHANGELOG.md) | Qobuz Connect Android SDK | 2026-11-21 |
| [Roon](docs/Roon/) | Roon RAAT 协议支持，提供 PCM/DSD 输出、MQA 核心解码、音源交接与双网恢复 | 2026-11-23 |
| [QYMultiroom](docs/QYMultiroom/) · [Changelog](docs/QYMultiroom/CHANGELOG.md) | 多房间音频同步与串流 SDK（Fat-AAR），提供角色控制、独立解码与 8 路 PCM 分发 | 2026-11-23 |
| [ScreenMirror](docs/ScreenMirror/) · [Changelog](docs/ScreenMirror/CHANGELOG.md) | 设备端投屏、客户端宽高比和触摸注入 | 2026-11-23 |
| <a href="docs/SerialPort/"><img src="https://img.shields.io/maven-central/v/io.github.qytech/serialport.svg" alt="Maven Central" style="vertical-align: middle;"></a> [SerialPort](docs/SerialPort/) | Android 串口访问与硬件设备通信 | 2026-11-21 |
| <a href="docs/AudioProbe/"><img src="https://img.shields.io/maven-central/v/io.github.qytech/qyaudioprobe.svg" alt="Maven Central" style="vertical-align: middle;"></a> <img src="https://img.shields.io/badge/★_推荐-Recommended-success?style=flat-square" alt="推荐" style="vertical-align: middle;"> [AudioProbe](docs/AudioProbe/) · [Changelog](docs/AudioProbe/CHANGELOG.md) | 高性能音频格式嗅探与元数据提取，支持 DSD、SACD、CUE 智能分轨、HTTP Range 局部嗅探与标签乱码修复 | 2026-09-22 |
| <a href="docs/MediaScanner/"><img src="https://img.shields.io/maven-central/v/io.github.qytech/qymediascanner.svg" alt="Maven Central" style="vertical-align: middle;"></a> <img src="https://img.shields.io/badge/★_推荐-Recommended-success?style=flat-square" alt="推荐" style="vertical-align: middle;"> [MediaScanner](docs/MediaScanner/) · [Changelog](docs/MediaScanner/CHANGELOG.md) | 多线程本地与外置存储媒体扫描引擎，支持发现阶段进度回调、增量秒级复扫与流式批量持久化分发 | 2026-11-21 |
| <a href="docs/QYMusicIndex/"><img src="https://img.shields.io/maven-central/v/io.github.qytech/qymusicindex.svg" alt="Maven Central" style="vertical-align: middle;"></a> [QYMusicIndex](docs/QYMusicIndex/) · [Changelog](docs/QYMusicIndex/CHANGELOG.md) | 基于 Rust JNI 的曲库拼音排序键、首字母分类与内存倒排搜索索引引擎（`0.0.1-snapshot` 预发布） | 2026-10-13 |

---

## 快速链接

[SDK 发布仓库](https://github.com/qytech/maven-releases) ·
[Maven Central](https://central.sonatype.com/) · 
[GitHub Pages](https://qytech.github.io/QYDocs/)

[配置 HiFiPlayer SDK Maven 仓库](docs/HiFiPlayer/) 后，按需添加依赖。

<!-- qydocs:dependencies -->
```kotlin
dependencies {
    implementation("io.github.qytech:audioplayer:1.2.12")
    implementation("io.github.qytech:networkstorage:0.1.12")
    implementation("io.github.qytech:qymultiroom:0.0.5")
    implementation("io.github.qytech:roon:0.1.9")
    implementation("io.github.qytech:screenmirror:0.1.2")
}
```

其他 13 个 SDK 通过 `mavenCentral()` 获取，具体坐标见各 SDK 接入页。版本中的小写 `-snapshot` 是公开坐标的一部分，按原样引用。

| SDK | Maven Central 坐标 |
| --- | --- |
| [Airplay](https://qytech.github.io/QYDocs/docs/Airplay/) | `io.github.qytech:airplay:0.0.10` |
| [AudioProbe](https://qytech.github.io/QYDocs/docs/AudioProbe/) | `io.github.qytech:qyaudioprobe:0.1.0` |
| [Cdrom](https://qytech.github.io/QYDocs/docs/Cdrom/) | `io.github.qytech:cdrom:0.2.11` |
| [DLNA](https://qytech.github.io/QYDocs/docs/DLNA/) | `io.github.qytech:dlna:0.2.10` |
| [MediaScanner](https://qytech.github.io/QYDocs/docs/MediaScanner/) | `io.github.qytech:qymediascanner:0.1.1` |
| [QYAirPlay2](https://qytech.github.io/QYDocs/docs/QYAirPlay2/) | `io.github.qytech:qyairplay2:0.1.3` |
| [QYCdrom](https://qytech.github.io/QYDocs/docs/QYCdrom/) | `io.github.qytech:qycdrom:0.0.3` |
| [QYDlna](https://qytech.github.io/QYDocs/docs/QYDlna/) | `io.github.qytech:qydlna:0.1.1` |
| [QYMusicIndex](https://qytech.github.io/QYDocs/docs/QYMusicIndex/) | `io.github.qytech:qymusicindex:0.0.1-snapshot` |
| [QYSpectrum](https://qytech.github.io/QYDocs/docs/QYSpectrum/) | `io.github.qytech:qyspectrum:0.0.1-snapshot` |
| [Qobuz](https://qytech.github.io/QYDocs/docs/Qobuz/) | `io.github.qytech:qobuz-connect:0.0.4` |
| [SerialPort](https://qytech.github.io/QYDocs/docs/SerialPort/) | `io.github.qytech:serialport:0.0.5` |
| [Spectrum](https://qytech.github.io/QYDocs/docs/Spectrum/) | `io.github.qytech:spectrum:0.2.3` |
<!-- /qydocs:dependencies -->

---

### AudioPlayer

Android 高保真音频播放组件，支持 DSD、MQA、SACD、CUE 分轨、网盘 / WebDAV 等场景。

- ✅ DSD（DFF / DSF）原生播放
- ✅ MQA 完整识别与展开
- ✅ SACD ISO 整轨 / 分轨播放，支持相邻曲目连续无缝播放（RAW / DST，Native / DoP / D2P），保留专辑原有曲间间隔
- ✅ CUE 分轨解析与无缝切歌，兼容常见文本编码和多种音频文件关联方式
- ✅ 常见音频容器内嵌歌词解析
- ✅ 网盘 / WebDAV 网络播放
- ✅ 连续快速定位时保留最后一次目标，减少重复暂停造成的播放停滞
- ✅ 阻塞读写、预加载与 Seek 的快速中断请求
- ✅ USB / DOP / D2P 硬件输出
- 已适配设备与固件上的 HDMI ARC 输入播放，使用无参入口 `HdmiArcPlayer()`；与用户选择的 HDMI 输出互斥
- 支持 Dolby（AC3、E-AC3、TrueHD）与 DTS-HD HDMI 透传输出
- 音频播放、USB Native DSD64、HDMI ARC 输入与多声道透传。

[依赖版本与用法](docs/AudioPlayer/)

[HDMI ARC 接入指南](docs/AudioPlayer/HDMI-ARC-INTEGRATION.md) · [Kotlin Demo](docs/AudioPlayer/HDMI-ARC-DEMO.md)

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
- 维护版本 `0.2.10`（2026-11-11）：移除 `io.github.qytech:core` 依赖，对外接口不变；新项目仍请迁移至 [QYDlna](docs/QYDlna/)

---

### QYDlna <img src="https://img.shields.io/badge/★_推荐-Recommended-success?style=flat-square" alt="推荐" style="vertical-align: middle;">

[![Maven Central](https://img.shields.io/maven-central/v/io.github.qytech/qydlna.svg)](https://central.sonatype.com/artifact/io.github.qytech/qydlna) <img src="https://img.shields.io/badge/★_推荐-Recommended-success?style=flat-square" alt="推荐" style="vertical-align: middle;">

Android 局域网 DLNA/UPnP 接收 SDK，提供 MediaRenderer（DMR）播放控制和可选 MediaServer（DMS）曲库浏览，统一入口为 `com.qytech.dlna.QYDLNA`。

- ✅ DMR 播放控制：播放、暂停、拖动、音量和静音
- ✅ 可选 DMS 本地音乐目录浏览
- ✅ QPlay、设备描述和状态回调
- ✅ 前台服务模式，支持长时间后台运行
- ✅ Android API 29+，当前仅提供 `arm64-v8a`
- 当前版本 `0.1.1`：新增播放前输出所有权回调 `onBeforePlayback` 与 `releasePlaybackOutput` 输出释放接口，详见[接入说明](docs/QYDlna/)和[更新日志](docs/QYDlna/CHANGELOG.md)

```kotlin
implementation("io.github.qytech:qydlna:0.1.1")
```

---

### AirPlay（Deprecated）

[![Maven Central](https://img.shields.io/maven-central/v/io.github.qytech/airplay.svg)](https://central.sonatype.com/artifact/io.github.qytech/airplay)

> Deprecated：旧版 `airplay` 已标记为过时。新项目推荐使用 [QYAirPlay2](docs/QYAirPlay2/)，旧版说明与历史记录仍保留。

Android AirPlay 接收与会话接入库，支持多设备连接、远程控制、元数据同步、封面接收和断线恢复。

- ✅ AirPlay 接收端与播放会话接入
- ✅ 多设备连接管理
- ✅ 远程控制、元数据同步与封面接收
- ✅ 网络状态自动处理与断线恢复

---

### QYAirPlay2 <img src="https://img.shields.io/badge/★_推荐-Recommended-success?style=flat-square" alt="推荐" style="vertical-align: middle;">

[![Maven Central](https://img.shields.io/maven-central/v/io.github.qytech/qyairplay2.svg)](https://central.sonatype.com/artifact/io.github.qytech/qyairplay2)

Android 局域网 AirPlay 音频接收 SDK，入口为 `com.qytech.airplay.QYAirPlay2`。

- 接收播放、歌曲信息、封面和进度，支持多手机播放接管
- 支持播放、暂停、切歌、进度与音量控制，具体能力取决于手机系统和音乐 App
- 可使用软件音量，或接入设备已有的硬件音量控制
- 支持主动断开当前手机，以及在开始播放前由宿主确认音频输出已准备好
- Android API 29+，当前仅提供 `arm64-v8a`；设备需配置 UDP 319/320
- 当前版本 `0.1.3`：新增带完成回调的 `disconnect(complete)` 以确认输出释放后再切源，详见[接入说明](docs/QYAirPlay2/)和[更新日志](docs/QYAirPlay2/CHANGELOG.md)

```kotlin
implementation("io.github.qytech:qyairplay2:0.1.3")
```

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

### QYSpectrum

[![Maven Central](https://img.shields.io/maven-central/v/io.github.qytech/qyspectrum.svg)](https://central.sonatype.com/artifact/io.github.qytech/qyspectrum)

基于 ARM NEON SIMD 与 Rust Direct JNI（Android API 29+、`arm64-v8a`）的实时音频频谱与弹道 VU 表引擎，支持 ALSA 硬件/数字回环捕获（含 Rockchip PDM 音量校准）与播放器后级 PCM 无锁注入。

- 当前版本 `0.0.1-snapshot`（2026-09-16，预发布快照）：详见[接入说明](docs/QYSpectrum/)和[更新日志](docs/QYSpectrum/CHANGELOG.md)

```kotlin
implementation("io.github.qytech:qyspectrum:0.0.1-snapshot")
```

---

### Cdrom

[![Maven Central](https://img.shields.io/maven-central/v/io.github.qytech/cdrom.svg)](https://central.sonatype.com/artifact/io.github.qytech/cdrom)

Android 平台外部 USB 光驱控制库。支持 CD 播放（基于 Native Oboe）、光盘信息获取（CDDB/FreeDB）、抓轨以及硬件控制（进出仓）。

- ✅ 高性能播放：Google Oboe 实现 Native 层音频回放
- ✅ 硬件控制：支持光驱进仓、出仓、状态检测
- ✅ 元数据支持：支持计算 DiscID（FreeDB/GnuDB 标准）
- ✅ 混合模式支持：完美处理 Mixed Mode CD（数据 + 音频）
- ✅ 抓轨功能：支持将 CD 音频轨道提取保存为 WAV 文件
- 当前版本 `0.2.11`：支持 `CdOutputCapabilities` 输出协商、异步 `release(onComplete)`、`16 → 10 → 1` 扇区读盘缓存与 100 ms 有界解码恢复；使用 Oboe 1.11，与同样基于 Oboe 1.11 的 [AudioPlayer](docs/AudioPlayer/) 配套，详见[接入说明](docs/Cdrom/)和[更新日志](docs/Cdrom/CHANGELOG.md)

```kotlin
implementation("io.github.qytech:cdrom:0.2.11")
```

---

### QYCdrom

[![Maven Central](https://img.shields.io/maven-central/v/io.github.qytech/qycdrom.svg)](https://central.sonatype.com/artifact/io.github.qytech/qycdrom)

基于 Rust 与系统租约服务的 CD-ROM 驱动与播放 SDK（不依赖 Oboe，不与 C++ `cdrom` 混用），支持可撤销独占租约、FFmpeg PCM/DTS-CD 播放、原子 WAV 抓轨和 DiscID 元数据查询。

- 当前版本 `0.0.3`：新增 `16 → 10 → 1` 扇区读盘缓存、100 ms 有界解码恢复及短尾帧排空优化，详见[接入说明](docs/QYCdrom/)和[更新日志](docs/QYCdrom/CHANGELOG.md)

```kotlin
implementation("io.github.qytech:qycdrom:0.0.3")
```

---

### NetworkStorage

网络存储管理，提供 SMB / NFS / WebDAV 等协议的设备发现、目录浏览与挂载管理能力。全面兼容现代与老旧 NAS/Samba 设备的匿名访问与协议自适应降级，并支持在卸载前协调播放器释放文件句柄。

- SMB/NFS 发现、连接、卸载协调和普通 Android 应用的用户态后端。

[依赖版本与用法](docs/NetworkStorage/)

---

### Qobuz

[![Maven Central](https://img.shields.io/maven-central/v/io.github.qytech/qobuz-connect.svg)](https://central.sonatype.com/artifact/io.github.qytech/qobuz-connect)

Qobuz Connect Android SDK，基于 Oboe 的音频输出、设备发现与播放控制。

- ✅ Qobuz Connect 协议支持
- ✅ 基于 Oboe 的音频输出
- ✅ 设备发现与控制
- ✅ minSdk 29，仅支持 arm64-v8a
- 当前版本 `0.0.4`：音频输出依赖升级至 Oboe 1.11

```kotlin
implementation("io.github.qytech:qobuz-connect:0.0.4")
```

同一应用集成多个音频组件时，推荐配套使用基于 Oboe 1.11 的 [AudioPlayer](docs/AudioPlayer/)、Cdrom `0.2.11`（`0.2.9`–`0.2.11`）、Qobuz Connect `0.0.4`。不要混用基于 Oboe 1.10 的 Cdrom `0.2.8` 或 Qobuz Connect `0.0.3`。

---

### Roon

[QYTech Maven 发布仓库](https://github.com/qytech/maven-releases)

Roon Raat 协议支持，提供 PCM/DSD 音频串流、MQA 核心解码、动态信号路径与双向音量同步。

- ✅ Roon Raat 协议支持（1.1.48）
- ✅ PCM 与 DSD 输出，支持格式由当前设备和输出通道决定
- ✅ MQA 核心解码（第一层展开）与状态指示
- ✅ 动态信号路径识别（模拟 / 数字 / USB）
- ✅ 双向硬件音量联动与静音控制
- ✅ 封面与多语言元数据实时同步
- ✅ 网络恢复后的服务重连；恢复播放需由 Roon 端明确发起
- 当前版本 `0.1.9`。详见[接入说明](docs/Roon/)。

```kotlin
implementation("io.github.qytech:roon:0.1.9")
```

---

### QYMultiroom

[QYTech Maven 发布仓库](https://github.com/qytech/maven-releases)

Android 多房间音频 SDK（API 29+，`arm64-v8a`）。宿主通过 `MultiRoomFactory` 创建运行时，使用设备、控制和音源三个公开入口。

- 当前版本 `0.0.5`。详见[接入说明](docs/QYMultiroom/)。

```kotlin
implementation("io.github.qytech:qymultiroom:0.0.5")
```

---

### ScreenMirror

设备端投屏运行时 SDK（Android API 29+），提供 `MediaProjection` 授权、镜像/扩展虚拟屏、H.264 低延迟发布与归一化单指远程触摸注入。

- 设备端投屏、客户端宽高比和触摸注入。

[依赖版本与用法](docs/ScreenMirror/)

---

### AudioProbe <img src="https://img.shields.io/badge/★_推荐-Recommended-success?style=flat-square" alt="推荐" style="vertical-align: middle;">

[![Maven Central](https://img.shields.io/maven-central/v/io.github.qytech/qyaudioprobe.svg)](https://central.sonatype.com/artifact/io.github.qytech/qyaudioprobe) <img src="https://img.shields.io/badge/★_推荐-Recommended-success?style=flat-square" alt="推荐" style="vertical-align: middle;">

Android 高性能音频格式嗅探与元数据提取组件，面向本地与网络高保真音频场景。

- ✅ 全格式本地音频解码与深度元数据提取
- ✅ DSD（DSF/DFF）与 SACD ISO 格式识别
- ✅ 智能编码 CUE 分轨解析（GB18030 / Big5 / Shift-JIS / UTF-8）
- ✅ HTTP / WebDAV / 私有网盘 Range 局部流式嗅探，无需下载整首文件
- ✅ 内嵌封面与同级歌词快速抽取
- ✅ 标签乱码修复（GBK→Latin1、UTF-8→GBK、异常撇号控制符等）

---

### MediaScanner <img src="https://img.shields.io/badge/★_推荐-Recommended-success?style=flat-square" alt="推荐" style="vertical-align: middle;">

[![Maven Central](https://img.shields.io/maven-central/v/io.github.qytech/qymediascanner.svg)](https://central.sonatype.com/artifact/io.github.qytech/qymediascanner) <img src="https://img.shields.io/badge/★_推荐-Recommended-success?style=flat-square" alt="推荐" style="vertical-align: middle;">

Android 多线程本地与外置存储媒体扫描引擎，支持海量曲库流式批量分发与增量极速复扫。

- ✅ 多线程并发目录遍历与高性能元数据提取
- ✅ 流式批量回调机制（`scanDirectoryStreaming`），零内存堆积
- ✅ 增量扫描版本比对（`encodeVersionCache`），秒级完成海量曲库复扫
- ✅ 细粒度失败统计（`traversalFailures` / `probeFailedFiles`）与原子级任务取消
- ✅ 扫描元数据随 AudioProbe 修复常见标签乱码
- ✅ 经过数播一体机真机万首高规格曲库压测验证（[查看性能报告](docs/MediaScanner/benchmark-report.md)）
- 当前版本 `0.1.1`：新增发现阶段实时进度回调 `onDiscoveryProgress`，同步更新内置 Native 库并优化增量快照编码内存，详见[接入说明](docs/MediaScanner/)和[更新日志](docs/MediaScanner/CHANGELOG.md)

```kotlin
implementation("io.github.qytech:qymediascanner:0.1.1")
```

---

### QYMusicIndex

[![Maven Central](https://img.shields.io/maven-central/v/io.github.qytech/qymusicindex.svg)](https://central.sonatype.com/artifact/io.github.qytech/qymusicindex)

基于 Rust Direct JNI（Android API 29+、`arm64-v8a`）的曲库拼音首字母/排序键提取与内存倒排索引引擎，提供 `PinyinSortUtil` 与 `NativeMusicIndex`。

- 当前版本 `0.0.1-snapshot`（2026-10-13，预发布快照）：详见[接入说明](docs/QYMusicIndex/)和[更新日志](docs/QYMusicIndex/CHANGELOG.md)

```kotlin
implementation("io.github.qytech:qymusicindex:0.0.1-snapshot")
```

---

## 技术栈

- Android Framework（minSdk 29）
- Kotlin / Java。各 SDK 的字节码目标和宿主编译要求见对应接入页。
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

> 仓库最后更新：2026-11-23
