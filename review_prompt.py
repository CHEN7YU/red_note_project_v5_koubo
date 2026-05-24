"""发送双平台选题 Prompt 给 GPT-5.4 审阅，获取改进建议"""
import sys, httpx
from openai import AzureOpenAI
from azure.identity import AzureCliCredential, get_bearer_token_provider

credential = AzureCliCredential(process_timeout=30)
token_provider = get_bearer_token_provider(
    credential, "https://cognitiveservices.azure.com/.default"
)

# 先测试 token 是否有效
print("正在获取 Azure AD token...")
try:
    test_token = token_provider()
    print(f"Token 获取成功 (长度: {len(test_token)})")
except Exception as e:
    print(f"Token 获取失败: {e}")
    print("请先运行: az login")
    sys.exit(1)

client = AzureOpenAI(
    azure_endpoint="https://rednote-openai-gpt41.openai.azure.com/",
    azure_ad_token_provider=token_provider,
    api_version="2024-12-01-preview",
    timeout=httpx.Timeout(180.0, connect=30.0),
)

# 读取双平台选题 Prompt（保留备用）
# with open(r"Prompts\双平台通用\01_选题.md", "r", encoding="utf-8") as f:
#     prompt_content = f.read()

MATERIAL = r"""
===== 当前 v2 抖音中文脚本（395字 / 70-85秒）=====
""" + open(r"output\本周脚本_AI人才断层悖论.md", "r", encoding="utf-8").read() + r"""

===== 新的修改建议（来自另一位 AI 顾问的反馈）=====

核心观点：应该用更权威的信源来增强说服力，并重构脚本结构。

1. 【信源升级】之前的素材来自二手快讯聚合站（Startup Fortune、DoNews），权威性不够。建议改用真正顶级信源：
   - Bloomberg 报道 IBM CEO 暂停招聘 AI 能替代的岗位（约30%非面向客户岗位）
   - Wired/TechCrunch 讨论 "The End of the Junior Developer"
   - Harvard Business Review 的"认知学徒制"(Cognitive Apprenticeship) 崩溃论

2. 【视觉背书】建议在视频中贴出 Bloomberg、Wired、HBR 的真实新闻截图，建立权威感

3. 【脚本重构建议】把抖音版改成 1.5-2 分钟，结构改为：
   - Hook（0-20秒）：直接放 Bloomberg IBM 截图 + "这不是贩卖焦虑"
   - 现象揭秘（20-50秒）：Wired "初级开发者终结" + 金字塔对比
   - 深度升华（50-90秒）：HBR "认知学徒制崩溃" 概念
   - 结尾转化（90-120秒）：从执行者到审核员的破局方案

4. 【关键金句】
   - "IBM 的 CEO 已经公开扣动了扳机：直接叫停 30% 可以被 AI 替代的岗位招聘"
   - "5 年后的高级专家从哪儿来？总不能从石头里蹦出来吧？"
   - "企业为了眼前的降本增效，亲手把年轻人向上攀爬的阶梯给砍断了"

5. 【CTA 改变】从"评论区聊聊"改为"点赞收藏+转给正在找工作的朋友"
"""

review_request = f"""你是一个资深短视频内容运营专家，同时精通 TikTok 和抖音的内容策略、算法逻辑和用户心理。你也对新闻素养和信源可信度有深入理解。

我有一份已经经过两轮优化的双平台口播脚本（v2版），现在收到了第三轮修改建议。这次的建议主要围绕"信源权威性升级"和"脚本结构重构"。

请你从以下角度评估这些建议是否值得采纳：

{MATERIAL}

请逐条分析：

## 一、信源升级建议的评估
1. IBM CEO 暂停招聘的 Bloomberg 报道——这个素材是否适合口播？引用时有什么风险（比如时效性、是否可能被误读）？
2. Wired "The End of the Junior Developer"——这个概念是否真实存在？用在口播中是否合适？
3. HBR "认知学徒制"——这个概念是否适合抖音/TikTok 观众？会不会太学术？

## 二、脚本结构重构的评估
1. 当前 v2 是 70-85 秒，建议改为 1.5-2 分钟。这个时长变化对完播率有什么影响？
2. 新结构（Hook→现象→HBR理论→破局方案）vs 旧结构（Hook→现象→情绪峰值→CTA），哪个更适合抖音/TikTok？
3. 新版增加了"普通人破局方案"段落，这是加分还是减分？

## 三、具体执行风险
1. 在视频中贴 Bloomberg/Wired/HBR 截图是否有版权风险？
2. 引用 IBM CEO 的具体数字（30%）是否需要核实？如果数字有出入怎么办？
3. "认知学徒制"这个词在抖音上是否会让观众觉得"太装"？

## 四、最终建议
综合考虑，你认为应该：
A. 全部采纳，按新版重写
B. 部分采纳，在 v2 基础上微调（具体说明保留哪些、改哪些）
C. 不采纳，v2 已经足够好

如果选 B，请输出修改后的完整脚本（抖音中文版 + TikTok英文版）。
"""

print("正在调用 GPT-5.4 评估脚本修改建议...\n")
try:
    response = client.chat.completions.create(
        model="gpt-5-4",
        messages=[
            {"role": "system", "content": "你是资深短视频内容运营专家，精通 TikTok 和抖音的算法、内容策略、用户心理和新闻素养。请用中文回答分析部分，脚本部分TikTok用英文、抖音用中文。"},
            {"role": "user", "content": review_request},
        ],
        temperature=0.5,
        max_completion_tokens=16000,
    )
except Exception as e:
    print(f"API 调用失败: {e}")
    sys.exit(1)

result = response.choices[0].message.content
print(result)

# 保存结果
output_path = r"output\GPT5_脚本修改评估_v3.md"
import os
os.makedirs("output", exist_ok=True)
with open(output_path, "w", encoding="utf-8") as f:
    f.write("# GPT-5.4 第三轮脚本修改建议评估\n\n")
    f.write(result)
print(f"\n\n✅ 已保存到: {output_path}")
