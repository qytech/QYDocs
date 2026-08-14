# Spectrum 模块

音频频谱分析与 VU 表处理组件，统一管理软件回采、硬件回采、频谱分析和左右声道 VU 显示。

## 依赖

```kotlin
implementation("io.github.qytech:spectrum:0.2.2")
```

> `VuMeterMode` 将随 Spectrum 后续版本发布。正式版本号确认前，Maven Central 依赖仍保持为 `0.2.2`。

## 功能特性

- ✅ FFT 频谱分析（支持配置 FFT 大小）
- ✅ 单声道 `SpectrumVuProcessor`
- ✅ 双声道分离 `StereoSpectrumVuProcessor`
- ✅ `SpectrumCaptureRuntime` 统一管理回采生命周期
- ✅ `AUTO`、`SOFTWARE`、`HARDWARE`、`OFF` 四种回采模式
- ✅ 不同硬件回采设备的固定参数适配
- ✅ VU 支持 `LOUDNESS` 真实响度与 `PEAK` 峰值两种显示方式
- ✅ 左右声道独立显示，不受硬件音量调节影响
- ✅ 多频段频谱显示

---

## 使用方法

```kotlin
private val spectrumRuntime = SpectrumCaptureRuntime()

fun initializeSpectrum() {
    spectrumRuntime.setListener(object : SpectrumVuUpdateListener {
        override fun onSpectrumDataUpdated(dbList: DoubleArray) {
            // 更新频谱 UI
        }

        override fun onVuDataUpdated(vuData: VuData) {
            // 更新左右声道 VU UI
        }
    })

    spectrumRuntime.setPolicy(SpectrumCapturePolicy.AUTO)
}

fun setSpectrumActive(active: Boolean) {
    spectrumRuntime.setSignalActive(active)
}

fun setSpectrumMode(policy: SpectrumCapturePolicy) {
    spectrumRuntime.setPolicy(policy)
}

fun setVuMode(mode: VuMeterMode) {
    spectrumRuntime.setVuMeterMode(mode)
}

fun releaseSpectrum() {
    spectrumRuntime.close()
}
```

`AUTO` 默认使用硬件回采。用户明确选择 `SOFTWARE`、`HARDWARE` 或 `OFF` 后，运行时以用户设置为准。

### 选择 VU 表显示方式

VU 表新增两种显示方式，可根据产品的视觉风格和使用场景选择：

- `LOUDNESS`：显示音频的短时真实响度，变化更平稳，适合观察音乐整体强弱。
- `PEAK`：显示左右声道峰值，对鼓点、瞬态和强音响应更明显，适合需要更大指针摆幅的界面。

默认使用 `LOUDNESS`，升级后不会改变现有显示效果。需要更明显的摆动时，可在创建运行时对象时选择 `PEAK`：

```kotlin
import com.qytech.spectrum.capture.SpectrumCaptureRuntime
import com.qytech.spectrum.capture.VuMeterMode

private val spectrumRuntime = SpectrumCaptureRuntime(
    vuMeterMode = VuMeterMode.PEAK,
)
```

也可以在应用运行期间切换。例如，将该方法连接到应用设置页：

```kotlin
fun applyVuMode(usePeak: Boolean) {
    spectrumRuntime.setVuMeterMode(
        if (usePeak) VuMeterMode.PEAK else VuMeterMode.LOUDNESS,
    )
}
```

模式切换只影响 VU 表数据，不会改变频谱柱、回采来源或当前播放状态。

---

## 更新日志

### 待发布（2026-08-14）

- 新增 `LOUDNESS` 与 `PEAK` 两种 VU 显示方式，客户可按产品界面选择真实响度或峰值响应
- 默认保持 `LOUDNESS`，现有应用升级后无需修改即可继续使用原有显示方式
- 支持在初始化时指定 VU 模式，也支持在应用运行期间即时切换
- `PEAK` 模式可增强鼓点和瞬态信号的显示幅度，让 VU 指针或灯条响应更明显

### v0.2.2（2026-08-05）

- 新增 `SpectrumCaptureRuntime`，统一管理回采模式、启停、监听和资源释放
- `AUTO` 默认使用硬件回采；用户选择 `SOFTWARE`、`HARDWARE` 或 `OFF` 时以用户设置为准
- 优化不同硬件回采设备的固定参数适配，移除按当前音频动态放大增益导致的频谱和 VU 跳动
- VU 统一使用左右声道 RMS 响度，硬件回采结果不受用户音量调节影响

---

### v0.2.1（2026-07-28）

- 修复不同硬件对应的回采数据不一致情况下数据异常问题

---

### v0.2.0（2026-07-24）

- 修复硬件回采数据不对的问题

---

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
