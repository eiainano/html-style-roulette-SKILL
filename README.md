# html-style-roulette 🎨🎲

> HTML 报告版式轮盘 —— 让 AI Agent 每次产出的 HTML 报告**随机换一套视觉风格**，告别审美疲劳。

一个 [Agent Skill](https://www.workbuddy.cn)（兼容 Claude Code 等 SKILL.md 格式）：内容骨架恒定，视觉层随机换装。无 API Key、无外部依赖，纯 Markdown + Python 脚本。

## 解决什么问题

让 AI 反复产出 HTML 调研报告时，它总会用同一种「白底蓝字卡片」审美——第 10 篇和第 1 篇长得一模一样。本技能把「版式」抽出来做成风格库：**每次写报告前先摇一次骰子**，18 种浅色版式随机抽一种（排除暗色系、避免与上次重复），按该版式的 CSS 令牌重新实现视觉层。

## 内容与皮肤分离

不管抽到哪种版式，报告的内容骨架恒定：

```
导读 + 阅读路径
每章：本章回答什么 → 读完你会知道
章末：本章三句话
事实与推断分开标注
信源清单（含日期与口径）
```

换的只是皮肤：组件形态（卡片→贴纸→便当格→图框）、色板、字体、图表样式。

## 用法

安装到技能目录（WorkBuddy `~/.workbuddy/skills/`、Claude Code `~/.claude/skills/`），然后：

```bash
# 抽一个版式（自动排除上次用过的，并写入 usage.log）
python3 pick_style.py

# 查看使用历史
python3 pick_style.py --history
```

脚本输出该版式的 CSS 令牌（色板 / 字体 / 组件形态），Agent 据此实现整份报告的视觉层。

## 风格库（18 种浅色 + 2 种排除）

| 已验证 | 待抽取 | 排除 |
|---|---|---|
| 默认白蓝卡片 · 财经编辑 · 卡通可爱 | 瑞士网格 · 终端 mono · Bento 便当格 · 杂志双栏 · 蓝图工程 · 学术 LaTeX · 报纸大版式 · 玻璃拟态 · 新拟物 · 像素 8-bit · 孟菲斯 · 包豪斯 · 铅字印刷 · 手账 · Notion 文档 | 赛博朋克霓虹 · 黑板粉笔（暗色系） |

每种版式在 `styles.json` 中带完整的 CSS 令牌速查，可直接照抄实现。

## 文件结构

```
html-style-roulette-SKILL/
├── SKILL.md        # 技能定义：触发词、工作流、硬规则
├── styles.json     # 风格库：18 种浅色版式的 CSS 令牌 + 暗色排除表
├── pick_style.py   # 随机抽取器：排除暗色/上次所用，写 usage.log
└── usage.log       # 自动生成的使用记录（gitignore）
```

## 硬规则

1. 浅色主题（暗色系永不入选）
2. 单文件、零外部依赖（不引外部字体/JS/CSS）
3. 内容骨架恒定，只换视觉层
4. 不加个人署名、水印、落款等元数据
5. 数据正确性优先于装饰

## 扩展

往 `styles.json` 的 `styles` 数组追加条目即可（id / name / used / tokens，tokens 至少含 bg、ink、accent、字体、组件形态五项）。欢迎 PR 补充新版式。

## License

MIT
