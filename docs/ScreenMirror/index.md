# ScreenMirror Android SDK

[QYTech Maven 发布仓库](https://github.com/qytech/maven-releases)
[![Changelog](https://img.shields.io/badge/Changelog-CHANGELOG.md-blue.svg)](./CHANGELOG.md)

ScreenMirror（`io.github.qytech:screenmirror`）是设备端投屏运行时 SDK，负责 `MediaProjection` 授权、镜像或扩展虚拟屏管理、H.264 低延迟视频流发布以及远程单指触摸注入。

> 当前版本为 `0.1.2`，于 2026-11-23 发布到 QYTech Maven 仓库。发布制品为经过 R8 混淆的 AAR，版本变化见[更新日志](CHANGELOG.md)。

## 依赖与运行环境

先按 [HiFiPlayer SDK 接入](../HiFiPlayer/index.md) 添加 QYTech Maven 仓库。

```kotlin
dependencies {
    implementation("io.github.qytech:screenmirror:0.1.2")
}
```

- Android API 29+。
- 库清单内置 `FOREGROUND_SERVICE`、`FOREGROUND_SERVICE_MEDIA_PROJECTION`、`INJECT_EVENTS` 与 `INTERNAL_SYSTEM_WINDOW` 权限，并声明 `ScreenCaptureConsentActivity` 与 `ScreenCaptureForegroundService`。
- `INJECT_EVENTS` 触摸注入及独立扩展虚拟屏能力仅在系统签名设备上可用；触摸数据默认 UDP 端口为 `SCREEN_MIRROR_POINTER_PORT`（`39822`）。

## 使用方法

### 1. 提供单例 `ScreenMirrorController`

库内的授权 Activity 与前台 Service 通过 Hilt 获取同一 `ScreenMirrorController` 单例，宿主需在 `SingletonComponent` 中注入应用级 `CoroutineScope` 与 `IO` 调度器：

```kotlin
import android.content.Context
import com.qytech.screenmirror.ScreenMirrorController
import dagger.Module
import dagger.Provides
import dagger.hilt.InstallIn
import dagger.hilt.android.qualifiers.ApplicationContext
import dagger.hilt.components.SingletonComponent
import kotlinx.coroutines.CoroutineDispatcher
import kotlinx.coroutines.CoroutineScope
import javax.inject.Singleton

@Module
@InstallIn(SingletonComponent::class)
object ScreenMirrorModule {
    @Provides
    @Singleton
    fun provideScreenMirrorController(
        @ApplicationContext context: Context,
        applicationScope: CoroutineScope,
        ioDispatcher: CoroutineDispatcher,
    ): ScreenMirrorController = ScreenMirrorController(
        context = context,
        applicationScope = applicationScope,
        ioDispatcher = ioDispatcher,
    )
}
```

### 2. 启动、注入触摸与停止会话

```kotlin
import com.qytech.screenmirror.RemotePointerEvent
import com.qytech.screenmirror.RemoteScreenFrameRate
import com.qytech.screenmirror.RemoteScreenMode
import com.qytech.screenmirror.RemoteScreenOrientation
import com.qytech.screenmirror.RemoteScreenResolution
import com.qytech.screenmirror.RemoteScreenSessionRequest

// 启动或查询当前已认证会话（同一时刻仅允许一个 ownerToken 持有投影）
val response = controller.start(
    authToken = sessionToken,
    request = RemoteScreenSessionRequest(
        orientation = RemoteScreenOrientation.LANDSCAPE,
        resolution = RemoteScreenResolution.NATIVE,
        frameRate = RemoteScreenFrameRate.FPS60,
        mode = RemoteScreenMode.EXTENDED,
        aspectRatio = 16f / 9f,
    ),
)

// 同一客户端重连时转移会话所有权，保留当前投影与流路径
controller.transferOwner(previousToken = oldToken, newToken = newToken)

// 注入经过认证并归一化（0f..1f）的单指触摸事件
controller.injectPointer(authToken = sessionToken, event = pointerEvent)

// 结束投屏并释放虚拟屏、编码器及前台服务（仅当前 ownerToken 生效）
controller.stop(authToken = sessionToken)
```

扩展屏可用 `aspectRatio` 传入客户端视图宽度与高度的比值。省略该参数时沿用原有尺寸选择。

## 更新日志

完整变更记录见 [更新日志](CHANGELOG.md)，返回[文档首页](../../README.md)。
