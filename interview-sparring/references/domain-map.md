# AI 工程师面试知识域地图

> Interview Sparring 用这张地图分类 JD 要求，映射到考察域。

## 知识域定义

### 1. RAG / 检索增强生成
- 文档处理（chunking 策略、PDF/表格解析）
- Embedding 选型（text-embedding-3 / BGE / bge-m3）
- 向量数据库（Chroma / Milvus / Qdrant / pgvector）
- 检索策略（向量 / BM25 / 混合检索 / Reranker）
- Query 改写与优化
- RAG 评估（Hit Rate / MRR / Faithfulness / RAGAS）
- 生产问题排查（检索不准 / 幻觉 / 延迟）

### 2. Agent / 智能体
- 核心概念（ReAct / Plan-and-Execute / 多 Agent）
- 工具设计（Function Calling / Tool Schema）
- 记忆系统（短期 / 长期 / MemGPT / Letta）
- 失效模式（死循环 / 幻觉工具调用 / 上下文爆炸）
- 框架（LangGraph / CrewAI / AutoGen）

### 3. MCP / 模型上下文协议
- 协议层原理（Host / Client / Server）
- 三类能力（Tools / Resources / Prompts）
- N+M 效应
- 与 REST/gRPC 的区别
- 实战：Adapter & Gateway 设计

### 4. Prompt 工程
- System Prompt 设计
- Few-shot / Chain-of-Thought / Self-Consistency
- 输出格式控制（JSON mode / Schema）
- Prompt 注入防护
- 评估与迭代方法

### 5. LLM 工程
- API 使用（Streaming / Token 管理 / 成本控制）
- 模型选型（GPT-4 / Claude / Gemini / 开源）
- Fine-tuning vs RAG vs Prompt 的选择
- 生产问题（Rate Limit / 延迟优化 / 幻觉控制）
- 可观测性（日志 / Tracing / 评估）

### 6. 系统设计
- AI 应用架构（单体 / 微服务 / Serverless）
- 数据流设计（实时 vs 离线 / 流式处理）
- 高可用与容错
- 成本估算与优化
- 安全（数据隐私 / 合规 / 越狱防护）

### 7. 搜索 / 信息检索
- 倒排索引 / Elasticsearch
- Query 理解（意图识别 / 实体识别 / 改写）
- 排序与重排
- 评估指标（NDCG / MAP / Recall@K）

### 8. 编码能力
- Python 基础（数据结构 / 算法 / 并发）
- API 设计（RESTful / GraphQL）
- 测试（单元测试 / 集成测试 / Mock）
- Git 工作流

## JD 关键词 → 知识域映射

| JD 中的关键词 | 映射到知识域 |
|---|---|
| RAG / 检索增强 / 知识库 | 1. RAG |
| Agent / 智能体 / 多步骤 / ReAct | 2. Agent |
| MCP / 协议 / Server / Tools | 3. MCP |
| Prompt / 提示词 / System Prompt | 4. Prompt |
| LLM / 大模型 / API / Token | 5. LLM 工程 |
| 架构 / 系统设计 / 高可用 | 6. 系统设计 |
| 搜索 / Elasticsearch / 召回 | 7. 搜索 |
| Python / 算法 / 代码 | 8. 编码 |
| LangChain / LlamaIndex / LangGraph | 2. Agent + 1. RAG |
| Embedding / 向量 / 相似度 | 1. RAG |
| Fine-tune / 微调 / RLHF | 5. LLM 工程 |
