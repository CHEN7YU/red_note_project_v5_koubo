# -*- coding: utf-8 -*-
"""GPT-5 改写双平台脚本 v2 — 更口语化、用词更简单"""
import subprocess, json, os, requests

ENDPOINT = "https://rednote-openai-gpt41.openai.azure.com"
API_VERSION = "2024-12-01-preview"
MODEL = "gpt-5-4"
OUTPUT_DIR = r"c:\repos\red_note_project_v5 口播\output\AI抢走新人岗位"

token = json.loads(subprocess.run(
    ["az", "account", "get-access-token", "--resource", "https://cognitiveservices.azure.com"],
    shell=True, capture_output=True, text=True, timeout=30
).stdout)["accessToken"]
print("Token OK")

# 读取 v1 脚本
with open(os.path.join(OUTPUT_DIR, "双平台脚本_v1.md"), "r", encoding="utf-8") as f:
    v1 = f.read()

prompt = """以下是 TikTok 英文 + 抖音中文的双平台口播脚本 v1。用户反馈："脚本别用复杂的词，口语化。"

请改写为 v2，两个版本都要改。要求：

## 英文版改写要求：
1. 更像跟朋友面对面聊天，不像在读稿或做报告
2. 用更短的句子，更多口语连接词（like, look, right, okay, so, honestly, here's the thing, basically）
3. 避免所有 SAT 词汇和书面表达（比如 "cognitive labor" → "thinking work"，"operating system for knowledge work" → 简化表达）
4. 数据穿插在聊天节奏里，不要一次堆砌
5. 150-220 words，所有核心事实不变
6. 保留表演提示标注
7. 语气参考：像 Fireship 或者跟同事吐槽科技圈

## 中文版改写要求：
1. 更像聊天，去掉所有"播音腔"和文绉绉的表达
2. 用更短的句子，更多口语过渡词（就是说、你想啊、说白了、关键是、然后呢、对吧）
3. 避免生硬术语，能用大白话说的绝不用专业词（比如"认知劳动"→"动脑子的活"，"重复性认知劳动"→"那些新人练手的活"）
4. 300-600 字，所有核心事实不变
5. 保留表演提示标注
6. 语气参考：像跟朋友在饭桌上聊一个刚看到的新闻

## 通用要求：
- 直接输出完整 v2 脚本（含脚本数据、录制建议、发布素材、两版差异说明），不需要解释改了什么
- 保持原来的输出格式

v1 脚本：
""" + v1

print("正在调用 GPT-5 改写为口语化 v2...\n")
url = f"{ENDPOINT}/openai/deployments/{MODEL}/chat/completions?api-version={API_VERSION}"
resp = requests.post(url,
    headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"},
    json={"messages": [{"role": "user", "content": prompt}], "temperature": 0.75, "max_completion_tokens": 6000},
    timeout=300)
resp.raise_for_status()
text = resp.json()["choices"][0]["message"]["content"]
print(text)

out = os.path.join(OUTPUT_DIR, "双平台脚本_v2.md")
with open(out, "w", encoding="utf-8") as f:
    f.write("# 双平台脚本 v2 — AI抢走新人岗位（口语化版）\n\n")
    f.write(text)
    f.write("\n")
print(f"\n✅ 已保存到 {out}")
