# 工作流细节：飞书命令、Base 写入、Obsidian、GitHub、调度

## ⚠️ lark-cli 实战踩坑铁律（血泪，务必照做）

这些坑会让扫描**静默失败**（返回空被误判成"无新会议"），是实跑中踩出来的：

- **`minutes +search` 必须带 `--owner-ids me`**。不带会返回 `ok:false` + 空 `data`，看起来像"没有新妙记"，其实是参数错误。
- **`--page-size` 最大 30**。实际命令写 `--page-size 30`；传 50/100 直接 validation 失败、空返回。分页用 `--page-token`，`has_more:true` 就继续拉。
- **先判 `ok` 再用 `data`**。`ok:false` 时读 `error.message`，别把错误当"无结果"。
- **按时间窗口搜会漏**："内容旧但最近才上传"的妙记，其 `start_time` 是旧的，窗口搜不到；要么放宽窗口，要么靠 `processed.jsonl` 去重后处理 owner 全量。
- **代理偶发 ECONNRESET**：经本机代理（如 Clash）时 search/notes 会偶发连接中断；同一命令最多重试 3 次。
- **`--output-dir` / `docs --content` 要相对路径**：报"must be a relative path within the current directory"时，先 `cd` 到目标目录再用 `--output-dir .`，或用 stdin。
- **lark-cli 依赖 node**：node 缺失时 lark-cli 直接 `env: node: No such file or directory`。定时脚本应先 `command -v node` 自检；缺了就 `brew install node`。
- **逐字稿可能为空**：妙记刚生成时转写可能还没好，`vc +notes` 拿到空逐字稿。这时**不要写空复盘文件**，把 token 记进 `processed.jsonl` 标 `archived:false`（下轮可重试），跳过。

## 粘贴文本 / 本地附件输入（pasted text）

当输入来自用户粘贴文本或本地 `.txt/.md` 附件，而不是飞书 URL/token：

1. 先读完所有用户指定文件。
2. 将文件名、录音日期、会议主题写入草稿 frontmatter；没有的信息写 `unknown`，不要猜；`source_mode: pasted-text`、`minute_token: none`、`minute_url: none`。
3. 跳过 token lookup、`minutes +search`、`vc +notes`；不需要 lark-cli/Feishu token。
4. 跳过 Base、Doc、GitHub push；换句话说，pasted text 是 **no Base/Doc/GitHub push** 的 draft-only 路径。
5. 不写 Obsidian 正式库；只有用户明确要求本地/私有持久化时，才写私有目标，且不 push。
6. 只生成 draft-only 学习复盘，并在 `⚠️ 来源边界` 写明“基于用户提供文本/本地附件，未连接飞书原始妙记”。
7. 不把原始粘贴文本、附件正文或 draft-only 复盘提交到公开仓库。
8. 不进入 `failures.jsonl` 的 Feishu-token 补偿队列；如果后续用户补充 Feishu URL/token，再按手动单条妙记流程补齐三端归档。

## 多来源资料包（source pack）

当用户一次提供多份会议链接、文档、论文、网页或本地附件：

1. 先列材料清单与读取状态；读取失败要显式报告。
2. 按 `evidence-protocol.md` 合并来源家族。同场会议的逐字稿、AI 纪要和不同平台总结不能当三重验证。
3. 统一时间码基准，记录其他平台偏移和转写歧义。
4. 默认 draft-only；只有用户明确要求保存或发布，才写目标系统。
5. 用户要求多 Agent 时，保留编号、角色、完成状态与补做关系；不能把启动当完成。
6. 在任何写入前追加 `assets/author-profile.json` 中的 X / Twitter 和微信号，并运行 `scripts/validate_deconstruction.py`。

公开发布前必须再检查：材料是否允许公开、真实人名/客户/业务数据是否脱敏、原始逐字稿是否被意外带入、联系方式是否准确可见。

## 飞书 Doc（详版，复用 miaoji-s 逻辑）

创建到个人云空间（或 config 的 `doc_parent_position`）：

```bash
lark-cli docs +create --api-version v2 --as user --parent-position my_library \
  --content '<title>YYYY-MM-DD｜会议标题｜道法术器拆解</title>...'
```

长文先建标题骨架，再 `docs +update --command append` 分段追加，避免一次性 content 过长。
追加总索引（若 config 有 `index_doc_token`）：

```bash
lark-cli docs +update --api-version v2 --as user --doc <index_doc_token> --command append \
  --content '<h2>YYYY-MM-DD｜标题</h2><p><a href="DOC_URL">详版</a>｜<a href="GITHUB_URL">Obsidian</a>｜<a href="MINUTE_URL">妙记</a></p>'
```

## 飞书 Base 写入（道法术器拆解库）

首次运行若 config 无 `base_app_token`，创建一张多维表格并记下 token/table_id 到 config。
表「道法术器拆解库」建议字段：

| 字段 | 类型 | 说明 |
|---|---|---|
| 会议标题 | 文本 | |
| 日期 | 日期 | |
| 场景类型 | 多选 | AI硬件/知识/人情世故/大佬分享/饭局闲聊/出海/自媒体运营 |
| 道 | 多行文本 | D-* 条目摘要 |
| 法 | 多行文本 | F-* |
| 术 | 多行文本 | S-* |
| 器 | 多行文本 | Q-* |
| 人/关系 | 多行文本 | P-* |
| 信号/钩子 | 多行文本 | X-* |
| 金句 | 多行文本 | Y-* |
| 今日最该记住 | 文本 | 看板那句 |
| Obsidian链接 | 超链接 | github_url |
| 飞书文档 | 超链接 | doc_url |
| 妙记链接 | 超链接 | minute_url |

每会写一行（用 lark-cli base 的记录写入命令，具体子命令以 `lark-cli base --help` 为准）。
把返回的 `record_id` 回填 processed.jsonl 与 Obsidian frontmatter。

> 每列只放该维度的**摘要**（标题 + 一句话），完整内容在 Obsidian/Doc。Base 是索引和筛选层，不是全文层。

## Obsidian 写入

1. 路径：`{obsidian_vault}/{obsidian_subdir}/{date}-{safe_title}.md`
   - `safe_title`：标题去掉 `/ \ : * ? " < > |`，空格保留或换 `-`。
2. frontmatter 沿用库里已有 `type: meeting-digest` 体例，新增 `场景类型` 与三端链接字段。
3. 正文按 `template.md`，并从 `assets/author-profile.json` 追加固定作者联系。
4. 写完运行 `python3 scripts/validate_deconstruction.py "{file}" --mode standard`；深度档改用 `--mode deep`。
5. 做幂等检查：同名文件已存在且 processed 标 archived → 跳过或按用户要求覆盖。

## GitHub push + 在线链接

```bash
cd "{obsidian_vault}"
git add "{obsidian_subdir}/{file}.md"
git commit -m "拆解: {date} {title}"
git push {remote} {branch}
```

在线链接（URL-encode 中文路径）：
`{github_blob_base}/{url-encoded-file}.md`

降级策略：
- `gh` 未登录或 push 失败 → 本地 commit 即可，回执标注未上线。
- 库为私有、需要公开可看的链接 → `gh gist create "{file}" --desc "{date} {title} 道法术器拆解"`，用 gist 链接（私密 gist 凭链接可看）。

## 调度（禁用 CronCreate）

**方案 A：GitHub Actions（推荐）**
在某个仓库放 `.github/workflows/decon.yml`，`cron: "0 14 * * *"`（UTC 14:00 = Asia/Shanghai 22:00），用 Claude Code / Codex CLI 执行 scan 提示词。需要在 runner 上具备 lark-cli 授权与库写权限——若 runner 无本地授权，改用方案 B。

**方案 B：本机 launchd / cron（最简单，推荐本地用户）**
macOS 用 launchd 每天 22:00 调用 Claude Code CLI 跑 scan 提示词。因为 lark-cli 授权、Obsidian 库、gh 登录都在本机，最省事。

**方案 C：复用 miaoji-s 已有调度器**
若已有 miaoji-s 的 22:00 调度，把其提示词替换为本 Skill 的 scan 提示词，并停用 miaoji-s 自身，避免重复处理。

## 失败补偿

`failures.jsonl` 每行记录 `{minute_token, stage, error, partial:{obsidian:true,base:false,doc:false,github:false}, retry_after:"next_scan"}`。
下轮扫描优先读 failures，只补未完成的 stage，不重复已成功步骤。
