# Android External CD-ROM Library (CdRom)

[![Maven Central](https://img.shields.io/maven-central/v/io.github.qytech/cdrom.svg)](https://central.sonatype.com/artifact/io.github.qytech/cdrom)
[![Changelog](https://img.shields.io/badge/Changelog-CHANGELOG.md-blue.svg)](./CHANGELOG.md)



一个用于 Android 平台（主要针对车载/工控设备）的外部 USB 光驱控制库。支持 CD 播放（基于 Native Oboe）、光盘信息获取（CDDB/FreeDB）、抓轨以及硬件控制（进出仓）。



## 引入依赖 (Installation)



在你的 `build.gradle` (Kotlin DSL) 中添加：



```Kotlin
dependencies {
    // 请使用最新版本
    implementation("io.github.qytech:cdrom:0.2.8")
}
```



### 权限说明 (Permissions)

AAR 库已内置并自动合并以下权限（宿主应用无需手动在 Manifest 中声明）：

```xml
<uses-permission android:name="android.permission.WAKE_LOCK" />
<uses-permission android:name="android.permission.FOREGROUND_SERVICE" />
<uses-permission android:name="android.permission.FOREGROUND_SERVICE_DATA_SYNC" />
<uses-permission android:name="android.permission.POST_NOTIFICATIONS" />
```



## 核心功能 (Features)



- **高性能播放**: 使用 Google Oboe 实现 Native 层音频回放，低延迟，支持 PCM 和 DTS CD。

- **硬件控制**: 支持光驱进仓、出仓、状态检测（无碟、开仓、就绪等）以及基于内核 Uevent 的状态通知。

- **元数据支持**: 支持计算 DiscID (FreeDB/GnuDB 标准) 和光盘布局信息，方便对接在线元数据服务。

- **混合模式支持**: 完美处理 Mixed Mode CD (数据+音频)，自动修正轨道时长，避免播放数据轨噪音。

- **生命周期解绑与后台全托管**:
  - **单例任务管理 (`CdromRipManager`)**: 抓轨生命周期彻底提升到进程级，独立于 Activity / ViewModel 页面。页面退出、重建或调用 `controller.release()` 时后台抓轨继续稳定运行，绝不误杀。
  - **内置保活守护服务 (`CdromRipService`)**: 抓轨期间自动提升为前台服务并持有 `PARTIAL_WAKE_LOCK`，防止切后台或息屏被系统冻结/挂起。
  - **状态单一来源与重附着 (Re-attach)**: 暴露响应式 `StateFlow<CdromRipStatus>`，页面重新进入时自动无缝接管并恢复抓轨进度显示。

- **高可靠原子抓轨引擎**:
  - **防残卷与原子性**: 采用 `.wav.tmp` 流式写入，100% 完整抓取并通过校验后原子替换至目标 `.wav`。取消或失败立即清理，杜绝在磁盘遗留残缺破损文件。
  - **伺服加速稳定**: 1x 提速至 32x 高速抓轨时自动进行马达伺服锁定检测，彻底杜绝播放后紧接抓轨进度卡 0% 的死锁。
  - **硬件互斥与总线独占**: 驱动层内置互斥锁，抓轨自动安全排斥并发播放，杜绝多线程竞争光驱底盘。

- **架构解耦**: 硬件控制 (`CdromController`) 与 播放引擎 (`CdPlayer`) 分离。

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



### 4. 抓轨 (Ripping)

抓轨将 CD 音轨高速提取并以标准 RIFF WAV (44.1kHz 16-bit Stereo PCM) 格式保存到本地文件。库内自带进程级后台守护单例与前台服务保活，即使发起调用的 Activity / ViewModel 被销毁，任务依然持续执行直到完成。

#### 方式 A：响应式异步托管（推荐）

```kotlin
// 1. 启动异步抓轨（默认 32x 倍速，由库内守护线程独立执行）
val targetFile = File(context.cacheDir, "track_01.wav")
cdromController.startRipTrack(
    track = 1,
    path = targetFile.absolutePath,
    speed = 32
)

// 2. 响应式监听进程级全局状态（支持页面重建与重新附着）
lifecycleScope.launch {
    cdromController.ripStatus.collect { status ->
        when (status) {
            is CdromRipStatus.Preparing -> println("准备中: Track ${status.track}")
            is CdromRipStatus.Ripping -> println("抓轨中: Track ${status.track}, 进度: ${(status.progress * 100).toInt()}%")
            is CdromRipStatus.Completed -> println("已完成: ${status.outputPath}")
            is CdromRipStatus.Cancelled -> println("已取消")
            is CdromRipStatus.Error -> println("抓轨失败: ${status.errorMessage} (code=${status.errorCode})")
            is CdromRipStatus.Idle -> println("空闲就绪")
        }
    }
}

// 3. 用户主动点击取消抓轨
fun cancelRip() {
    cdromController.cancelRip()
}
```

#### 方式 B：同步阻塞式调用（向下兼容）

```kotlin
val targetFile = File(context.cacheDir, "track_01.wav")
val speed = 32 // 建议 1~32x

// 内部自动受到后台保活服务与 WakeLock 保护
val result = cdromController.saveAudioTrackToFile(
    track = 1,
    path = targetFile.absolutePath,
    speed = speed,
    callback = object : CdromProgressCallback {
        override fun onProgressUpdate(track: Int, progress: Float) {
            // progress: 0.0f ~ 1.0f
        }
    }
)
```

#### 抓轨状态码速查表

| 状态码 | 含义 | 行为表现与磁盘文件状态 |
|:---:|---|---|
| **`0`** | **抓轨成功** | 100% 扇区读取并通过校验，临时 `.wav.tmp` 成功原子重命名为目标路径，回调 `1.0f`。 |
| **`-1`** | **主动取消** | 调用 `cancelRip()` 或 `stopSaveTrack()`。**立即物理删除 `.tmp` 文件，目标路径不存在任何文件**。 |
| **`-2`** | **硬件 / I/O 错误** | 物理扇区重试失败、断开连接或磁盘写入故障。立即物理删除 `.tmp` 文件，无残卷遗留。 |
| **`-3`** | **重命名失败** | 抓轨完成但系统重命名系统调用失败（如权限不足），自动删除 `.tmp` 文件。 |
| **`-4`** | **任务重入排斥** | 已有抓轨线程正在执行中，互斥锁阻止重入。 |
| **`1`** | **参数/光盘未就绪** | 无效音轨号或光驱状态非 `CDS_DISC_OK`，不执行读盘动作。 |

### 5. 资源释放 (Resource Release)

在页面销毁（如 `onCleared` 或 `onDestroy`）中释放本地监听资源：

```kotlin
fun release() {
    // 释放 Controller 本地监听资源
    // 【重要提示】：若后台当前正在抓轨，release() 会自动保护底层硬件与抓轨任务持续运行，绝不误杀！
    cdromController.removeCdromDeviceListener()
    cdromController.release()
    
    cdPlayer.removeListener(playerListener)
    cdPlayer.release()
}
```

> **注意**：切勿在 `onCleared()` 中调用 `stopSaveTrack()` 或 `cancelRip()`！取消方法仅能在用户明确点击 UI“停止/取消”按钮时调用。离开页面时调用 `cdromController.release()` 会安全保留后台抓轨，用户重新进入该页面时会自动恢复进度。



---



## 更新日志 (Changelog)

> 完整独立变更历史请参阅专属更新日志文档：**[CHANGELOG.md](./CHANGELOG.md)**

### v0.2.8 (20260917)
1. **生命周期完全解绑与后台全托管**：引入进程级单例管理器 `CdromRipManager`，彻底解除抓轨任务与 Activity / ViewModel 生命周期的绑定。即使界面退出、屏幕旋转、销毁调用 `controller.release()`，后台抓轨任务依然在守护单例中平稳运行，绝不误杀。
2. **内置前台保活服务**：内置 `CdromRipService` 与 `PARTIAL_WAKE_LOCK`，Manifest Merger 自动合并，有效防止 App 切入后台或息屏时被 Android 系统限制冻结（cgroup freezer）或查杀。
3. **状态单一来源与重附着（Re-attach）**：暴露响应式 `controller.ripStatus: StateFlow<CdromRipStatus>`，新页面或重建页面打开时自动无缝同步正在抓轨的音轨与精准百分比。
4. **现代化异步 API**：新增 `controller.startRipTrack(track, path, speed)`、`controller.cancelRip()`、`controller.addRipProgressListener` 等接口；原有同步阻塞接口 `saveAudioTrackToFile(...)` 完全向后兼容并自动获得保活保护。

### v0.2.7 (20260916)
1. **防残卷与原子性保障**：使用 `.wav.tmp` 临时文件流式写入，100% 完整抓取并校验通过后原子重命名至最终目标 `.wav`。中途取消或硬件报错立即物理清理，杜绝在磁盘遗留残缺破损文件。
2. **动态扇区边界截断**：读取严格对齐音轨结束 LBA，防止跨入光盘 Lead-out 触发物理报错。
3. **伺服提速稳定检测**：从 1x 播放提速至高速（如 32x）抓轨时自动进行主轴马达伺服锁定检测，彻底杜绝先播放后抓轨进度卡 0% 的死锁现象。
4. **驱动硬件互斥锁**：引入底层硬件互斥锁，抓轨自动安全排斥并发播放，杜绝多线程竞争底层 ioctl。

### v0.2.6 (20260902)
1. 优化 CD 播放功能稳定性，降低偶发卡顿和无响应风险。
2. 改进光盘托盘开关的异常恢复能力。
3. 增强设备状态识别与兼容性，提升使用可靠性。

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

