# 妙记拆解 · 道法术器

> 监控飞书妙记 → 把会议纪要拆成「道·法·术·器·人/关系·信号/钩子·金句」七维认知资产 → 同时归档到 Obsidian、飞书多维表格、飞书在线文档 → 推送 GitHub 并回执在线链接。

`miaoji-decon` 不写流水账式纪要，而是用「道法术器」这把筛子，把每场会里**可复用的认知（道/法）、即时可执行的清单（术/器/信号）、关系资产（人）、可传播的原话（金句）** 全部捞出来，沉淀成可回查、可检索、可分发的资产。

它是 [`siuserxiaowei/miaoji-s`](https://github.com/siuserxiaowei/miaoji-s) 的升级版：把通用 8 节纪要换成道法术器七维拆解，并多了 Obsidian + GitHub 两个出口。

## 能做什么

- 定时扫描 / 手动处理飞书妙记新录音（去重 + 失败补偿）。
- 按场景分类（AI硬件 / 知识 / 人情世故 / 大佬分享 / 饭局闲聊）自适应详略。
- 道法术器七维拆解，每条带三标签（来源/价值/时间）+ 稳定 ID + 交叉引用，价值评级走三步决策树，严格区分"讲者讲 vs 我引申"、不编造。
- 三端归档：Obsidian「会议纪要拆解」+ 飞书「道法术器拆解库」多维表格 + 飞书在线文档，三向互链。
- push 进 Obsidian 库的 GitHub 仓库，回执对外在线链接。

## 七维

| 维度 | 回答 | 收什么 |
|---|---|---|
| 🌌 道 | 为什么/本质 | 底层判断、规律、核心概念 |
| 🧭 法 | 什么思路 | 策略、可迁移方法论、商业模式 |
| 🛠 术 | 怎么做 | 具体动作、技巧、SOP、打法 |
| 🧰 器 | 用什么 | 工具、资源、数据、人脉渠道 |
| 👤 人/关系 | 谁/立场 | 谁说的、潜台词、对我的意义 |
| 📡 信号/钩子 | 追什么 | 值得追的线索 + 待办 |
| 💬 金句 | 留哪句 | 讲者原话（保留措辞） |

口诀：**道是方向，法是路线，术是车技，器是车；人是同路人，信号是路标，金句是沿途的碑。**

## 安装

```bash
npx -y skills add siuserxiaowei/miaoji-decon -g --skill miaoji-decon -y --full-depth
```

装完重启 Codex / Claude Code。

## 触发方式

```text
/妙记拆解
/道法术器
/dfsq
/拆解妙记
/会议纪要拆解
```

手动处理一条：

```text
/妙记拆解 处理 https://xxx.feishu.cn/minutes/obcnXXXX
```

自动扫描：

```text
/妙记拆解 scan
```

## 运行依赖

- `lark-cli`（飞书命令行，已授权）—— 读妙记、写飞书文档/Base。
- `git` + `gh`（已登录）—— push Obsidian 库、生成在线链接。
- 一个本地 Obsidian 库（其本身是 git 仓库，远程指向 GitHub）。

## 本地状态

`~/.miaoji-decon/`：`config.json`（配置 + 上次扫描时间）、`processed.jsonl`（去重）、`failures.jsonl`（失败补偿）、`artifacts/`、`drafts/`。

## 一篇拆解长什么样

见 [`skills/miaoji-decon/examples/sample-AI硬件午餐会.md`](skills/miaoji-decon/examples/sample-AI硬件午餐会.md) —— 一场 2 小时的智能硬件午餐会，飞书原 AI 摘要把它整成了"客户购车情况"，道法术器拆解则捞出了品牌护城河打法、AI token 采购决策、玄学命理变现漏斗、698元×800台预售未发货的现金流雷。

## 参考来源

- [`siuserxiaowei/miaoji-s`](https://github.com/siuserxiaowei/miaoji-s)：工程骨架（监控/去重/失败队列/索引收口）。
- [`situker/sk-info-assets`](https://github.com/situker/sk-info-assets)：三标签、价值决策树、稳定 ID、交叉引用。
- [`xiaomo-agi/xiaomo-skills`](https://github.com/xiaomo-agi/xiaomo-skills)：哨兵扫描、场景分类、禁用 CronCreate 的教训。
- [`situker/situk-yangtao-perspective`](https://github.com/situker/situk-yangtao-perspective)：诚实边界、不编造、区分一手 vs 引申。

只吸收工作流与结构思路，不复制大段内容。
