# QYMultiroom 更新日志

本文档记录 `io.github.qytech:qymultiroom` 各版本的变更内容。

## v0.0.6 - 2026-11-25

- 修复系统预装应用（`FLAG_SYSTEM` 且未覆盖更新）启动多房间接收子进程时找不到 ICU 库的问题：检测到 `ANDROID_I18N_ROOT/lib64/libandroidicu.so` 时自动补充 `LD_LIBRARY_PATH`。
- 同步发布 `0.0.6` 正式 AAR、组件许可证及配套 Native 对应源码包，对外接入接口不变。[Native 对应源码](https://github.com/qytech/maven-releases/releases/download/qymultiroom-0.0.6/qymultiroom-0.0.6-native-sources.zip)

## v0.0.5 - 2026-11-21

- 通过 QYTech GitHub Pages Maven 仓库交付单一 AAR。宿主使用 `MultiRoomFactory` 和公开的设备、控制与音源接口接入。
- `currentPlaybackSharingGroup(serverId)` 按主机和当前音源绑定标识可加入的共享组，覆盖暂停、并发加入和邀请恢复场景。
- 更新 ARM64 解码组件，提供与正式制品匹配的 Native 对应源码、补丁、重建脚本及校验值。[Native 对应源码](https://github.com/qytech/maven-releases/releases/download/qymultiroom-0.0.5/qymultiroom-0.0.5-native-sources.zip)

## v0.0.4 - 2026-11-11

- 修复 Fat-AAR 打包时嵌入子模块字节码仍引用子模块 `R$string` 的问题，统一重定位到 `com.qytech.multi_room.R`，解除消费者 Release R8 打包失败。

## v0.0.3 - 2026-11-10

- 稳定 `RoleControl` 设备命名与音源标识契约：新增 `deviceName`、`renameDevice(name)`、`renameSource(name)`、`prepareServer()`、`joinSource()` 及 `RoleConfig.sourceId`。
- 完善 `LocalPlayGate` 与接收器输出释放门控，在本地或独占播放开始前释放多房间收听输出。
- 改进设备改名同步、延迟显示及随机设备 UUID 持久化（基于 `noBackupFilesDir`）。

## v0.0.2-snapshot - 2026-10-29

- 对齐多房间设备绑定、共享就绪与主题适配逻辑，统一 14 个内部子模块 Fat-AAR 打包配置。

## v0.0.1-snapshot - 2026-10-29

- 初始版本：独立 `qymultiroom` Fat-AAR 发布结构，提供 Snapserver/Snapclient 运行时、音源队列与独立解码能力。
