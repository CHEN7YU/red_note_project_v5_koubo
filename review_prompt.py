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
以下是GPT-5.4生成的双平台脚本原稿，以及一位资深短视频运营专家给出的详细反馈。请评估这些修改建议是否值得采纳。

===== 原始 TikTok 英文脚本（199 words / 78秒）=====

[HOOK - 前3秒]
Companies thought AI would let them fire junior employees and save money. Instead, they're paying *more* for senior people to clean up AI mistakes.

[BODY]
That's the hiring paradox nobody talks about.
More than 43% of companies say they plan to cut entry-level roles this year. In tech, 74% of CEOs have already frozen or reduced junior hiring.

Sounds efficient, right? AI writes the first draft, AI does the admin, AI handles the basic analysis.
But those "basic" jobs used to be the training ground. They were the first rung on the ladder. Remove that rung, and five years later you don't have enough people with judgment.

And judgment is the one thing AI can't mass-produce.
In IT, AI is already doing around 40% of basic coding work. So companies are rebuilding teams around verification, architecture decisions, and accountability.
Translation: fewer cheap juniors, more expensive seniors.

One report showed an AI-transformed 100-person engineering team can push average labor cost from $25,000 to $58,000 per person.
Why? Because catching one bad AI assumption buried six layers deep is not a 6-week bootcamp skill. That takes years.

[TWIST]
Here's the real risk: companies aren't just cutting jobs. They're cutting the apprenticeship system that created future managers, future experts, future leaders.
The insurance industry alone has 400,000 senior workers nearing retirement in the US. If AI blocks the entry path now, who replaces them later?

[CTA]
So what happens next: do companies bring back junior roles in a new form, or are we heading into a massive "no experience, no talent pipeline" crisis?
Drop your take below.

===== 原始抖音中文脚本（531字 / 2分08秒）=====

[HOOK]
AI最先替代的，不一定是最贵的人。但最后最贵的代价，可能是企业自己来付。

[引入]
现在很多公司都在干一件事：把初级岗位砍掉。
为什么？很简单。以前要招一批应届生做表格、写基础代码、整理材料、跑分析。现在老板一看，诶，这些活AI也能干，那我还招这么多人干嘛？

[干货1]
问题来了。初级岗位不只是"干杂活"的，它其实是一个 apprenticeship model，也就是"学徒式培养通道"。
很多知识型工作，根本不是上个6周培训班就能会的。你得先跟着资深员工打辅助，处理重复任务，慢慢学判断、学业务、学边界。
这个过程看起来低效，但它是企业培养未来骨干的唯一入口。

[干货2]
现在这个入口，正在被AI掐断。
有研究说，超过43%的企业计划今年削减初级岗位；科技行业里，74%的CEO已经冻结或者缩减了初级招聘。
表面上看，是省了人头。
但另一面是什么？AI把基础活做了，公司反而更需要高价的人来做 verification，也就是"验证"；做 architecture judgment，也就是"架构判断"；还要做 accountability，也就是"出了问题谁负责"。

[亮点/信息差]
这就出现了一个很反常识的结果：
老板本来想用AI裁掉底部70个初级员工省钱，最后发现，不得不花两倍薪资去招几个能"给AI擦屁股"的高级审核员。
而且这个高级审核员，不是速成班能培养出来的。
因为AI最危险的错误，往往不是特别蠢的错，而是"看起来对，其实底层假设错了六层"的那种错。这个靠经验，不靠提示词。

[与你的关系]
这事对中国人意味着什么？
第一，如果你是学生或者应届生，别再只卷"执行力"了。纯搬运、纯整理、纯基础产出，最容易被AI吃掉。你要尽快补的是判断力、表达能力、业务理解，还有和AI协作的能力。
第二，如果你是管理者，别只盯着短期降本。把初级岗位全砍了，三五年后你会发现，中层断档，老人退休，团队没人接班。
第三，国内很多行业也会遇到一样的问题：互联网、金融、咨询、运营、研发，都会出现"底层岗位变少，但高阶能力更贵"的倒挂。

[CTA]
AI时代，初级岗位会不会彻底消失？
还是说，它只是从"干活的人"变成"会用AI、会审AI的人"？
评论区聊聊，你觉得未来3年，最危险的入门岗是哪一种？关注我，下一条我可以继续讲：普通人怎么重新设计自己的"第一份工作"。

===== 运营专家给出的修改建议 =====

1. TikTok版评分 8.8/10，抖音版 9.2/10

2. 【TikTok版核心问题】信息密度偏高，太像"咨询报告"
   - 建议删掉：$25k→$58k、"six layers deep"、100-person engineering team detail
   - 建议强化情绪句，如："Companies removed the bottom rung of the ladder… then realized nobody could climb anymore."
   - 核心观点：TikTok要的是"制造顿悟感"而不是"解释趋势"

3. 【金句前置】建议把 "AI isn't replacing the job. It's replacing the learning path." 提前到前15秒，因为这是核心认知反转

4. 【抖音版核心问题】太长（531字/2分08秒），建议压缩到350-420字/55-90秒
   - apprenticeship model 解释重复，建议只留一句："很多知识型工作，本来就是靠'先打辅助，再学判断'成长起来的。"
   - 删掉过多英文术语翻译（verification/architecture judgment/accountability那段）

5. 【Hook优化建议】
   - 中文版改为："AI最危险的，不是抢工作。而是它正在让新人失去'成长为高手'的机会。" 然后接 "很多公司裁掉应届生后，最近发现一个问题：未来没人接班了。"
   - 英文版加一句："The scary part isn't losing the job. It's losing the chance to become good at anything."

6. 【人格化】两边都要更像"一个人突然意识到不对劲"，而不是"分析师讲趋势"

7. 【命运感强化】建议加一句："以前的问题是：你能力不够。现在的问题是：AI可能连你练级的机会都不给了。" — 预测会炸评论区

8. 【数据引用方式】不要说"research says"，改成"according to hiring surveys this year"更自然，且要准备来源截图
"""

review_request = f"""你是一个资深短视频内容运营专家，同时精通 TikTok 和抖音的内容策略、算法逻辑和用户心理。

我有一份双平台口播脚本（TikTok英文版 + 抖音中文版），以及一位运营专家给出的详细修改建议。

请你评估：
1. 这8条修改建议中，哪些你完全同意？哪些你有不同意见？
2. 有没有他漏掉的问题？
3. 如果让你来改，你会怎么改？请直接输出修改后的完整脚本（TikTok + 抖音两版）。

以下是原稿和修改建议：
{MATERIAL}

请输出：

## 一、对8条建议的逐条评估
（同意/部分同意/不同意 + 理由）

## 二、你发现的额外问题

## 三、修改后的完整脚本
（TikTok英文版 + 抖音中文版，含表演提示、字数、时长）
"""

print("正在调用 GPT-5.4 评估修改建议...\n")
try:
    response = client.chat.completions.create(
        model="gpt-5-4",
        messages=[
            {"role": "system", "content": "你是资深短视频内容运营专家，精通 TikTok 和抖音的算法、内容策略和用户心理。请用中文回答分析部分，脚本部分TikTok用英文、抖音用中文。"},
            {"role": "user", "content": review_request},
        ],
        temperature=0.5,
        max_completion_tokens=8000,
    )
except Exception as e:
    print(f"API 调用失败: {e}")
    sys.exit(1)

result = response.choices[0].message.content
print(result)

# 保存结果
output_path = r"output\GPT5_评估修改建议.md"
import os
os.makedirs("output", exist_ok=True)
with open(output_path, "w", encoding="utf-8") as f:
    f.write("# GPT-5.4 对修改建议的评估 + 修改后脚本\n\n")
    f.write(result)
print(f"\n\n✅ 已保存到: {output_path}")
