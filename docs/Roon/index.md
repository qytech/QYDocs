# Roon Android SDK

[![Maven Central](https://img.shields.io/maven-central/v/io.github.qytech/roon.svg)](https://central.sonatype.com/artifact/io.github.qytech/roon)

当前版本：`0.1.3`，提供 Roon 音频接收、播放控制、设备音频能力查询与宿主音源切换接口。

## 添加依赖

```kotlin
implementation("io.github.qytech:roon:0.1.3")
```

## 升级说明

高采样率播放需要宿主按实际输出能力启动 Roon。在输出路由稳定后，于后台线程查询；`outputDevice` 为宿主确认的实际媒体输出设备，不能仅按已连接设备的优先级选择。

```kotlin
import com.qytech.roon.extensions.getSupportedRoonFormats

val supportedFormats = applicationContext.getSupportedRoonFormats(outputDevice)
val maxDsdRate = supportedFormats
    .filter { it.sampleType.equals("DSD", ignoreCase = true) }
    .maxOfOrNull { it.sampleRate / 44_100 } ?: 0
```

将 `supportedFormats` 和 `maxDsdRate` 传入现有 `RoonServiceManager.startRoon` 调用。查询结果为空时保持未启动，并提示当前输出没有可用格式。已有宿主若使用固定格式列表或 192 kHz 上限，需要同步调整；实际支持规格取决于设备、固件与输出通道。

切换输出后需要重新查询，并在关闭旧 Roon 接收服务后重新启动以更新格式协商。`updateSignalPath()` 只更新输出路径信息。Roon 开关显示与 ARC 输入切换仍由宿主应用管理。

### 多音源切换

`0.1.3` 新增输出交接接口。已有 `init(context, callback, playbackController)` 入口保留；同时集成本地播放、CD 或其他接收协议的宿主，应接入以下流程，仅升级依赖不会自动完成宿主音源管理。

- **从 Roon 切到其他音源**：在非主线程的串行播放控制任务中调用 `RoonServiceManager.releasePlaybackOutput()`。它会等待当前 Roon 音频输出释放，返回 `true` 后才可启动下一音源；返回 `false` 时停止本次切换并提示失败。请求已取消或被更新时，也不得继续启动下一音源。此方法保留 Roon 接收服务，`pause()` 仍用于普通暂停。
- **从其他音源切回 Roon**：初始化时传入 `IRoonOutputCallback`。`onPreparePlaybackOutput(request)` 回调中将工作派发到宿主的串行播放控制任务后立即返回，不阻塞 Binder 回调线程。开始释放旧音源前检查 `request.isCurrent()`；确认旧音源实际释放后再次检查，仍有效才调用 `request.complete(true)`。释放失败时对仍有效的请求调用 `request.complete(false)`。过期请求不得改变当前音源，也不得启动输出。

```kotlin
RoonServiceManager.init(
    appContext = applicationContext,
    callback = roonCallback,
    playbackController = playbackController,
    outputCallback = outputCallback,
)
```

其中 `outputCallback` 由宿主实现 `IRoonOutputCallback.Stub()`，其回调参数为 `IRoonOutputPreparation`。播放控制、取消操作和音源归属更新应在宿主同一串行任务中处理，异步释放完成后仍需核对请求是否有效。SDK 的准备请求在 5 秒后失效；拒绝、超时或回调断开时不会开始本次输出。

不再使用 Roon 功能时，调用 `RoonServiceManager.release()` 注销回调并解绑服务。普通音源切换无需关闭接收服务。

已知限制：部分设备停止 Roon 接收服务时仍可能异常退出，本版本未包含该 SDK 内部问题的修复。输出释放接口不能视为该问题已解决；独立集成、双向音源切换与长期播放仍需在目标设备上复验。

## 更新日志

### v0.1.3（2026-10-23）

- 新增音频输出释放接口，供宿主在切换音源前确认 Roon 已释放输出。
- 新增播放前准备回调，支持宿主先释放其他音源，再允许 Roon 开始输出。
- 改善输出切换时的停止与重新准备流程，阻止已失效的播放请求重新占用输出。
- 保留原有初始化入口与普通暂停行为；多音源交接需要宿主接入新增接口。

### v0.1.2（2026-10-20）

- 修复部分场景下播放中断及异常退出问题。
- 改善暂停、恢复与音频格式切换时的播放稳定性。
- 完善设备音频能力识别，支持按实际输出通道上报 PCM/DSD 格式。

### v0.1.1（2026-09-29）

1. 修复部分 24-bit 及高规格曲目播放异常与噪声问题，提升高码率音频输出品质
2. 新增 MQA 核心解码支持与状态指示
3. 新增输出信号路径（模拟、数字、USB）动态识别与实时上报
4. 优化音频输出稳定性，消除偶发断音与播放欠载
5. 完善硬件音量双向联动与状态同步
6. 优化断网恢复与离线连接机制，增强网络自愈稳定性
7. 补齐封面二进制流与完整多语言元数据展示支持

### v0.1.0（2026-06-23）

1. 更新了 Roon Raat 1.1.47
2. 修复了 Roon 播放 DSD512 卡顿问题
3. 新增了 Roon 封面同步

```kotlin
override fun onArtworkChanged(mimeType: String?, data: ByteArray?) {
}
```


