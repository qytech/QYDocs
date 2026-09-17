# QYAudioProbe Android SDK

[![Maven Central](https://img.shields.io/maven-central/v/io.github.qytech/qyaudioprobe.svg)](https://central.sonatype.com/artifact/io.github.qytech/qyaudioprobe)

QYAudioProbe 是专为 Android 音频播放系统设计的高保真音频格式嗅探与元数据提取库。支持主流无损与高解析音频格式、DSD/SACD、CUE 智能分轨、内嵌封面与歌词提取，并支持 HTTP/WebDAV 网络音频 Range 局部嗅探。客户统一调用 `com.qytech.audioprobe.AudioMetadataProbe`。

---

## 1. 环境与依赖

- **系统要求**：Android API 29+ (Android 10+)
- **架构支持**：`arm64-v8a`
- **支持音频格式**：FLAC, APE, WAV, MP3, AAC, OGG, OPUS, WMA, ALAC, AIFF, DSD (DSF/DFF), SACD ISO, CUE 分轨表等

在模块级 `build.gradle.kts` 中添加依赖：

```kotlin
dependencies {
    implementation("io.github.qytech:qyaudioprobe:0.0.2-snapshot")
}
```

---

## 2. 常见场景使用方法

### 2.1 嗅探本地单曲（协程挂起，推荐）

适用于获取单首歌曲的完整信息、标签、内嵌封面与歌词。该方法为挂起函数，内部自动在 IO 线程调度，可直接在主线程协程中发起：

```kotlin
import com.qytech.audioprobe.AudioMetadataProbe
import androidx.lifecycle.viewModelScope
import kotlinx.coroutines.launch

viewModelScope.launch {
    val filePath = "/storage/emulated/0/Music/Hotel_California.flac"
    val result = AudioMetadataProbe.probe(filePath)

    result.onSuccess { info ->
        // 1. 音频格式与规格
        val format = info.format         // 编码格式，如 "FLAC", "DSD", "MP3"
        val sampleRate = info.sampleRate // 采样率 (Hz)，如 44100, 192000
        val bitDepth = info.bitDepth     // 位深 (bit)，如 16, 24
        val channels = info.channels     // 声道数，如 2 (立体声)
        val durationMs = info.durationMs // 时长 (毫秒)
        val isDsd = info.isDsd           // 是否为 DSD 音频

        // 2. 歌曲标签与封面
        val track = info.tracks.firstOrNull()
        val title = track?.title ?: "未知标题"
        val artist = track?.artist ?: "未知艺术家"
        val album = track?.album ?: "未知专辑"
        val coverPath = info.coverPath   // 本地封面图片绝对路径，可直接传给 Coil/Glide 加载
        val lyrics = info.lyrics         // 内嵌或同级伴生 LRC 歌词文本
    }.onFailure { error ->
        println("音频解析失败: ${error.message}")
    }
}
```

### 2.2 极速格式嗅探（<0.1ms，用于角标展示）

在播放列表或媒体库列表中，若只需快速展示格式标签（如 `DSD`, `Hi-Res`, `24bit/192kHz` 图标），调用 `probeFormatFast` 仅读取文件头部极少量字节，耗时不到 0.1 毫秒：

```kotlin
val profile = AudioMetadataProbe.probeFormatFast("/sdcard/Music/test.dsf")
if (profile != null) {
    println("格式: ${profile.format}, 采样率: ${profile.sampleRate}Hz, 声道: ${profile.channels}")
}
```

### 2.3 解析 CUE 分轨专辑或 SACD ISO

对于单张大文件搭配 CUE 分轨表（或 SACD ISO 镜像），`probe` 会自动将专辑拆解为完整的独立音轨列表：

```kotlin
val result = AudioMetadataProbe.probe("/storage/emulated/0/Music/Album.cue")

result.onSuccess { info ->
    println("专辑名称: ${info.tracks.firstOrNull()?.album}")
    println("总曲目数: ${info.tracks.size} 首")

    // 遍历专辑内每一首分轨
    info.tracks.forEach { track ->
        println("序号: ${track.trackNumber}, 标题: ${track.title}, 艺术家: ${track.artist}")
        println("分轨时长: ${track.durationMs} ms")
        println("在母带大文件中的起始偏移: ${track.startOffsetMs} ms, 结束偏移: ${track.endOffsetMs} ms")
    }
}
```

### 2.4 网络流与 HTTP Range 局部嗅探

针对 HTTP、WebDAV、私有网盘等远程音频链接，使用 `probeHttp` 可通过 HTTP Range 仅读取首尾少量关键帧，无需下载整首大文件：

```kotlin
val httpResult = AudioMetadataProbe.probeHttp(
    url = "https://example.com/music/test.flac"
)
httpResult.onSuccess { info ->
    println("远程音频时长: ${info.durationMs} ms, 格式: ${info.format}")
}
```

---

## 3. 核心 API 参考

| 方法 | 类型 | 说明 |
|---|---|---|
| `probe(filePath, dispatcher)` | 挂起函数 (main-safe) | 完整解析本地文件（标签、音轨、封面、歌词），返回 `Result<AudioProbeInfo>` |
| `probeSync(filePath)` | 同步阻塞 | 在当前调用线程同步解析本地文件，返回 `AudioProbeInfo?`（建议在后台线程调用） |
| `probeFormatFast(filePath)` | 同步极速 (<0.1ms) | 仅读取文件头格式信息，返回 `AudioFormatProfileInfo?` |
| `resourceVersionSync(filePath)` | 同步阻塞 | 获取伴生文件（LRC/CUE/封面）的最后修改时间戳，用于增量校验 |
| `probeHttp(url, headers)` | 挂起函数 (main-safe) | 基于 HTTP Range 局部嗅探远程网络音频 |
| `probeHttpCue(cueUrl, audioUrl)` | 挂起函数 (main-safe) | 嗅探远程 CUE 分轨表并关联物理音频 |
| `decodeText(bytes)` | 纯函数 | 自动识别字符集（GB18030, Big5, Shift-JIS, UTF-8 等）并转为 UTF-8 文本 |

---

## 4. 核心数据模型

### 4.1 `AudioProbeInfo`（音频信息实体）

| 字段 | 类型 | 说明 |
|---|---|---|
| `format` | `String` | 编码格式名称，如 `FLAC`, `DSD`, `APE`, `WAV`, `MP3`, `AAC` 等 |
| `container` | `String` | 容器格式名称 |
| `durationMs` | `Long` | 音频总时长（毫秒） |
| `sampleRate` | `Int` | 采样率（Hz），如 44100, 96000, 192000, 2822400 (DSD64) |
| `bitDepth` | `Int` | 采样位深（bit），如 16, 24, 32 |
| `channels` | `Int` | 声道数（1 为单声道，2 为立体声） |
| `bitrateKbps` | `Long` | 比特率（kbps） |
| `isDsd` | `Boolean` | 是否为 DSD 编码音频 |
| `coverPath` | `String?` | 提取落盘的本地高分辨率封面文件路径（支持 Coil / Glide 直接加载） |
| `lyrics` | `String?` | 提取到的歌词内容（支持内嵌 USLT / SYLT 标签及同名外部 LRC） |
| `tracks` | `List<AudioProbeTrack>` | 音轨列表（普通单曲为 1 轨；CUE / SACD ISO 为完整分轨列表） |
| `properties` | `Map<String, String>` | 音频流原始元数据扩展字典 |

### 4.2 `AudioProbeTrack`（分轨信息实体）

| 字段 | 类型 | 说明 |
|---|---|---|
| `trackNumber` | `Int?` | 音轨序号（如 1, 2, 3） |
| `discNumber` | `Int?` | 盘片序号（多碟专辑如 CD1, CD2） |
| `title` | `String` | 歌曲标题（若未填写则自动回退为文件名） |
| `artist` | `String` | 艺术家名称 |
| `album` | `String` | 专辑名称 |
| `albumArtist` | `String?` | 专辑艺术家 |
| `durationMs` | `Long` | 该音轨时长（毫秒） |
| `startOffsetMs` | `Long` | 在整轨母带文件中的起始偏移毫秒（单曲独立文件时为 0） |
| `endOffsetMs` | `Long?` | 在整轨母带文件中的结束偏移毫秒 |
| `lyrics` | `String?` | 该音轨对应的歌词文本 |
| `audioFilePath` | `String` | 对应的物理音频文件绝对路径 |

---

## 5. 常见问题与注意事项

1. **多语言与特殊编码乱码问题**：
   - 早期部分港台唱片或老歌采用 Big5、GBK / GB18030 或日文 Shift-JIS 编码。QYAudioProbe 内置了自适应智能字符集检测，会自动转换输出为标准的 UTF-8 字符串，无需宿主手动转码。
2. **封面图片缓存与加载**：
   - 解析到的内嵌封面会自动提取保存至应用缓存目录（如 `/data/user/0/<package>/cache/covers/`），返回的 `coverPath` 为标准的本地绝对路径。宿主可以直接使用 `AsyncImage(model = info.coverPath)` 进行展示。
3. **主线程安全性**：
   - `AudioMetadataProbe.probe` 挂起函数是 main-safe 的，可在 ViewModel 或 Compose 事件中直接安全调用。
