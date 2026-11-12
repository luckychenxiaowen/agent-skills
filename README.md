# agent-skills

一个 AI 产品人在真实工作里攒下的 Skill 集。不是合集，是每次踩坑后改过的那一版。

首批放出 **7 个**，全部为个人业余自研、且通过权属与内容审查。这里是 Skill 文档与配套模板，不是一个运行时框架——每个目录独立可用，复制进你自己的 Agent 的 skills 目录即可。

## 为什么只有 7 个

原本整理出 16 个自研 Skill，逐项过了三道门：**是不是我写的 / 有没有不能外发的内容 / 公开后会被怎么读**。8 个被留在本批之外（依赖第三方服务、涉及具体安全机制、或需要额外声明），1 个含具体雇主语境暂缓。判断依据见 [EXCLUDED.md](EXCLUDED.md)。

宁可少发，不发错。

## 声明

本仓库是**个人业余项目**，与雇主无关，不含任何公司内部数据、业务代码或内部文件。首批 7 个 Skill 均不含第三方代码，唯一外部依赖是 `wechat-miniprogram-publish` 里提到的微信开放平台流程（那是平台操作说明，不是代码引用）。

## Skill 清单

| Skill | 分类 | 干什么 |
|---|---|---|
| [ai-detox-system](skills/ai-detox-system) | 内容方法 | AI 味去除与信息可信度五层检测 |
| [skill-writer](skills/skill-writer) | Skill 工程 | 把内容重写成 Skill 规范格式 |
| [self-evolution](skills/self-evolution) | Skill 工程 | 技能使用复盘与自我进化模板 |
| [wechat-miniprogram-publish](skills/wechat-miniprogram-publish) | 平台与部署 | 微信小程序从 0 发布上线全流程（注册 / 包体积 / 域名 / 备案 / 提审） |
| [guiguzi-perspective](skills/guiguzi-perspective) | 思维视角 | 鬼谷子纵横捭阖视角（博弈 / 谈判 / 组织） |
| [huangshigong-perspective](skills/huangshigong-perspective) | 思维视角 | 黄石公素书三略视角（处世 / 进退取舍） |
| [taigong-perspective](skills/taigong-perspective) | 思维视角 | 姜太公六韬视角（战略布局 / 人才 / 竞争） |

### 三类怎么来的

- **内容方法 / Skill 工程**：写给 Agent 用的方法论——怎么把输出写得像人、怎么写一个 Skill、怎么复盘一个 Skill
- **平台与部署**：把踩过的坑写成可复跑流程
- **思维视角**：三个古代思想框架，用来换角度看决策问题；不是史料考据，是分析脚手架

## 用法

1. 进任意 `skills/<name>/`，先读 `SKILL.md` 的 frontmatter（触发条件写在 description 里）
2. 把整个目录复制到你的 Agent 的 skills 目录
3. 有 `references/` 的是配套模板，按需取用；不需要额外安装依赖

## 关于思维视角类

这三个 Skill 是对传统思想框架的**结构化整理**，用于辅助分析，不代表对原典的权威解读，也不构成任何医疗、法律、投资或职业建议。框架是工具，判断是你的。

## 暂缓与剔除

见 [EXCLUDED.md](EXCLUDED.md)。

## 许可

[MIT](LICENSE)。Copyright (c) 2026 luckychenxiaowen。

## 发布前

`python scripts/check-before-push.py` 必须全项 PASS；新增 Skill 的规范见 [CONTRIBUTING.md](CONTRIBUTING.md)。
