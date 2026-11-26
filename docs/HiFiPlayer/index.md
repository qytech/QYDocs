# HiFiPlayer SDK 接入

AudioPlayer、NetworkStorage、QYMultiroom、Roon 和 ScreenMirror 的下列版本已发布到 QYTech 的公开 Maven 仓库，Gradle 可以匿名下载。[发布仓库](https://github.com/qytech/maven-releases)

## 配置 Gradle

在项目的 `settings.gradle.kts` 中，把下面的仓库加到已有的 `dependencyResolutionManagement.repositories` 里，放在其他 Maven 仓库之前。保留 `google()` 和 `mavenCentral()` 以解析传递依赖。

```kotlin
maven("https://qytech.github.io/maven-releases/") {
    content {
        includeModule("io.github.qytech", "audioplayer")
        includeModule("io.github.qytech", "networkstorage")
        includeModule("io.github.qytech", "qymultiroom")
        includeModule("io.github.qytech", "roon")
        includeModule("io.github.qytech", "screenmirror")
    }
}
```

在使用 SDK 的模块的 `build.gradle.kts` 中按需选择依赖。

<!-- qydocs:dependencies -->
```kotlin
dependencies {
    implementation("io.github.qytech:audioplayer:1.2.12")
    implementation("io.github.qytech:networkstorage:0.1.12")
    implementation("io.github.qytech:qymultiroom:0.0.6")
    implementation("io.github.qytech:roon:0.1.9")
    implementation("io.github.qytech:screenmirror:0.1.2")
}
```

其他 13 个 SDK 通过 `mavenCentral()` 获取，具体坐标见各 SDK 接入页。版本中的小写 `-snapshot` 是公开坐标的一部分，按原样引用。

| SDK | Maven Central 坐标 |
| --- | --- |
| [Airplay](https://qytech.github.io/QYDocs/docs/Airplay/) | `io.github.qytech:airplay:0.0.10` |
| [AudioProbe](https://qytech.github.io/QYDocs/docs/AudioProbe/) | `io.github.qytech:qyaudioprobe:0.1.0` |
| [Cdrom](https://qytech.github.io/QYDocs/docs/Cdrom/) | `io.github.qytech:cdrom:0.2.11` |
| [DLNA](https://qytech.github.io/QYDocs/docs/DLNA/) | `io.github.qytech:dlna:0.2.10` |
| [MediaScanner](https://qytech.github.io/QYDocs/docs/MediaScanner/) | `io.github.qytech:qymediascanner:0.1.1` |
| [QYAirPlay2](https://qytech.github.io/QYDocs/docs/QYAirPlay2/) | `io.github.qytech:qyairplay2:0.1.3` |
| [QYCdrom](https://qytech.github.io/QYDocs/docs/QYCdrom/) | `io.github.qytech:qycdrom:0.0.3` |
| [QYDlna](https://qytech.github.io/QYDocs/docs/QYDlna/) | `io.github.qytech:qydlna:0.1.1` |
| [QYMusicIndex](https://qytech.github.io/QYDocs/docs/QYMusicIndex/) | `io.github.qytech:qymusicindex:0.0.1-snapshot` |
| [QYSpectrum](https://qytech.github.io/QYDocs/docs/QYSpectrum/) | `io.github.qytech:qyspectrum:0.0.1-snapshot` |
| [Qobuz](https://qytech.github.io/QYDocs/docs/Qobuz/) | `io.github.qytech:qobuz-connect:0.0.4` |
| [SerialPort](https://qytech.github.io/QYDocs/docs/SerialPort/) | `io.github.qytech:serialport:0.0.5` |
| [Spectrum](https://qytech.github.io/QYDocs/docs/Spectrum/) | `io.github.qytech:spectrum:0.2.3` |
<!-- /qydocs:dependencies -->

## 模块文档

- [AudioPlayer](../AudioPlayer/index.md) 支持通过 Android USB Host 向已授权的山灵 UA4 输出双声道 Native DSD64。
- [NetworkStorage](../NetworkStorage/index.md) 允许普通 Android 应用注册自己的 SMB/NFS 用户态后端。
- [QYMultiroom](../QYMultiroom/index.md) 提供设备间同步收听、共享分组及播放器接入。
- [Roon](../Roon/index.md) 提供 Roon 音频接收、分组播放和宿主音源切换接口。
- [ScreenMirror](../ScreenMirror/index.md) 支持在扩展屏会话中指定客户端视图宽高比。

## 下载宿主 APK

有宿主仓库读取权限的交付用户可登录 GitHub，下载最新正式版的两个签名 APK。APK 的版本跟随宿主 Release，Gradle 依赖使用各 SDK 自己的版本号。[Latest Release](https://github.com/qytech/QYHifiPlayer/releases/latest) · [QYHiFiPlayer](https://github.com/qytech/QYHifiPlayer/releases/latest/download/QYHiFiPlayer-release.apk) · [CadenzaPlayer](https://github.com/qytech/QYHifiPlayer/releases/latest/download/CadenzaPlayer-release.apk)
