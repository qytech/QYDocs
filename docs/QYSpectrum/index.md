# QYSpectrum Android SDK

[![Maven Central](https://img.shields.io/maven-central/v/io.github.qytech/qyspectrum.svg)](https://central.sonatype.com/artifact/io.github.qytech/qyspectrum)
[![Changelog](https://img.shields.io/badge/Changelog-CHANGELOG.md-blue.svg)](./CHANGELOG.md)

QYSpectrum（`io.github.qytech:qyspectrum`）是基于 ARM NEON SIMD 与 Rust Direct JNI 的实时音频频谱与弹道 VU 表引擎，支持 ALSA 硬件/数字回环捕获（含硬件 PDM 音量校准）、播放器后级 PCM 直传监听与 `DirectByteBuffer` 快速分析路径。对外统一入口为 `com.qytech.qyspectrum.QYSpectrum`。

> 当前版本：`0.0.1-snapshot`（2026-09-16，预发布快照版本；另有传统 Java/Oboe 组件 [Spectrum](../Spectrum/)）。版本变化见[更新日志](CHANGELOG.md)。

## 依赖与运行环境

```kotlin
dependencies {
    implementation("io.github.qytech:qyspectrum:0.0.1-snapshot")
}
```

- Android API 29+，Java 17，仅提供 `arm64-v8a`（内置 `libqy_spectrum.so`）。
- 未额外声明危险权限；硬件声卡直采与数字回环依赖配套固件及底层 ALSA 音频路径支持。

## 核心能力（v0.0.1-snapshot）

- **实时捕获会话**：`QYSpectrum.createCaptureSession(...)` 管理声卡发现、路由切换与 Rockchip PDM 硬件增益校准，暴露 `state: StateFlow<CaptureSessionState>` 与 `frames: StateFlow<SpectrumFrame?>`。
- **播放器后级 PCM 监听**：`QYSpectrum.createPlaybackTap(...)` 通过原生无锁环形缓冲接收 PCM 数据（支持 `PCM16_LE`、`PCM24_LE`、`PCM32_LE`、`FLOAT32_LE`），在非实时线程按渲染节拍计算 `SpectrumFrame`。
- **快速直通路径与诊断查询**：提供 `QYSpectrum.createFastPath(sampleRate, fftSize)`、`defaultConfig()`、`standard20Frequencies()` 与 `listAvailableSoundcards()`。

## 使用方法

### 1. 声卡硬件 / 数字回环捕获

```kotlin
import com.qytech.qyspectrum.CapturePriority
import com.qytech.qyspectrum.CaptureSessionState
import com.qytech.qyspectrum.QYSpectrum

val session = QYSpectrum.createCaptureSession(
    context = applicationContext,
    runtimeScope = applicationScope,
)

// 观察状态与最新 20 段频谱/VU 帧
// state 为 Starting 或 Switching 时应清空/忽略旧帧
lifecycleScope.launch {
    session.state.collect { state ->
        if (state is CaptureSessionState.Unavailable) {
            // 根据 state.reason 处理无可用采集源或权限/打开失败
        }
    }
}

lifecycleScope.launch {
    session.frames.collect { frame ->
        frame ?: return@collect
        val bands = frame.bands          // 20 段左声道归一化幅度 (0.0f ~ 1.0f)
        val rightBands = frame.rightBands
        val leftVuDb = frame.leftVuDb    // 弹道 VU 电平 (dB)
        val rightVuDb = frame.rightVuDb
    }
}

// start / updatePriority / stop / release 为 suspend 函数（内部切换至 ioDispatcher 并加锁串行化）
session.start(CapturePriority.AUTO)
// 切换优先级示例：CapturePriority.HARDWARE_FIRST / SOFTWARE_FIRST / HARDWARE_ONLY / SOFTWARE_ONLY
session.stop()
session.release()
```

### 2. 播放器后级 PCM 监听（`PlaybackSpectrumTap`）

```kotlin
import com.qytech.qyspectrum.PcmFormat
import com.qytech.qyspectrum.QYSpectrum

val tap = QYSpectrum.createPlaybackTap(
    sampleRateHz = 44100,
    fftSize = 4096,
    pcmFormat = PcmFormat.PCM16_STEREO,
)

// 音频回调线程注入：pcm 必须为 direct、little-endian 且 position == 0 的完整帧缓冲
fun onAudioPcm(pcm: ByteBuffer, sizeBytes: Int) {
    tap.submitPcm(pcm, sizeBytes)
}

// UI/工作定时线程拉取渲染帧（禁止在实时音频回调中调用 renderFrame）
val frame = tap.renderFrame()

// 确认音频回调完全停止后再关闭端点，释放原生句柄
tap.close()
```

- `SpectrumFastPath.process(pcm)` 与 `close()` 须在同一个串行工作线程中调用，并同样要求 `direct` 且小端序（`ByteOrder.LITTLE_ENDIAN`）的 `ByteBuffer`。

## 更新日志

完整变更记录见 [更新日志](CHANGELOG.md)，返回[文档首页](../../README.md)。
