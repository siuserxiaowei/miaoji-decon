#!/usr/bin/env python3
from __future__ import annotations

import sys
from pathlib import Path


REQUIRED_TEMPLATE_HEADINGS = [
    "## ⏱ 如果只读 10 分钟",
    "## 🎯 这篇真正能学什么",
    "## 🧭 道法术器势（→ 你可以怎么用）",
    "## 📚 深挖：N 个值得单独学的知识点",
    "## 🛠 可直接复用的方法（含\"不要误读成\"）",
    "## 📅 7 天作业",
    "## 🤔 回到自己业务的追问",
    "## 👥 关键人物与资源（这桌人能给你什么）",
    "## 💬 金句",
    "## ⚠️ 来源边界",
]

REQUIRED_SKILL_PHRASES = [
    "pasted-text",
    "出海",
    "自媒体运营",
    "--owner-ids me",
    "--page-size 30",
]

REQUIRED_WORKFLOW_PHRASES = [
    "--owner-ids me",
    "--page-size 30",
    "pasted text",
    "failures.jsonl",
]

PRIVATE_EXAMPLE_WARNING = "真实复盘仅存于私有 Obsidian 库"
ROBOTS_META = "noindex, nofollow, noarchive, nosnippet"


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def require_file(root: Path, relative: str, errors: list[str]) -> Path:
    path = root / relative
    if not path.exists():
        errors.append(f"missing required file: {relative}")
    return path


def require_phrases(text: str, phrases: list[str], label: str, errors: list[str]) -> None:
    for phrase in phrases:
        if phrase not in text:
            errors.append(f"{label} missing required phrase: {phrase}")


def validate_repo(root: Path) -> list[str]:
    errors: list[str] = []

    skill_path = require_file(root, "skills/miaoji-decon/SKILL.md", errors)
    workflow_path = require_file(root, "skills/miaoji-decon/references/workflow.md", errors)
    template_path = require_file(root, "skills/miaoji-decon/references/template.md", errors)
    examples_path = require_file(root, "skills/miaoji-decon/examples/README.md", errors)
    index_path = require_file(root, "docs/index.html", errors)
    enc_path = require_file(root, "docs/enc.json", errors)

    if errors:
        return errors

    require_phrases(read_text(skill_path), REQUIRED_SKILL_PHRASES, "SKILL.md", errors)
    require_phrases(read_text(workflow_path), REQUIRED_WORKFLOW_PHRASES, "workflow.md", errors)
    require_phrases(read_text(template_path), REQUIRED_TEMPLATE_HEADINGS, "template.md", errors)

    examples_text = read_text(examples_path)
    if PRIVATE_EXAMPLE_WARNING not in examples_text:
        errors.append("public examples must warn that real deconstructions stay private")
    if "真实复盘内容" in examples_text:
        errors.append("public examples must not contain real meeting deconstruction content")

    if ROBOTS_META not in read_text(index_path):
        errors.append("docs/index.html must keep noindex/noarchive robots meta")
    if enc_path.stat().st_size == 0:
        errors.append("docs/enc.json must not be empty")

    return errors


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    errors = validate_repo(root)
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1
    print("miaoji-decon repository validation passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
