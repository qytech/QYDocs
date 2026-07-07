# Cdrom 更新日志

# Android External CD\-ROM Library \(CdRom\)



\[\![Maven Central](https://img.shields.io/maven-central/v/io.github.qytech/cdrom.svg)\]\(https://central\.sonatype\.com/artifact/io\.github\.qytech/cdrom\)



一个用于 Android 平台（主要针对车载/工控设备）的外部 USB 光驱控制库。支持 CD 播放（基于 Native Oboe）、光盘信息获取（CDDB/FreeDB）、抓轨以及硬件控制（进出仓）。



## 引入依赖 \(Installation\)



在你的 `build.gradle` \(Kotlin DSL\) 中添加：



```Kotlin
dependencies {
    // 请使用最新版本
    implementation("io.github.qytech:cdrom:0.2.5")
}
```



## 核心功能 \(Features\)



- **高性能播放**: 使用 Google Oboe 实现 Native 层音频回放，低延迟，支持 PCM 和 DTS CD。

- **硬件控制**: 支持光驱进仓、出仓、状态检测（无碟、开仓、就绪等）。

- **元数据支持**: 支持计算 DiscID \(FreeDB/GnuDB 标准\) 和光盘布局信息，方便对接在线元数据服务。

- **混合模式支持**: 完美处理 Mixed Mode CD \(数据\+音频\)，自动修正轨道时长，避免播放数据轨噪音。

- **抓轨功能**: 支持将 CD 音频轨道提取保存为 WAV 文件。

- **架构解耦**: 硬件控制 \(`CdromController`\) 与 播放引擎 \(`CdPlayer`\) 分离。

## 使用指南 \(Usage Guide\)



### 1\. 初始化



推荐在 ViewModel 中管理 `CdromController` 和 `CdPlayer` 的生命周期。



```Kotlin
// 1. 硬件控制器：负责状态监听、TOC 获取、抓轨、进出仓
private val cdromController = CdromController(context)

// 2. 播放器：负责音频播放控制 (Native Oboe)
private val cdPlayer = CdPlayer()

// 初始化逻辑
fun init() {
    // 设置硬件监听
    cdromController.setCdromDeviceListener(object : CdRomDeviceListener {
        override fun onAttached() {
            // 设备插入，初始化底层资源
            cdromController.init()
        }
        
        override fun onDetached() {
             // 设备拔出，释放资源
             stop()
        }
        
        override fun onDriveStatusChange(status: CdromDriveStatus) {
            // 处理光驱状态：如 CDS_TRAY_OPEN (开仓), CDS_DISC_OK (就绪)
        }
        
        override fun onDiscStatusChange(status: CdromDiscStatus) {
             // 处理光盘状态：如 CDS_AUDIO (CD), CDS_MIXED (混合光盘)
             if (status == CdromDiscStatus.CDS_AUDIO || status == CdromDiscStatus.CDS_MIXED) {
                 // 获取 TOC (轨道列表)
                 val toc = cdromController.getCdRomToc()
                 // 获取 DiscID 用于查询网络信息
                 val discId = cdromController.getFreeDBId()
             }
        }
    })
    
    // 设置播放监听
    cdPlayer.addListener(object : CdPlayerListener {
        override fun onProgress(current: Long, total: Long) {
            // 更新进度条
        }
        override fun onStateChanged(state: CdPlaybackState) {
            // 更新播放状态 (PLAYING, PAUSED, IDLE)
        }
        // ... 其他回调
    })
    
    // 首次初始化
    cdromController.init()
}
```



### 2\. 播放控制



```Kotlin
// 播放指定轨道 (trackIndex 从 1 开始)
fun play(trackIndex: Int) {
    // 准备并播放
    cdPlayer.prepare(trackIndex)
    cdPlayer.play()
}

// 暂停
fun pause() {
    cdPlayer.pause()
}

// 停止
fun stop() {
    cdPlayer.stop()
}

// 拖动进度 (0.0f - 1.0f)
fun seek(percent: Float) {
    val duration = cdPlayer.getDuration()
    val targetMs = (duration * percent).toLong()
    cdPlayer.seekTo(targetMs)
}
```



### 3\. 硬件控制 \(进出仓\)



```Kotlin
fun eject() {
    // 弹出前建议先停止播放
    cdPlayer.stop()
    
    // 发送弹出指令 (包含物理指令和软件指令的双重保障)
    val ret = cdromController.eject()
}

fun closeTray() {
    cdromController.closeTray()
}
```



### 4\. 抓轨 \(Ripping\)



```Kotlin
fun ripTrack(trackIndex: Int, savePath: String) {
    // 抓轨时必须停止播放
    cdPlayer.stop()
    
    cdromController.saveAudioTrackToFile(trackIndex, savePath, object : CdromProgressCallback {
        override fun onProgressUpdate(track: Int, progress: Float) {
            // 更新抓轨进度
        }
    })
}
```



### 5\. 资源释放



在 `onCleared` 或 `onDestroy` 中必须释放资源：



```Kotlin
fun release() {
    cdromController.removeCdromDeviceListener()
    cdromController.release()
    
    cdPlayer.removeListener(playerListener)
    cdPlayer.release()
}
```



---



## 更新日志 \(Changelog\)


### v0\.2\.5 \(20260616\)

1. 添加了 CdromTrayCloseEvent 关仓事件，需要打上对应补丁

```YAML
enum class CdromTrayCloseEvent(val code: Int) {
    *CLOSING*(0),
    *DISC_READY*(1),
    *CLOSED_EMPTY*(2),
    *UNKNOWN*(-1);
}



interface CdRomDeviceListener {
    fun onDetached()
    fun onAttached()
    fun onDiscStatusChange(status: CdromDiscStatus)
    fun onDriveStatusChange(status: CdromDriveStatus)
*    *fun onTrayCloseEvent(event: CdromTrayCloseEvent) {}
}
```

[0001\-report\-cdrom\-state\-event\-from\-kernel\.patch](图片和附件/0001-report-cdrom-state-event-from-kernel.patch)

### v0\.2\.4 \(202260615\)

1. 修复 discid\_get\_id 获取失败问题

### V0\.2\.3 （20260603）

1. 更新cdrom可能存在闪退、抓轨卡顿问题

### V0\.2\.2

1. 修复CDROM可能存在ANR问题

### v0\.2\.1

1. 修复了CD\-ROM和U盘同时使用检测异常问题

### v0\.2\.0

1. 修复CDROM HeapTaskDaemon 错误 

### v0\.1\.9

1. 修复播放时插拔再播放状态不对问题

2. 修复空盘状态下开关没有状态回调异常问题

### V0\.1\.8

1. 抓轨速度控制：在抓轨（ripping）时添加了转速控制参数，默认使用 x32 倍速以提高抓取效率。

    ```Plain Text
    cdrom.saveAudioTrackToFile(track, path, speed, cdTrackSaveProgress)
    ```

### v0\.1\.7

1. 添加了CDRom自动无缝播放的功能 

    ```Java
    interface CdPlayerListener {
        fun onPrepared()
        fun onProgress(current: Long, total: Long)
        fun onError(code: Int, msg: String)
        fun onStateChanged(state: CdPlaybackState)
        fun onComplete()
        
        // 新增当前轨迹回调
        fun onTrackChanged(trackIndex: Int)
    }
    
    
    interface CdromTrackCallback {
        fun onTrackCallback(data: ByteArray, size: Long, progress: Float)
        // 新增当前轨迹回调
        fun onTrackChanged(trackIndex: Int)
    }
    ```

### v0\.1\.6

1. 修复了 `CdPlayer` 中DTS播放失败问题

### v0\.1\.5

1. 修复了部分CDROM设备抓轨供电不足导致失败问题

### v0\.1\.4

1. 修复了可能出现 `monitorUeventLoop` 异常问题

### v0\.1\.3

- **\[重构\]** 引入全新的 `CdPlayer` 架构，底层采用 Oboe 实现高性能音频回放，显著降低延迟。

- **\[优化\]** `CdromController` 与播放逻辑解耦，专注于硬件控制和数据提取。

- **\[修复\]** 修复多线程下可能导致的 Use\-After\-Free 崩溃问题。

- **\[优化\]** 优化播放缓冲策略，解决播放进度可能出现的“快进”现象。

### v0\.1\.2

- **\[优化\]** 移除 Java 层 AudioTrack 依赖，全部音频流处理下沉至 Native 层。

- **\[修复\]** 修复在某些 Android 12\+ 设备上 USB 权限获取导致的初始化失败问题。

### v0\.1\.1

- **\[修复\]** 修复 DTS CD 播放异常（噪音或无法识别）的问题。

- **\[新增\]** 增加对 DTS 音频流的自动检测与解码支持。

### v0\.1\.0

- **\[修复\]** 修复 Mixed Mode CD \(混合模式光盘\) 最后一曲时长计算错误的问题（自动扣除 Data Track 前的 Gap）。

- **\[修复\]** 修复播放状态机逻辑：在 Pause 之后调用 Stop，再获取状态时仍返回 Pause 的问题。

### v0\.0\.8

- **\[修复\]** 修复了播放过程中可能存在的无法响应开仓指令的问题。

- **\[优化\]** 整体稳定性优化，减少 ANR。

- **\[变更\]** 内核更新了 cdrom 状态上报机制 \(Uevent\)，取消了库内部的定时轮询操作，降低 CPU 占用。

### v0\.0\.7

- **\[修复\]** 修复不同光盘调用 `getDiscId` 和 `getFreeDBDiscID` 可能返回相同 ID 的哈希冲突问题。

- **\[修复\]** 修复部分特定光驱插拔时导致的 Native 层闪退问题。

## 待办与已知问题 \(TODO / Known Issues\)



- \[Fixed in v0\.1\.3\] 部分客户反馈多次开光仓后无法获取到驱动状态问题 \(已通过重构状态机和 Uevent 监听解决\)。

- \[Fixed in v0\.1\.3\] 部分情况下可能存在播放无声音输出问题 \(已通过 Oboe 替换 AudioTrack 解决\)。

- \[Wait\] 针对极其老旧的 USB 光驱的兼容性测试。

