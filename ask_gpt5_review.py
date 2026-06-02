# -*- coding: utf-8 -*-
"""快速调用 GPT-5 审阅素材是否足够"""
import sys, subprocess, json
from openai import AzureOpenAI

ENDPOINT = "https://rednote-openai-gpt41.openai.azure.com/"
API_VERSION = "2024-12-01-preview"
MODEL = "gpt-5-4"

# 直接用 az cli 获取 token，避免 AzureCliCredential 挂起
print("获取 Azure AD token...")
result = subprocess.run(
    ["az", "account", "get-access-token", "--resource", "https://cognitiveservices.azure.com"],
    shell=True,
    capture_output=True, text=True, timeout=30
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

MATERIAL = r"""
📄 文章 1：
* 标题：黄仁勋批CEO将裁员归咎AI，称说法太敷衍
* 来源：36氪 / 观察者网 / 每日经济新闻
* 发布日期：2026年5月25日 - 5月27日
* 核心信息：
  1. 黄仁勋在新加坡CNA 50分钟专访中，公开炮轰把裁员甩锅AI的CEO
  2. 揭穿时间线漏洞——生成式AI过去6个月才有规模化生产力，但裁员两年前就开始了
  3. 指出部分高管这么做纯粹为了"听起来很专业很聪明"，掩盖经营不善
  4. 重申普通人不会输给AI，只会输给更懂AI的竞争对手
* 数据亮点：50分钟专访一句财报芯片参数没提，全聚焦打工人饭碗
* 金句："把AI与裁员连结在一起的说法实在太懒惰了……一些主管这么说只是想让自己听起来很专业、很聪明，我真的很讨厌这样，这是很不负责任的。"

📄 文章 2：
* 标题：老板裁员最锋利的刀！科技行业一季度狂裁8万人：50%因为AI
* 来源：快科技 / 日经亚洲（Nikkei Asia）
* 发布日期：2026年4月9日
* 核心信息：
  1. 2026年前4个月全球科技行业78,557人被裁，37,638个岗位归因于AI（47.9%）
  2. 甲骨文3月底突袭裁员3万人（占全球1/5），凌晨3点切断权限
  3. 高知特首席AI官拆穿：多数裁员与AI实际生产力提升无关，是低利率时期过度招聘的修正
  4. OpenAI CEO奥特曼也承认行业存在严重"AI洗白（AI-Washing）"
* 数据亮点：47.9%岗位消失归咎AI，但专家指出AI真正颠覆性生产力跃迁至少还需6个月-1年
* 金句：高知特首席AI官："从财务和讨好资本市场角度看，AI成了完美的替罪羊。"

📄 文章 3：
* 标题：当硅谷用AI"洗白"裁员决策，"岗位消失论"是一场幻觉吗？
* 来源：证券时报 / 第一财经
* 核心信息：
  1. 定义"AI洗白式裁员"：和Greenwashing一样，把传统裁员包装成科技转型
  2. 资本市场荒谬闭环：说亏钱裁员股价跌，说AI转型裁员股价涨6%（如Snap案例）
  3. 底层岗位确实有真实替代：初级代码、基础客服等领域AI已有自动化替代效应
  4. IBM CEO承认这更像对前几年"暴饮暴食式过度招聘"的自然修正
* 数据亮点：IBM 2026年入门级AI岗位招聘规模扩大三倍，岗位不是消失而是结构换血
* 金句："当前许多裁员实质上是将传统重组包装成AI驱动的创新"
"""

SYSTEM_PROMPT = """你是一个资深短视频内容运营专家，同时精通 TikTok（海外英文60-90秒）和抖音（国内中文1-3分钟）的科技/AI 口播内容。

你的任务是审阅博主收集的素材，评估是否足够支撑一期双平台视频（TikTok 英文版 + 抖音中文版），并给出具体建议。"""

USER_PROMPT = f"""我准备做一期关于"AI洗白式裁员"的双平台口播视频（TikTok 英文 60-90秒 + 抖音中文 1-3分钟）。

以下是我收集的三篇核心素材：

{MATERIAL}

请从以下维度帮我评估：

1. **素材充足度**：这些素材是否足够支撑 TikTok 60-90秒 + 抖音 1-3分钟？哪些部分信息量溢出可以砍？哪些部分还薄弱？

2. **事实硬度**：哪些数据/案例足够硬可以直接用？哪些需要额外核实或加注？有没有潜在的事实风险？

3. **双平台适配**：
   - TikTok 英文版应该聚焦哪个核心冲突点？
   - 抖音中文版应该怎么切入才能让国内打工人产生代入感？
   - 两个版本的叙事重心应该怎么差异化？

4. **缺失素材建议**：还需要补充什么？特别是国内大厂的对照案例（阿里、腾讯、字节等用"业务聚焦""组织架构优化"等委婉说法的裁员案例）。

5. **风险评估**：这个话题在两个平台分别有什么审核/敏感风险？怎么规避？

请直接给出可操作的建议，不要客套。"""

print("正在调用 GPT-5.4 审阅素材...\n")
response = client.chat.completions.create(
    model=MODEL,
    messages=[
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": USER_PROMPT},
    ],
    temperature=0.4,
    max_completion_tokens=4000,
)

result = response.choices[0].message.content
print(result)

# 保存结果
out_path = r"c:\repos\red_note_project_v5 口播\output\AI裁员洗白\GPT5_素材审阅.md"
import os
os.makedirs(os.path.dirname(out_path), exist_ok=True)
with open(out_path, "w", encoding="utf-8") as f:
    f.write(f"# GPT-5.4 素材审阅 — AI洗白式裁员\n\n{result}\n")
print(f"\n✅ 已保存到 {out_path}")
