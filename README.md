# SKILLS 技能库

本仓库保存了用于 Dify/OpenCode 的 Agent Skills，每个 Skill 都是独立的工具模块，可通过 `/skill-name` 命令调用。

## 📋 技能分类总览

| 分类 | 数量 | 说明 |
|------|------|------|
| [🎨 创意与设计](#-创意与设计) | 6 | 算法艺术、视觉设计、图表、GIF 等 |
| [📊 文档与办公](#-文档与办公) | 6 | Word、Excel、PPT、PDF 等文档处理 |
| [💼 招聘与求职](#-招聘与求职) | 12 | JD 生成、简历优化、面试辅导、职业规划等 |
| [🛠️ 开发与工程](#-开发与工程) | 6 | 架构图、流程图、代码审查、MCP 开发等 |
| [🔍 研究与分析](#-研究与分析) | 4 | 深度研究、数据分析、网页抓取等 |
| [🤖 Agent 元技能](#-agent-元技能) | 8 | Skill 管理、Agent 浏览器、自我评估等 |
| [📝 内容创作](#-内容创作) | 3 | 文章写作、内部沟通、主题工厂等 |
| [📦 实用工具](#-实用工具) | 2 | 文件解压、技能查找等 |

---

## 🎨 创意与设计

### algorithmic-art
**描述**: 使用 p5.js 创建算法艺术，支持种子随机性和交互式参数探索。用于生成艺术、流程场、粒子系统等。

### canvas-design
**描述**: 使用设计哲学创建精美的静态视觉艺术作品，输出 .png 和 .pdf 格式。

### chart-visualization
**描述**: 数据可视化图表生成工具。

### diagram-maker
**描述**: 图表制作工具，支持 Excalidraw 风格的图表创建。

### drawio-skill
**描述**: Draw.io 图表技能，支持架构图、流程图、时序图等多种图表类型的创建和编辑。

### slack-gif-creator
**描述**: 创建针对 Slack 优化的动画 GIF，提供约束条件、验证工具和动画概念。

---

## 📊 文档与办公

### docx
**描述**: 全面的 Word 文档处理工具，支持创建、编辑、修订跟踪、评论添加和文本提取。

### xlsx
**描述**: 全面的电子表格处理工具，支持公式、格式化、数据分析和可视化。

### pptx
**描述**: 全面的 PPT 演示文稿处理工具，支持创建、编辑、模板使用和演讲者备注。

### pdf
**描述**: 全面的 PDF 处理工具包，支持文本和表格提取、创建新 PDF、合并/拆分文档和表单处理。

### archify
**描述**: 创建精美的架构图、工作流图、时序图、数据流图和生命周期图，支持 HTML/SVG 导出和多种格式输出。

### theme-factory
**描述**: 为幻灯片、文档、报告、HTML 页面等提供主题样式工具包，包含 10 种预设主题。

---

## 💼 招聘与求职

### career-planning-1.0.3
**描述**: 职业规划技能，融合杠杆效应、中国式战略方法论，帮助用户建立长远认知和战略思维，制定职业转型或发展策略。

### interview-coach
**描述**: 完整的求职辅导系统，包含 JD 解析、简历优化、故事库、模拟面试、薪酬谈判等 23 个命令。

### interview-scorecard
**描述**: 基于《Who》和《Work Rules!》方法论的面试评分卡生成工具，帮助设计结构化面试流程。

### interview-sparring
**描述**: JD 驱动的诊断式面试陪练，动态追踪弱项，与模拟面试的区别在于诊断式循环。

### jd-assistant
**描述**: JD 助手，支持快速 JD 生成和完整招聘包（含面试指南、Offer Letter）。

### jd-generator
**描述**: 基于简历信息精准推导岗位需求，生成符合劳动法合规、行业对标的岗位描述。

### job-post-builder
**描述**: 端到端招聘文档生成，包含岗位描述、结构化面试指南和 Offer Letter 模板。

### resume-builder
**描述**: 简历构建工具。

### resume-modern
**描述**: 现代风格简历生成工具。

### resume-optimizer
**描述**: 简历优化工具，提升简历质量和匹配度。

### tailored-resume-generator
**描述**: 分析职位描述并生成定制简历，突出相关经验、技能和成就，最大化面试机会。

### labor-contract-review-1.0.0 / labor-contract-review-tmp
**描述**: 劳动合同审查工具。

---

## 🛠️ 开发与工程

### claude-api
**描述**: Claude API / Anthropic SDK 参考指南，包含模型 ID、定价、参数、流式传输、工具使用、MCP、Agent、缓存等完整文档。

### code-review
**描述**: 代码审查技能。

### mcp-builder
**描述**: 创建高质量 MCP（Model Context Protocol）服务器的指南，支持 Python（FastMCP）和 Node/TypeScript（MCP SDK）。

### web-artifacts-builder
**描述**: 使用现代前端技术（React、Tailwind CSS、shadcn/ui）创建复杂 HTML 工件的工具套件。

### webapp-testing
**描述**: 使用 Playwright 与本地 Web 应用交互和测试的工具包。

### frontend-design
**描述**: 创建具有高品质设计的独特、生产级前端界面。

---

## 🔍 研究与分析

### deep-research
**描述**: 深度研究技能。

### data-analysis
**描述**: 数据分析技能，包含 Python 分析脚本。

### data-scraper-agent
**描述**: 数据抓取 Agent。

### github
**描述**: GitHub 操作技能。

---

## 🤖 Agent 元技能

### skill-creator
**描述**: 创建有效技能的指南。

### skill-installer
**描述**: 从精选列表或 GitHub 仓库路径安装 Codex Skills。

### skill-writer
**描述**: 引导用户完成创建 Agent Skills 的流程。

### find-skills
**描述**: 技能查找工具。

### agent-browser-1.0.0
**描述**: Agent 浏览器工具。

### agent-memory
**描述**: Agent 记忆管理。

### agent-self-evaluation
**描述**: Agent 自我评估。

### security-check
**描述**: 安全检查工具。

### self-improving-agent-1.0.0
**描述**: 自我改进 Agent。

---

## 📝 内容创作

### article-writing
**描述**: 撰写文章、指南、博客文章、教程、通讯等长内容，支持从示例或品牌指南中提炼的独特声音。

### internal-comms
**描述**: 内部沟通写作资源集，支持状态报告、领导层更新、3P 更新、公司通讯、FAQ、事故报告等。

### doc-coauthoring
**描述**: 引导用户完成结构化文档协作写作流程。

---

## 📦 实用工具

### unzip-all-1.0.0
**描述**: 递归解压所有嵌套压缩包（zip/7z/rar），支持中文文件名。

### brand-guidelines
**描述**: 应用 Anthropic 官方品牌颜色和排版到任何工件。

---

## 📁 其他技能

### unzip-all
**描述**: 递归解压文件夹中的所有压缩包。

### aihot-wb7k2-1.0.0
**描述**: AI 热点追踪技能。

### daily-ai-news-skill-0.1.0
**描述**: 每日 AI 新闻技能。

### byted-web-search
**描述**: 字节跳动网页搜索技能。

---

## 🚀 快速使用指南

### 安装技能
```bash
# 通过 skill-installer 安装
npx skills add <author>/<skill-name>
```

### 调用技能
```bash
# 在对话中使用 /skill-name 调用
/skill-name
```

### 查看技能详情
每个技能目录下的 `SKILL.md` 文件包含：
- 技能描述和使用场景
- 详细的使用说明
- 示例和最佳实践
- 限制条件和注意事项

---

## 📊 技能统计

- **总技能数**: 57+
- **分类数**: 8
- **最后更新**: 2026-09-08

---

## 🔗 相关资源

- [OpenCode 官方文档](https://docs.opencode.dev)
- [Dify 官方文档](https://docs.dify.ai)
- [Anthropic Claude API](https://docs.anthropic.com)

---

*本 README 由 Atlas 自动生成，如有遗漏或错误请手动修正。*
