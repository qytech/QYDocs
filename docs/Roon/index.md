# Roon Android SDK

[![Maven Central](https://img.shields.io/maven-central/v/io.github.qytech/roon.svg)](https://central.sonatype.com/artifact/io.github.qytech/roon)

当前版本：`0.1.2`，提供 Roon 音频接收、播放控制与设备音频能力查询。

## 添加依赖

```kotlin
implementation("io.github.qytech:roon:0.1.2")
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

已知限制：部分设备停止 Roon 服务时仍可能异常退出，本版本未包含该问题修复。独立集成及输出切换需在目标设备上复验。

## 更新日志

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


