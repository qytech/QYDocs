# HDMI ARC Kotlin Demo

更新日期：2026-10-19。配套阅读：[接入指南](HDMI-ARC-INTEGRATION.md)。

本示例在前台页面依次播放、暂停、恢复、停止后重启，退出或失败时释放。复制下面两个完整文件，再在页面注册一次即可运行。

## 1. 运行前准备

- 使用已适配 ARC 的设备与固件：Android API 29+、`arm64-v8a`。
- 电视连接 ARC 端口、启用 ARC/CEC，先选 PCM 并持续播放有声内容。
- 停止其他播放，选择本地音频输出，确认音量正常。
- **ARC 输入与 HDMI 输出互斥。** Demo 不切换输出，也不自动重连；切换顺序见 [注意事项](HDMI-ARC-INTEGRATION.md#4-注意事项)。

## 2. 添加依赖

工程配置 Maven Central；应用模块添加以下依赖。已有兼容的协程和 Lifecycle 版本时复用现有配置。

```kotlin
dependencies {
    implementation("io.github.qytech:audioplayer:1.2.7")
    implementation("org.jetbrains.kotlinx:kotlinx-coroutines-android:1.11.0")
    implementation("androidx.lifecycle:lifecycle-runtime-ktx:2.11.0")
}
```

在应用模块新建以下两个文件。可保留 `com.example.arcdemo` 包名；修改包名时同步调整两个文件和调用处的 import。

## 3. 核心示例：HdmiArcDemo.kt

```kotlin
package com.example.arcdemo

import android.util.Log
import com.qytech.audioplayer.player.HdmiArcPlayer
import com.qytech.audioplayer.player.PlaybackState
import com.qytech.audioplayer.player.PlayerListener
import kotlinx.coroutines.CompletableDeferred
import kotlinx.coroutines.CoroutineDispatcher
import kotlinx.coroutines.withContext
import kotlinx.coroutines.withTimeoutOrNull

private const val TAG = "HdmiArcDemo"

/** 在工作线程验证 ARC 调用顺序，并在结束、失败或取消时释放会话。 */
suspend fun runHdmiArcDemo(
    ioDispatcher: CoroutineDispatcher,
) = withContext(ioDispatcher) {
    val failure = CompletableDeferred<String>()
    val player = HdmiArcPlayer()
    val listener = object : PlayerListener {
        override fun onPrepared() {
            Log.i(TAG, "onPrepared")
        }

        override fun onStateChanged(state: PlaybackState) {
            Log.i(TAG, "state=$state")
        }

        override fun onError(code: Int, msg: String) {
            // 回调只发布错误，播放器由下方 finally 统一释放。
            failure.complete("ARC error $code: $msg")
            Log.e(TAG, "ARC error $code: $msg")
        }

        override fun onProgress(
            track: Int,
            current: Long,
            total: Long,
            progress: Float,
        ) = Unit

        override fun onComplete() = Unit
    }

    suspend fun listenFor(durationMillis: Long) {
        val error = withTimeoutOrNull(durationMillis) { failure.await() }
        check(error == null) { error.orEmpty() }
    }

    try {
        player.addListener(listener)
        check(player.prepareAndCheck()) { "ARC prepare failed; check logs" }
        check(player.getState() == PlaybackState.PREPARED)

        check(player.playAndCheck()) { "ARC play failed" }
        check(player.getState() == PlaybackState.PLAYING)
        Log.i(TAG, "Step 1: listen for 30 seconds")
        listenFor(30_000)

        check(player.pauseAndCheck()) { "ARC pause failed" }
        check(player.getState() == PlaybackState.PAUSED)
        Log.i(TAG, "Step 2: paused for 3 seconds")
        listenFor(3_000)

        check(player.playAndCheck()) { "ARC resume failed" }
        check(player.getState() == PlaybackState.PLAYING)
        Log.i(TAG, "Step 3: resumed; listen for 30 seconds")
        listenFor(30_000)

        player.stop()
        check(player.getState() == PlaybackState.STOPPED) { "ARC stop failed" }
        check(player.prepareAndCheck()) { "ARC prepare after stop failed" }
        check(player.playAndCheck()) { "ARC restart failed" }
        check(player.getState() == PlaybackState.PLAYING)
        Log.i(TAG, "Step 4: restarted; listen for 30 seconds")
        listenFor(30_000)
        Log.i(TAG, "API sequence passed; listening result must be checked manually")
    } finally {
        player.removeListener(listener)
        player.release()
        check(player.getState() == PlaybackState.IDLE)
        Log.i(TAG, "ARC released")
    }
}
```

## 4. 接入页面生命周期：HdmiArcDemoLifecycle.kt

页面可见时运行一轮；离开页面时取消并等待释放，再次进入会重新运行。

```kotlin
package com.example.arcdemo

import android.util.Log
import androidx.lifecycle.Lifecycle
import androidx.lifecycle.LifecycleOwner
import androidx.lifecycle.lifecycleScope
import androidx.lifecycle.repeatOnLifecycle
import kotlinx.coroutines.CancellationException
import kotlinx.coroutines.CoroutineDispatcher
import kotlinx.coroutines.Job
import kotlinx.coroutines.awaitCancellation
import kotlinx.coroutines.launch

/** 页面可见时运行一轮 Demo，离开页面时取消并等待释放。 */
fun LifecycleOwner.launchHdmiArcDemo(
    ioDispatcher: CoroutineDispatcher,
): Job = lifecycleScope.launch {
    repeatOnLifecycle(Lifecycle.State.STARTED) {
        try {
            runHdmiArcDemo(ioDispatcher)
        } catch (cancelled: CancellationException) {
            throw cancelled
        } catch (linkage: LinkageError) {
            Log.e("HdmiArcDemo", "SDK loading failed", linkage)
        } catch (failure: Exception) {
            Log.e("HdmiArcDemo", "Demo failed", failure)
        }
        // 完成或失败后留在当前页面等待，避免自动重试。
        awaitCancellation()
    }
}
```

在现有 Activity 添加 import，并在 `onCreate()` 的 `super.onCreate(...)` 之后注册一次：

```kotlin
import com.example.arcdemo.launchHdmiArcDemo
import kotlinx.coroutines.Dispatchers

// 放在现有 Activity 的 onCreate() 中，super.onCreate(...) 之后：
launchHdmiArcDemo(ioDispatcher = Dispatchers.IO)
```

Fragment 使用 `viewLifecycleOwner.launchHdmiArcDemo(...)`，在视图创建后注册。不要在重组、点击或 `onStart()` 中重复注册。

## 5. 运行与注意事项

打开页面后依次播放 30 秒、暂停 3 秒、恢复播放 30 秒、停止后重启播放 30 秒，最后释放。日志中的成功状态仍需结合实际听音判断。

```shell
adb logcat -v threadtime HdmiArcDemo:I '*:S'
```

- 保持同一任务在工作线程串行操作，不把播放器交给其他按钮或协程。
- 回调只记录或传递事件，不调用播放器的控制或状态查询方法。
- 输入不可用或启动失败时检查失败返回值；持续输入错误进入 `ERROR`。示例会记录错误并在 `finally` 释放，重试需新建实例。
- 切源或主动结束时，在协程中对返回的 `Job` 调用 `cancelAndJoin()`，等待释放后再启动其他播放；不能只取消就立即创建新实例。
- 选择 HDMI 输出前结束 Demo 并取消 ARC 待恢复任务；后续重连不能重新启动 ARC。断连演示需退出页面，恢复连接后再进入。
- 示例只演示短暂停；长暂停恢复失败时结束会话并重新创建。静音本身合法，接口状态不能代替听音。

失败时保存 `Demo failed`、`SDK loading failed` 或 `onError` 的错误信息交给设备方；出现明显噪声时停止测试。后台播放和自动恢复由完整应用管理。
