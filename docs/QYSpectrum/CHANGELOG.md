# QYSpectrum 更新日志

## 0.0.1-snapshot - 2026-09-16

### 新增

- 初始预发布快照：基于 ARM NEON SIMD 与 Rust Direct JNI（`libqy_spectrum.so`）的音频频谱与弹道 VU 引擎，提供 `QYSpectrum.createCaptureSession(...)`（含 Rockchip PDM 硬件音量校准与 `CaptureSessionState` 状态机）、`PlaybackSpectrumTap` 无锁后级 PCM 接入端点与 `SpectrumFastPath`。
- Maven 坐标：`io.github.qytech:qyspectrum:0.0.1-snapshot`（仅 `arm64-v8a`，Android API 29+）。
