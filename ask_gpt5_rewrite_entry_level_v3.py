# -*- coding: utf-8 -*-
"""GPT-5 改写双平台脚本 v3 — 修正 Codex 表述 + 加建设性结尾"""
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

# 读取 v2 脚本
with open(os.path.join(OUTPUT_DIR, "双平台脚本_v2.md"), "r", encoding="utf-8") as f:
    v2 = f.read()

prompt = """以下是 TikTok 英文 + 抖音中文的双平台口播脚本 v2。用户有两个重要修改意见：

## 修改意见 1：Codex 不是行业领先者，要改成更全面的 AI 编程工具格局

脚本 v2 过度强调 OpenAI Codex（400万周活、非程序员占20%），但事实上 Codex 在 AI 编程工具里远不是唯一玩家，甚至不一定是最强的。目前 AI 编程工具的格局是多家竞争：

**Claude Code（Anthropic）实际案例数据：**
- Stripe 把 Claude Code 部署给了 1,370 名工程师，一个团队用 Claude Code 4 天完成了 10,000 行 Scala 转 Java 的迁移，原本预估需要 10 个工程师-周
- Wiz 用 Claude Code 20 小时把 50,000 行 Python 迁移到 Go，原本预估 2-3 个月
- Rakuten（乐天）把新功能交付时间从 24 个工作日缩短到 5 天，工程师现在并行跑多个 Claude Code session
- Ramp 用 Claude Code 把事故调查时间缩短了 80%，非工程团队（销售、风控、财务）现在直接用自然语言查数据仓库，不用写 SQL
- Anthropic 自己说："the majority of code is now written by Claude Code"（大部分代码现在是 Claude Code 写的）
- Claude Code 已经不只是给程序员用的——PM、创始人、设计师、运营团队都在用它直接造东西

**其他 AI 编程工具：**
- GitHub Copilot（微软/OpenAI）
- Cursor（用 Claude 和 GPT 模型）
- Devin（自主编程 Agent）
- Google Gemini Code Assist

**修改方向：**
不要只讲 Codex。改成讲"AI 编程/AI Agent 工具整体正在改变谁写代码、谁做工作"。可以同时举 Codex 的非程序员增长数据和 Claude Code 的企业案例，说明这不是某一家公司的事，而是整个行业的趋势。这样更有说服力，也避免给 OpenAI 免费打广告。

## 修改意见 2：结尾缺建设性意见，听众听完觉得"完了没出路"

现在的脚本结尾只是抛出问题让评论区讨论，但听众（尤其应届生和职场新人）听完会觉得焦虑又绝望。

需要在结尾加一段**具体可操作的建议**（30秒左右），让观众觉得"虽然形势严峻，但我知道该怎么做了"。

建议方向（供参考，你来组织语言）：
1. **主动做 AI 的"副驾驶"而不是等着被替代** — 现在就开始用 AI 工具做项目，不要等公司教你
2. **用 AI 工具自己造作品集** — 既然企业不给练级机会，就自己给自己造练级场。用 Claude Code / Cursor / Copilot 做 side project，这就是你的新"实习经历"
3. **从"执行者"跳到"编排者"** — 不要只学怎么干活，学怎么定义问题、判断结果、同时管多个 AI
4. **一人公司/Solopreneur** — 利用 AI 工具直接做产品，跳过"先给别人打工积累经验"这条老路

## 通用要求：
- 保持口语化（v2 的语气不要变回书面语）
- 保持两个版本的差异化（TikTok vs 抖音的受众差异）
- TikTok 版控制在 70-100 秒（加了建议部分会稍长一点，但不要超过 100 秒）
- 抖音版控制在 2-3 分钟
- 保留表演提示标注
- 直接输出完整 v3 脚本（含脚本数据、录制建议、发布素材、两版差异说明），不需要解释改了什么
- 保持原来的输出格式

v2 脚本：
""" + v2

print("正在调用 GPT-5 生成 v3（修正 Codex + 加建设性结尾）...\n")
url = f"{ENDPOINT}/openai/deployments/{MODEL}/chat/completions?api-version={API_VERSION}"
resp = requests.post(url,
    headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"},
    json={"messages": [{"role": "user", "content": prompt}], "temperature": 0.7, "max_completion_tokens": 6000},
    timeout=300)
resp.raise_for_status()
text = resp.json()["choices"][0]["message"]["content"]
print(text)

out = os.path.join(OUTPUT_DIR, "双平台脚本_v3.md")
with open(out, "w", encoding="utf-8") as f:
    f.write("# 双平台脚本 v3 — AI抢走新人岗位（修正AI工具格局 + 建设性结尾）\n\n")
    f.write(text)
    f.write("\n")
print(f"\n✅ 已保存到 {out}")
