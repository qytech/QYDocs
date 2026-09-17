# QYMediaScanner Android SDK <img src="https://img.shields.io/badge/★_推荐-Recommended-success?style=flat-square" alt="推荐" style="vertical-align: middle;">

[![Maven Central](https://img.shields.io/maven-central/v/io.github.qytech/qymediascanner.svg)](https://central.sonatype.com/artifact/io.github.qytech/qymediascanner)
[![Changelog](https://img.shields.io/badge/Changelog-CHANGELOG.md-blue.svg)](./CHANGELOG.md)
<img src="https://img.shields.io/badge/★_推荐-Recommended-success?style=flat-square" alt="推荐" style="vertical-align: middle;">

QYMediaScanner 是专为 Android HiFi 播放设备设计的高性能多线程媒体扫描引擎。用于扫描本地存储、SD 卡、U 盘、移动硬盘或局域网共享目录中的音频文件，自动提取完整歌曲标签与封面，支持流式批量持久化和秒级增量复扫。客户统一使用 `com.qytech.mediascanner.QYMediaScanner`。

---

## 1. 环境与依赖

- **系统要求**：Android API 29+ (Android 10+)
- **架构支持**：`arm64-v8a`
- **支持文件格式**：FLAC, WAV, DSF, DFF, APE, MP3, M4A, AAC, OGG, OPUS, WMA, ALAC, AIFF, CUE 分轨等常见音频文件

在模块级 `build.gradle.kts` 中添加依赖：

```kotlin
dependencies {
    implementation("io.github.qytech:qymediascanner:0.0.2-snapshot")
}
```

---

## 2. 常见场景使用方法

### 2.1 流式批量扫描入库（推荐，适合海量曲库）

这是最推荐的核心用法。扫描引擎通过 `onBatch` 定期将一组曲目（如 300 首）回调给宿主，宿主可以直接在数据库中以单个事务批量写入。这样既保证了万首曲库扫描时内存零堆积，又保证了界面进度条的流畅更新：

```kotlin
import com.qytech.mediascanner.QYMediaScanner
import androidx.lifecycle.viewModelScope
import kotlinx.coroutines.launch

class MediaLibraryViewModel : ViewModel() {
    // 实例化扫描器：工作线程数推荐配置为 2 ~ 4（平衡性能与发热）
    private var scanner: QYMediaScanner? = null

    fun startScan(directoryPath: String) {
        viewModelScope.launch {
            val mediaScanner = QYMediaScanner(maxWorkers = 2)
            scanner = mediaScanner

            val report = mediaScanner.scanDirectoryStreaming(
                directoryPath = directoryPath,
                batchSize = 300, // 推荐每批 300 首，与数据库事务深度契合
                onDiscovery = { totalFiles ->
                    // 1. 发现文件总数回调：可用于初始化进度条最大值
                    println("在目录中发现音频文件: $totalFiles 个")
                },
                onProgress = { percent, currentFile ->
                    // 2. 扫描实时进度：百分比 (0~100) 与当前正在处理的文件路径
                    println("进度: $percent%, 正在处理: $currentFile")
                },
                onBatch = { batchTracks ->
                    // 3. 批量音轨分发：将该批次批量写入 Room / 本地数据库
                    println("收到批次音轨: ${batchTracks.size} 首，执行批量持久化")
                    myMediaRepository.insertTracksBatch(batchTracks)
                }
            )

            // 4. 扫描完成汇总
            println("扫描结束！耗时: ${report.elapsedMs} ms, 成功入库: ${report.scannedTracks} 首")
            println("跳过未变动: ${report.unchangedTracks} 首, 失败文件数: ${report.failedFiles}")
        }
    }

    fun stopScan() {
        // 用户点击“取消扫描”时，立即原子中断
        scanner?.cancel()
    }
}
```

### 2.2 全量小型扫描（适合小型单目录）

如果只需要快速扫描一个包含几十首歌曲的小文件夹（如单张专辑目录），可使用单次扫描接口：

```kotlin
val (report, trackList) = scanner.scanDirectory(
    directoryPath = "/storage/USB_DISK/Jay_Chou_Album",
    onProgress = { percent, currentFile ->
        println("正在扫描: $percent%")
    }
)

println("扫描完成，共找到 ${trackList.size} 首歌曲")
```

### 2.3 增量极速复扫（秒级完成十万首复扫）

当用户再次点击“扫描”或接入已有磁盘时，可以通过传入已有数据库中的文件修改时间与伴生资源修改时间，引擎会自动比对并直接跳过未变动文件，十万首大曲库也能在数秒内完成复扫：

```kotlin
// 1. 从宿主数据库中查询现有文件的修改时间快照
val fileModTimes: Map<String, Long> = myDatabase.getAllFileModifiedTimes()
val resourceModTimes: Map<String, Long> = myDatabase.getAllResourceModifiedTimes()

// 2. 编码为版本比对快照
val versionBuffer = QYMediaScanner.encodeVersionCache(
    versions = fileModTimes,
    resourceVersions = resourceModTimes
)

// 3. 传入快照发起增量扫描
val report = scanner.scanDirectoryStreaming(
    directoryPath = "/storage/emulated/0/Music",
    batchSize = 300,
    versionCacheBuffer = versionBuffer,
    onBatch = { batchTracks ->
        // 每首音轨的 isUnchanged 标识表示该文件是否未变动
        // 增量复扫时，只需对发生变化或新增的曲目进行数据库更新
        val changedTracks = batchTracks.filterNot { it.isUnchanged }
        if (changedTracks.isNotEmpty()) {
            myMediaRepository.insertTracksBatch(changedTracks)
        }
    }
)
```

---

## 3. 核心 API 参考

| 方法 | 类型 | 说明 |
|---|---|---|
| `scanDirectoryStreaming(...)` | 挂起函数 | 流式批量扫描指定目录，支持背压与增量比对快照，返回 `MediaScanReport` |
| `scanDirectory(directoryPath, onProgress)` | 挂起函数 | 单次全量扫描指定目录，返回 `(MediaScanReport, List<CanonicalScannedTrack>)` |
| `cancel()` | 普通方法 | 立即原子取消当前正在执行的扫描任务 |
| `encodeVersionCache(versions, resourceVersions)` | 伴生工具 | 将文件修改时间字典编码为高效版本快照，用于增量复扫 |

---

## 4. 核心数据模型

### 4.1 `CanonicalScannedTrack`（扫描音轨实体）

| 字段 | 类型 | 说明 |
|---|---|---|
| `sourcePath` | `String` | 音频文件在磁盘上的物理绝对路径 |
| `uri` | `String` | 文件的 URI 形式 |
| `title` | `String` | 歌曲标题（音频标签为空时自动回退为文件名） |
| `artist` | `String` | 艺术家名称 |
| `album` | `String` | 专辑名称 |
| `albumArtist` | `String` | 专辑艺术家 |
| `genre` | `String` | 音乐流派（如 Pop, Classical, Rock） |
| `year` | `Int?` | 发行年份 |
| `trackNumber` | `Int?` | 音轨序号（如 1, 2, 3） |
| `discNumber` | `Int?` | 盘片序号（如 1, 2） |
| `durationMs` | `Long` | 歌曲时长（毫秒） |
| `sampleRate` | `Int` | 采样率（Hz），如 44100, 192000 |
| `bitDepth` | `Int` | 采样位深（bit），如 16, 24 |
| `channels` | `Int` | 声道数（1 为单声道，2 为双声道） |
| `bitrateKbps` | `Long` | 比特率（kbps） |
| `format` | `String` | 格式名称（如 `FLAC`, `DSD`, `WAV`, `MP3`） |
| `isDsd` | `Boolean` | 是否为 DSD 编码音频 |
| `isCueTrack` | `Boolean` | 是否由 CUE 分轨表生成的独立音轨 |
| `cuesheetPath` | `String?` | 关联的 CUE 文件路径 |
| `lyrics` | `String?` | 内嵌歌词或同目录伴生歌词 |
| `embeddedPicturePath` | `String?` | 内嵌封面提取保存的本地图片路径 |
| `externalPicturePath` | `String?` | 同级目录中发现的封面图片路径（如 `cover.jpg`, `folder.jpg`） |
| `isUnchanged` | `Boolean` | 增量扫描中文件是否未发生修改 |

### 4.2 `MediaScanReport`（扫描结果报告）

| 字段 | 类型 | 说明 |
|---|---|---|
| `totalFiles` | `Int` | 发现的音频文件总数 |
| `scannedTracks` | `Int` | 成功解析并输出的有效音轨总数 |
| `unchangedTracks` | `Int` | 命中增量缓存跳过重复解析的音轨数 |
| `failedFiles` | `Int` | 解析失败或损坏的文件总数 |
| `traversalFailures` | `Int` | 因权限不足或磁盘 I/O 错误无法访问的目录/文件数 |
| `probeFailedFiles` | `Int` | 物理文件可访问但音频元数据损坏的文件数 |
| `elapsedMs` | `Long` | 扫描总耗时（毫秒） |
| `cancelled` | `Boolean` | 用户是否主动取消了扫描 |
| `complete` | `Boolean` | 目录遍历是否完整完成（无意外中断） |

---

## 5. 推荐配置与最佳实践

1. **工作线程数推荐 (`maxWorkers`)**：
   - **数播一体机 / 车机**：推荐配置为 **`2 ~ 4`**。在 4 核设备实测中，4 线程可获得 **2.3× 综合加速**，总扫描耗时大幅缩减，且设备平均 CPU 占用率仅约 26%，温升仅 2.7 °C，处于极佳的能效与温控平衡状态。
   - **便携 HiFi 播放器（电池供电）**：推荐配置为 **`2`**，兼顾扫描速度与续航发热。
2. **批次大小推荐 (`batchSize`)**：
   - 推荐配置为 **`200 ~ 500`** 首/批（默认 300 首最佳），配合 Room 的 `@Transaction` 批量写入，可彻底杜绝频繁的小事务导致的主线程 UI 卡顿。
3. **真机性能数据参考**：
   - 查看在数播一体机真机上针对 4,000+ 首无损音频的完整压测报告：[扫描与入库性能基准测试报告](benchmark-report.md)。
