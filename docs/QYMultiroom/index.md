# QYMultiroom Android SDK

QYMultiroom 为 Android 设备提供局域网多房间共享和同步收听。宿主可通过同一个 `MultiRoom` 实例控制本机、管理远端设备和分组，并接入自己的播放器。

> 当前版本为 `0.0.6`，发布于 2026-11-25。[更新日志](CHANGELOG.md) · [正式 AAR](https://qytech.github.io/maven-releases/io/github/qytech/qymultiroom/0.0.6/qymultiroom-0.0.6.aar) · [SHA-256](https://qytech.github.io/maven-releases/io/github/qytech/qymultiroom/0.0.6/qymultiroom-0.0.6.aar.sha256)

## Gradle 接入

按 [HiFiPlayer SDK 接入](../HiFiPlayer/index.md) 在 `settings.gradle.kts` 添加 QYTech Maven 仓库。在设备应用的 `build.gradle.kts` 中配置：

```kotlin
android {
    compileSdk = 37
    defaultConfig {
        minSdk = 29
        ndk { abiFilters.add("arm64-v8a") }
    }
    packaging.jniLibs.useLegacyPackaging = true
}

dependencies {
    implementation("io.github.qytech:qymultiroom:0.0.6")
}
```

同时接入 ScreenMirror 的宿主可使用已验证的 `screenmirror:0.1.2`，该版本为投屏 SDK 的混淆类分配了独立包名。[ScreenMirror 接入说明](../ScreenMirror/index.md)

## 创建运行时和接入播放器

由设备端服务或其他应用级生命周期所有者创建并持有一个实例。宿主的本地播放器实现 `PlayerSource`，向 SDK 提供当前曲目、状态和支持的操作。普通工厂接入无需配置 Hilt 或 KSP。

```kotlin
import android.content.Context
import com.qytech.multi_room.android.MultiRoomFactory
import com.qytech.multi_room.api.common.RoomConfig
import com.qytech.multi_room.api.control.MultiRoom
import com.qytech.multi_room.api.source.PlayerSource

fun createRoom(context: Context, deviceName: String): MultiRoom =
    MultiRoomFactory.create(context, RoomConfig(deviceName = deviceName))

suspend fun openRoom(room: MultiRoom, player: PlayerSource) {
    room.open().getOrThrow()
    room.sources.register(player).getOrThrow()
    room.sources.select(player.id).getOrThrow()
}
```

- 设备端完成 `openRoom` 后，用户开启共享时调用 `room.device.startSharing()`，关闭共享时调用 `room.device.stopSharing()`。辅机可用 `room.device.leaveListening()` 退出收听。调用方应处理这些操作返回的 `Result`。
- 独立手机控制端在前台生命周期的协程中调用 `room.control.runSession()` 保持发现和控制连接。取消协程会释放该次会话。
- 整个设备运行时退出时调用 `room.close()` 并检查结果。省略 `RoomConfig.deviceId` 时，SDK 在应用的 `noBackupFilesDir` 保存每台设备的随机身份。制作量产镜像时，应让每台设备在首次启动时生成自己的身份。
- 系统应用声音采集需要相应的固件签名、音频路由与采集权限。普通播放器可通过 `PlayerSource` 提供文件或 PCM。

## Native 组件

AAR 带有 ARM64 的 Snapserver、Snapclient、缓存编解码、SACD/JNI 解码器和 C++ 运行库。内置文件音源默认输出 48 kHz、16 位、双声道 PCM。各组件的许可证、对应源码、补丁和离线构建脚本随正式版本提供。[组件说明及许可证](https://qytech.github.io/maven-releases/io/github/qytech/qymultiroom/0.0.6/qymultiroom-0.0.6-notices.zip) · [Native 对应源码](https://github.com/qytech/maven-releases/releases/download/qymultiroom-0.0.6/qymultiroom-0.0.6-native-sources.zip)
