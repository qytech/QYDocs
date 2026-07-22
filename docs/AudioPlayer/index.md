# AudioPlayer 模块

Android 高保真音频播放组件，支持 DSD、MQA、SACD、CUE 分轨、网盘 / WebDAV 等场景。

## 依赖

```kotlin
implementation("io.github.qytech:audioplayer:1.1.4")
```

## 功能特性

- ✅ DSD（DFF / DSF）原生播放，支持 Native DSD、DoP 和 D2P 输出模式
- ✅ MQA 完整识别与展开，支持手动控制展开开关
- ✅ SACD ISO 整轨 / 分轨播放
- ✅ CUE 分轨解析与无缝切歌
- ✅ 网盘 / WebDAV 网络播放，支持缓存、拖动与请求取消
- ✅ USB / DOP / D2P 硬件输出
- ✅ 多格式支持：FLAC、WAV、APE、MP3、AAC、DTS、MQA、DSD、PCM
- ✅ 下一音源预加载与连续切换
- ✅ 最大输出采样率设置与自动重采样
- ✅ 完善的资源释放与状态管理，支持暂停、恢复、切歌及设备状态变化

---

## 更新日志

### v1.1.4

- 新增 `dtsPassthroughEnabled` 参数（Boolean，默认 `false`），用于控制 DTS 音频是否通过 HDMI 透传。当 HDMI 支持 DTS 透传时，设置为 `true` 即可启用透传输出。

### v1.1.3

- 新增 `mqaUnfoldEnabled` 参数（Boolean，默认 `true`），用于控制 MQA 解码时是否自动展开至最高采样率。设置为 `false` 时可锁定输出采样率，避免部分 DAC 对展开后高采样率不支持的问题。

### v1.1.2

- 新增下一音源预加载与连续切换能力，减少连续播放时的等待时间。
- 新增最大输出采样率设置。播放高于设定值的 PCM 或 D2P 音频时，可自动向下重采样至指定采样率。
- 完善 DSD 播放配置，支持 Native DSD、DoP 和 D2P 输出模式。
- 优化网络音源的缓存、拖动和请求取消行为，提升 WebDAV、HTTP 等远程音源的播放体验。
- 优化音频输出与资源释放流程，提高暂停、恢复、切歌及存储设备或 DAC 状态变化时的稳定性。
- 修复部分 FLAC 文件不兼容问题。

> **特别说明**
>
> - `maxSampleRate` 默认值为 `0`，升级后不会改变原有输出采样率策略。
> - 最大采样率是用户指定的输出策略，不代表播放器能够自动识别 DAC 的全部能力。如果 DAC 不支持指定采样率，播放器会进入错误状态并通过 `PlayerListener.onError(...)` 通知业务层，不会导致应用崩溃。

### v1.1.1

- 添加 `forceRelease`，防止 USB 播放中拔出设备时闪退

### v1.1.0

- 修复部分文件 MQA 无法识别的问题

### v1.0.9

- 修复部分文件乱码和元数据空白的问题

### v1.0.8

- 优化网盘资源播放起播速度

### v1.0.7

- 添加 MQA 支持，新增三个 MQA 状态字段

```kotlin
data class MediaInfo(
    val sourceId: String,
    val sampleRate: Int,
    val channels: Int,
    val bitrate: Long,
    val bitDepth: Int,
    val format: String,
    val title: String = "Unknown Title",
    val artist: String = "Unknown Artist",
    val album: String = "Unknown Album",
    // MQA 状态：0=非 MQA；非 0=已识别/认证
    val mqaUiState: Int = 0,
    // MQA 原始采样率 (Hz)
    val mqaOriginalRate: Int = 0,
    // MQA 展开后的输出采样率 (Hz)
    val mqaOutputRate: Int = 0,
)
```

---

### v1.0.6

- 修复部分文件专辑信息获取错误问题

### v1.0.5

- 修复 DSD 和 PCM 之间切换可能存在的播放异常

### v1.0.4

- 修复 DSD512 卡顿问题

### v1.0.3

- 修复切换输入输出时可能导致无法播放的问题

### v1.0.2（2026-05-08）

- 修复了 ISO 在没有无缝播放情况下可能出现下一曲开头问题
- 修复了网盘播放时可能出现的闪退情况

### v1.0.1

- 修复输入输出切换时的兼容性问题

### v1.0.0

- 修复了 ISO 和 CUE Seek 异常问题

---

### v0.9.9

- 修复了无缝播放修改导致的 Seek 异常问题

### v0.9.8

- 优化了无缝播放的体验

### v0.9.7

> 注：0.9.6 升级了 Gradle 版本，此版本暂时回退

- 修复了低于 44.1kHz 采样率播放异常问题

### v0.9.5

- 优化了 GC 频繁问题

### v0.9.4

- 添加了 SACD 之间的无缝切换
- 修复了部分无缝播放异常问题

### v0.9.3

- 修复部分 CUE 无缝播放问题

### v0.9.2

- 修复了索尼精选 Seek 0 异常问题

### v0.9.1

- 修复了索尼精选 Seek 状态异常问题

### v0.9.0

- 修复了局域网 `webdav` 播放时失败的问题

---

### v0.8.9

- 修复 `DST` 二次封装格式的音频检测不全问题

### v0.8.8

- 添加无缝播放功能，目前针对 SACD 和其他曲目之间暂时不支持无缝

```kotlin
playerManager.setNextMediaSource(
    DefaultMediaSource(
        uri = nextNextAudio.sourceId
    )
)
```

### v0.8.7

- 针对 DSD 整轨文件修改起播为 Byte Seek 提速

### v0.8.6

- 修复内嵌封面获取失败问题

### v0.8.5

- 修复 DTS 格式二次封装为 FLAC 格式时播放杂音问题

### v0.8.3

- 修复 APE 暂停之后继续播放进度跳变问题

### v0.8.2

- 更新部分 ID3 乱码问题

### v0.8.1

- 修复了 DSD CUE 文件播放非第一曲时进度不对的问题

### v0.8.0

- 修复了 CUE 部分指向的音频原文件错误问题
- 修复了 APE 进度更新异常问题
- 修复了 DFF 文件 Seek 不对的问题

---

### v0.7.7

- 修复了同轴光纤时 DOP 可能出现异常问题

### v0.7.6

- 修改了 AudioTrack 创建逻辑

### v0.7.5

- 修复了 64Bit 音频显示问题
- 修复了 DSD128 以上的 DSD 音频 Seek 慢的问题

### v0.7.4

- 修复了本地 CUE 和网络 CUE 播放参数的兼容性问题

### v0.7.3

- 修复 `AudioPlayerFactory` 播放 CUE 时同时传入 Offset 和 CUE+TrackId 时可能出现播放异常

### v0.7.2

- `PlayerListener` 添加了 `onMetadata(mediaInfo: MediaInfo)` 接口

```kotlin
data class MediaInfo(
    val sampleRate: Int,
    val channels: Int,
    val bitrate: Long,
    val bitDepth: Int,
    val format: String,
    val title: String = "Unknown Title",
    val artist: String = "Unknown Artist",
    val album: String = "Unknown Album",
)
```

### v0.7.1

- 修复 Seek 失败问题

---

### v0.6.9

- 修复了部分文件播放时进度播放异常的问题

### v0.6.8

- 修复了开机第一次播放 DSD512 时可能出错的问题

### v0.6.7

- 修复了扫描时文件夹中存在专辑或封面图时的关联问题

### v0.6.6

- 修复了 D2P 和 DOP 参数问题

### v0.6.5

- 修复了网盘播放 CUE 时分轨异常问题
- 修复了 SACD DST 可能出现无法自动下一首问题

### v0.6.4

- 修复了网络 CUE 扫描时元数据错误
- 修复了 DTS 播放时闪退问题
- 修复了播放到最后 3 秒就触发 Complete 的问题

### v0.6.3

- 修复了整轨 Seek 问题
- 修复了扫描网络资源时文件名显示错误问题
- 修复了 CUE 解析音频和实际音频对不上问题
- 修改了网盘的起播缓存大小，默认最小 3 秒或 256K

### v0.6.2

- 修复网络参数对本地播放的影响

### v0.6.0

- 添加了 WebDAV 的音频扫描功能

```kotlin
val webDavUrl = "https://dav.jianguoyun.com/dav/音频测试/左右声道测试_PCM_44.1k.wav"
val webDavUser = ""
val webDavPwd = ""

AudioProbe.probeFile(webDavUrl, webDavUser = webDavUser, webDavPwd = webDavPwd)
AudioProbe.probe(webDavUrl, ScanProfile.WebDav(webDavUser, webDavPwd))
```

---

### v0.5.8

- 修复了网盘数据扫描问题
- 修复了网盘播放问题
- 新增了部分网盘播放和扫描参数

### v0.5.0

- 修复了频繁切歌可能出现的异常

### v0.4.9

- 修复了 `DffAudioFrame` 被移除但其他库仍在使用的问题

### v0.4.8

- 优化了扫描和解析文件速度
- 优化了播放和切歌速度
- 优化了 SACD 播放逻辑，NATIVED2P、DOP 都正常播放
- 优化了 CUE 播放，传入 CUE 文件和对应 TrackID
- 新增了 `PlayerListener` 合并了之前的 `OnProgressListener` 和 `OnPlaybackStateChangeListener`

```kotlin
public interface PlayerListener {
    fun onPrepared()
    fun onProgress(track: Int, current: Long, total: Long, progress: Float)
    fun onError(code: Int, msg: String)
    fun onComplete()
    fun onStateChanged(state: PlaybackState)
}
```

---

### v0.4.6

- 修复了 DST 播放异常问题
- 添加了 ISO 文件扫描同目录下封面图功能

## TODO

- [x] 修复 DST native 播放卡顿问题
- [x] 修复 DST Seek 问题
