# QYTech CD-ROM 更新日志

本文档记录 QYTech CD-ROM (`io.github.qytech:cdrom`) 驱动与服务库的所有重要版本更新与变更。

## 0.2.8 - 2026-09-17

### 新增
- **生命周期完全解绑与后台全托管**：引入进程级单例管理器 `CdromRipManager`，彻底解除抓轨任务与 Activity / ViewModel 生命周期的绑定。即使界面退出、屏幕旋转、销毁调用 `controller.release()`，后台抓轨任务依然在守护单例中平稳运行，绝不误杀。
- **内置前台保活服务 (`CdromRipService`)**：库内置 Android 前台服务与 `PARTIAL_WAKE_LOCK`，利用 Manifest Merger 自动注入宿主（宿主无需额外配置 Manifest），有效防止 App 切入后台或息屏时被 Android 系统限制冻结（cgroup freezer）或查杀。
- **响应式状态流与重附着 (Re-attach)**：暴露 `controller.ripStatus: StateFlow<CdromRipStatus>`（支持 `Idle`、`Preparing`、`Ripping`、`Completed`、`Cancelled`、`Error`），新页面或重建页面打开时可立即无缝同步正在抓轨的音轨与精准百分比。
- **现代化异步抓轨 API**：新增 `controller.startRipTrack(track, path, speed)`、`controller.cancelRip()`、`controller.addRipProgressListener` 等接口；原有同步阻塞接口 `saveAudioTrackToFile(...)` 完全向后兼容并自动获得保活保护。

### 优化
- 改造 `CdromController.release()` 内部语义：后台抓轨任务活跃时自动保护底层 Native 控制器与硬件设备 `fd`，仅清理当前 UI 局部监听与 Handler 回调，杜绝资源泄漏与任务误杀。

---

## 0.2.7 - 2026-09-16

### 修复
- **防残卷与原子性保障**：使用 `.wav.tmp` 临时文件流式写入，100% 完整抓取并校验通过后原子重命名至最终目标 `.wav`。中途取消或硬件报错立即物理清理，杜绝在磁盘遗留几秒残缺破损文件。
- **动态扇区边界截断**：读取严格对齐音轨结束 LBA，防止跨入光盘 Lead-out 触发物理报错。
- **伺服提速稳定检测**：从 1x 播放提速至高速（如 32x）抓轨时自动进行主轴马达伺服锁定检测，彻底杜绝先播放后抓轨进度卡 0% 的死锁现象。
- **驱动硬件互斥锁**：引入底层硬件互斥锁（`ioMtx` 与 `ripMtx`），抓轨自动安全排斥并发播放，杜绝多线程竞争底层 ioctl。

---

## 0.2.6 - 2026-09-02

### 优化
- 优化 CD 播放功能稳定性，降低偶发卡顿和无响应风险。
- 改进光盘托盘开关的异常恢复能力。
- 增强设备状态识别与兼容性，提升使用可靠性。

---

## 0.2.5 - 2026-06-16

### 新增
- 添加 `CdromTrayCloseEvent` 关仓事件（`CLOSING`、`DISC_READY`、`CLOSED_EMPTY`），支持精准感知关仓机械动作与盘片稳定状态。
- `CdRomDeviceListener` 新增 `onTrayCloseEvent(event: CdromTrayCloseEvent)` 回调。

---

## 0.2.4 - 2026-06-15

### 修复
- 修复 `discid_get_id` 获取失败问题。

---

## 0.2.3 - 2026-06-03

### 修复
- 修复 CD-ROM 可能存在的闪退与抓轨卡顿问题。

---

## 0.2.2 - 2026-05-20

### 修复
- 修复 CD-ROM 可能存在的 ANR 问题。

---

## 0.2.1 - 2026-05-10

### 修复
- 修复 CD-ROM 和 U 盘同时使用时设备检测异常问题。

---

## 0.2.0 - 2026-04-18

### 修复
- 修复 CD-ROM `HeapTaskDaemon` 异常问题。

---

## 0.1.9 - 2026-03-25

### 修复
- 修复播放时插拔光驱再播放状态异常的问题。
- 修复空盘状态下托盘开关没有状态回调的问题。

---

## 0.1.8 - 2026-03-10

### 新增
- 抓轨速度控制：抓轨（ripping）接口增加转速控制参数 `speed`，默认使用 32x 倍速以提高抓取效率。

---

## 0.1.7 - 2026-02-20

### 新增
- 新增 CD-ROM 自动无缝播放功能与跨曲目切换监听回调 `onTrackChanged(trackIndex: Int)`。

---

## 0.1.6 - 2026-01-15

### 修复
- 修复 `CdPlayer` 中 DTS-CD 播放失败问题。

---

## 0.1.5 - 2025-12-10

### 修复
- 修复部分 CD-ROM 设备抓轨时供电不足导致失败的问题。

---

## 0.1.4 - 2025-11-20

### 修复
- 修复可能出现的 `monitorUeventLoop` 线程异常退出问题。

---

## 0.1.3 - 2025-10-15

### 重构
- 引入全新 `CdPlayer` 架构，底层采用 Google Oboe 实现高性能音频回放，显著降低延迟。
- `CdromController` 与播放逻辑解耦，专注于硬件控制和数据提取。

### 修复
- 修复多线程并发操作下可能导致的 Use-After-Free 内存崩溃。
- 优化播放缓冲策略，解决播放进度可能出现的“快进”跳音现象。

---

## 0.1.2 - 2025-09-10

### 优化
- 移除 Java 层 AudioTrack 依赖，全部音频流处理下沉至 Native 层。
- 修复在某些 Android 12+ 设备上 USB 权限获取导致的初始化失败问题。

---

## 0.1.1 - 2025-08-15

### 新增
- 增加对 DTS 音频流的自动检测与解码支持。

### 修复
- 修复 DTS CD 播放异常（噪音或无法识别）的问题。

---

## 0.1.0 - 2025-07-20

### 修复
- 修复 Mixed Mode CD (混合模式光盘) 最后一曲时长计算错误的问题（自动扣除 Data Track 前的 Gap）。
- 修复播放状态机逻辑：在 Pause 之后调用 Stop，再获取状态时仍返回 Pause 的问题。

---

## 0.0.8 - 2025-06-15

### 优化
- 内核更新 CD-ROM 状态上报机制 (Uevent)，取消库内部的定时轮询操作，大幅降低 CPU 占用。
- 整体稳定性优化，减少 ANR。

### 修复
- 修复播放过程中可能存在的无法响应开仓指令的问题。

---

## 0.0.7 - 2025-05-20

### 修复
- 修复不同光盘调用 `getDiscId` 和 `getFreeDBDiscID` 可能返回相同 ID 的哈希冲突问题。
- 修复特定光驱插拔时导致的 Native 层闪退问题。
