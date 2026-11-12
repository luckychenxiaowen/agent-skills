#!/usr/bin/env python3
"""Pre-push hygiene check for agent-skills. Run from repo root."""
import os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEXT_EXT = {".md",".js",".mjs",".cjs",".py",".json",".yaml",".yml",".html",".txt",".sh",".ps1",".bat",".css",".ts",".jsx",".tsx",".toml",".env"}
FORBIDDEN_FILES = {"accounts.json", "wechat_baseline.json", "Cookies", "Cookies-journal"}
# 首批白名单：只允许这 7 个 Skill 入库，防止误把待审内容带回来
ALLOWED_SKILLS = {
 "ai-detox-system", "skill-writer", "self-evolution",
 "wechat-miniprogram-publish", "guiguzi-perspective",
 "huangshigong-perspective", "taigong-perspective",
}
# 敏感词用拼接构造，避免本文件自命中
CORP = ["顺" + "丰", "领" + "慧", "丰" + "声", "薛" + "航", "内部资料", "商业机密"]
PATTERNS = {
 "private_key": re.compile(r"BEGIN [A-Z ]*PRIVATE KEY"),
 "live_key": re.compile(r"sk-[A-Za-z0-9]{20,}"),
 "real_appid": re.compile(r"wx[0-9a-fA-F]{16}"),
 "private_ip": re.compile(r"(10\.\d{1,3}\.\d{1,3}\.\d{1,3}|192\.168\.\d{1,3}\.\d{1,3})"),
 "abs_path": re.compile(r"[A-Za-z]:[\\/](Users|workspaces)[\\/]"),
 "home_dir": re.compile(r"[A-Za-z]:[\\/]+Users[\\/]+", re.I),
}
results = []

def check(label, ok, detail=""):
    results.append((label, bool(ok), detail))

for req in ("README.md","LICENSE",".gitignore","EXCLUDED.md","PUBLISH.md","CONTRIBUTING.md","CHANGELOG.md"):
    check("file: " + req, os.path.isfile(os.path.join(ROOT, req)))

skills_root = os.path.join(ROOT, "skills")
skill_dirs = sorted(d for d in os.listdir(skills_root) if os.path.isdir(os.path.join(skills_root, d))) if os.path.isdir(skills_root) else []
check("skill count == 7", len(skill_dirs) == 7, "found %d" % len(skill_dirs))
check("skill whitelist exact match", set(skill_dirs) == ALLOWED_SKILLS,
      "extra=" + ",".join(sorted(set(skill_dirs) - ALLOWED_SKILLS)))
for d in skill_dirs:
    check("skill doc: " + d, all(os.path.isfile(os.path.join(skills_root, d, f)) for f in ("SKILL.md","README.md")))

hits = {k: [] for k in PATTERNS}
corp_hits = []
file_hits = []
for dp, dns, fns in os.walk(ROOT):
    dns[:] = [x for x in dns if x not in {".git","node_modules","__pycache__"}]
    for fn in fns:
        rel = os.path.relpath(os.path.join(dp, fn), ROOT).replace("\\", "/")
        if fn in FORBIDDEN_FILES:
            file_hits.append(rel)
        if fn.startswith(".env") and not fn.endswith(".example"):
            file_hits.append(rel)
        if os.path.splitext(fn)[1].lower() not in TEXT_EXT:
            continue
        if rel.startswith("scripts/"):
            continue
        try:
            t = open(os.path.join(dp, fn), encoding="utf-8", errors="ignore").read()
        except Exception:
            continue
        for k, rgx in PATTERNS.items():
            if rgx.search(t):
                hits[k].append(rel)
        for w in CORP:
            if w in t:
                corp_hits.append(rel + " [" + w + "]")

for k, v in hits.items():
    check("no " + k, not v, ", ".join(v[:4]))
check("no employer-specific terms", not corp_hits, ", ".join(corp_hits[:4]))
check("no credential/state files", not file_hits, ", ".join(file_hits[:4]))

for label, ok, detail in results:
    print(("PASS  " if ok else "FAIL  ") + label + (("  -> " + detail) if detail and not ok else ""))
bad = [r for r in results if not r[1]]
print("\n%d checks, %d failed" % (len(results), len(bad)))
sys.exit(1 if bad else 0)
