---
name: qydocs-maintainer
description: 维护 QYDocs 中的 QYTech Android SDK Markdown 文档。用于新增 SDK 模块文档、更新版本与变更日志、同步根 README 导航和日期、补充 Android/Kotlin 接入示例、审查文档一致性或修复链接与格式问题。
---

# QYDocs 文档维护

## 开始前

1. 阅读仓库根目录的 `AGENTS.md`。
2. 阅读目标模块全文和根 `README.md`；新增模块时再选一个结构接近的模块作为参考。
3. 需要决定标题、代码块、版本记录或首页写法时，读取 [references/style-guide.md](references/style-guide.md)。
4. 区分已确认事实与推断。版本号、日期、Maven 坐标、API 签名和兼容性必须有用户输入、源码或发布源支撑。

## 选择工作流

### 更新模块版本

1. 定位模块主文档、独立 `CHANGELOG.md`（如有）和根 `README.md` 中的所有相关信息。
2. 将新版本放在历史记录最前，并说明 Added、Changed、Fixed 中实际发生的内容，不扩大结论。
3. 同步依赖示例、最新版本说明、根导航日期、根模块摘要和仓库最后更新时间。
4. 搜索旧版本号与旧日期，逐项判断剩余结果是否属于历史记录。

### 新增模块

1. 创建 `docs/<Module>/index.md`，目录大小写与产品名一致。
2. 只写有可靠信息支撑的章节；不创建空的 API、状态模型或 FAQ。
3. 在根 `README.md` 增加导航行和模块摘要；若已发布到 Maven Central，沿用现有徽章格式。
4. 检查模块链接、Maven 坐标和代码示例。

### 补充或重构文档

1. 保留原始技术含义与历史版本记录。
2. 优先修复用户正在触及的段落；不要借机全库格式化。
3. 让示例保持最小、可复制，并明确初始化、监听、控制和释放资源的顺序。
4. 对 JNI、线程、权限、ABI、minSdk 和资源释放等约束使用明确措辞。

### 审查文档

1. 检查重复事实是否一致，重点关注版本、日期、坐标、API 名称和参数单位。
2. 检查示例是否泄露凭据、是否遗漏必要权限与资源释放。
3. 检查相对链接、代码围栏和标题结构。
4. 报告问题时给出文件与行号；只有用户要求修改时才编辑文件。

## 验证

在仓库根目录运行：

```powershell
python .codex/skills/qydocs-maintainer/scripts/validate_docs.py
git diff --check
git diff -- README.md docs .codex AGENTS.md
```

将校验脚本的 `ERROR` 视为必须修复。`WARN` 可能来自历史文档；若警告位于本次修改区域则修复，否则在交付时简要说明。

最后用 `rg` 搜索本次涉及的版本号、日期、Maven 坐标或 API 名称，确认所有应同步位置均已更新。
