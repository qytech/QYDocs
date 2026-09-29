# Roon Android SDK

## 添加依赖

```kotlin
implementation("io.github.qytech:roon:0.1.1")
```

## 更新日志

### v0.1.1（2026-09-29）

1. 修复部分 24-bit 及高规格曲目播放异常与噪声问题，提升高码率音频输出品质
2. 新增 MQA 核心解码支持与状态指示
3. 新增输出信号路径（模拟、数字、USB）动态识别与实时上报
4. 优化音频输出稳定性，消除偶发断音与播放欠载
5. 完善硬件音量双向联动与状态同步
6. 优化断网恢复与离线连接机制，增强网络自愈稳定性
7. 补齐封面二进制流与完整多语言元数据展示支持

### v0.1.0（2026-06-23）

1. 更新了 Roon Raat 1.1.47
2. 修复了 Roon 播放 DSD512 卡顿问题
3. 新增了 Roon 封面同步

```kotlin
override fun onArtworkChanged(mimeType: String?, data: ByteArray?) {
}
```


