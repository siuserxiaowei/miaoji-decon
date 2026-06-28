# 妙记拆解 · 道法术器势

<!-- SIUSER-REPO-GUIDE:START -->
## Repository Guide

### What This Repository Does

妙记拆解复盘系统：监控飞书妙记，把会议自动拆成可学习、可追问、可归档的深度复盘。

English summary: Meeting deconstruction system that turns Feishu minutes into learnable reviews and follow-up assets.

### Online Entry Points

- GitHub repository: https://github.com/siuserxiaowei/miaoji-decon
- Live / GitHub Pages: https://siuserxiaowei.github.io/miaoji-decon/
- Default branch: `main`
- Primary language: `not specified`

### How To Read / Learn This Repository

1. 先读本 README，确认项目目标、在线入口和本地运行方式。
2. 打开上方 Live / GitHub Pages 链接，先从最终效果理解项目。
3. 优先阅读线上页面或 `index.html`，再看 `data/`、`assets/`、`scripts/` 等生成材料。
4. 如果要修改内容，先小范围改动，再运行本 README 中的验证命令。

### Clone This Repository

```bash
git clone https://github.com/siuserxiaowei/miaoji-decon.git
cd miaoji-decon
```

### Run Or View Locally

```bash
python3 -m http.server 8000
```

然后打开 `http://127.0.0.1:8000/`。

本地验证 / Local validation:

```bash
python3 scripts/validate_repo.py
python3 -m unittest discover -s tests -v
python3 -m compileall .
```

### Repository Map

| Path | Purpose |
| --- | --- |
| `README.md` | 项目入口说明，先读这里。 |
| `docs/` | 文档或 GitHub Pages 输出目录。 |
| `skills/` | 项目目录。 |

### Maintenance Notes

- Keep this README in sync when the project purpose, live link, or run commands change.
- Prefer small, focused commits when changing code, data, or generated pages.
- Run the relevant build or validation command before publishing changes.
- If this is a generated/static archive, update the source data first, then regenerate the public files.

### Privacy And Safety

- Do not commit API keys, tokens, passwords, cookies, private URLs, or internal account data.
- Keep private source material out of public GitHub Pages output unless it has been explicitly cleared for publication.
- When in doubt, run a quick secret scan such as `rg -n "token|secret|password|access_key|authorization"` before pushing.
<!-- SIUSER-REPO-GUIDE:END -->

> 监控飞书妙记 → 把每场会自动拆成一篇**能学到东西的「深度学习复盘」** → 归档到 Obsidian、飞书、并推送 GitHub。

`miaoji-decon` 的产出**不是流水账、不是贴标签归档，而是复盘**——让一个没能在现场充分参与的人，会后能**学到东西、还知道回去 7 天干啥**。道法术器势是分析的尺子（幕后），端到你面前的是能学到东西的人话（台前）。

一句话准则：**读完最重要的不是收藏，是选一个动作在 7 天内验证。**

它是 [`siuserxiaowei/miaoji-s`](https://github.com/siuserxiaowei/miaoji-s) 的升级版：把通用纪要换成深度学习复盘，并多了 Obsidian + GitHub + Wiki 复利三个出口。

## 一篇复盘的固定结构

```
⏱ 如果只读 10 分钟        ← N 条带走判断，全文最重要一屏
🎯 这篇真正能学什么        ← 这场会练的是什么眼力
🧭 道法术器势(→你可以怎么用) ← 一张表：层 | 本场榨干版 | 动作化的"怎么用"
📚 深挖：N 个知识点         ← 重心。每个三段：是什么 / 为什么重要 / 你能用
🛠 可直接复用的方法        ← 每个含"不要误读成"
📅 7 天作业               ← Day1-7，把"学到"逼成"做到"
🤔 回到自己业务的追问      ← 逼读者迁移到自己身上
👥 关键人物与资源          ← 把"人/关系"变成资源地图
💬 金句                   ← 原话 + 一句"在说什么"
⚠️ 来源边界
```

**框架基准（生财有术 / AI破局）**：道以明向、法以立本、术以立策、器以成事、势以察时——道=做对的事，法术器=把事做对，势=何时做。

## 能做什么

- 定时扫描 / 手动处理飞书妙记新录音（去重 + 失败补偿）。
- 支持用户粘贴会议纪要/逐字稿或提供本地文本附件，进入 draft-only 学习复盘模式；没有 Feishu token 时不写 Base/Doc、不 push GitHub。
- 按场景分类（AI硬件 / 知识 / 人情世故 / 大佬分享 / 饭局闲聊 / 出海）自适应详略。
- 深挖每场会的信息点/知识点，按学习复盘结构组织；严格区分"讲者讲 vs 我引申"、数字带销售口径标存疑、不堆标签噪声、不编造、信息空就少写别注水。
- 三端归档：Obsidian「会议纪要拆解」+ 飞书在线文档/多维表格 + push GitHub。
- 两层复利：复盘是 source 层，把道/法/势/人 升华进 Wiki 母库（概念页/人物页），越攒越厚。

## 安装

```bash
npx -y skills add siuserxiaowei/miaoji-decon -g --skill miaoji-decon -y --full-depth
```

装完重启 Codex / Claude Code。触发词：`/妙记拆解`、`/道法术器`、`/dfsq`。

## 一篇复盘长什么样

复盘产物为**内部私有资料**，含真实人名/业务，仅存于本地 Obsidian 库与内部飞书，不在公开仓库或公开网页展示。本仓库只公开 skill 代码与模板。

## 运行依赖

- `lark-cli`（飞书命令行，已授权）—— 读妙记、写飞书文档/Base。
- `git` + `gh`（已登录）—— push 库、生成在线链接。
- 一个本地 Obsidian 库（其本身是 git 仓库，远程指向 GitHub）。

## 本地状态

`~/.miaoji-decon/`：`config.json`（配置 + 上次扫描时间）、`processed.jsonl`（去重）、`failures.jsonl`（失败补偿）、`artifacts/`、`drafts/`。

## 定时自动扫描

`~/.miaoji-decon/scan.sh` + macOS launchd（`com.miaoji-decon.scan`，每天 8:00）headless 调 `claude` 执行扫描提示词：扫新妙记 → 深度学习复盘 → 写 Obsidian → push GitHub。**禁止用 `CronCreate`**（7 天过期）。

## 参考来源

- [`siuserxiaowei/miaoji-s`](https://github.com/siuserxiaowei/miaoji-s)：工程骨架（监控/去重/失败队列）。
- [`situker/sk-info-assets`](https://github.com/situker/sk-info-assets)：信息资产化的结构意识。
- [`xiaomo-agi/xiaomo-skills`](https://github.com/xiaomo-agi/xiaomo-skills)：哨兵扫描、场景分类、禁用 CronCreate 的教训。
- [`situker/situk-yangtao-perspective`](https://github.com/situker/situk-yangtao-perspective)：诚实边界、不编造、区分一手 vs 引申。
- 学习复盘结构借鉴自 `situker/scai-meeting-minutes-wiki`（如果只读10分钟 / 这篇能学什么 / 7天作业 / 回到业务追问）。

只吸收工作流与结构思路，不复制大段内容。
