---
name: news-briefing
description: Read the latest freshNews or dailyFreshNews file in NewsOfCodex (or a user-provided directory), parse it into structured sections/items, and produce a not-too-long Chinese briefing that prioritizes importance and sensitivity without flattening everything into a timeline. Use --mode fresh (default) for current-period briefings, or --mode daily for same-day cumulative briefings. Supports both new (dailyFreshNews_YYYY-MM-DD.md) and legacy (YYYY-MM-DD_dailyFreshNews.md) naming. Use --file to bypass the finder and read a specific file directly.
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
  - 同时兼容旧命名 `YYYY-MM-DD_dailyFreshNews.md`
  - 同日新旧并存时，优先新命名
- 若直接传入 `--file <path>`，则跳过 finder，直接使用该文件

3. Parse the Markdown into structured JSON.

```bash
python3 /Users/x/.codex/skills/news-briefing/scripts/parse_freshnews.py --file "<freshnews-path>"
```

4. Read [references/summary-rubric.md](references/summary-rubric.md) before writing the summary.

5. Produce a Chinese briefing that is not too long, but still selective and substantive.

## Output Rules

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
## 当前关注
- 对当前时段内最重要、最敏感、最值得先看的新闻做 3-5 条综合概括

## 市场
- 宏观、资产价格、油运、汇率、商品、企业交易与市场风险

## 科技
- AI、Apple、半导体、平台产品、关键科技公司动态

## 其余简报
- ...
```

- `当前关注` 不是“今日总结”，而是“这一个 freshNews 时间窗口里最值得先看什么”。
- 如果本轮文件里市场或科技不构成独立板块，可以省略对应区块，直接并入 `其余简报`。
- 如果 `郭明錤` 有推文，优先并入 `科技`，必要时可提升到 `当前关注`。
- 只写“发生了什么”。不要写“没有发生什么”、不要写“本轮未检出”、不要为了凑板块去补说明性空话。

## Interpretation Guidance

- Treat war, sanctions, diplomacy, regulation, macro shocks, public safety, and major corporate leadership/legal events as higher sensitivity.
- If several items describe the same event from different sources, synthesize once and mention that multiple sources echoed it.
- Write in briefing language, not commentary language.
- Prefer concrete event summaries over source-by-source recitation.
