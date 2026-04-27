---
name: news-briefing
description: Read the latest freshNews or dailyFreshNews file in NewsOfCodex (or a user-provided directory), parse it into structured sections/items, and produce a Chinese briefing. Default to output mode `fileout`, which overwrites `NewsOfCodex/news_briefing/NewsBriefing.md`. Support source execution modes `fresh`, `daily`, and `filein`, plus output modes `fileout` and `chat`.
---

# News Briefing

## Workflow

1. Resolve the source directory.
   - Default:
     `/Users/x/Library/Mobile Documents/iCloud~md~obsidian/Documents/Mind/NewsOfCodex`
   - If the user explicitly gives another directory or file, use that instead.

2. Find the newest file.

```bash
python3 /Users/x/.codex/skills/news-briefing/scripts/find_latest_freshnews.py --dir "<news-dir>" --mode <fresh|daily>
```

- `--mode fresh`（默认）：查找最新 `YYYY-MM-DD-HH-mm_freshNews.md`（当前时段快讯）
- `--mode daily`：查找最新 `dailyFreshNews_YYYY-MM-DD.md`（当日累计）
- 若直接传入 `--file <path>`，则跳过 finder，直接使用该文件
- finder payload 现在还会返回：
  - `mode`
  - `file_name`
  - `execution_time`：本地 `Asia/Shanghai` 时间，格式固定为 `M月D日 H:mm`
  - `execution_timezone`

3. Parse the Markdown into structured JSON.

```bash
python3 /Users/x/.codex/skills/news-briefing/scripts/parse_freshnews.py --file "<freshnews-path>"
```

4. Read [references/summary-rubric.md](references/summary-rubric.md) before writing the summary.

5. Produce a Chinese briefing that is not too long, but still selective and substantive.

6. Output the final result.
- Default output mode is `fileout`.
- `fileout` means: write the full Markdown briefing to
  `/Users/x/Library/Mobile Documents/iCloud~md~obsidian/Documents/Mind/NewsOfCodex/news_briefing/NewsBriefing.md`
  and overwrite the previous file.
- Use `chat` only if the user explicitly asks for direct chat output, current skill output, or no file writing.
- In `fileout` mode, write the complete Markdown through:

```bash
python3 /Users/x/.codex/skills/news-briefing/scripts/write_briefing_file.py
```

- Pass the full Markdown body through stdin.
- In `fileout` mode, reply in chat only with a short write receipt.

## Output Rules

- All outputs must begin with this fixed header block before any news body:

```markdown
## 简报信息
- 执行模式：`fresh`
- 输出模式：`fileout`
- 使用文件：`2026-04-27-00-00_freshNews.md`
- 执行时间：`4月27日 0:39`
```

- Header field rules:
  - `执行模式` must be `fresh`, `daily`, or `filein`
  - `输出模式` must be `fileout` or `chat`
  - `使用文件` must be file name only, never the full path
  - if there is no actual file name because the user pasted content inline, `使用文件` must be `inline-content`
  - `执行时间` must use local `Asia/Shanghai` time in `M月D日 H:mm`
- Use finder-provided `mode`, `file_name`, and `execution_time` when available.
- Default output mode is `fileout`; switch to `chat` only when the user explicitly asks for chat output.
- Fallback rule: if the user directly provides a file without finder payload, set `执行模式` to `filein`, use the provided file name, and generate `执行时间` from the current local `Asia/Shanghai` time.
- Pasted-content fallback: if the user only pastes content and no file name is available, set `执行模式` to `filein`, set `使用文件` to `inline-content`, and generate `执行时间` from the current local `Asia/Shanghai` time.
- In `fileout` mode, the full Markdown must be written to the fixed `NewsBriefing.md` path.
- Ground the summary in parsed `title`, `time`, `url`, `section`, and optional quoted text only.
- Do not invent facts that are not supported by the file.
- Prefer merging duplicate or closely related items across sections into one higher-level point.
- Prioritize sensitivity and importance over chronology-only retelling.
- Ignore empty sections except when they matter for explaining source coverage.
- Keep the briefing reasonably short by default:
  - usually 3-5 current-priority items
  - plus 3-6 supporting bullets
- Do not include links in the final summary unless the user explicitly asks for them.
- Do not include meta explanations such as `为什么重要：...`.
- Treat sensitivity as part of ranking inside `当前关注`; do not force a separate `敏感信号` section unless the user explicitly asks for it.
- Write in briefing tone rather than essay/analysis tone:
  - shorter sentences
  - fewer causal digressions
  - more direct newsroom-style wording
- If a topic bucket has no substantive items, omit it quietly instead of writing that nothing happened.
- Pay explicit attention to geopolitical developments, especially wars, ceasefires, sanctions, diplomacy, export controls, and strategic chokepoints.
- Pay explicit attention to frontier tech topics, especially:
  - AI
  - Apple
  - semiconductors / infra
- If `郭明錤` has any non-empty items in the file, include them in the summary instead of omitting them as low priority.
- If AI, Apple, or `郭明錤` do not have substantive developments in the current file, do not add “no update” filler.
- Keep the briefing focused on the news itself. Do not pad the summary with source names such as `Reuters World` or `Sina · China News` unless the source identity is itself newsworthy.

## Recommended Structure

Use this structure unless the user asks for another format:

```markdown
## 简报信息
- 执行模式：`fresh`
- 输出模式：`fileout`
- 使用文件：`2026-04-27-00-00_freshNews.md`
- 执行时间：`4月27日 0:39`

## 当前关注
- 对当前时段内最重要、最敏感、最值得先看的新闻做 3-5 条综合概括

## 地缘政治
- 战争、停火、军事行动、制裁、外交、出口管制、台海/中东/中美动向，以及能源通道、关键供应链与战略基础设施风险

## 市场
- 宏观、资产价格、油运、汇率、商品、企业交易与市场风险

## 科技
- AI、Apple、半导体、平台产品、关键科技公司动态

## 其余简报
- ...
```

- The fixed header is mandatory and must appear before `## 当前关注`.
- `输出模式` must always appear in the header.
- `当前关注` 不是“今日总结”，而是“这一个 freshNews 时间窗口里最值得先看什么”。
- 地缘类新闻若属于本轮最值得先看的高优先级事项，可进入 `当前关注`；其余可归入 `地缘政治`。
- 如果本轮文件里地缘政治、市场或科技不构成独立板块，可以省略对应区块，直接并入 `当前关注` 或 `其余简报`。
- 如果 `郭明錤` 有推文，优先并入 `科技`，必要时可提升到 `当前关注`。
- 只写“发生了什么”。不要写“没有发生什么”、不要写“本轮未检出”、不要为了凑板块去补说明性空话。

## Interpretation Guidance

- Treat war, sanctions, diplomacy, regulation, macro shocks, public safety, and major corporate leadership/legal events as higher sensitivity.
- Put war, ceasefire, military action, sanctions, diplomacy, export controls, cross-strait developments, Middle East tensions, maritime chokepoint risks, and strategic infrastructure disputes under `地缘政治` unless they are more urgent as `当前关注`.
- Do not put ordinary elections, cabinet reshuffles, party politics, or domestic legislative maneuvering under `地缘政治` unless they materially affect international alignment, security, or cross-border policy.
- If several items describe the same event from different sources, synthesize once and mention that multiple sources echoed it.
- Write in briefing language, not commentary language.
- Prefer concrete event summaries over source-by-source recitation.
