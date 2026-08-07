#!/usr/bin/env python3
"""Validate structural invariants of the QYDocs Markdown repository."""

from __future__ import annotations

import re
import sys
from pathlib import Path
from urllib.parse import unquote, urlsplit


ROOT = Path(__file__).resolve().parents[4]
DOCS = ROOT / "docs"
MARKDOWN_LINK = re.compile(r"(?<!!)\[[^\]]+\]\(([^)]+)\)")
HTML_LINK = re.compile(r"<a\s+[^>]*href=[\"']([^\"']+)[\"']", re.IGNORECASE)


def report(kind: str, path: Path, message: str, line: int | None = None) -> None:
    location = path.relative_to(ROOT).as_posix()
    if line is not None:
        location += f":{line}"
    print(f"{kind} {location}: {message}")


def local_target(raw: str, source: Path) -> Path | None:
    value = raw.strip().strip("<>").split(maxsplit=1)[0]
    parts = urlsplit(value)
    if parts.scheme or parts.netloc or value.startswith(("#", "mailto:")):
        return None
    path = unquote(parts.path)
    if not path:
        return None
    return (source.parent / path).resolve()


def main() -> int:
    errors = 0
    warnings = 0
    files = [ROOT / "README.md", *sorted(DOCS.rglob("*.md"))]

    for module in sorted(path for path in DOCS.iterdir() if path.is_dir()):
        if not (module / "index.md").is_file():
            report("ERROR", module, "模块目录缺少 index.md")
            errors += 1

    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    linked_modules = {
        match.group(1).rstrip("/").split("/")[-1]
        for match in re.finditer(r"\]\(docs/([^)/]+)/?\)", readme)
    }
    actual_modules = {path.name for path in DOCS.iterdir() if path.is_dir()}
    for module in sorted(actual_modules - linked_modules):
        report("WARN", ROOT / "README.md", f"导航表可能缺少模块 {module}")
        warnings += 1

    for path in files:
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError as exc:
            report("ERROR", path, f"不是有效 UTF-8：{exc}")
            errors += 1
            continue

        fence_lines = [i for i, line in enumerate(text.splitlines(), 1) if line.lstrip().startswith("```")]
        if len(fence_lines) % 2:
            report("ERROR", path, "代码围栏未闭合", fence_lines[-1])
            errors += 1

        h1_lines = [i for i, line in enumerate(text.splitlines(), 1) if re.match(r"^#\s+", line)]
        if len(h1_lines) != 1:
            report("WARN", path, f"一级标题数量为 {len(h1_lines)}，建议保持 1 个")
            warnings += 1

        for match in [*MARKDOWN_LINK.finditer(text), *HTML_LINK.finditer(text)]:
            target = local_target(match.group(1), path)
            if target is None:
                continue
            line = text.count("\n", 0, match.start()) + 1
            if not target.exists():
                # The repository contains historical references to release
                # attachments that were never committed. Keep them visible
                # without making the baseline validation unusable.
                report("WARN", path, f"相对链接目标不存在：{match.group(1)}", line)
                warnings += 1

    print(f"\n检查完成：{errors} 个错误，{warnings} 个警告，扫描 {len(files)} 个 Markdown 文件。")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
