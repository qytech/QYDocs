# NetworkStorage 模块

Android 网络存储管理组件，提供 SMB 与 NFS 的发现、挂载、连接检测和卸载能力。

## 依赖

```kotlin
implementation("io.github.qytech:networkstorage:0.1.7")
```

## 卸载前协调播放资源

从 v0.1.7 开始，`SambaStorageManager` 与 `NfsStorageManager` 可接收 `StorageRemovalCoordinator`。驱动调用实际卸载接口前会先执行该回调，业务侧可在回调中停止播放并关闭挂载点上的文件句柄。

```kotlin
val removalCoordinator = StorageRemovalCoordinator { mountPoint ->
    // 业务侧 suspend 方法：停止使用该挂载点的播放任务，并等待文件句柄关闭。
    playbackStorageCoordinator.stopAndClose(mountPoint)
}

val sambaManager = SambaStorageManager(
    context = applicationContext,
    storageRemovalCoordinator = removalCoordinator,
)

val nfsManager = NfsStorageManager(
    context = applicationContext,
    storageRemovalCoordinator = removalCoordinator,
)
```

`playbackStorageCoordinator.stopAndClose(...)` 代表接入方自己的播放资源协调实现，不属于 NetworkStorage SDK。回调返回 `true` 表示清理已完成；驱动最多等待 1 秒，随后继续执行卸载。未传入协调器时使用 `StorageRemovalCoordinator.NONE`，行为与旧版本一致。

## 更新日志

### v0.1.7（2026-08-07）

- 新增 `StorageRemovalCoordinator`，支持 SMB/NFS 卸载前通知业务侧清理播放资源。
- `SambaStorageManager` 与 `NfsStorageManager` 构造函数新增可选协调器参数，未传入时保持原有调用方式。
- 卸载前协调最多等待 1 秒，避免业务侧清理异常导致卸载流程长期阻塞。

### v0.1.6（2026-08-03）

- 修复 NFS 挂载目录加载不全问题

### v0.1.5（2026-06-05）

1. 修复NetBIOS广播扫描不到Nsd设备问题

## v0\.1\.4 \(20260602\)

1. 优化匿名登录失败问题

## v0\.1\.3 （20260521）

1. 修复部分V1挂在失败问题

## v0\.1\.2 （20260417）

1. 修复匿名登录异常问题

## V0\.1\.1

1. 修复Samba v1\.0 的服务器挂载失败问题 ，需要固件打下面补丁

[samba\-version1\.0\-mount\-issue\.7z](图片和附件/samba-version1.0-mount-issue.7z)



