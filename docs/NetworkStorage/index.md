# NetworkStorage 模块

Android 网络存储管理组件，提供 SMB 与 NFS 的发现、挂载、连接检测和卸载能力。

## 依赖与权限

先按 [HiFiPlayer SDK 接入](../HiFiPlayer/index.md) 添加 QYTech Maven 仓库。

```kotlin
implementation("io.github.qytech:networkstorage:0.1.12")
```

- `minSdk = 29`、Java 17，支持 SMB 1.0/2.x/3.x（含匿名免密访问与协议降级）及 NFS 发现与挂载。
- `0.1.11` 起已移除 `io.github.qytech:libdsm` 与 `io.github.qytech:core` 依赖，不再包含 Native `libdsm` 动态库；AAR 清单内置 `INTERNET`、`ACCESS_NETWORK_STATE`、`CHANGE_WIFI_MULTICAST_STATE` 权限并自动合并到宿主应用。

## 普通 Android 应用

固件宿主可以继续使用原有挂载接口。普通应用可在初始化 SMB/NFS 管理器前注册进程级的 `UserSpaceMounts` 实现。

```kotlin
import com.qytech.networkstorage.UserSpaceMounts

fun configureNetworkStorage(backend: UserSpaceMounts) {
    UserSpaceMounts.install(backend)
}
```

宿主后端实现 `connect(config)`、`disconnect(path)` 和 `volumes(protocol)`，负责共享连接及其文件访问。后续可复用管理器的连接、断开和卷列表接口。实现网络 I/O 时使用后台线程，断开连接时释放文件句柄和网络会话。

## 使用方法与卸载前协调

从 v0.1.7 开始，`SambaStorageManager` 与 `NfsStorageManager` 可接收 `StorageRemovalCoordinator`。驱动调用实际卸载接口前会先执行该回调，业务侧可在回调中停止播放并关闭挂载点上的文件句柄；退出或销毁管理器时应调用 `release()` 取消发现协程并释放内部发现运行时与解析器资源：

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

sambaManager.setDiscoveryListener { servers -> /* 更新已发现 SMB 列表 */ }
sambaManager.startDiscovery()

// 页面/服务销毁时停止发现并释放内部资源
sambaManager.stopDiscovery()
sambaManager.release()
nfsManager.release()
```

`playbackStorageCoordinator.stopAndClose(...)` 代表接入方自己的播放资源协调实现，不属于 NetworkStorage SDK。回调返回 `true` 表示清理已完成；驱动最多等待 1 秒，随后继续执行卸载。未传入协调器时使用 `StorageRemovalCoordinator.NONE`，行为与旧版本一致。

## 更新日志

### v0.1.12（2026-11-21）

- 增加 SMB/NFS 用户态挂载后端注册接口，普通应用可复用管理器的连接、断开和卷列表操作。
- 按实际后端复核掉线状态，SMB 登录凭据仅在同一服务器内复用。

### v0.1.11（2026-11-11）

- 移除 `io.github.qytech:libdsm` 与 `io.github.qytech:core` 依赖（同步移除对应 `libdsm` ProGuard 规则），不再携带 Native `libdsm` 动态库。
- NetBIOS 主机名发现与反查从 Native `libdsm` 切换为 JCIFS 节点状态查询，配合 mDNS、SMB 445 端口扫描及本地 IPv4 `/24` 网段枚举；公开 `SambaStorageManager`、`NfsStorageManager`、`StorageRemovalCoordinator` 与 `release()` 接口保持不变。
- 说明：`0.1.10` 为内部发布配置过渡标签，未进入 Maven Central，对外正式版本为 `0.1.11`。

### v0.1.9（2026-10-13）

- 优化 mDNS 服务发现生命周期管理，引入基于启动代次的会话隔离机制，避免停止与重启后的过期回调交叉污染。
- 延迟并串行化底层网络发现初始化（`NetworkDiscoveryRuntime`），保持 `SambaStorageManager` / `NfsStorageManager` 原有构造与卸载协调接口不变。

### v0.1.8（2026-10-09）

- 增强 Samba 跨平台设备兼容性，全面支持老旧设备（SMB 1.0 / CIFS）与现代网络存储设备（SMB 2.x / SMB 3.x）的自适应协商与连接。
- 优化匿名登录访问体验，支持无需账号密码直接浏览与挂载开放共享目录（兼容 Windows 共享、主流品牌 NAS 以及 Linux Samba 服务器）。
- 优化网络存储协议协商与降级流程，大幅降低连接建立耗时，提升连接成功率。
- 提升底层网络挂载兼容性，保障各类存储设备在匿名访问模式下的稳定挂载。

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

[samba\-version1\.0\-mount\-issue\.7z](https://github.com/qytech/QYDocs/blob/main/docs/NetworkStorage/%E5%9B%BE%E7%89%87%E5%92%8C%E9%99%84%E4%BB%B6/samba-version1.0-mount-issue.7z)
