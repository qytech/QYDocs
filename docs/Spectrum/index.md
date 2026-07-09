# Spectrum 模块

音频频谱分析与 VU 表处理组件，支持单声道/双声道分离处理、音量增益补偿等功能。

## 依赖

```kotlin
implementation("io.github.qytech:spectrum:0.1.9")
```

## 功能特性

- ✅ FFT 频谱分析（支持配置 FFT 大小）
- ✅ 单声道 `SpectrumVuProcessor`
- ✅ 双声道分离 `StereoSpectrumVuProcessor`
- ✅ 音量增益补偿
- ✅ 硬件回采 / 软件回采双策略
- ✅ 多频段频谱显示

---

## 更新日志

### v0.1.9（2026-07-09）

- 优化硬件回采的情况下杂波问题和 VU 表显示

---

### v0.1.8（2026-07-07）

- 优化底噪

---

### v0.1.7（2026-06-16）

- 优化部分频点不准的问题，默认的 `fftSize = 4096` 效果更好

### v0.1.6（2026-06-08）

- 将 `SpectrumVuProcessor` 和 `StereoSpectrumVuProcessor` 改为单例，避免可能出现的节点占用情况

```kotlin
SpectrumVuProcessor.getInstance(fftSize = 1024)
StereoSpectrumVuProcessor.getInstance(fftSize = 1024)
```

### v0.1.4

- `BaseSpectrumVuCapture` 新增 `setVolumeCompensationGain(gain: Double)` 接口
- 将前处理环节的增益放大作用于处理器，使频谱及 VU 表信号能按照用户的增益平滑缩放

---

### v0.1.3

- 修复部分音频频谱出现杂波的问题
- 新增 `StereoSpectrumVuProcessor` 用于处理左右声道分离的频谱显示

```kotlin
class StereoSpectrumVuProcessor(
    sampleRate: Int = 44100,
    fftSize: Int = 1024,
    windowType: WindowType = WindowType.HANNING,
    muteThreshold: Double = 5e-4,
    private val bandCount: Int = 128,
    private val minFreq: Double = 50.0,
    private val maxFreq: Double = 20000.0,
)

StereoSpectrumVuView(context).apply {
    setBarCount(128)
}

private var spectrumVuProcessor: StereoSpectrumVuProcessor? = null

fun startRecord() {
    spectrumVuProcessor = StereoSpectrumVuProcessor(bandCount = 128)
    spectrumVuProcessor?.setStereoSpectrumListener(object : StereoSpectrumVuUpdateListener {
        override fun onStereoSpectrumUpdated(
            leftDbList: DoubleArray,
            rightDbList: DoubleArray,
        ) {
            _dbLeftList.value = leftDbList
            _dbRightList.value = rightDbList
        }
        
        override fun onVuDataUpdated(vuData: VuData) {
            _vuData.value = vuData
        }
    })
    spectrumVuProcessor?.setCapturePriority(LoopbackPriority.PRIORITY_SOFTWARE_ONLY)
    spectrumVuProcessor?.start()
}

fun stopRecord() {
    spectrumVuProcessor?.removeStereoSpectrumListener()
    spectrumVuProcessor?.stop()
    spectrumVuProcessor?.release()
}
```

### v0.1.2

- 修复硬件回采时左右声道的 VU 表底噪被放大问题
- 区分软件回采和硬件回采；只有硬件回采才需要归一化
- 新增软件回采和硬件回采的策略设置，默认采用 `PRIORITY_AUTO`

```kotlin
enum class LoopbackPriority {
    PRIORITY_AUTO,
    PRIORITY_SOFTWARE_FIRST,
    PRIORITY_HARDWARE_FIRST,
    PRIORITY_SOFTWARE_ONLY,
    PRIORITY_HARDWARE_ONLY
}

class SpectrumVuProcessor {
    fun setCapturePriority(priority: LoopbackPriority)
}
```

---

### v0.0.9

- 修复了架构兼容性
- 分离处理逻辑：如需自己计算处理数据，直接使用 `LoopbackProcessor`；如需库直接处理数据，请使用 `SpectrumVuProcessor`

### v0.0.7

- 修复了回采可能出现闪退的问题
- 修复了回采频繁开关可能导致设备级录音通道被占用且没有释放
- `LoopbackProcessor` 新增 `release` 方法，组件销毁时必须调用

### v0.0.6

- 修复多线程快速来回开关回采时可能导致的闪退异常
