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
📄 文章 1: CEOs plan to cut junior roles as AI reshapes hiring
来源: Startup Fortune (Oliver Wyman Forum), 2026-05-22
- AI 正在自动化传统入门级分析和行政岗位，这些岗位是中高级岗位的"训练场"
- 仅美国保险业就有40万资深员工即将退休，但底层补充通道已被AI掐断
- "非正式学徒制(informal apprenticeship model)"正处于崩溃边缘
- 金句: "Without those early rungs on the ladder, the informal apprenticeship model that has sustained the industry for generations is at risk."

📄 文章 2: AI加速替代初级岗位，青年就业压力加剧
来源: DoNews (奥纬咨询全球CEO研究), 2026-05-23
- 超过43%的企业计划今年削减初级岗位（比2025年翻倍）
- 科技行业中74%的CEO已冻结或缩减了初级岗位招聘
- 警告：裁员速度快于AI成熟应用和人才培养速度，将危及组织长期韧性

📄 文章 3: Re-engineering the IT pyramid
来源: Financial Express, 2026-05-19
- 传统IT"金字塔"正在倒转：AI承担了40%的基础代码工作
- 新时代需要"验证、架构判断和问责"，无法通过"校园大规模招聘+6周培训"速成
- 100人研发团队模型中，AI转型让人均用工成本从2.5万美元飙升至5.8万美元
- 金句: "You cannot train a thousand fresh graduates into the kind of judgement that catches a flawed AI-generated assumption embedded six layers deep... That takes years of domain experience."

📄 文章 4: 麻省理工AI专家警告：用自动化替代Z世代入门员工是"透支未来"
来源: 新浪财经/《财富》杂志, 2026-05-02
- MIT专家Andrew McAfee警告：从入口处压缩年轻人才招聘，会彻底破坏培养未来管理者的通道
- 学习复杂知识型工作的唯一方式是先给资深员工"打杂"处理常规事务
- 76%的Z世代已习惯使用独立AI工具，在所有世代中比例最高
- 金句: "If we over-automate these steps too quickly, we lose this apprentice ladder."

核心洞察：企业本意是用AI裁掉底部70个初级员工省钱，结果发现不得不花两倍薪资去高薪聘请能"给AI擦屁股"的高级审核员。
"""

review_request = f"""角色：你是一个同时运营 TikTok 和抖音的科技博主的内容总监。你的风格是：
- 一个人面对镜头，用聊天的语气讲干货
- 每句话都有信息量，零废话
- TikTok 标杆: @techwithtim, @fireship 的节奏感
- 抖音标杆: 半佛仙人的信息密度 + 何同学的亲和力

任务：根据以下素材，同时输出两个版本的口播脚本：
- 版本 A：TikTok 英文脚本（60-90 秒）
- 版本 B：抖音中文脚本（1-3 分钟）

两个版本不是互相翻译！是根据不同观众重新组织内容。

---
【素材】
{MATERIAL}
---

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

脚本要求：
- 开头 3 秒必须是 hook（黄金 3 秒留人）
- 不要用 "Hey guys"/"大家好我是xxx" 等开场
- 每 15-20 秒要有一个"信息钩子"（让人不舍得划走）
- 标注 [停顿]、[加重语气]、[手势]、[惊讶] 等表演提示
- 结尾要引导评论区讨论

输出格式：
---
## 🇺🇸 TikTok 英文版

🎬 脚本：
[HOOK - 前3秒]
（表演提示）台词

[BODY - 主要内容]
（表演提示）台词

[TWIST - 反转/对比]
（表演提示）台词

[CTA - 结尾]
（表演提示）台词

📊 字数：xxx words | 预估时长：xx 秒

---

## 🇨🇳 抖音中文版

🎬 脚本：
[HOOK - 前3秒]
（表演提示）台词

[引入 - 背景]
（表演提示）台词

[干货1]
（表演提示）台词

[干货2]
（表演提示）台词

[亮点/信息差]
（表演提示）台词

[与你的关系]
（表演提示）台词

[CTA - 结尾]
（表演提示）台词

📊 字数：xxx 字 | 预估时长：x 分 xx 秒

---

## 🔀 两版差异说明：
- Hook 不同在哪：
- 举例不同在哪：
- 结尾引导不同在哪：
- 预测哪边效果更好：

## 📌 两平台发布素材：

**TikTok：**
- 标题（3个版本）：
- Hashtags（15-20个）：
- Description：
- 最佳发布时间（EST）：

**抖音：**
- 标题（3个版本）：
- 话题标签（15-20个）：
- 视频简介：
- 最佳发布时间（北京时间）：

## 💡 录制建议：
- 语速建议：
- 情绪曲线：
- 是否需要屏幕截图/数据图：
"""

print("正在调用 GPT-5.4 生成双平台脚本...\n")
try:
    response = client.chat.completions.create(
        model="gpt-5-4",
        messages=[
            {"role": "system", "content": "你是同时运营 TikTok 和抖音的科技博主内容总监。TikTok 脚本用英文，抖音脚本用中文。脚本要口语化、有节奏感、有信息密度。"},
            {"role": "user", "content": review_request},
        ],
        temperature=0.6,
        max_completion_tokens=6000,
    )
except Exception as e:
    print(f"API 调用失败: {e}")
    sys.exit(1)

result = response.choices[0].message.content
print(result)

# 保存结果
output_path = r"output\本周脚本_AI人才断层悖论.md"
import os
os.makedirs("output", exist_ok=True)
with open(output_path, "w", encoding="utf-8") as f:
    f.write("# 本周双平台脚本 — AI 人才断层悖论\n\n")
    f.write(f"生成时间: 2026-05-24\n\n")
    f.write(result)
print(f"\n\n✅ 脚本已保存到: {output_path}")
