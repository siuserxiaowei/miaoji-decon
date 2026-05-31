# 工作流细节：飞书命令、Base 写入、Obsidian、GitHub、调度

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
| 场景类型 | 多选 | AI硬件/知识/人情世故/大佬分享/饭局闲聊 |
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
3. 正文按 `template.md`。
4. 写完做幂等检查：同名文件已存在且 processed 标 archived → 跳过或按用户要求覆盖。

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
