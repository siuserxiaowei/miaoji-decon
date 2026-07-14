# 妙记拆解 · 道法术器势

<!-- SIUSER-REPO-GUIDE:START -->
## 项目介绍 / Project Introduction

### 中文
妙记拆解复盘系统：监控飞书妙记，把会议自动拆成可学习、可追问、可归档的深度复盘。

### English
Meeting deconstruction system that turns Feishu minutes into learnable reviews and follow-up assets.

## 使用方式 / Usage

### 中文
1. 优先打开在线入口或本地静态服务查看最终页面。
2. 内容型仓库通常从 `README.md`、`docs/`、`data/` 或 `content/` 开始阅读。
3. 更新资料后，重新生成或刷新静态页面，并检查链接、图片和文字是否正常。

### English
1. Start with the live link or a local static server to view the final page.
2. For content repositories, begin with `README.md`, `docs/`, `data/`, or `content/`.
3. After updating material, regenerate or refresh the static page and check links, images, and copy.

## 入口与元信息 / Entry Points & Metadata

- GitHub 仓库 / Repository: https://github.com/siuserxiaowei/miaoji-decon
- Live / 在线入口：https://siuserxiaowei.github.io/miaoji-decon/
- 公开复盘索引 / Public-safe digests: https://siuserxiaowei.github.io/miaoji-decon/public/
- 默认分支 / Default branch: `main`
- 主要语言 / Primary language: `project`
- 可见性 / Visibility: `public`
- 仓库类型 / Repository type: `source`

## 本地运行 / Local Run

```bash
git clone https://github.com/siuserxiaowei/miaoji-decon.git
cd miaoji-decon
python3 -m http.server 8000
```

本地验证 / Local validation:

```bash
python3 scripts/validate_repo.py
python3 -m unittest discover -s tests -v
python3 -m compileall .
```

验证某篇准备发布的拆解：

```bash
python3 skills/miaoji-decon/scripts/validate_deconstruction.py path/to/report.md --mode deep
```

## 仓库结构 / Repository Map

| 路径 / Path | 中文说明 | English |
| --- | --- | --- |
| `README.md` | 项目入口说明，先读这里。 | Main project entry point and orientation. |
| `docs` | 文档或 GitHub Pages 输出目录。 | Documentation or GitHub Pages output. |
| `docs/public` | 脱敏公开版复盘页面。 | Public-safe digest pages. |
| `docs/superpowers` | 本次设计与实施计划。 | Design and implementation plans. |
| `skills` | skill 主体、模板与工作流说明。 | Skill files, templates, and workflow references. |
| `scripts` | 仓库静态校验脚本。 | Repository validation scripts. |
| `tests` | 校验脚本的单元测试。 | Unit tests for validation scripts. |
| `.gitignore` | 本地运行与缓存忽略规则。 | Ignore rules for local runtime and cache files. |

## 维护备注 / Maintenance Notes

- 中文：当项目目标、在线入口、运行命令或目录结构变化时，同步更新本说明。
- English: Keep this guide updated when the project purpose, live link, run commands, or structure changes.
- 中文：修改代码、数据或生成页面后，优先运行相关构建、测试或校验命令。
- English: After changing code, data, or generated pages, run the relevant build, test, or validation command.

## 安全与隐私 / Safety & Privacy

- 中文：不要提交 API key、token、密码、cookie、私有链接或内部账号资料。
- English: Do not commit API keys, tokens, passwords, cookies, private URLs, or internal account data.
- 中文：公开 GitHub Pages 前，确认资料已脱敏并允许公开。
- English: Before publishing GitHub Pages output, confirm the material is redacted and cleared for public release.
<!-- SIUSER-REPO-GUIDE:END -->



> 监控飞书妙记 → 把每场会自动拆成一篇**能学到东西的「深度学习复盘」** → 归档到 Obsidian、飞书、并推送 GitHub。

`miaoji-decon` 的产出**不是流水账、不是贴标签归档，而是复盘**——让一个没能在现场充分参与的人，会后能**学到东西、还知道回去 7 天干啥**。道法术器势是分析的尺子（幕后），端到你面前的是能学到东西的人话（台前）。

一句话准则：**读完最重要的不是收藏，是选一个动作在 7 天内验证。**

现在也支持“多来源资料包”：同一场会议的逐字稿、飞书 AI 纪要、腾讯会议总结会先合并为一个来源家族，再做证据分级，不会把三份同源材料误写成三重验证。

它是 [`siuserxiaowei/miaoji-s`](https://github.com/siuserxiaowei/miaoji-s) 的升级版：把通用纪要换成深度学习复盘，并多了 Obsidian + GitHub + Wiki 复利三个出口。

## 一篇复盘的固定结构

```
先说结论                   ← 先给缺席者真正需要的判断
🧾 材料与证据口径          ← 原始/同源/独立/推断，统一时间码
🚦 可信度总览              ← 高/中/低可信，限制过度传播
⏱ 如果只读 10 分钟        ← N 条带走判断，全文最重要一屏
🎯 这篇真正能学什么        ← 这场会练的是什么眼力
🧭 道法术器势(→你可以怎么用) ← 一张表：层 | 本场榨干版 | 动作化的"怎么用"
📚 深挖：N 个知识点         ← 重心。每个三段：是什么 / 为什么重要 / 你能用
🛠 可直接复用的方法        ← 每个含"不要误读成"
📅 7 天作业               ← Day1-7，把"学到"逼成"做到"
🤔 回到自己业务的追问      ← 逼读者迁移到自己身上
👥 关键人物与资源          ← 把"人/关系"变成资源地图
💬 金句                   ← 原话 + 一句"在说什么"
🔎 来源与时间码索引         ← 重要结论能回到原文
⚠️ 来源边界
作者联系                   ← 固定 X / Twitter + 微信号
```

**框架基准（生财有术 / AI破局）**：道以明向、法以立本、术以立策、器以成事、势以察时——道=做对的事，法术器=把事做对，势=何时做。

## 能做什么

- 定时扫描 / 手动处理飞书妙记新录音（去重 + 失败补偿）。
- 支持用户粘贴会议纪要/逐字稿或提供本地文本附件，进入 draft-only 学习复盘模式；没有 Feishu token 时不写 Base/Doc、不 push GitHub。
- 支持多个 URL/文档/会议页面的 `source-pack` 深度拆解，先做来源家族、主张台账、时间码基准和反方审计。
- 快速 / 标准 / 深度三档路由：短材料不套重流程；多来源、高风险或明确要求 20 Agent 时才进入深度档。
- 按场景分类（AI硬件 / 知识 / 人情世故 / 大佬分享 / 饭局闲聊 / 出海 / 自媒体运营）自适应详略。
- 深挖每场会的信息点/知识点，按学习复盘结构组织；严格区分"讲者讲 vs 我引申"、数字带销售口径标存疑、不堆标签噪声、不编造、信息空就少写别注水。
- 多 Agent 任务保存逐个编号与完成/中断/失败/补做状态，不把“已启动”写成“已完成”。
- 每篇拆解强制附作者联系：X / Twitter [`@_HIT_SZ_`](https://x.com/_HIT_SZ_)、微信号 `siuserxiaowei`；漏任一项，发布校验失败。
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
