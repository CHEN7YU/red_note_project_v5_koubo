# -*- coding: utf-8 -*-
"""GPT-5 改写 TikTok 脚本 v2 — 更口语化"""
import subprocess, json, os, requests

token = json.loads(subprocess.run(
    ["az", "account", "get-access-token", "--resource", "https://cognitiveservices.azure.com"],
    shell=True, capture_output=True, text=True, timeout=30
).stdout)["accessToken"]
print("Token OK")

# 读取 v1 脚本
with open(r"c:\repos\red_note_project_v5 口播\output\AI裁员洗白\TikTok_脚本_v1.md", "r", encoding="utf-8") as f:
    v1 = f.read()

prompt = """以下是 TikTok 英文口播脚本 v1，用户反馈"太书面了，不够口语化"。

请改写为 v2，要求：
1. 更像跟朋友面对面聊天，不像在读稿
2. 用更短的句子，更多口语连接词（like, look, right, okay, so, honestly, here's the thing）
3. 去掉所有新闻播报感的表达（如 "That was reported by CNA on May 25"），改成自然提及
4. 数据不要一次性堆砌，穿插在对话节奏里
5. 保持 150-220 words，保持所有核心事实不变
6. 保留 [停顿]、[加重语气]、[手势] 等表演提示标注
7. 不要用 Hey guys / What's up 开头
8. 语气参考：像 Fireship 或者跟同事吐槽科技圈的感觉

v1 脚本：
""" + v1 + """

直接输出完整 v2 脚本（含表演提示），不需要解释改了什么。保持原来的输出格式（脚本数据、录制建议、发布素材都要）。"""

print("正在调用 GPT-5.4 改写脚本...\n")
url = "https://rednote-openai-gpt41.openai.azure.com/openai/deployments/gpt-5-4/chat/completions?api-version=2024-12-01-preview"
resp = requests.post(url,
    headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"},
    json={"messages": [{"role": "user", "content": prompt}], "temperature": 0.75, "max_completion_tokens": 3000},
    timeout=180)
resp.raise_for_status()
text = resp.json()["choices"][0]["message"]["content"]
print(text)

out = r"c:\repos\red_note_project_v5 口播\output\AI裁员洗白\TikTok_脚本_v2.md"
with open(out, "w", encoding="utf-8") as f:
    f.write(f"# TikTok 英文脚本 v2 — 口语化版本\n\n{text}\n")
print(f"\n✅ 已保存到 {out}")
