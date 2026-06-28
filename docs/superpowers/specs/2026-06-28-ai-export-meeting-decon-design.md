# AI Export Meeting Deconstruction Design

## Context

The input meeting is a high-density offline sharing session about AI export entrepreneurship, product leverage, learning in public, and X/Twitter creator growth. It exposes a gap in the current `miaoji-decon` skill:

- The skill is strong for Feishu Minutes scan/manual URL flows, but does not clearly describe how to handle pasted meeting text when no `minute_token` is available.
- The scene taxonomy mentions `出海` in the template but the main skill routing table does not make `出海` or `自媒体运营` first-class routes.
- The public repository correctly avoids publishing real meeting deconstructions, but it lacks a validation guard that prevents future accidental public examples or broken template structure.

This change keeps real deconstruction output private. The public repo should improve the workflow, template, and validation layer only.

## Goals

1. Add an explicit pasted-text/manual-draft mode for meeting notes supplied as local text, attachments, or transcript snippets.
2. Add first-class scene routing for `出海` and `自媒体运营`, with emphasis on product leverage, public learning, platform distribution, conversion, and 7-day execution.
3. Make the output template better for entrepreneurial sharing sessions without turning every meeting into noisy labels.
4. Add a lightweight repository validator so future changes can check privacy, template shape, required command caveats, and static page safety.
5. Update the README with the new workflow and validation command.

## Non-Goals

- Do not commit the actual pasted meeting content, transcript, or generated private digest to this public repository.
- Do not implement Feishu API behavior directly in Python; `lark-cli` remains the integration boundary.
- Do not change `docs/enc.json` or publish decrypted/internal meeting data.
- Do not add a package manager, web framework, or build step.

## Product Behavior

### Pasted-Text Mode

When the user provides pasted text, local transcript files, or exported meeting notes without a Feishu URL/token, the skill should enter draft-only mode:

1. Read all supplied local text files before analysis.
2. Treat the material as source text, not as an already-verified transcript.
3. Generate the learning digest in the same fixed structure as normal.
4. Mark source boundaries clearly: no `minute_token`, no Feishu Doc/Base write, no GitHub public link.
5. Save only to a private destination when the user or local workflow asks for persistence.

### Scene Routing

`出海` and `自媒体运营` should be first-class scene types:

- `出海`: emphasize leverage, pricing/geography differences, product validation, payments, support load, distribution, and risk.
- `自媒体运营`: emphasize platform mechanics, cold start, account positioning, content formats, conversion paths, monetization, and misleading shortcuts to avoid.

Mixed scenes are allowed. For this meeting type, likely scene tags are `[大佬分享, 知识, 出海, 自媒体运营]`.

### Output Emphasis

For entrepreneurial sharing meetings, the digest should extract:

- 5-8 independent takeaways for fast reading.
- A `道法术器势` table where each row ends in an action.
- Deep-dive knowledge points that distinguish speaker claims from model interpretation.
- Reusable methods with a `不要误读成` warning.
- A 7-day assignment plan that turns learning into a small validation loop.
- People/resources as a resource map, while avoiding unverified personal claims.

## Architecture

The repository remains a static skill/documentation repository.

- `skills/miaoji-decon/SKILL.md` owns triggers, modes, scene routing, external command rules, and safety boundaries.
- `skills/miaoji-decon/references/template.md` owns the visible digest structure and writing standard.
- `skills/miaoji-decon/references/workflow.md` owns command-level operational details and fallback handling.
- `scripts/validate_repo.py` owns repository-level static checks.
- `tests/test_validate_repo.py` gives the validator deterministic coverage without extra dependencies.
- `README.md` remains the human entry point and should mention pasted-text mode plus validation.

## Quality Gates

- `python3 -m unittest discover -s tests -v`
- `python3 scripts/validate_repo.py`
- `python3 -m compileall .`
- `rg -n "token|secret|password|access_key|authorization|appSecret|accessToken" .`

The secret scan may match documented placeholder text and the password input in `docs/index.html`; those are acceptable if no real secrets appear.

## Parallel Work Slices

To support parallel subagent work, file ownership is split as follows:

- Worker A: `skills/miaoji-decon/SKILL.md`
- Worker B: `skills/miaoji-decon/references/workflow.md` and `skills/miaoji-decon/references/template.md`
- Worker C: `scripts/validate_repo.py` and `tests/test_validate_repo.py`
- Worker D: `README.md` and `skills/miaoji-decon/examples/README.md`

Workers must not edit files outside their assigned set. The controller integrates and runs the global quality gates.
