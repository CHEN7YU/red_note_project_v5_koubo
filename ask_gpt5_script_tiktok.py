# -*- coding: utf-8 -*-
"""GPT-5 写 TikTok 英文脚本 — AI洗白式裁员（使用 requests 直调 REST API）"""
import sys, subprocess, json, os, requests

ENDPOINT = "https://rednote-openai-gpt41.openai.azure.com"
API_VERSION = "2024-12-01-preview"
MODEL = "gpt-5-4"

print("获取 Azure AD token...")
result = subprocess.run(
    ["az", "account", "get-access-token", "--resource", "https://cognitiveservices.azure.com"],
    shell=True, capture_output=True, text=True, timeout=30
)
if result.returncode != 0:
    print(f"az 获取 token 失败: {result.stderr}")
    sys.exit(1)
token = json.loads(result.stdout)["accessToken"]
print("Token OK")

def chat(messages, temperature=0.7, max_tokens=4000):
    url = f"{ENDPOINT}/openai/deployments/{MODEL}/chat/completions?api-version={API_VERSION}"
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    body = {"messages": messages, "temperature": temperature, "max_completion_tokens": max_tokens}
    resp = requests.post(url, headers=headers, json=body, timeout=180)
    resp.raise_for_status()
    return resp.json()["choices"][0]["message"]["content"]

EXTRACTED_POINTS = r"""
## 核心论点
A lot of tech layoffs are being presented as "AI-related," but Jensen Huang argues that explanation is often too convenient — because the timing of many cuts doesn't cleanly match when generative AI became truly usable at scale.

## 必用事实（经过核实）
1. Jensen Huang said connecting layoffs to AI is a "lazy" and "irresponsible" narrative. — CNA, May 25, 2026
2. Huang said generative AI has only become meaningfully productive at scale in roughly the last six months, suggesting some layoff timelines do not neatly line up with AI deployment. — CNA, May 25, 2026
3. Nikkei Asia reported 78,557 tech jobs were cut globally in Q1 2026. — Nikkei Asia, Apr 8, 2026
4. Nikkei also reported that AI's full labor impact may still be ahead, citing Cognizant's chief AI officer. — Nikkei Asia, Apr 8, 2026
5. Huang later said in Taipei: "AI is not the reason we are going to have layoffs. AI is the way we avoid it, so that we could be more successful." — Nikkei Asia, May 27, 2026
6. Nvidia is expanding in Taiwan, with plans to grow local headcount to 4,000. — Nikkei Asia, May 27, 2026
7. Layoffs.fyi tracks 115,430 tech layoffs in 2026 YTD across 152 companies. — Layoffs.fyi

## 可用但需谨慎表达
- Some companies appear to frame restructuring in AI terms even when the timeline is more complicated. 用 "framed as" / "presented as"
- The bigger disruption from AI may still be coming. 用 "may be yet to come"
- Nvidia's expansion as contrast: while some cut jobs citing AI, Nvidia presents AI as a hiring driver. 不要泛化

## 不能用（未核实）
- Oracle 3万人裁员数字
- 奥特曼 AI-washing 原话
- Snap 股价涨6%
- IBM 三倍招聘
- "47.9% caused by AI" 这种绝对归因

## 最强 Hook 候选
1. "What if 'AI layoffs' are being used as a cover story?"
2. "Nvidia's CEO just called the AI layoff narrative 'lazy.'"
3. "AI is getting blamed for layoffs before AI is fully rolled out."

## 核心反转
AI may be the headline, but not always the real timeline. Some cuts may be more about broader restructuring, cost pressure, or investor messaging than immediate AI replacement.

## CTA 候选
1. "Do you think companies are using AI as an excuse for layoffs — or just saying the quiet part out loud?"
2. "If AI's biggest job impact is still ahead, are we early… or already late?"
"""

SYSTEM_PROMPT = """你是一个 TikTok 爆款口播脚本作家。你的视频风格是：
- 一个人面对镜头，快节奏讲科技资讯
- 语气像在跟朋友聊天，不是读新闻
- 每句话都有信息量，零废话
- 标杆博主风格：类似 @techwithtim, @fireship 的节奏感

写作原则：
- 用 "framed as" / "presented as" 而非 "caused by" / "lied" 等绝对化表达
- 只用经过核实的事实
- 口语化英文，避免书面语"""

USER_PROMPT = f"""根据以下提炼好的要点，写一个 60-90 秒的 TikTok 英文口播脚本。

{EXTRACTED_POINTS}

脚本要求：
1. 总字数：150-220 words（对应 60-90 秒语速）
2. 开头 3 秒必须是 hook（让人停住不划走）
3. 不要用 "Hey guys", "What's up" 等陈旧开场
4. 每 2-3 句话要有一个"信息炸弹"（数据、对比、反转）
5. 结尾要有一个开放性问题，引导评论
6. 口语化英文，避免书面语
7. 标注 [停顿]、[加重语气]、[手势] 等表演提示

输出格式：
---
🎬 脚本：

[HOOK - 前3秒]
（表演提示）台词

[BODY - 主要内容]
（表演提示）台词

[TWIST/对比 - 转折点]
（表演提示）台词

[CTA - 结尾]
（表演提示）台词

---
📊 脚本数据：
- 总字数：xxx words
- 预估时长：xx 秒
- Hook 类型：[震惊/疑问/反常识/对比]

💡 录制建议：
- 语速：[快/中/慢]
- 情绪：[兴奋/严肃/惊讶]
- 建议画面：[是否需要屏幕截图/数据图]

🏷️ TikTok 发布素材：
- 标题选项 × 3（标注风格）
- Hashtags × 8-10
- 最佳发布时间（EST）
---"""

print("正在调用 GPT-5.4 写脚本...\n")
result_text = chat(
    messages=[
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": USER_PROMPT},
    ],
    temperature=0.7,
    max_tokens=4000,
)
print(result_text)

# 保存
out_path = r"c:\repos\red_note_project_v5 口播\output\AI裁员洗白\TikTok_脚本_v1.md"
import os
os.makedirs(os.path.dirname(out_path), exist_ok=True)
with open(out_path, "w", encoding="utf-8") as f:
    f.write(f"# TikTok 英文脚本 v1 — AI洗白式裁员\n\n{result_text}\n")
print(f"\n✅ 已保存到 {out_path}")
