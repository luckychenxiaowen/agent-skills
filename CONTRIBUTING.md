# 加一个新 Skill

1. 在 `skills/` 下建目录，目录名用小写连字符
2. 必须有 `SKILL.md`（frontmatter 含 name / description / 触发条件）
3. 必须有 `README.md`，写清分类、来源、第三方依赖与出处
4. 配置类文件只放 `*.example.*`，真实配置进 `.gitignore`
5. 不写本机绝对路径、账号、内部数据、雇主名称
6. 引用第三方框架要标出处；带原 LICENSE 的目录保留原文件
7. 跑 `python scripts/check-before-push.py`，全项 PASS 才提交

流程整合算原创，底层框架不算——标注清楚就行，别把别人的东西写成自己的。
