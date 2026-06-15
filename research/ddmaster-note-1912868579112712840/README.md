# 洋哥商业心法 · 妙记拆解产物索引

来源：<https://biji.ddmaster.com/note/1912868579112712840>
处理日期：2026-06-15

## 主文件

- `2026-06-15-洋哥商业心法-术法道器势拆解.md`：最终深度拆解与补充分析。
- `normalized-materials.md`：清洗版素材库，包含妙记智能总结原文、逐句文字记录、课堂资料索引与 OCR。
- `source-acquisition.md`：来源采集审计，记录接口定位、授权边界与脱敏处理。

## 原始数据

- `raw-note-detail.json`：笔记详情/智能总结接口返回，已脱敏媒体签名 URL。
- `raw-original.json`：文字记录/课堂资料接口返回，已脱敏媒体签名 URL。
- `raw-children-count.json`：子笔记计数。
- `raw-children.json`：子笔记列表接口返回。
- `fetch-summary.json`：抓取摘要，不包含登录凭据。

## 课堂资料

- `class-materials/images/`：9 张课堂图片本地副本。
- `class-materials/image-index.json`：课堂图片索引。
- `class-materials/ocr-results.json`：OCR 结构化结果。
- `class-materials/ocr-combined.md`：OCR 汇总，质量仅作辅助。

## 安全说明

- 未保存浏览器 token、refresh token、device id。
- 原始接口中的临时签名媒体 URL 已替换为 `[redacted_signed_media_url]`。
- 音频二进制未落库；文字记录已完整保存在 `normalized-materials.md`。
