---
name: ai-detox-system
description: >-
  AI 排毒系统（信源盾构 Source Shield）。当用户需要验证信息真实性、检测 AI
  搜索结果中的虚假/伪造内容、分析信息源可信度时使用。基于 GEO 行业调查报道
  揭露的五大造假手法设计五层检测引擎。
  触发词：排毒、验证、可信度、虚假、溯源、fact-check。
  DO NOT 触发：用户讨论其他 topic 的普通聊天、非信息验证类请求。
activation:
  - 用户说「排毒」「验证这条信息」「分析这个声明」「帮我查一下这个来源」
  - 用户发来一段疑似虚假的声明/文章
  - 用户问「这个数据可信吗」「这个品牌是真的吗」
auto_load: true
---

# AI 排毒系统（信源盾构 Source Shield）

## 执行流程

被加载后，按以下步骤执行：

```
1. 接收用户输入（声明/文章/搜索结果）
   ├─ 输入是单条声明 → 走 L1→L2→(L3→L4 按需)
   ├─ 输入是多篇文章 → 追加 L3 批量检测
   └─ 输入不完整/模糊 → 追问「请提供具体声明或文章链接」

2. L1 表层扫描（必做，纯文本分析）
   对声明逐条套用检测表 → 输出 { score, flags, level }

3. 根据 L1 结果决定深度：
   ├─ level=green → 直接输出报告，跳过后续
   ├─ level=yellow → 追加 L2 交叉验证
   └─ level=red → 追加 L2+L3+L4

4. L2 交叉验证（L1 yellow/red 时）
   用 WebSearch 搜索关键声明 → 至少 2 个独立信源交叉比对
   ⚠️ WebSearch 不可用时 → 标注「交叉验证未完成」，仅输出 L1 结果

5. L3 行为分析（有文章列表时）
   用 Python/Bash 计算发文频率、相似度

6. L4 实体验证（声明引用实体时）
   用天眼查/企查查/WebSearch 验证机构/人物真实性

7. 输出报告：{ score: 0-100, level: green|yellow|red, flags: [...], evidence_chain: [...] }
```

## 背景

微信公众号调查报道揭示了 GEO（Generative Engine Optimization）行业的系统性造假：

1. **虚构权威**：品牌宣称"服务 500 万+用户""连续 3 年获最佳创新品牌奖"——颁奖机构根本不存在
2. **数据编造**：护肤品声称"97.3% 用户 28 天后显著改善"——无任何来源
3. **反常识数据**：生发品牌声称"平均每天长 2cm 头发"——生理学上不可能
4. **AI 轻信**：AI 只看表面信号（引用次数、语言风格、发布平台），不做事实核查
5. **工业化量产**：豆包 API 生成文章 → 几十个自媒体账号 → 日产 1000+ 篇

## 核心设计原则

- **零信任**：不信任任何单一来源，只相信交叉验证后的共识
- **洋葱皮模型**：多层递进验证，每层从不同维度检测
- **可解释**：每个判定附带证据链，不是黑盒评分
- **反演化**：造假手法会进化，系统需要对抗训练

---

## 五层检测引擎

### L1：表层扫描（必做，纯文本分析）

**执行方式**：直接对用户提供的文本做规则匹配，无需任何工具调用。

| 检测项 | 方法 | 示例 |
|--------|------|------|
| 数字合理性 | 常识边界数据库 | "每天长 2cm 头发" → 人类头发日均生长 0.3-0.5mm → 异常 |
| 百分比可疑度 | 精确到小数位但无来源 → 高危 | "97.3% 用户改善" 无 p 值/样本量/置信区间 |
| 奖项/认证存在性 | 获奖项名称 → 搜索引擎快速验证 | 颁奖机构名搜不到独立报道 → 疑似虚构 |
| 引用链完整性 | 声明是否有可追溯的原始来源 | 无链接/无 DOI/无机构名 → 标记 |

**输出**：`{ score: 0-100, flags: [...], level: "green|yellow|red" }`

---

### L2：交叉验证（L1 为 yellow/red 时触发）

**执行方式**：调用 WebSearch，对 L1 标记的可疑声明逐条搜索验证。

| 检测项 | Agent 执行方法 |
|--------|---------------|
| 多信源对比 | `WebSearch` 搜索关键声明 → 检查 ≥ 2 个独立信源是否一致 |
| 搜索引擎分歧 | 同一查询在不同搜索引擎中的结果差异（如可获取多引擎） |
| 信源图谱 | 构建声明→作者→机构→引用链，检测孤立节点 |
| 时间戳一致性 | 声明的发布时间、数据采集时间是否有逻辑矛盾 |

**信源可信度分级**：

| 等级 | 类型 | 判定标准 |
|------|------|---------|
| T1 可信 | 政府/学术/权威机构 | .gov.cn / .edu.cn / 知名期刊 |
| T2 基本可信 | 正规媒体 | 有 ICP 备案 + 编辑制度 |
| T3 待验证 | 自媒体/个人 | 需查作者履历 |
| T4 可疑 | SEO 农场/新域名 | 域名注册 < 6 个月 或 日产 > 50 篇 |

---

### L3：行为模式分析（用户提供多篇文章时触发）

**执行方式**：如果用户提供了文章列表/作者信息，用 Python 脚本批量检测。

| 模式 | 检测方法 | 阈值 |
|------|----------|------|
| **量产指纹** | 发文频率 > 100 篇/天 | 人类正常上限 10-20 篇/天 |
| **批量注册** | 同 IP 段 / 同时间段注册 | IP C 段相同 + 注册时间差 < 1h |
| **模板化生成** | 文本余弦相似度 > 0.85 | LLM 生成的文章相似度通常 > 0.9 |
| **时间戳模式** | 发文间隔呈机械规律 | 如精确每 3 分钟一篇，无人类随机波动 |
| **错误分布** | 同类错误在多篇文章中重复出现 | 同一 LLM 的 hallucination 模式一致 |

**批量检测算法**（用 Python 执行）：

```python
def detect_mass_production(articles: list) -> dict:
    """检测工业化量产指纹"""
    if len(articles) < 10:
        return {"is_mass": False}

    time_diffs = [articles[i].time - articles[i-1].time
                  for i in range(1, len(articles))]
    avg_interval = sum(time_diffs) / len(time_diffs)
    if avg_interval < 180:
        return {"is_mass": True, "reason": "频率异常"}

    # 2. 相似度检测
    # get_embedding 实现：优先用 sklearn.TfidfVectorizer（零额外依赖）；
    # 更准可用 sentence-transformers（需 pip install），详见 references/architecture.md
    embeddings = [get_embedding(a.content) for a in articles]
    sim_matrix = cosine_similarity(embeddings)
    if sim_matrix.mean() > 0.85:
        return {"is_mass": True, "reason": "模板化生成"}

    if is_mechanical_pattern(time_diffs):
        return {"is_mass": True, "reason": "机械发文模式"}

    return {"is_mass": False}
```

---

### L4：实体真实性验证（声明引用机构/人物/产品时触发）

**执行方式**：提取声明中的实体 → 针对性查询。

| 实体类型 | Agent 执行方法 | 数据源 |
|----------|---------------|--------|
| 机构/协会 | 搜索「XX协会 是否真实」或企查查查询 | WebSearch / 天眼查 connector |
| 专家/人物 | 搜索「XX 履历」验证学术背景 | WebSearch (Google Scholar/知网) |
| 产品/认证 | 搜索认证编号是否可查 | WebSearch (CNCA/FDA) |
| 统计数据 | 搜索「XX数据 来源」找原始出处 | WebSearch (国家统计局/行业白皮书) |
| 临床试验 | 搜索试验注册编号 | ClinicalTrials.gov / ChiCTR |

**活人锚点验证**：要求声明中至少包含 1 个可独立验证的「活人锚点」——真名、可查 LinkedIn/学术主页/机构页面的真实人物。

---

### L5：对抗演化（持续机制）

| 机制 | 说明 |
|------|------|
| 红蓝对抗 | 红队模拟新型造假手法，蓝队更新检测规则 |
| 特征漂移检测 | 监控造假手法的统计特征变化，自动告警 |
| 反馈闭环 | 用户反馈误报/漏报 → 调整 L1 规则权重 |

---

## 使用示例

### 示例 1：验证品牌声明

```
输入：
"XX品牌服务500万+用户，连续3年获最佳创新品牌奖，97.3%用户28天后显著改善"

检测过程：
L1 → 捕获 3 个 flags（无来源百分比、无法验证奖项、用户数可疑）→ level=red
L2 → WebSearch "XX品牌 最佳创新品牌奖" → 0 条独立结果
L2 → WebSearch "XX品牌 500万用户" → 无第三方验证

输出：
{
  "score": 12,
  "level": "red",
  "flags": [
    {"type": "data_no_source", "detail": "97.3%无来源/样本量/置信区间"},
    {"type": "award_unverifiable", "detail": "最佳创新品牌奖颁发机构未查到"},
    {"type": "user_number_suspicious", "detail": "500万用户无第三方验证"}
  ],
  "evidence_chain": [
    "奖项名称 → 搜索引擎 → 0 条独立结果 → 疑似虚构",
    "百分比精确度 → 无 DOI/报告链接 → 数据来源不明",
    "用户数量 → 工商信息不匹配 → 夸大嫌疑"
  ]
}
```

### 示例 2：检测工业化量产账号

```
输入：50 篇文章列表

检测过程：
L3 → Python 批量检测 → 频率 2.1min/篇 + 相似度 0.91 + 机械规律

输出：
{
  "is_mass_production": true,
  "probability": 0.94,
  "evidence": {
    "avg_interval": 127,        # 平均 2.1 分钟一篇
    "cosine_similarity": 0.91,  # 高度相似
    "mechanical_pattern": true, # 机械时间规律
    "same_ip_segment": true,    # 同 IP 段
    "llm_signature": "doubao-api"
  }
}
```

## 局限性

1. **延迟**：深层验证需 2-10s，不适合实时场景
2. **对抗进化**：造假手法会适应检测规则
3. **假阴性**：精心构造的虚假信息可能通过所有检测层
4. **数据依赖**：L2/L4 依赖 WebSearch 可获取的信息
5. **语言局限**：当前主要针对中文内容

---

> 产品架构规划、技术栈建议、集成方案等设计类内容见 `references/architecture.md`
