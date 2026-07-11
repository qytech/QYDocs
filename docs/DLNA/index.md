# DLNA/QPlay 模块

Android DLNA 媒体渲染器（DMR），支持 QPlay 协议，实现手机 - 设备同步控制、播放列表管理、歌词回调等功能。

## 依赖

```kotlin
dependencies {
    implementation("io.github.qytech:dlna:0.2.7")
}
```

## 功能特性

- ✅ DLNA DMR 媒体渲染器
- ✅ QPlay 协议支持
- ✅ 播放列表管理（支持超长歌单分片下发）
- ✅ 歌词回调
- ✅ 手机-设备同步控制（进度、音量、播放状态）
- ✅ SQ 音质支持

---

## 更新日志

### [0.2.7] — 2026-07-11

**优化**

- 优化播放状态切换时不同步和下一首慢问题

---

### [0.2.6] — 2026-06-26

**修复**

- 修复控制端断开后继续播放问题

**新增**

- 添加 `onProgressChanged(positionMs: Long, durationMs: Long)` 回调
- `onProgressChanged(progress: Float)` 与 `onProgressChanged(positionMs: Long, durationMs: Long)` 只需重写其中一个

---

### [0.2.5] — 2026-06-12

**优化**

- 优化了设备端与 QQ 音乐的信息同步问题

### [0.2.4] — 2026-06-12

**修复**

- 修复切歌进度不同步问题

**新增**

- 添加 QPlay 歌词回调

```java
interface IDLNAMediaEventListener {
    fun onMetaDataChanged(trackInformation: MusicMetaData?)
    fun onQPlayQueueChanged(
        queue: List<QPlayTrackMetaData>,
        index: Int,
        audioInfo: QPlayAudioInfo? = null
    )
    
    // QPlay 控制端下发的 LRC 歌词
    fun onLyricChanged(songId: String, lyric: String)
    
    fun onProgressChanged(progress: Float)
    fun onVolumeChanged(value: Float)
    fun onMuteChanged(mute: Boolean)
    fun onPlayStatusChanged(isPlaying: Boolean)
}
```

---

### [0.2.3] — 2026-06-06

**优化**

- 优化了 QPlay 鉴权失败的提示

### [0.2.2] — 2026-06-01

- 移除了首次播放 FLAC 时可能出现异常的处理，确保其他稳定性

### [0.2.1] — 2026-05-29

- 修复了手机进度不同步问题

### [0.2.0] — 2026-05-22

- 修复了 QPlay 首次播放 FLAC 异常问题

---

### [0.1.8] — 2026-04-28

- 优化了播放列表跳曲问题

### [0.1.7] — 2026-04-16

- 优化了手机和设备端信息同步

### [0.1.6] — 2026-04-15

- 修复默认播放 200 首后如果没有获取到新的播放列表从第一曲开始
- 修复概率出现网络异常导致播放失败问题

### [0.1.5] — 2026-04-07

- 新增检查开机后的首次音频焦点回调结果
- 修复连接稳定性较差，挂载连接后手机断连
- 修复了播放延迟问题

### [0.1.4] — 2026-04-01

**新增**

- 增强 QPlay 队列处理能力，支持更大的播放列表容量
- 支持按 `startingIndex / nextIndex` 处理分片队列数据，便于控制端下发超长歌单
- 新增设备端主动选择 QPlay 歌曲的控制能力

**优化**

- 优化 QPlay 播放状态回调，`onPlayStatusChanged` 同时提供 `playbackState` 与 `isPlaying`
- 优化设备端切歌后的手机端 UI 同步链路，减少控制端依赖轮询确认当前曲目的延迟
- 优化 `setTracksInfo` 日志输出，避免打印整包曲目数据导致日志噪音过大

**使用示例**

```kotlin
private val mediaEventListener = object : IDLNAMediaEventListener {
    override fun onPlayStatusChanged(playbackState: Int, isPlaying: Boolean) {
        Timber.d("onPlayStatusChanged playbackState=$playbackState isPlaying=$isPlaying")
    }
    
    override fun onQPlayQueueChanged(
        queue: List<QPlayTrackMetaData>,
        trackId: Int,
        audioInfo: QPlayAudioInfo?
    ) {
        Timber.d("queueSize=${queue.size}, currentTrack=$trackId, audioInfo=$audioInfo")
    }
}

fun selectQPlayTrack(index: Int) {
    DLNAMediaRender.qPlaySelect(index)
}
```

---

### [0.1.3]

**新增**

- 新增 QPlay `SQ` 音质支持

**修复**

- 修复 `QPlayAudioInfo` 回调支持，控制端现在可以拿到采样率、声道、位深等音频信息

**使用示例**

```kotlin
override fun onQPlayQueueChanged(
    queue: List<QPlayTrackMetaData>,
    index: Int,
    audioInfo: QPlayAudioInfo?
) {
    Timber.d("queue=$queue, index=$index, audioInfo=$audioInfo")
}
```

### [0.1.2]

**新增**

- 新增 DLNA 播放过程中的音频参数回调，包括采样率、声道数、码率、位深与音频格式

**使用示例**

```kotlin
override fun onMetaDataChanged(trackInformation: MusicMetaData?) {
    Timber.d("trackInformation=$trackInformation")
}

override fun onQPlayQueueChanged(
    queue: List<QPlayTrackMetaData>,
    index: Int,
    audioInfo: QPlayAudioInfo?
) {
    Timber.d("sampleRate=${audioInfo?.sampleRate}, bitDepth=${audioInfo?.bitDepth}")
}
```

### [0.1.1]

**修复**

- 修复 Android 设备在部分场景下无法自动播放下一首的问题

**使用示例**

```kotlin
DLNAMediaRender.addDLNAMediaEventListener(mediaEventListener)
DLNAMediaRender.startService(
    application = app,
    deviceName = "qytech dmr",
    uuid = UUID.nameUUIDFromBytes("DLNAMediaRender".toByteArray())
)
```

---

### [0.1.0]

**修复**

- 修复 QPlay 播放完成后不会自动播放下一曲的问题

**使用示例**

```kotlin
fun mediaControllerQPlayNext() {
    DLNAMediaRender.qPlayNext()
}

fun mediaControllerQPlayPrevious() {
    DLNAMediaRender.qPlayPrevious()
}
```

### [0.0.9]

**修复**

- 修复 `updateTransportState` 空指针问题，提升状态同步稳定性

**使用示例**

```kotlin
override fun onServiceConnected() {
    Timber.d("DLNA service connected")
}

override fun onServiceDisconnected() {
    Timber.d("DLNA service disconnected")
}
```
