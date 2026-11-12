# 暂缓与剔除说明

开源不是把目录整个搬上来。下面是被挡在首批之外的东西，以及放回条件。

## 1. 首批范围

首批只放 **7 个**通过三道门（权属 / 内容 / 公开后怎么被读）的 Skill。以下 8 个自研 Skill **未纳入本批**，源文件仍在本地，未被删除：

| Skill | 未纳入原因 | 放回条件 |
|---|---|---|
| `wechat-monitor` | 依赖第三方 wewe-rss，且含真实账号配置与运行基线（已剔除，只留 `.example`） | 保留上游标注 + 确认配置模板无真实值 |
| `wewe-rss-deploy` | 依赖第三方 Docker 镜像与部署流程 | 标注上游出处 |
| `web-game-ai-rec` | 含 CDP 脚本与案例文件，需补充依赖说明 | 清路径 + 补 Chromium / CDP 出处 |
| `skill-detector` | 整合两个第三方 evaluator，目录内 LICENSE 署名第三方作者（MIT） | 保留原 LICENSE + 标注为衍生作品，不写「纯自研」 |
| `codex-cli-setup` | 含绕过审批参数与替代安装法，措辞易被误读为教人绕过安全控制 | 改写为「说明参数存在及其风险」 |
| `force-delete-windows` | 直接写明内部安全钩子机制与绕过方法 | 彻底改写为通用排查文档，删去内部产品名与钩子名 |
| `baiyun-perspective` | 16 处提及当代在世作者，无免责声明 | 补观点归属声明 |
| `nihaixia-perspective` | 含 11 处中医 / 健康术语 | 已有免责，需强化「不替代执业医师诊断」 |

> 说明：`skill-detector` 的流程整合与红队设计是原创的，底层框架不是。源库 INDEX.md 写「仅收录自研技能」，这是一处需要如实修正的地方——按 MIT 的衍生作品要求处理，不冒称纯自研。

## 2. 明确暂缓：`ai-job-replacement-analyzer`

**原因**：`SKILL.md` 里出现 13 处具体雇主名称，`assets/template.html` 里另有 1 处；内容还涉及具体岗位替代风险分析。原样发布会让个人仓库和雇主语境绑在一起，解释成本远大于收益。

**恢复条件**（三条全满足才可补发）：

1. 全部雇主名称替换成通用占位（如 `<COMPANY>`）
2. 人工复核，确认不含内部岗位信息、组织架构、业务数据
3. `python scripts/check-before-push.py` 全项 PASS

## 3. 运行时数据文件（已剔除）

| 文件 | 原因 |
|---|---|
| `config/accounts.json` | 真实账号配置，含 5 个账号条目 |
| `scripts/wechat_baseline.json` | 运行基线状态，不是源码 |

## 4. 未纳入的其他来源

- 一批航空业务类 Skill（对账 / 财务翻译 / 飞越许可等）：领域知识来自职务场景，含大量业务词与金额、航班号形态，**不脱敏后发**，只可抽象成方法写文章
- 「待确认归属」灰色清单（`xiaohongshu`、`ima-skills`、`content-factory` 等 14 个）：归属未由作者本人确认，一律不碰
- 第三方市场包（jimliu-* / baoyu-* / skywork-* / skillhub 等）：不是自研
- 打包副本 `.zip`、演示 `.gif`、项目内重复版本 `_from_projects/`、含本机路径的源库 `INDEX.md`
