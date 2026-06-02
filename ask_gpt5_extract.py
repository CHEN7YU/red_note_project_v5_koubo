# -*- coding: utf-8 -*-
"""GPT-5 提炼要点 — TikTok 英文版（AI洗白式裁员）"""
import sys, subprocess, json
from openai import AzureOpenAI

ENDPOINT = "https://rednote-openai-gpt41.openai.azure.com/"
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

client = AzureOpenAI(
    azure_endpoint=ENDPOINT,
    azure_ad_token=token,
    api_version=API_VERSION,
)

# ── 已核实的英文原始信源 ──────────────────────────────────────

ENGLISH_SOURCES = r"""
## 已核实的英文原始信源

### Source 1: CNA (Channel NewsAsia)
- 标题: "'Lazy' narrative to connect AI to job cuts, says Nvidia boss Jensen Huang"
- 链接: https://www.channelnewsasia.com/business/ceo-job-cuts-lazy-ai-nvidia-jensen-huang-6140246
- 日期: 2026年5月25日（2 days ago）
- 内容: Jensen Huang 接受新加坡 CNA 专访，公开批评 CEO 们把裁员归咎于 AI 的做法是 "lazy" 和 "irresponsible"。指出生成式 AI 在过去 6 个月内才真正具备规模化生产力，裁员时间线和 AI 落地时间不匹配。

### Source 2: Nikkei Asia (核心数据源)
- 标题: "Nearly 80,000 tech jobs cut in Q1, but AI's full impact may be yet to come"
- 链接: https://asia.nikkei.com/business/technology/artificial-intelligence/nearly-80-000-tech-jobs-cut-in-q1-but-ai-s-full-impact-may-be-yet-to-come
- 作者: Yifan Yu
- 日期: 2026年4月8日
- 内容: 2026年Q1全球科技行业裁员 78,557 人。Cognizant（高知特）首席 AI 官指出，AI 的真正影响尚未完全显现。文章采访 Cognizant，该公司在旧金山和班加罗尔设立了 AI 实验室。

### Source 3: Nikkei Asia (最新黄仁勋表态)
- 标题: "Nvidia spending up to $150bn a year on Taiwan AI suppliers: Jensen Huang"
- 链接: https://asia.nikkei.com/business/technology/artificial-intelligence/nvidia-spending-up-to-150bn-a-year-on-taiwan-ai-suppliers-jensen-huang
- 作者: Lauly Li and Cheng Ting-Fang
- 日期: 2026年5月27日（今天）
- 内容: 黄仁勋在台北说 "AI is not the reason we are going to have layoffs. AI is the way we avoid it, so that we could be more successful."
- 补充: Nvidia 将在台湾的员工扩大到 4000 人（quadruple hiring）

### Source 4: Layoffs.fyi (实时追踪数据)
- 链接: https://layoffs.fyi/
- 2026年至今: 115,430 tech employees laid off, 152 tech companies with layoffs
- 维护者: Roger Lee (startup founder), 被 Bloomberg, WSJ, NYT 引用过

### Source 5: 中文二手报道汇总的关键事实点
- 黄仁勋原话（中文转述）: "把AI与裁员连结在一起的说法实在太懒惰了……一些主管这么说只是想让自己听起来很专业、很聪明，我真的很讨厌这样，这是很不负责任的。"
- 甲骨文3月底裁员（需额外核实具体数字，GPT-5审阅建议谨慎使用）
- 奥特曼提到 AI-Washing（需核实是否为原话）
- Snap 宣布AI裁员后股价涨6%（需核实具体日期）
- IBM 2026年入门级AI岗位招聘扩大三倍（需核实来源）

### GPT-5 素材审阅的关键提醒（已完成）
- 47.9% 不要说成"AI导致"，要说成"被归因为AI (framed as AI-related)"
- 甲骨文3万人数字没核实前不要上主文案
- 表达用 "many", "some", "framed as" 而非绝对化
"""

SYSTEM_PROMPT = """你是一个专业的 TikTok 科技/AI 口播内容策划。

你的任务是根据提供的英文原始信源，提炼出适合制作 TikTok 英文口播视频（60-90秒）的核心要点。

提炼原则：
1. 只用经过核实的事实，对存疑数据标注
2. 英文表达要适合口播，不要书面语
3. 用 "framed as" / "presented as" 而非 "caused by" 等绝对化表达
4. 重点突出冲突性和反常识感
5. 每个要点都标注出处"""

USER_PROMPT = f"""以下是我围绕"AI-Washing Layoffs（AI洗白式裁员）"话题收集的英文原始信源。
请帮我提炼出适合 TikTok 英文口播视频（60-90秒，约150-220 words）的核心要点。

{ENGLISH_SOURCES}

请按以下格式输出：

---
## 🎯 核心论点（一句话）
[这期视频要传达的核心信息]

## 📊 可用事实要点（按使用优先级排序）

### 必用（经过核实、最硬的事实）
1. [要点] — 出处: [来源]
2. ...

### 可用（有一定支撑但需谨慎表达）
1. [要点] — 出处: [来源] — ⚠️ 注意: [使用时的措辞建议]
2. ...

### 不建议用（风险高或未核实）
1. [要点] — 原因: [为什么不用]
2. ...

## 🪝 最强 Hook 候选（前3秒，3个选项）
1. [英文 hook]
2. [英文 hook]
3. [英文 hook]

## 🔄 核心反转/Twist
[视频中间段的反常识反转点是什么]

## 💬 CTA / 评论区引导（2个选项）
1. [英文问题]
2. [英文问题]

## ⚠️ 需要额外核实的点
1. [什么需要核实] — 建议核实方式: [怎么查]
---"""

print("正在调用 GPT-5.4 提炼要点...\n")
response = client.chat.completions.create(
    model=MODEL,
    messages=[
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": USER_PROMPT},
    ],
    temperature=0.4,
    max_completion_tokens=4000,
)

result_text = response.choices[0].message.content
print(result_text)

# 保存
out_path = r"c:\repos\red_note_project_v5 口播\output\AI裁员洗白\GPT5_提炼要点_TikTok.md"
import os
os.makedirs(os.path.dirname(out_path), exist_ok=True)
with open(out_path, "w", encoding="utf-8") as f:
    f.write(f"# GPT-5.4 提炼要点 — TikTok 英文版（AI洗白式裁员）\n\n{result_text}\n")
print(f"\n✅ 已保存到 {out_path}")
