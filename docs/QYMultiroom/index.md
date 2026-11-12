# QYMultiroom Android SDK

[![Maven Central](https://img.shields.io/maven-central/v/io.github.qytech/qymultiroom.svg)](https://central.sonatype.com/artifact/io.github.qytech/qymultiroom)
[![Changelog](https://img.shields.io/badge/Changelog-CHANGELOG.md-blue.svg)](./CHANGELOG.md)

QYMultiroom（`io.github.qytech:qymultiroom`）为 Android 设备提供多房间音频同步、音源编排与控制端能力，将 `runtime`、`core`、`source`、`decoder`、`media`、`server`、`client`、`control`、`feature` 等模块打包为单一 Fat-AAR。

> 当前版本：`0.0.4`（2026-11-11）。版本变化见[更新日志](CHANGELOG.md)。

## 依赖与运行环境

```kotlin
dependencies {
    implementation("io.github.qytech:qymultiroom:0.0.4")
}
```

- Android API 29+，仅提供 `arm64-v8a`（包含 `libsnapserver.so`、`libsnapclient.so`、`libroomcodec.so`、`libmulti_room_decoder.so` 与 `libc++_shared.so`）。
- 权限：库清单声明 `INTERNET`、`MODIFY_AUDIO_SETTINGS`、`RECORD_AUDIO`、`MODIFY_AUDIO_ROUTING`、`CAPTURE_AUDIO_OUTPUT`、`MEDIA_CONTENT_CONTROL`、`WAKE_LOCK`。
- 多房间传输输出固定为 `48kHz / 16bit / 2ch` 交错 PCM，最多支持 8 路逻辑通道（`pcm-1` 至 `pcm-8`）；不支持 Native DSD、DoP 或裸 `.dsd` 文件。
- 发布 POM 已移除内部宿主工程依赖；若宿主直接引用其公共契约中的宿主侧模块接口（如 `LocalPlayGate` 或业务存储/远程协议模块），需在宿主构建中提供对应依赖。

## 主要变更与能力（v0.0.4）

- **Fat-AAR 资源命名空间修复（`0.0.4`）**：在打包前将嵌入子模块的资源 `R` / `R$` 引用统一重定位到 `com.qytech.multi_room.R`，解决消费者开启 Release R8 时的缺类失败。
- **设备命名与输出交接（`0.0.3`）**：`RoleControl` 暴露本机设备名称状态 `deviceName`、改名接口 `renameDevice` / `renameSource` 与 `LocalPlayGate`，支持多房间接收器在本地起播前释放音频输出。
- **独立解码与设备身份**：支持本机/USB/Samba/NFS 音源以及外部 CUE、DSF/DFF（DSD64/128 转 PCM）和双声道 SACD ISO 解码；本机随机设备 UUID 保存在 `noBackupFilesDir`。

## 使用方法

### 1. 构建并持有 `RoleControl`

在应用级 `SingletonComponent` 中通过 `RoleBuilder` 构建全局 `RoleControl` 单例（提供应用级 `CoroutineScope` 与 `IO` 调度器）：

```kotlin
import com.qytech.multi_room.core.runtime.contract.RoleControl
import com.qytech.multi_room.runtime.RoleBuilder
import com.qytech.multi_room.runtime.data.RoleConfig
import com.qytech.multi_room.runtime.store.DeviceIdentity

val identity = DeviceIdentity({ context.noBackupFilesDir }, Dispatchers.IO)

val roleControl: RoleControl = RoleBuilder(
    context = applicationContext,
    scope = applicationScope,
    io = Dispatchers.IO,
    config = {
        val deviceId = identity.read()
        RoleConfig(
            hostId = deviceId,
            hostName = deviceName,
            clientId = deviceId,
            clientName = Build.MODEL,
            remoteHostId = "waiting-host",
            remoteAddress = "127.0.0.1",
            sourceId = "local-source",
        )
    },
).build()
```

### 2. 角色控制与释放

```kotlin
// 观察运行状态与设备名称
roleControl.state.collect { state -> /* serverOn, phase 等 */ }
roleControl.deviceName?.collect { name -> /* 当前设备名 */ }

// 启停共享音源 / 加入本机收听 / 重命名
roleControl.setServer(true)
roleControl.joinSource()
roleControl.renameDevice("Living Room")

// 切换至本地独占播放前，通过 localGate 协调释放多房间接收输出
roleControl.localGate?.let { /* 按宿主播放器门控接入 */ }

// 退出多房间运行时释放 Server 与 Client 资源
roleControl.stop()
```

- 接入内置 Compose 界面时，可在 Hilt 环境中直接挂载 `com.qytech.multi_room.feature.route.MultiRoomFeature()`。
- **系统镜像约束**：`noBackupFilesDir` 中的多房间设备身份不可打包复制到多台量产设备，否则同局域网同名设备会发生服务发现冲突。

## 更新日志

完整变更记录见 [更新日志](CHANGELOG.md)，返回[文档首页](../../README.md)。
