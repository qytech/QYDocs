# QYMusicIndex 更新日志

## 0.0.1-snapshot - 2026-10-13

### 新增

- 初始预发布快照：基于 Rust JNI（`libqy_musicindex.so`）提供 `PinyinSortUtil` 拼音首字母/排序键与分组索引提取，以及 `NativeMusicIndex` 内存倒排搜索、排序、分区统计与磁盘快照持久化能力。
- Maven 坐标：`io.github.qytech:qymusicindex:0.0.1-snapshot`（仅 `arm64-v8a`，Android API 29+）。
