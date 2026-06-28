# AI Export Meeting Deconstruction Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Upgrade `miaoji-decon` so pasted meeting text and AI export/X creator meetings are handled explicitly, safely, and verifiably.

**Architecture:** This remains a static skill repository. The main skill owns behavior, references own detailed workflow/template rules, and a dependency-free Python validator enforces privacy and structure. Real meeting content stays out of the public repo.

**Tech Stack:** Markdown skill docs, static HTML, Python 3.9 standard library, `unittest`, `git`, `rg`.

## Global Constraints

- Do not commit the pasted meeting transcript, real private deconstruction output, Feishu private URLs, or decrypted content.
- Do not modify `docs/enc.json`.
- Do not add npm, Python package, framework, or generated dependency lock files.
- Keep real examples private; public examples may only be synthetic or explanatory.
- `lark-cli` remains the Feishu integration boundary.
- `docs/index.html` must keep `noindex, nofollow, noarchive, nosnippet`.
- All worker tasks must stay inside their assigned file ownership.

---

## File Structure

- `skills/miaoji-decon/SKILL.md`: trigger modes, scene taxonomy, command boundaries, return contract.
- `skills/miaoji-decon/references/workflow.md`: operational details for scan/manual URL/pasted text, failure compensation, command caveats.
- `skills/miaoji-decon/references/template.md`: visible digest structure and scene-specific extraction prompts.
- `scripts/validate_repo.py`: static validator with no third-party dependencies.
- `tests/test_validate_repo.py`: unit tests for validator behavior using temporary files.
- `README.md`: human-facing overview, pasted-text mode, validation command.
- `skills/miaoji-decon/examples/README.md`: public example policy.

## Task 1: Add Repository Validator

**Files:**
- Create: `scripts/validate_repo.py`
- Create: `tests/test_validate_repo.py`

**Interfaces:**
- Produces: command `python3 scripts/validate_repo.py`
- Produces: importable functions `read_text(path: Path) -> str`, `validate_repo(root: Path) -> list[str]`, and `main() -> int`
- Consumes: repository files listed in File Structure

- [ ] **Step 1: Write failing tests**

Create `tests/test_validate_repo.py`:

```python
import tempfile
import unittest
from pathlib import Path

from scripts.validate_repo import validate_repo


class ValidateRepoTests(unittest.TestCase):
    def make_repo(self, missing_template_heading=False, public_real_example=False):
        tmp = tempfile.TemporaryDirectory()
        root = Path(tmp.name)
        (root / "skills/miaoji-decon/references").mkdir(parents=True)
        (root / "skills/miaoji-decon/examples").mkdir(parents=True)
        (root / "docs").mkdir()

        skill = root / "skills/miaoji-decon/SKILL.md"
        skill.write_text("pasted-text\n出海\n自媒体运营\n--owner-ids me\n--page-size 30\n", encoding="utf-8")

        headings = [
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
        if missing_template_heading:
            headings.pop()
        (root / "skills/miaoji-decon/references/template.md").write_text("\n".join(headings), encoding="utf-8")

        (root / "skills/miaoji-decon/references/workflow.md").write_text(
            "--owner-ids me\n--page-size 30\npasted text\nfailures.jsonl\n",
            encoding="utf-8",
        )
        example_text = "真实复盘内容" if public_real_example else "真实复盘仅存于私有 Obsidian 库"
        (root / "skills/miaoji-decon/examples/README.md").write_text(example_text, encoding="utf-8")
        (root / "docs/index.html").write_text("noindex, nofollow, noarchive, nosnippet", encoding="utf-8")
        (root / "docs/enc.json").write_text("{}", encoding="utf-8")
        return tmp, root

    def test_valid_repo_has_no_errors(self):
        tmp, root = self.make_repo()
        self.addCleanup(tmp.cleanup)
        self.assertEqual(validate_repo(root), [])

    def test_missing_template_heading_is_error(self):
        tmp, root = self.make_repo(missing_template_heading=True)
        self.addCleanup(tmp.cleanup)
        errors = validate_repo(root)
        self.assertTrue(any("来源边界" in error for error in errors))

    def test_public_real_example_is_error(self):
        tmp, root = self.make_repo(public_real_example=True)
        self.addCleanup(tmp.cleanup)
        errors = validate_repo(root)
        self.assertTrue(any("public examples" in error for error in errors))


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Run test and verify it fails**

Run: `python3 -m unittest tests.test_validate_repo -v`

Expected: FAIL with `ModuleNotFoundError: No module named 'scripts.validate_repo'`.

- [ ] **Step 3: Implement validator**

Create `scripts/validate_repo.py`:

```python
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
```

- [ ] **Step 4: Run tests and validator**

Run:

```bash
python3 -m unittest tests.test_validate_repo -v
python3 scripts/validate_repo.py
```

Expected: all tests pass and validator prints `miaoji-decon repository validation passed`.

- [ ] **Step 5: Commit**

```bash
git add scripts/validate_repo.py tests/test_validate_repo.py
git commit -m "test: add miaoji-decon repo validator"
```

## Task 2: Update Main Skill Behavior

**Files:**
- Modify: `skills/miaoji-decon/SKILL.md`

**Interfaces:**
- Produces: explicit `pasted-text` mode used by the validator
- Produces: first-class `出海` and `自媒体运营` scene routing
- Consumes: existing workflow references and template structure

- [ ] **Step 1: Add pasted-text trigger and mode**

In `触发方式` and `工作模式`, add a Mode D named `粘贴文本 / 本地附件草稿模式` with the literal marker `pasted-text`. It must say:

```markdown
### 模式 D：粘贴文本 / 本地附件草稿模式（pasted-text）

用户直接贴出会议纪要、逐字稿，或提供本地 `.txt/.md` 附件时，先读完所有附件，再进入 draft-only 处理：

- 不要求 `minute_token`。
- 不调用 `minutes +search` 或 `vc +notes`。
- 不写飞书 Base/Doc，不 push GitHub。
- 输出仍按 `references/template.md` 的学习复盘结构。
- 来源边界写明：基于用户提供的粘贴文本/附件，未连接飞书妙记原始记录。
```

- [ ] **Step 2: Add scenes**

Extend the scene table with:

```markdown
| 出海 | 海外产品/支付/定价/增长/SEO/社媒/客服/合规 | 道、法、势重；术要落到验证动作 |
| 自媒体运营 | X/推特/公众号/小红书/内容涨粉/商单/联盟营销 | 法、术、信号重；必须拆冷启动、内容格式、转化路径 |
```

- [ ] **Step 3: Add AI export meeting extraction rule**

Near the learning digest section, add a short rule:

```markdown
创业分享/出海/X 自媒体类会议，额外检查五类资产：产品机会、分发渠道、冷启动动作、变现路径、误读风险。没有逐字稿支撑时，把它写成“可验证假设”，不要写成事实。
```

- [ ] **Step 4: Run validator**

Run: `python3 scripts/validate_repo.py`

Expected: pass after Task 1 is present.

- [ ] **Step 5: Commit**

```bash
git add skills/miaoji-decon/SKILL.md
git commit -m "feat: document pasted text deconstruction mode"
```

## Task 3: Update Workflow And Template References

**Files:**
- Modify: `skills/miaoji-decon/references/workflow.md`
- Modify: `skills/miaoji-decon/references/template.md`

**Interfaces:**
- Produces: workflow text containing literal `pasted text`
- Produces: template support for entrepreneurial/X-media meetings
- Consumes: Mode D from Task 2

- [ ] **Step 1: Update workflow**

Add a section after the `lark-cli` caveats:

```markdown
## 粘贴文本 / 本地附件输入（pasted text）

当输入来自用户粘贴文本或本地 `.txt/.md` 附件，而不是飞书 URL/token：

1. 先读完所有用户指定文件。
2. 将文件名、录音日期、会议主题写入草稿 frontmatter；没有的信息写 `unknown`，不要猜。
3. 跳过 `minutes +search`、`vc +notes`、Base、Doc、GitHub push。
4. 只生成 draft-only 学习复盘，并在 `⚠️ 来源边界` 写明“基于用户提供文本，未连接飞书原始妙记”。
5. 如果后续用户补充 Feishu URL/token，再按手动单条妙记流程补齐三端归档。
```

- [ ] **Step 2: Update template**

Add a subsection after `框架基准`:

```markdown
## 出海 / 自媒体运营会议的额外提取清单

遇到 AI 出海、独立开发者、X/推特自媒体、商单/联盟营销类分享，深挖时额外检查：

- **产品机会**：讲者实际验证过什么需求，哪些只是观点。
- **分发渠道**：SEO、社媒、Handle 曝光、大 V 转发、社群、广告分别承担什么角色。
- **冷启动动作**：第一篇内容、第一批背书、第一轮用户如何拿到。
- **变现路径**：订阅、商单、联盟营销、课程/社群、创作者收益分别适合什么条件。
- **误读风险**：不要把个体结果误读成普遍规律，不要把平台红利误读成能力闭环。
```

- [ ] **Step 3: Run validator**

Run: `python3 scripts/validate_repo.py`

Expected: pass after Task 1 is present.

- [ ] **Step 4: Commit**

```bash
git add skills/miaoji-decon/references/workflow.md skills/miaoji-decon/references/template.md
git commit -m "docs: add export creator meeting workflow guidance"
```

## Task 4: Update README And Public Example Policy

**Files:**
- Modify: `README.md`
- Modify: `skills/miaoji-decon/examples/README.md`

**Interfaces:**
- Produces: README mention of pasted text mode and validation command
- Consumes: validator command from Task 1

- [ ] **Step 1: Add README workflow note**

In `能做什么`, add a bullet:

```markdown
- 支持用户粘贴会议纪要/逐字稿或提供本地文本附件，进入 draft-only 学习复盘模式；没有 Feishu token 时不写 Base/Doc、不 push GitHub。
```

In `Run Or View Locally`, add:

```bash
python3 scripts/validate_repo.py
python3 -m unittest discover -s tests -v
```

- [ ] **Step 2: Tighten example policy**

Replace `skills/miaoji-decon/examples/README.md` with:

```markdown
# Examples Policy

真实复盘仅存于私有 Obsidian 库与内部飞书。请勿在公开仓库放真实会议内容、逐字稿、私人 URL、真实人物关系图或未清洗的会议结论。

允许放在这里的只有：

- 完全虚构的 synthetic 示例。
- 不含真实人物、公司、token、链接的格式说明。
- 用来测试模板结构的最小 Markdown 片段。
```

- [ ] **Step 3: Run validation**

Run:

```bash
python3 scripts/validate_repo.py
python3 -m unittest discover -s tests -v
python3 -m compileall .
```

Expected: all pass.

- [ ] **Step 4: Commit**

```bash
git add README.md skills/miaoji-decon/examples/README.md
git commit -m "docs: document pasted text draft workflow"
```

## Final Integration

- [ ] Run `git log --oneline --decorate -8`.
- [ ] Run `python3 -m unittest discover -s tests -v`.
- [ ] Run `python3 scripts/validate_repo.py`.
- [ ] Run `python3 -m compileall .`.
- [ ] Run `rg -n "token|secret|password|access_key|authorization|appSecret|accessToken" .`.
- [ ] Review `git diff main...HEAD --stat`.
- [ ] Confirm `docs/enc.json` is unchanged.
