# Summary Rubric

## Primary Goal

Turn the latest `freshNews.md` into a short but useful Chinese briefing that helps the reader answer:

1. What deserves attention first in this current time window?
2. Which developments are most sensitive or consequential?
3. What matters for markets, tech, China, or geopolitical risk?

## Importance Signals

Score items higher when they involve:

- war, ceasefire, military action, sanctions, diplomacy
- strategic geopolitical developments: export controls, maritime chokepoints, cross-border security shifts, alliance changes
- central government, ministry, regulator, court, or policy actions
- major market impact: oil, FX, rates, commodities, supply chains
- major company events: CEO changes, lawsuits, shutdowns, restructurings
- repeated coverage across multiple sections/sources

## Sensitivity Signals

Treat these as especially sensitive:

- armed conflict and escalation
- China / US / Middle East / Taiwan related developments
- sanctions, export controls, maritime chokepoints, and strategic infrastructure disputes
- public safety or casualty events
- export controls, bans, or regulatory crackdowns
- strategic infrastructure, chips, AI infrastructure, energy chokepoints

## Compression Rules

- Do not list every title one by one if several titles point to the same story cluster.
- Prefer one synthesized bullet instead of repeating similar titles.
- When compressing repeated coverage, preserve the latest status and any meaningful developments over time instead of flattening the story into one static point.
- Separate "important" from merely "new".
- If a section is large but repetitive, summarize the cluster instead of enumerating all items.

## Output Style

- Chinese only.
- Direct, concrete wording.
- Prefer briefing tone over analytical essay tone.
- Avoid exaggerated certainty.
- Do not include links by default.
- Do not include rationale labels such as `为什么重要`.
- Do not include “no update” filler such as “AI 没有新增信号” or “未检出某人推文”.
- Do not foreground source labels like `Reuters World` or `Sina · China News` in the briefing body unless source identity itself is material.
- Default to 5 sections:
  - `当前关注`
  - `地缘政治`
  - `市场`
  - `科技`
  - `其余简报`
- Treat sensitivity as a ranking signal inside `当前关注`; do not force a separate `敏感信号` section unless the user asks for one.
- If geopolitics is weak in the current file, compress or omit the `地缘政治` section instead of writing absence statements.

## Tech Priority

- Always scan explicitly for:
  - AI
  - Apple
  - semiconductors
  - frontier model / infra / platform news
- If the `郭明錤` section has items, they should be summarized rather than silently omitted.
- If tech is weak in the current file, compress or omit the `科技` section instead of writing absence statements.
