# -*- coding: utf-8 -*-
"""GPT-5 一稿变两稿 — AI抢走新人岗位（TikTok英文 + 抖音中文）"""
import subprocess, json, os, requests

ENDPOINT = "https://rednote-openai-gpt41.openai.azure.com"
API_VERSION = "2024-12-01-preview"
MODEL = "gpt-5-4"
OUTPUT_DIR = r"c:\repos\red_note_project_v5 口播\output\AI抢走新人岗位"

os.makedirs(OUTPUT_DIR, exist_ok=True)

print("获取 Azure AD token...")
result = subprocess.run(
    ["az", "account", "get-access-token", "--resource", "https://cognitiveservices.azure.com"],
    shell=True, capture_output=True, text=True, timeout=30
)
if result.returncode != 0:
    print(f"az 获取 token 失败: {result.stderr}")
    raise SystemExit(1)
token = json.loads(result.stdout)["accessToken"]
print("Token OK")

def chat(messages, temperature=0.7, max_tokens=6000):
    url = f"{ENDPOINT}/openai/deployments/{MODEL}/chat/completions?api-version={API_VERSION}"
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    body = {"messages": messages, "temperature": temperature, "max_completion_tokens": max_tokens}
    resp = requests.post(url, headers=headers, json=body, timeout=300)
    resp.raise_for_status()
    return resp.json()["choices"][0]["message"]["content"]

# ── 素材要点 ──────────────────────────────────────────────────

EXTRACTED_POINTS = r"""
🎯 核心论点：
AI 没有大规模替代员工，但正在优先替代"新人阶段（beginner stage）"。企业不是在裁掉资深员工，而是在停止招聘和培养初级员工。真正断裂的不是岗位，而是职业成长阶梯（career ladder）。

📊 关键事实（按冲击力排序）：

1. OpenAI Codex 周活跃用户 400万+，非程序员用户占 20% 且增长速度是开发者的 3 倍。AI 首先冲击的不是程序员，而是助理、分析师、初级白领。（Axios, 2026-06-02）

2. 微软调研 20,000 名 AI 用户发现：员工角色正从"执行者（Author）"变成"编辑者（Editor）→ 指挥者（Director）→ 编排者（Orchestrator）"。49% AI 使用场景属于认知劳动，企业未来结构是"少量人管理大量 Agent"。（Microsoft Blog, 2026-05-05）

3. MIT 劳动经济学家 David Autor 团队研究发现：历史上每次技术革命都会为 30 岁以下大学毕业生创造新入口岗位，但 AI 可能第一次直接吃掉年轻人的入门工作。（MIT News, 2026-05-21）

4. ClickUp 裁掉 22% 员工，CEO 公开表示这不是成本削减而是 AI-first 重组。推出百万美元薪资带——用更少更强的人 + AI 替代大量中低级岗位。（TechCrunch, 2026-05-25）

5. Sam Altman、Dario Amodei 等 AI CEO 集体转向：2025 年大谈失业潮，2026 年开始强调 AI 提升生产力、不再强调失业。原因：社会反弹严重，Gen Z 成为最焦虑群体。（Business Insider, 2026-06-02）

🔥 社区最强观点（Reddit r/technology + r/cscareerquestions）：
- "AI is not replacing the entry-level job, it is replacing the entry-level learning path."
- "Remove the bottom of the ladder and there's no ladder anymore."
- "Everybody says: we'll just hire seniors from somewhere else. Nobody wants to be the somewhere else."
- "My manager told me they aren't renewing my junior contract because 'the API doesn't complain about working weekends.' I have a CS degree and I'm competing with a 10-cent token call."

💡 信息差亮点（国内很少报道）：
- 微软提出 Author → Editor → Director → Orchestrator 角色转型框架
- OpenAI Codex 定位已从"程序员工具"变成"知识工作操作系统"，首先冲击的是初级白领而非程序员
- AI 第一次可能阻断年轻人进入职业体系的入口（MIT 的核心担忧）

📈 故事线：
第一幕：OpenAI、微软推动 Agent 化办公（Axios + Microsoft）
→ 第二幕：AI 优先接管新人做的重复工作（Codex + Copilot）
→ 第三幕：企业停止培养新人（MIT + ClickUp）
→ 第四幕：职业阶梯开始断裂（Reddit 社区讨论）
→ 第五幕：AI CEO 开始改口（Business Insider）

🗣️ 可用金句：
- "AI doesn't replace the 10-year veteran; it replaces the 0-year graduate. We are burning the bottom rungs of the career ladder."
- "What declines is the amount of tactical, step-by-step execution work humans do themselves."
- "We aren't seeing a drop in productivity; we're seeing the total elimination of the 'apprentice' tier."
- "Knowledge workers now represent about 20 percent of users and are growing more than three times as fast."
"""

# ── Prompt ────────────────────────────────────────────────────

SYSTEM_PROMPT = """你是一个同时运营 TikTok 和抖音的科技博主的内容总监。
你需要根据同一份素材，同时产出两个版本的口播脚本。
两个版本不是互相翻译，而是根据不同平台和观众重新组织内容。

写作风格：
- TikTok：像 @fireship 或跟朋友快速聊科技的感觉，口语化英文，高密度快节奏
- 抖音：像半佛仙人的信息密度 + 何同学的亲和力，像在咖啡馆跟朋友分享重要消息
- 两个版本都要：零废话、每句有信息量、表演提示标注"""

USER_PROMPT = f"""根据以下提炼好的要点，同时输出两个版本的口播脚本：
- 版本 A：TikTok 英文脚本（60-90 秒）
- 版本 B：抖音中文脚本（1-3 分钟）

{EXTRACTED_POINTS}

关键差异化要求：

| 维度 | TikTok 英文版 | 抖音中文版 |
|------|-------------|-----------|
| 时长 | 60-90 秒（150-220 words） | 1-3 分钟（300-600 字） |
| Hook 风格 | 震惊/反常识 | 信息差/与你有关 |
| 信息密度 | 高密度快节奏 | 适中，有解释空间 |
| 举例方式 | 用海外公司/场景举例 | 用国内场景/公司类比 |
| 术语处理 | 英文术语直接用 | 英文术语+中文解释 |
| 争议角度 | 偏全球视角 | 偏"对中国人意味着什么" |
| CTA | 开放性问题 | 引导评论+关注 |

脚本通用要求：
1. 开头 3 秒必须是 hook（让人停住不划走）
2. 不要用 "Hey guys", "What's up", "大家好我是xxx" 等陈旧开场
3. 每 2-3 句话要有一个"信息炸弹"（数据、对比、反转）
4. 结尾引导评论互动
5. 标注 [停顿]、[加重语气]、[手势] 等表演提示
6. 口语化，不要书面语

输出格式：

## 🇺🇸 TikTok 英文版

🎬 脚本：
[HOOK - 前3秒]
（表演提示）台词

[BODY - 主要内容]
（表演提示）台词

[TWIST/对比 - 转折点]
（表演提示）台词

[CTA - 结尾]
（表演提示）台词

📊 字数：xxx words | 预估时长：xx 秒
Hook 类型：[震惊/疑问/反常识/对比]

💡 录制建议：
- 语速：
- 情绪：
- 建议画面：

🏷️ TikTok 发布素材：
- 标题选项 × 3（标注风格）
- Hashtags × 8-10
- 最佳发布时间（EST）

---

## 🇨🇳 抖音中文版

🎬 脚本：
[HOOK - 前3秒]
（表演提示）台词

[引入 - 背景交代]
（表演提示）台词

[干货1]
（表演提示）台词

[干货2]
（表演提示）台词

[信息差/亮点]
（表演提示）台词

[与你的关系]
（表演提示）台词

[CTA - 结尾]
（表演提示）台词

📊 字数：xxx 字 | 预估时长：x 分 xx 秒
Hook 类型：[震惊/疑问/反常识/信息差]
信息钩子数量：x 个

💡 录制建议：
- 语速：
- 情绪曲线：
- 是否需要画面切换/屏幕截图

🏷️ 抖音发布素材：
- 标题选项 × 3（标注风格）
- 话题标签 × 8-10
- 最佳发布时间（北京时间）

---

## 🔀 两版差异说明：
- Hook 不同在哪：
- 举例不同在哪：
- 结尾引导不同在哪：
- 预测哪边效果更好：
"""

# ── 执行 ──────────────────────────────────────────────────────

print("正在调用 GPT-5 生成双平台脚本...\n")
result_text = chat([
    {"role": "system", "content": SYSTEM_PROMPT},
    {"role": "user", "content": USER_PROMPT},
], temperature=0.7, max_tokens=6000)

print(result_text)

# 保存完整输出
out_path = os.path.join(OUTPUT_DIR, "双平台脚本_v1.md")
with open(out_path, "w", encoding="utf-8") as f:
    f.write("# 双平台脚本 v1 — AI抢走新人岗位\n\n")
    f.write(result_text)
    f.write("\n")
print(f"\n✅ 已保存到 {out_path}")
