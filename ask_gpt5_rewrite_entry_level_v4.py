# -*- coding: utf-8 -*-
"""GPT-5 改写双平台脚本 v4 — 建议部分场景化：如果你是X，你可以用AI来Y"""
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

with open(os.path.join(OUTPUT_DIR, "双平台脚本_v3.md"), "r", encoding="utf-8") as f:
    v3 = f.read()

prompt = """以下是 TikTok 英文 + 抖音中文的双平台口播脚本 v3。

用户反馈：建议部分太笼统了，不够具体。要改成"如果你是……你可以用 AI 来……"的格式，让不同身份的人听完立刻知道自己该做什么。

## 修改要求：

只改 SOLUTION/建议 部分（两个版本都改），其他部分保持不变。

### 改法：
用"如果你是 [具体身份]，你可以用 AI 来 [具体动作]"的句式，举 3-4 个具体场景。

参考方向（你来组织成口语化的脚本语言，别照搬）：

**身份 + 具体动作举例：**
- 如果你是**计算机专业的学生**：别光写课程作业了。用 Claude Code 或 Cursor 做一个真的 side project——比如给学校食堂做个点评小程序，或者写个自动整理论文的工具。带着这个作品去面试，比简历上写"熟练掌握 Python"强 10 倍。
- 如果你是**市场/运营/非技术岗**：你不用学编程。用 AI 帮你自动生成周报、做数据可视化、写竞品分析。你的竞争力不是"会不会写代码"，是"能不能用 AI 把活干得又快又好"。
- 如果你是**转行的人/工作 1-3 年**：别只投简历了。用 AI 工具做一个作品集——比如用 Cursor 搭个个人网站，用 AI 分析一个行业数据集写成报告。这就是你新的"实习经历"。
- 如果你是**想创业/做副业的人**：以前得先攒几年经验才敢动手。现在你一个人加上 AI，就能做出一个 MVP 产品、一个自动化服务、甚至一个小工具卖给别人。门槛从来没有这么低过。

### 英文版同理：
用 "If you're a [role], use AI to [specific action]" 的格式，举 3 个场景，简短有力。

### 通用要求：
- 保持口语化（v3 的聊天语气不要变）
- 建议部分控制在 TikTok 30 秒以内、抖音 40 秒以内
- 直接输出完整 v4 脚本（全部内容，含脚本数据、录制建议、发布素材、两版差异说明）
- 保持原来的输出格式
- 不需要解释改了什么

v3 脚本：
""" + v3

print("正在调用 GPT-5 生成 v4（场景化建议）...\n")
url = f"{ENDPOINT}/openai/deployments/{MODEL}/chat/completions?api-version={API_VERSION}"
resp = requests.post(url,
    headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"},
    json={"messages": [{"role": "user", "content": prompt}], "temperature": 0.7, "max_completion_tokens": 6000},
    timeout=300)
resp.raise_for_status()
text = resp.json()["choices"][0]["message"]["content"]
print(text)

out = os.path.join(OUTPUT_DIR, "双平台脚本_v4.md")
with open(out, "w", encoding="utf-8") as f:
    f.write("# 双平台脚本 v4 — AI抢走新人岗位（场景化建议版）\n\n")
    f.write(text)
    f.write("\n")
print(f"\n✅ 已保存到 {out}")
