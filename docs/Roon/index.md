# Roon Android SDK

[![Maven Central](https://img.shields.io/maven-central/v/io.github.qytech/roon.svg)](https://central.sonatype.com/artifact/io.github.qytech/roon)

当前版本：`0.1.6`，提供 Roon 音频接收、播放控制、设备音频能力查询与宿主音源切换接口。

## 依赖与运行环境

```kotlin
implementation("io.github.qytech:roon:0.1.6")
```

- Android API 29+，仅提供 `arm64-v8a`；宿主需包含 SDK 的 Native 库。
- 保留 SDK 清单声明的 `RoonService` 独立进程 `:roon_process`，不要合并到宿主主进程或改名。关闭端点时会检查该进程名并退出专用进程。

## 升级说明

### 从 0.1.5 升级到 0.1.6

`0.1.6` 保留现有 `RoonServiceManager`、`IRoonCallback` 和 `IRoonOutputCallback` 公共接口，升级后行为如下：

- **回调连接恢复**：`IRoonCallback` 改为单一连接托管并监听 Binder 死亡；发送失败时仅清理当前失效订阅而不向上抛出 `RemoteException`，活跃播放与其它回调不受影响。宿主恢复或重建后需重新调用 `registerCallback(...)` / `registerOutputCallback(...)` 恢复订阅。
- **输出握手重连**：`RoonOutputHandshake` 在单次 5 秒截止时间内，支持在宿主重连或替换时等待并重发输出准备请求；宿主显式拒绝、注销、停止或切源接管仍立即取消准备。

### 从 0.1.4 升级到 0.1.5

`0.1.5` 保留现有初始化、播放控制和音源交接公共接口。升级依赖后，需确认以下行为：

- **交出输出后重新播放**：调用 `releasePlaybackOutput()` 会取消 Roon 的音源选择状态，阻止自动下一曲或迟到的准备请求重新占用输出。重新使用 Roon 时，由用户在 Roon 端明确发起播放，SDK 再通过已有准备回调向宿主申请输出。
- **关闭与重启服务**：关闭端点时，SDK 释放音频输出并退出专用 `:roon_process`，最终退出路径不再调用已失效的 RAAT 回调。宿主关闭功能仍使用 `RoonServiceManager.release()`；再次开启时重新调用 `init(...)` 和 `startRoon(...)`，不要复用旧服务连接。
- **恢复播放**：网络恢复或重新打开 Roon 后，服务恢复不等于自动续播。已记录的回归通过 Roon Core 显式播放恢复，宿主不应承诺自动续播。

本次未修改 RAAT SDK 二进制，也不包含系统音频 HAL 补丁；不能据此推断所有 SDK 生命周期问题均已解决。

### 从 0.1.3 或更早版本升级

`0.1.4` 保留现有初始化、播放控制和音源交接接口，无需新增宿主调用。使用 SDK 内置 PCM 输出时，播放位置上报和分组定时起播改为依据有效的硬件呈现时钟；设备需要提供正确的音频时间戳。时钟暂时不可用时，不会用软件累计时间强行开始本次定时播放。

本次时钟改进主要适用于内置 PCM 输出。DSD、DoP、DSD 转 PCM 的源路径及宿主自定义播放控制器仍沿用既有时钟逻辑，需要在目标设备上分别验证。SDK 不包含系统音频固件，也不要求所有设备统一刷入 HAL 补丁；只有确认固件存在时间戳或帧计数错误时，才需要设备厂商处理。

输出交接会等待旧音频输出实际释放完成。宿主仍应在后台串行任务中调用 `releasePlaybackOutput()`，仅在返回 `true` 且切换请求仍有效时启动下一音源；失败、超时或中断时不得继续切换。

## 输出格式与路由

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

## 多音源切换

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

## 生命周期与资源释放

不再使用 Roon 功能时，调用 `RoonServiceManager.release()` 注销回调并解绑服务。普通音源切换无需关闭接收服务。

三种操作的用途不同：

| 操作 | 用途 | 完成条件 |
|------|------|------|
| `pause()` | 普通暂停 | 不作为输出已释放的确认 |
| `releasePlaybackOutput()` | 切换到其他音源，保留接收服务 | 后台串行调用返回 `true`，且宿主切换请求仍有效 |
| `release()` | 关闭 Roon 功能 | 注销回调、解绑并停止服务；不作为同步输出交接接口 |

## 验证范围与已知限制

根据 `0.1.5` 发布验收记录，2026-11-07 的 app-cadenza Release 在 RK3576 / SPDIF / S32、44.1 kHz 环境完成 10 轮播放中网络接口断开/恢复、5 轮播放中关闭/重开 Roon，以及约 8 分 8 秒连续播放，未出现新增崩溃。恢复播放由 Roon Core 显式触发。Native CTest 4/4、Roon 46 项及播放器 280 项 JVM 测试通过。

2026-11-09 发布记录确认 `0.1.5` AAR 与上述验收候选字节一致；发布当天未重新执行实机测试。上述结果来自关联项目的验收记录，不是本文档维护时重新运行的测试。

- `0.1.5` 修复了断网后最终退出时调用失效回调导致的已知崩溃路径；不代表 RAAT SDK 内部所有生命周期缺陷均已修复。
- 普通暂停期间，已排队的音频可能继续输出至队列排空；暂停即时静音与快速恢复需在目标设备上复验。
- 本次回归未覆盖物理听音、小时级长稳、物理网线插拔、其他格式/输出或 64 位 HAL 服务播放。分组同步、DSD/DoP、双向音源切换等场景仍需在目标设备上分别验收。
- Maven 服务端发布状态已确认；发布记录中公开仓库下载受限，远端 AAR 下载后的哈希复核仍待完成。

## 更新日志

### v0.1.6（2026-11-11）

- 统一 `IRoonCallback` 单连接托管并监听 Binder 死亡，通过底层 Binder 身份安全注销订阅；发送遇到 `RemoteException` 时仅清理当前失效订阅，不再传播到 JNI 回调线程。
- 改进音频输出准备握手（`RoonOutputHandshake`）：在单次 5 秒截止时间内支持宿主重连或替换后继续完成准备；显式拒绝、注销、停止/释放或切源接管仍取消请求。
- 保留原有 `RoonServiceManager`、回调接口与独立 `:roon_process` 使用方式。

### v0.1.5（2026-11-09）

- 修复断网后端点最终退出时调用失效 SDK 回调导致的崩溃，退出时停止写线程并关闭旧端点入口。
- 调整服务关闭流程，释放输出后退出专用 Roon 进程，并在关闭前注销宿主回调。
- 完善音源交接后的选择状态，阻止自动下一曲或迟到请求重新占用已交出的输出；重新播放需由 Roon 端明确发起。
- 修复输出准备失败后的回调清理，避免继续使用已失效的回调上下文。

### v0.1.4（2026-11-03）

- 改善内置 PCM 播放的位置上报与分组定时起播，减少排队音频对同步时钟的影响。
- 修复硬件时钟暂时不可用时，定时起播误用软件累计时间的问题。
- 完善停止和音源切换时的资源释放确认，避免旧音频输出尚未释放便确认交接成功。
- 保留现有初始化与播放控制接口，延续 `0.1.3` 的宿主音源交接流程。

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
