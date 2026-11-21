# HiFiPlayer SDK 接入

AudioPlayer、NetworkStorage 和 ScreenMirror 的下列版本已发布到 QYTech 的公开 Maven 仓库，Gradle 可以匿名下载。[发布仓库](https://github.com/qytech/maven-releases)

## 配置 Gradle

在项目的 `settings.gradle.kts` 中，把下面的仓库加到已有的 `dependencyResolutionManagement.repositories` 里，放在其他 Maven 仓库之前。保留 `google()` 和 `mavenCentral()` 以解析传递依赖。

```kotlin
maven("https://qytech.github.io/maven-releases/") {
    content {
        includeModule("io.github.qytech", "audioplayer")
        includeModule("io.github.qytech", "networkstorage")
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
    implementation("io.github.qytech:screenmirror:0.1.1")
}
```
<!-- /qydocs:dependencies -->

## 模块文档

- [AudioPlayer](../AudioPlayer/index.md) 支持通过 Android USB Host 向已授权的山灵 UA4 输出双声道 Native DSD64。
- [NetworkStorage](../NetworkStorage/index.md) 允许普通 Android 应用注册自己的 SMB/NFS 用户态后端。
- [ScreenMirror](../ScreenMirror/index.md) 支持在扩展屏会话中指定客户端视图宽高比。

## 下载宿主 APK

有宿主仓库读取权限的交付用户可登录 GitHub，下载最新正式版的两个签名 APK。APK 的版本跟随宿主 Release，Gradle 依赖使用上方示例中的 SDK 版本。[Latest Release](https://github.com/qytech/QYHifiPlayer/releases/latest) · [QYHiFiPlayer](https://github.com/qytech/QYHifiPlayer/releases/latest/download/QYHiFiPlayer-release.apk) · [CadenzaPlayer](https://github.com/qytech/QYHifiPlayer/releases/latest/download/CadenzaPlayer-release.apk)
