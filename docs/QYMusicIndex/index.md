# QYMusicIndex Android SDK

[![Maven Central](https://img.shields.io/maven-central/v/io.github.qytech/qymusicindex.svg)](https://central.sonatype.com/artifact/io.github.qytech/qymusicindex)
[![Changelog](https://img.shields.io/badge/Changelog-CHANGELOG.md-blue.svg)](./CHANGELOG.md)

QYMusicIndex（`io.github.qytech:qymusicindex`）是基于 Rust 与 Direct JNI（`libqy_musicindex.so`）的曲库拼音首字母/排序键提取与内存倒排搜索索引引擎。主要入口为 `PinyinSortUtil` 与 `NativeMusicIndex`。

> 当前版本：`0.0.1-snapshot`（2026-10-13，预发布快照版本）。版本变化见[更新日志](CHANGELOG.md)。

## 依赖与运行环境

```kotlin
dependencies {
    implementation("io.github.qytech:qymusicindex:0.0.1-snapshot")
}
```

- Android API 29+，Java 17，仅提供 `arm64-v8a`（内置 `libqy_musicindex.so`）。
- 无需额外 Android 清单权限；若 Native 动态库未加载（如本机 JVM 单测环境），`PinyinSortUtil` 会自动回退为规范化字符排序，可通过 `NativeMusicIndex.sortKeyVersion`（已加载为 `1`，回退为 `0`）判断持久化的排序键是否需要重建。

## 核心能力（v0.0.1-snapshot）

- **拼音首字母与确定性排序键**：`PinyinSortUtil.getPinyinInitial(...)`、`getPinyinSortKey(...)`、`createComparator(...)` 与 `computeSectionIndices(...)` 支持汉字全拼/首字母提取与 `#` / `A`–`Z` 索引分区计算。
- **内存倒排检索与序列化快照**：`NativeMusicIndex` 支持单条/批量曲目插入（`insert`、`batchInsert`）、删除、多字段排序输出、分区索引计算及磁盘快照保存/加载（`persist`、`load`）。

## 使用方法

### 1. 拼音排序与侧边栏分组索引

```kotlin
import com.qytech.musicindex.NativeMusicIndex
import com.qytech.musicindex.sort.PinyinSortUtil

val initial = PinyinSortUtil.getPinyinInitial("海阔天空") // 'H'，数字与符号归为 '#'
val sortKey = PinyinSortUtil.getPinyinSortKey("海阔天空")
val keyVersion = NativeMusicIndex.sortKeyVersion       // 1 表示原生拼音排序键，0 表示回退键

val sorted = tracks.sortedWith(
    PinyinSortUtil.createComparator({ it.title }, ascending = true),
)
val sectionIndices = PinyinSortUtil.computeSectionIndices(sorted) { it.title }
```

### 2. 内存倒排索引（含磁盘快照与释放）

在后台 I/O 线程构建与写入索引；销毁索引实例时务必调用 `close()` 释放原生句柄：

```kotlin
import com.qytech.musicindex.IndexSortField
import com.qytech.musicindex.NativeMusicIndex
import com.qytech.musicindex.model.IndexedTrack

val index = NativeMusicIndex.create()
if (index.isAvailable) {
    index.insert(IndexedTrack(id = 1L, title = "海阔天空", artist = "Beyond", album = "乐与怒"))
    index.batchInsert(moreTracks)

    val matchedIds = index.search("hktk", limit = 50)
    val sortedIds = index.getSortedTrackIds(sortField = IndexSortField.TITLE, ascending = true)
    val sections = index.getSectionIndices(sortField = IndexSortField.TITLE, ascending = true)

    index.persist(snapshotFile.absolutePath)
}

// 不再使用时释放原生索引内存
index.close()
```

- 若持久化快照或大规模索引插入在后台协程执行，应串行化写入并在所有索引操作结束后调用 `close()`。

## 更新日志

完整变更记录见 [更新日志](CHANGELOG.md)，返回[文档首页](../../README.md)。
