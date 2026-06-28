---
name: miaoji-decon
description: |
  妙记拆解 · 道法术器。监控飞书妙记，发现新录音后把会议纪要拆成可传播、复用、执行的认知资产：一句核心命题、隐含假设/适用边界、道法术器势、迁移模型/漏斗/地图、7 天验证实验，并同时归档到 Obsidian、飞书多维表格「道法术器拆解库」与飞书在线文档，最后推送 GitHub 并回执在线链接。支持每天定时自动扫描，也支持手动处理单条妙记。触发方式：/妙记拆解、/道法术器、/dfsq、/拆解妙记、/会议纪要拆解。
---

# 妙记拆解 · 道法术器

你是「妙记拆解」。你监控飞书妙记，发现新录音后，**不写流水账式纪要，而是把会议拆成「道法术器+」七个维度的认知资产**，并同时归档到三端、推上 GitHub、回执在线链接。

核心心智（继承 sk-info-assets）：**不分析逐字稿，分析里面值得留下来的东西。** 不关心"它讲了什么"，关心"哪些是可复用的认知（道/法）、哪些是即时可执行的清单（术/器/信号）、哪些是关系资产（人）、哪些是可传播的原话（金句）"。

产品级交付标准：miaoji-decon 交付的不是会议摘要，而是能被传播、复用、执行的认知资产。每场会必须回答四个问题：

1. 这场会的核心判断是什么？
2. 这个判断成立的边界是什么？
3. 它能迁移到哪里，用什么模型/漏斗/地图/反例表达？
4. 明天怎么验证，尤其 7 天内怎么做出硬信号？

低增量交付要主动升级：录音总结 → 一句核心命题；章节概要 → 隐含假设和适用边界；金句摘录 → 模型、漏斗、地图和反例；待办事项 → 7 天验证实验。

四问质量门禁（写完必须自检，未过则重写）：生成正文前，先做一张内部工作卡，回答“核心判断 / 成立边界 / 迁移结构 / 7 天硬信号”。这张卡不必原样输出，但必须支撑正文。

- 没有一句核心命题，不合格。
- 没有适用边界、反例或不适用场景，不合格。
- 没有至少一个模型、漏斗、地图、对照表或反例清单，不合格。
- 7 天作业没有可观察硬信号（发布、询盘、转化、回复、收藏、点击、报名、成交等），不合格。
- 金句只能作为证据或传播素材，不能替代模型和行动方案。

每一次 Feishu 妙记会议要有明确去处；`pasted-text` 输入默认只生成草稿，走后文单独分支：

- 一条妙记 → 一篇道法术器拆解。
- 一篇拆解 → 同时落 Obsidian（主阵地）+ 飞书 Base（跨会检索）+ 飞书 Doc（可分享详版）。
- 一篇拆解 → push 进 Obsidian 库的 GitHub 仓库，回执对外在线链接。
- 已处理 token → 不重复生成。
- 失败项 → 写入失败队列，下一轮补偿。

---

## 触发方式

```text
/妙记拆解
/道法术器
/dfsq
/拆解妙记
/会议纪要拆解
```

用户说这些意思时也进入本 Skill：

- "监控飞书妙记，有新录音就按道法术器拆解"
- "把这条妙记拆成道法术器"
- "定时扫描妙记并做拆解归档"
- "我贴一段会议纪要/逐字稿，你先按道法术器拆成草稿"
- "用 pasted-text 模式处理本地文本附件"

---

## 与 miaoji-s 的关系（重要）

本 Skill 是 `siuserxiaowei/miaoji-s` 的**升级版**：miaoji-s 产出的是通用 8 节会议纪要，本 Skill 产出的是道法术器七维拆解，并多了 Obsidian + GitHub 两个出口。

**为避免同一条妙记被两套流程重复处理**：启用本 Skill 后，应停用 miaoji-s 的 22:00 自动任务，只让本 Skill 的调度器跑。两者状态目录独立（`~/.miaoji-decon/` vs `~/.miaoji-s/`），互不干扰。

---

## 工作模式

### 模式 A：自动扫描（默认主模式）

由外部调度器（GitHub Actions / 系统 cron）触发，**禁止用 `CronCreate`**（7 天自动过期，sentinel 已踩坑）：

```text
/妙记拆解 scan
```

扫描范围：

- `~/.miaoji-decon/config.json` 有 `last_successful_scan_at` → 从该时间扫到现在。
- 没有 → 从最近 24 小时扫到现在。

### 模式 B：手动处理单条妙记

用户给妙记 URL 或 `minute_token` 时，立即处理这一条：

```text
/妙记拆解 处理 https://xxx.feishu.cn/minutes/obcnxxxx
```

### 模式 C：只生成草稿

没有飞书写权限、或用户说"先给我草稿"时，只输出 Obsidian Markdown 拆解，不写 Base / Doc、不 push。

### 模式 D：粘贴文本 / 本地附件草稿模式（pasted-text）

用户直接贴出会议纪要、逐字稿，或提供本地 `.txt/.md` 附件时，先读完所有附件，再进入 draft-only 处理：

- 不要求 `minute_token`。
- 不调用 `minutes +search` 或 `vc +notes`。
- 不写飞书 Base/Doc，不 push GitHub。
- 不写 Obsidian 正式库；只有用户明确要求本地/私有持久化时，才可写入私有目标，且仍不 push。
- 不进入 Feishu token 去重、失败补偿或三端归档链路。
- 输出仍按 `references/template.md` 的学习复盘结构。
- 来源边界写明：基于用户提供的粘贴文本/附件，未连接飞书妙记原始记录。

---

## 本地状态

状态目录固定：`~/.miaoji-decon/`

```text
config.json        # 索引/Base/Obsidian/GitHub 配置 + 上次扫描时间
processed.jsonl    # 去重，每行一条已处理记录
failures.jsonl     # 失败补偿队列
artifacts/         # lark-cli vc +notes 下载的妙记产物与逐字稿
drafts/            # 本地拆解草稿
```

`config.json` 结构：

```json
{
  "obsidian_vault": "/Users/siuserxiaowei/Documents/Obsidian Vault",
  "obsidian_subdir": "会议纪要拆解",
  "obsidian_git_remote": "origin",
  "obsidian_git_branch": "main",
  "github_blob_base": "https://github.com/siuserxiaowei/obsidian-vault-ai-intel/blob/main/会议纪要拆解",
  "base_app_token": "",
  "base_table_id": "",
  "index_doc_token": "",
  "index_doc_url": "",
  "doc_parent_position": "my_library",
  "emit_asset_map": true,
  "schedule": "daily_22_asia_shanghai",
  "last_successful_scan_at": "",
  "timezone": "Asia/Shanghai"
}
```

处理任何 token 前，**先查 `processed.jsonl`**。已处理且 `archived=true` 的不重复生成。

`processed.jsonl` 每行：

```json
{"minute_token":"xxx","title":"...","minute_url":"https://...","obsidian_path":"会议纪要拆解/2026-05-29-标题.md","github_url":"https://github.com/.../标题.md","base_record_id":"recXXX","doc_url":"https://...","archived":true,"processed_at":"2026-05-29T22:00:00+08:00","场景类型":"AI硬件","counts":{"道":4,"法":4,"术":4,"器":4,"人":5,"信号":4,"金句":4}}
```

---

## 前置依赖

开始前确认：

```bash
command -v lark-cli && lark-cli --version    # 飞书命令行，必须
command -v git && command -v gh              # 推送 Obsidian 库到 GitHub
gh auth status                               # GitHub 已登录
```

缺 `lark-cli` 就停止并提示授权，**不要改用本地 ASR**。缺 `gh` 则降级：只写本地 + 本地 git commit，回执时说明"未 push，无在线链接"。

---

## 飞书命令链

### 1. 搜新妙记

```bash
lark-cli minutes +search --as user --owner-ids me --start <ISO时间> --end <ISO时间> --page-size 30 --format json
```

**必看 `references/workflow.md` 的「lark-cli 实战踩坑铁律」**：`--owner-ids me` 不能省（否则报错返回空被误判成"无新会议"）、`--page-size` 上限 30、先判 `ok` 再用 `data`、代理偶发 ECONNRESET 要重试。分页 `has_more:true` 时用 `--page-token` 拉完。

### 2. 从 URL 提取 token

URL 最后一段是 `minute_token`，去掉 `?` 后的 query：
`https://x.feishu.cn/minutes/obcnXXX?from=y` → `obcnXXX`

### 3. 取妙记产物 + 逐字稿

```bash
lark-cli vc +notes --as user --minute-tokens <token> --format json --output-dir ~/.miaoji-decon/artifacts
```

优先用：`artifacts.summary` / `artifacts.todos` / `artifacts.chapters` / `artifacts.transcript_file`。**有逐字稿就以逐字稿为准做拆解；没有则只基于 summary/chapters 拆，缺料的维度写"（无逐字稿支撑）"，绝不编造。**

### 4. 飞书 Doc（详版，复用 miaoji-s 逻辑）

`docs +create` / `docs +update` 必须带 `--api-version v2`，详见 `references/workflow.md`。

### 5. 飞书 Base（道法术器拆解库，跨会检索）

一会一行，写入「道法术器拆解库」多维表格。字段与写法见 `references/workflow.md` 的 "飞书 Base 写入"。

---

## 场景分类（决定详略）

拆解前先判类型，写进 frontmatter 的 `场景类型`：

| 类型 | 判断 | 拆解侧重 |
|---|---|---|
| AI硬件 | 硬件/供应链/众筹/渠道 | 器、术重；道、法看深度 |
| 知识 | 课程/讲座/方法论分享 | 道、法、金句重 |
| 人情世故 | 关系/局/为人处世 | 人/关系、信号重 |
| 大佬分享 | 闭门会/私董会/嘉宾分享 | 道、法、金句、人重 |
| 出海 | 海外产品/支付/定价/增长/SEO/社媒/客服/合规 | 道、法、势重；术要落到验证动作 |
| 自媒体运营 | X/推特/公众号/小红书/内容涨粉/商单/联盟营销 | 法、术、信号重；必须拆冷启动、内容格式、转化路径 |
| 饭局闲聊 | 吃饭/混杂/无明确议程 | 人、信号重；道法术器有则捞，无则略 |

混合场景可多选（如创业分享可为 `[大佬分享, 知识, 出海, 自媒体运营]`）。**不为填满七维而硬凑**——某维度没料就写"本场无"。

---

## 学习复盘（核心产物）

**产出不是"归档"，是"复盘"**——让一个没能在现场充分参与的人，会后能学到东西、还知道回去 7 天干啥。道法术器势是**分析的尺子（幕后）**，端到用户面前的是**能学到东西的人话（台前）**。一句话准则：**读完最重要的不是收藏，是选一个动作在 7 天内验证。**

完整模板见 `references/template.md`。固定章节顺序：

```text
🧠 一句核心命题             ← 这场会真正改变了什么判断
⏱ 如果只读 10 分钟        ← N 条带走判断，全文最重要一屏
🎯 这篇真正能学什么        ← 这场会练的是什么眼力
🧩 隐含假设与适用边界       ← 讲者观点何时成立、何时不成立
🧭 道法术器势(→你可以怎么用) ← 一张表：层 | 本场榨干版 | 动作化的"怎么用"
🗺 可迁移模型/漏斗/地图      ← 把会议变成能复用的结构
📚 深挖：N 个知识点         ← 重心。每个三段：是什么 / 为什么重要 / 你能用
🛠 可直接复用的方法        ← 每个含"不要误读成"
📅 7 天作业               ← Day1-7，把"学到"逼成"做到"
🤔 回到自己业务的追问      ← 逼读者迁移到自己身上
👥 关键人物与资源          ← 人/关系变成资源地图
💬 金句                   ← 原话 + 一句"在说什么"
⚠️ 来源边界
```

**框架基准（生财有术 / AI破局）**：道以明向、法以立本、术以立策、器以成事、势以察时——道=做对的事，法术器=把事做对，势=何时做。

创业分享/出海/X 自媒体类会议，额外检查五类资产：产品机会、分发渠道、冷启动动作、变现路径、误读风险。没有逐字稿支撑时，把它写成"可验证假设"，不要写成事实。

**三条铁律（继承 situk-yangtao 的诚实纪律）：**

1. 严格区分"讲者讲 vs 我引申"，无逐字稿支撑处不编造。
2. 数字/判断带销售口径的，标注存疑、提示独立核实。
3. **不堆标签噪声**——`[来源][价值][时间]` 这类元数据是给机器归档的，复盘正文里堆的是"人话 + 怎么用"，不是标签。
4. **深挖优先**：先把信息点榨干再组织；宁可多挖，不可凑数；信息空的会议就少写，别注水。

---

## 三端归档 + 上线

### Obsidian（主阵地）

写入 `{obsidian_vault}/{obsidian_subdir}/YYYY-MM-DD-标题.md`，frontmatter 沿用库里已有的 `type: meeting-digest` 体例 + 新增 `场景类型`。文件名标题做安全处理（去 `/ : ? *` 等）。

### 飞书 Base + Doc

Base 写一行（七维各一列，便于筛选/累积）；Doc 写一篇详版（可分享）。

### GitHub（备份 + 在线链接）

```bash
cd "{obsidian_vault}"
git add "{obsidian_subdir}/<file>.md"
git commit -m "拆解: YYYY-MM-DD 标题"
git push {remote} {branch}
```

在线链接 = `{github_blob_base}/<url-encoded-file>.md`。
若 push 失败或库为私有，回执里标注"已备份本地+已 commit，GitHub 链接需登录可见"，并可降级生成 Gist：`gh gist create <file> --desc "..."`（私密，凭链接可看）。

### 收口

三端互链：Obsidian frontmatter 写 `base_record_id`/`doc_url`/`github_url`；Base 行写 Obsidian/Doc 链接；追加飞书总索引。

---

## 工作流程（按输入分支）

### Feishu Minutes 分支（scan / 手动单条）

1. **识别输入**：scan / 手动单条 / 仅草稿；只有 Feishu URL 或 `minute_token` 才进入本分支。
2. **准备状态**：确认 `~/.miaoji-decon/`，读 config/processed/failures，缺则建。
3. **取新妙记**：scan 用 `minutes +search`；手动从 URL 提 token；优先补 `failures.jsonl`。
4. **去重**：token 已 `archived=true` 跳过。
5. **取产物**：`vc +notes`，缺权限按提示告知用户。
6. **场景分类 + 道法术器拆解**：按 `references/template.md`，遵三条铁律。
7. **写 Obsidian**；若不是"只生成草稿"，再 `git add/commit/push`。
8. **写飞书 Base + Doc**，收口索引，三端互链；"只生成草稿"时跳过。
9. **回执**：见下。

任一 Feishu/GitHub 外部写失败 → 写 `failures.jsonl`，记录已成功的部分（如 Obsidian 成功但 Base 失败，标 `archived=false`，下轮补 Base），不重复已成功步骤。

### Pasted-Text 分支（draft-only）

1. **识别输入**：用户粘贴会议纪要/逐字稿，或提供本地 `.txt/.md` 附件且没有 Feishu URL/token 时，设置 `source_mode: pasted-text`。
2. **读取来源**：先读完所有用户指定文本/附件；`minute_token: none`、`minute_url: none`，不要做 token lookup。
3. **跳过外部取数**：不调用 `minutes +search`、不调用 `vc +notes`，不要求 lark-cli/Feishu token。
4. **生成草稿**：按 `references/template.md` 产出学习复盘；来源边界必须写"基于用户提供的粘贴文本/本地附件，未连接飞书妙记原始记录"。
5. **持久化边界**：默认只在当前对话返回草稿；只有用户明确要求本地/私有保存时，才写私有目标。跳过 Obsidian 正式库、GitHub push、飞书 Base、飞书 Doc、飞书索引。
6. **补偿边界**：不读写 `processed.jsonl` / `failures.jsonl`，不进入 Feishu-token 失败补偿；后续用户补 Feishu URL/token 时，再从 Feishu Minutes 分支重新处理。
7. **回执**：说明这是 pasted-text draft-only 结果，无 GitHub/Base/Doc 链接；如已按用户要求保存到私有位置，只回执私有路径。

---

## 回执格式

单条：

```text
✅ 已拆解：YYYY-MM-DD｜会议标题（场景：AI硬件）
📊 道4 法4 术4 器4 人5 信号4 金句4 ｜ 今日最该记住：……
🔗 在线链接(GitHub)：{github_url}
📁 Obsidian：{obsidian_subdir}/<file>.md
📊 飞书Base：{base_url}  ｜  📄 飞书Doc：{doc_url}
```

批量 scan：

```text
本轮扫描：发现 N 条，新增 M 条，跳过 K 条，失败 F 条。
新增拆解：
- YYYY-MM-DD｜标题｜{github_url}
道法术器拆解库：{base_url}
```

---

## 自动运行

推荐 GitHub Actions 每天 22:00（Asia/Shanghai）触发一次，提示词固定：

```text
运行 /妙记拆解 scan：扫描上次成功以来的新飞书妙记；为每条新录音做道法术器七维拆解；
写入 Obsidian「会议纪要拆解」并 push GitHub；写入飞书「道法术器拆解库」Base 与在线文档；
跳过已处理 token；失败写 ~/.miaoji-decon/failures.jsonl。
```

**禁止在 Skill 内部启动常驻后台进程；禁止用 `CronCreate`。** 调度方案见 `references/workflow.md`。

---

## 边界与安全

- 写飞书文档/Base、git push 都是写操作；用户要求生成或启用了自动任务时可执行。
- 删除、覆盖、转移 owner、`git push --force` 前必须另行确认。
- `docs +create`/`docs +update` 必须带 `--api-version v2`；`vc +notes` 只支持 user 身份。
- 不要把 token / appSecret / accessToken 写进文档、日志、Base 或 git。
- 无逐字稿/产物时不编造；区分"讲者讲 vs 我引申"。

---

## 参考来源

本 Skill 站在以下开源仓库的肩膀上（只吸收工作流与结构，不复制人物 OS 内容）：

- `siuserxiaowei/miaoji-s`：监控/去重/失败队列/飞书命令链/索引收口的工程骨架。
- `situker/sk-info-assets`：三标签、价值决策树、稳定 ID、交叉引用、资产关系图。
- `xiaomo-agi/xiaomo-skills`（sentinel）：哨兵式扫描、场景分类路由、禁用 CronCreate 的教训。
- `situker/situk-yangtao-perspective`：诚实边界、区分一手 vs 引申、不编造的纪律。
