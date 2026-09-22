# QYMediaScanner 更新日志

## 0.1.0 - 2026-09-22

### 发布
- 正式版 `0.1.0` 定版，Maven 坐标为 `io.github.qytech:qymediascanner:0.1.0`。
- 扫描入库的标题/艺术家/专辑随 AudioProbe 0.1.0 获得标签乱码与异常控制符修复（GBK→Latin1、UTF-8→GBK、撇号控制符等）。

## 0.0.2-snapshot - 2026-09-17

### 优化
- 优化流式版本比对缓冲区编码，提供零临时分配接口。
- 细化 `MediaScanReport` 扫描统计：补充 `traversalFailures`（目录遍历失败）与 `probeFailedFiles`（文件探测失败），收敛 `complete` 字段为纯遍历完整性标识。
- 增强 JNI 批次回调异常向宿主层冒泡传播机制，提升流式批次传输稳定性。

## 0.0.1-snapshot - 2026-09-16

### 新增
- 初始版本发布：多线程本地与外置存储媒体扫描库，支持音频元数据提取、增量缓存快照与海量曲库流式批量分发。
