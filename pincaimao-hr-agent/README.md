# 聘才猫 HR 助手 (pincaimao-hr-agent)

聘才猫人力资源垂类大模型驱动的全能 HR AI 助手，覆盖招聘全链路。基于 OpenClaw 框架，通过聘才猫开放平台 API 提供真实业务能力。

提供方：湖南聘才猫智能人力科技有限公司 · https://www.pincaimao.com

版本：v1.0.0

## 能力概览

本助手封装 10 个聘才猫平台技能，按场景自动路由：

**求职者侧**

- 简历诊断 (pincaimao-resume-diagnosis)：对照目标 JD 解析并诊断简历
- 简历优化 (pincaimao-resume-optimize)：按目标岗位优化/改写简历
- 职业规划 (pincaimao-career-planning-v2)：基于简历生成职业建议
- 模拟面试 (pincaimao-mock-interview)：多轮模拟面试，支持文本/视频模式

**招聘方侧**

- JD 助手 (pincaimao-jd-assistants)：根据岗位描述生成招聘 JD、结构化标签
- 面试出题 (pincaimao-interview-question)：根据 JD 和简历生成面试题
- 面试报告 (pincaimao-interview-reports)：根据 JD 和面试录音生成面试报告
- 在线面试 (pincaimao-online-interview)：多轮 AI 在线面试，支持报告回调

**合规侧**

- 劳动合同卫士 (pincaimao-labor-contracts)：分析劳动合同并生成评估报告

底层接口由 pincaimao-basic 提供（文件上传、会话、消息、语音转文字、简历 JSON 上传等）。

## 运行要求

- OpenClaw 运行环境
- 系统已安装：curl、python3
- 推荐模型：火山引擎 Coding Plan 系列（如 doubao-seed-2.0-pro）；亦可使用 deepseek-v3.2、glm-4.7 等

## 凭证配置（重要）

所有技能统一通过聘才猫平台 API key 鉴权，只需配置以下环境变量。未配置或 key 无效时，平台能力将返回 401。key 不写入任何文件，仅由运行环境注入。

| 环境变量 | 对应能力 |
|----------|----------|
| PCM_API_KEY | 所有平台 API 能力 |

### 如何获取 key

通过聘才猫智能体平台注册并完成认证后，创建 API key：

https://www.pincaimao.com/agents/login?invite_code=uwqc

> 注意：所有技能统一读取 `PCM_API_KEY`。

## 技能实现说明

每个技能均含 `scripts/main.py` 真实现：脚本读取对应环境变量中的 key，调用聘才猫开放平台 API 完成业务（文件上传 + chat-bot-messages）。脚本仅依赖 Python 标准库，无第三方包，可在具备 python3 的环境直接运行。各 skill 的 `scripts/` 目录附带共享底座 `pcm_common.py`（封装文件上传与对话接口）。

SKILL.md 同时保留原始 curl 接口契约说明，供 Agent 理解参数语义与排错。脚本入口用法见各 SKILL.md 顶部"脚本入口"一节。

### 文件路径安全

涉及文件上传的脚本对传入的本地文件路径做安全校验：路径经 realpath 解析后须位于允许的根目录内（默认当前工作目录），可通过环境变量 `PCM_ALLOWED_FILE_ROOT` 指定其它根目录；超出范围或含 `../` 遍历的路径将被拒绝，防止越权读取系统文件。

- **禁止重定向跟随**：所有平台请求禁用 HTTP 自动重定向，避免在跨域重定向场景下携带 Authorization 头（API key）泄漏至第三方域。
- **错误信息脱敏**：异常提示不回显服务器原始响应体与具体文件路径，仅保留状态码等排错所需的最小信息。

## 目录结构

```
pincaimao-hr-agent/
├── AGENT.md       人设、技能绑定与执行逻辑
├── SOUL.md        身份与性格
├── RULES.md       硬性规则（凭证安全、数据隐私、合规边界）
├── config.json    元数据与模型建议
├── skills/        10 个技能（文件夹形式）
│   ├── pincaimao-basic/
│   ├── pincaimao-resume-diagnosis/
│   ├── pincaimao-resume-optimize/
│   ├── pincaimao-career-planning-v2/
│   ├── pincaimao-jd-assistants/
│   ├── pincaimao-interview-question/
│   ├── pincaimao-interview-reports/
│   ├── pincaimao-mock-interview/
│   ├── pincaimao-online-interview/
│   └── pincaimao-labor-contracts/
└── README.md      本文件
```

## 使用示例

配置好对应 key 后，以自然语言交互即可，例如：

- "用 JD 助手根据这段岗位描述生成招聘 JD：……"
- "诊断这份简历对照这个岗位的匹配度"（需先上传简历文件）
- "根据这个 JD 和候选人简历出 5 道面试题"

## 数据与合规说明

- 简历、JD、个人信息等用户数据仅用于当前任务处理，不长期留存、不外传第三方。
- 劳动合同审查结论仅供参考，涉及重大法律风险请咨询专业律师，本助手不作最终法律判断。
- 招聘相关产出遵循中国劳动法规，不引入与岗位无关的歧视性标准。
