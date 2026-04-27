# news-briefing

`news-briefing` 是一个用于生成中文新闻简报的 Codex skill。

它会读取最新的 `freshNews` 或 `dailyFreshNews` Markdown 文件，解析其中的分区与条目，再输出一版偏编辑式、不过度冗长的中文简报。

## 能做什么

- 自动定位最新新闻文件
- 兼容 `fresh` 与 `daily` 两种模式
- 支持新旧两种 `dailyFreshNews` 文件命名
- 将 Markdown 解析为结构化 JSON
- 生成更偏“简报”而不是“长文分析”的中文摘要
- 在正文前强制输出固定头部信息
- 对 AI、Apple、半导体、基础设施和 `郭明錤` 相关内容做显式关注

## 目录结构

- `SKILL.md`：skill 定义、工作流与输出规则
- `scripts/find_latest_freshnews.py`：查找最新新闻文件
- `scripts/parse_freshnews.py`：解析新闻 Markdown
- `references/summary-rubric.md`：摘要写作 rubric
- `agents/openai.yaml`：agent 界面配置

## 默认新闻目录

默认读取：

```text
/Users/x/Library/Mobile Documents/iCloud~md~obsidian/Documents/Mind/NewsOfCodex
```

如果调用方显式传入其他目录或文件，则应以用户指定路径为准。

## 用法

查找最新时段快讯：

```bash
python3 scripts/find_latest_freshnews.py --dir "<news-dir>" --mode fresh
```

查找最新当日累计：

```bash
python3 scripts/find_latest_freshnews.py --dir "<news-dir>" --mode daily
```

直接指定文件：

```bash
python3 scripts/find_latest_freshnews.py --dir "<news-dir>" --file "<freshnews-path>"
```

解析 Markdown：

```bash
python3 scripts/parse_freshnews.py --file "<freshnews-path>"
```

## 推荐工作流

1. 先定位最新 `freshNews` 或 `dailyFreshNews` 文件
2. 再把 Markdown 解析成结构化数据
3. 阅读 `references/summary-rubric.md`
4. 按 `SKILL.md` 的规则输出中文简报

## 固定头部

所有输出都必须在正文前加上这一段：

```md
## 简报信息
- 执行模式：`fresh`
- 使用文件：`2026-04-27-00-00_freshNews.md`
- 执行时间：`4月27日 0:39`
```

字段说明：
- `执行模式`：`fresh` / `daily` / `file`
- `使用文件`：只写文件名，不写完整路径
- 如果用户只是直接粘贴内容、没有文件名，`使用文件` 固定写 `inline-content`
- `执行时间`：生成这份简报时的本地时间，时区固定 `Asia/Shanghai`，格式固定 `M月D日 H:mm`

说明：
- `执行时间` 不是新闻发布时间
- `执行时间` 不是源文件名里的时间片段
- 正文区块仍从 `## 当前关注` 开始，不改原来的摘要结构

## 输出风格

- 以“当前最值得先看什么”为核心
- 优先压缩重复报道，避免逐条复述标题
- 默认保留 3-5 条 `当前关注`
- 其余内容按 `市场`、`科技`、`其余简报` 组织
- 正文前必须先输出 `## 简报信息`
- 不默认附链接
- 不写“为什么重要”这类元说明
- 不用“本轮无更新”之类的填充句
- 尽量使用简报式、新闻编辑式语言，而不是长篇评论体

## 文件命名兼容

`fresh` 模式查找：

```text
YYYY-MM-DD-HH-mm_freshNews.md
```

`daily` 模式兼容：

```text
dailyFreshNews_YYYY-MM-DD.md
YYYY-MM-DD_dailyFreshNews.md
```

若同日新旧命名同时存在，优先新命名。

## 相关文件

- Skill 说明：[SKILL.md](/Users/x/.codex/skills/news-briefing/SKILL.md)
- 摘要 rubric：[references/summary-rubric.md](/Users/x/.codex/skills/news-briefing/references/summary-rubric.md)
