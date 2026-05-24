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

MATERIAL = open(r"output\archive\本周脚本_AI人才断层悖论_v2.5.md", "r", encoding="utf-8").read()

review_request = f"""你是一个资深短视频内容运营专家，同时精通 TikTok 和抖音的内容策略、算法逻辑和用户心理。

以下是我目前的双平台口播脚本（v2.5版）：

{MATERIAL}

---

这个脚本有两个严重问题，我需要你帮我重写：

## 问题 1：车轱辘话
核心观点"AI 抢走了新人变强的机会/学习路径"被换词重复了至少 4-5 次：
- Hook: "先抢走了新人变强的机会"
- 主体2: "入口被AI吃掉了"
- 情绪峰值: "连练级机会都不给了"
- 结尾: "人成长为高手的那条路"
- 英文版同样: "replacing the learning path" → "remove the training ground" → "enough reps to become great"

同一个意思转了三四圈，观众会觉得内容空洞。

## 问题 2：缺乏建设性
整条视频的逻辑是：问题 → 问题的解释 → 问题的情绪放大 → 问题的再次重复 → 你怎么看？
观众看完只觉得"哦好可怕"，但没有获得感。唯一的新信息（"初级岗少了，高级人才更贵了"这个悖论）只用了两句话带过。

## 重写要求

请按以下结构重写，每层都是新信息，不要重复前面说过的话：

### 结构（层层递进，每段都给新东西）：
1. **Hook（5秒）**：抛出悖论，只说一次，之后不再重复
2. **机制（15-20秒）**：具体怎么断的？不要用"入口没了"这种抽象话，举具体的岗位/场景例子（比如初级开发者以前靠改bug学架构，现在AI写代码他连改的机会都没有）
3. **悖论展开（15-20秒）**：省钱变花钱，展开讲，不是一句带过。为什么高级人才更贵？AI 犯错的特点是什么？为什么需要经验丰富的人？
4. **怎么办（10-15秒）**：给一个明确、具体的方向，不要空喊"提升判断力"，要说清楚具体做什么
5. **CTA（5-10秒）**

### 硬性要求：
- 抖音中文版：400-450字，75-90秒
- TikTok英文版：155-175 words，60-72秒
- 英文要口语化，像聪明朋友聊天，不要新闻腔
- 中文要人话，不要学术术语
- 每一段都必须有前一段没有的新信息
- 可以轻量提 Bloomberg 等信源做背书，但不要硬塞
- 保留录制提示和发布素材（标题×3、hashtags、发布时间）

请直接输出完整的重写版脚本，不需要分析过程。
"""

print("正在调用 GPT-5.4 重写脚本 v3...\n")
try:
    response = client.chat.completions.create(
        model="gpt-5-4",
        messages=[
            {"role": "system", "content": "你是资深短视频内容创作者，精通 TikTok 和抖音的口播脚本写作。你的风格是“聪明朋友跟你聊天”，不是播新闻也不是上课。脚本部分 TikTok 用口语化英文、抖音用人话中文。"},
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
output_path = r"output\GPT5_脚本_v3.md"
import os
os.makedirs("output", exist_ok=True)
with open(output_path, "w", encoding="utf-8") as f:
    f.write("# GPT-5.4 脚本 v3 重写\n\n")
    f.write(result)
print(f"\n\n✅ 已保存到: {output_path}")
