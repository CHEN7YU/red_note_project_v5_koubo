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

MATERIAL = open(r"output\本周脚本_华为τ定律.md", "r", encoding="utf-8").read()

ORIGINAL_SOURCE = r"""
## 华为韬(τ)定律 — 原始资料

### 来源
华为官网新闻稿：https://www.huawei.com/cn/news/2026/5/ieee-iscas-tau-scaling
发布时间：2026年5月25日

### 事件
在 IEEE 国际电路系统研讨会 ISCAS 2026（上海）上，华为何庭波发表主旨演讲"半导体新路径探索与实践"，发布了韬(τ)定律。

### 核心概念
韬(τ)定律提出以"时间(τ)缩微"替代"几何缩微"作为半导体与电子系统演进的新指导原则——通过逻辑折叠等创新技术，持续压缩信号传播时延，不断提升晶体管密度，从而实现半导体与电子系统的持续演进。

### 背景
近年来，主导半导体产业半个多世纪的摩尔定律正面临严峻的物理极限和经济效益双重挑战。面对晶体管几何缩微放缓，晶体管成本红利消退等发展困境，如何跨越传统工艺路径的局限，探索出一条全新的可持续演进路线，已成为全球半导体行业亟待攻克的共同难题。韬(τ)定律正是解答这一难题的方案。

### 技术层级
华为创新性地提出了"逻辑折叠(LogicFolding)"等核心技术，构建了贯穿器件、电路、芯片到系统层面的多层级协同优化体系。该体系以系统性降低时间常数τ为目标：
- 器件层面：通过优化晶体管和互连电阻及寄生电容，从物理底层最大限度缩微器件级时间常数τ
- 电路层面：通过逻辑折叠技术突破传统平面布局的物理边界，显著缩短关键路径的走线长度并有效降低信号传播的电阻和电容负载，实现晶体管密度和电路性能大幅提升
- 芯片层面：通过"软件、架构、芯片"的全栈软硬芯协同设计，基于实际工作负载实现指令流和数据流的细粒度控制，提高系统级并行度和效率
- 系统层面：定义灵衢总线，重构计算系统互联协议，实现超节点的统一内存编址和原生内存语义，大幅降低系统通信时延

### 实践成果
在过去六年的实践中，基于韬(τ)定律，华为已成功设计并量产了381款芯片，广泛覆盖了千行百业的需求。其中，将于2026年秋季面世的麒麟芯片，率先采用了逻辑折叠技术，性能大幅提升。预计到2031年，基于韬(τ)定律的高端芯片将实现重大性能突破。

### 何庭波原话
"未来一定属于开放合作。在半导体演进的路径上，没有一家企业可以独自完成所有答案。在韬(τ)定律的路径下，我们期待与全球科学家、工程师和产业伙伴紧密合作，共同推动半导体与电子产业持续发展。"

### 潜在的叙事角度（供参考）
1. 摩尔定律要"死"了 → 华为说"不用怕，换个思路继续进化"
2. 美国制裁 → 华为被逼出了一条新路 → 这条路可能比老路还好
3. "几何缩微"到头了 → "时间缩微"接棒 → 用类比解释（比如：不是把房子建得更小，而是让房子里的通道更短、效率更高）
4. 逻辑折叠 = 把电路从平面变成立体，像把一张纸折起来缩短距离
5. 381款芯片已量产 = 不是PPT定律，是已经在用的东西
"""

review_request = f"""你是一个资深短视频口播脚本改稿专家。你的任务是把下面的脚本改得更口语化、更像“聊天”，而不是“写文章”。

## 当前 v1 脚本
{MATERIAL}

## 原始资料（供你确认事实）
{ORIGINAL_SOURCE}

### 改稿要求

**重点改英文版，中文版也顺便改一下。**

#### 英文版（重点）：
1. **用短句。** 每句话不超过15个词。长句拆开。复合句改成简单句。
2. **别用书面语。** 把 "specifically" "efficiency" "obsessing" "insanely" 这类词换掉。用人说话的词。例如：
   - "Shrinking gets insanely expensive" → "Making stuff smaller? It costs a fortune now."
   - "stop obsessing only over size" → "quit trying to make everything tinier"
   - "better efficiency" → "runs way better"
3. **加比喻。** 每个技术概念边上加一个"你那个朋友一听就懂"的比喻。比如：
   - 逻辑折叠：像地铁站地图里加了一条换乘捷径，车还是那么大，但到站快了一倍
   - 时间缩微：像快递公司不是买更小的卡车，而是重新规划路线让送货更快
4. **节奏感。** 短-短-稍长-短。像说rap一样有节奏。不要每句话一样长。
5. **保持 155-175 words，不要超。**

#### 中文版：
1. 口语化程度已经不错，但可以再加几个不那么"科普腔"的表达
2. "时间常数"这个词换掉，普通人不懂
3. "几何尺寸"也尽量不用，用更白话的说法
4. 保持 400-450 字

#### 不要改的东西：
- 叙事结构、段落顺序不变
- 事实数据不变（381款、秋季麒麟、2031）
- 客观基调不变
- 录制提示、发布素材、标题、hashtags 等元数据可以微调但不用大改

请输出完整的 v2 脚本，格式和 v1 一样。只输出改好的脚本，不需要解释你改了什么。
"""

print("正在调用 GPT-5.4 改稿 v2（更口语化）...\n")
try:
    response = client.chat.completions.create(
        model="gpt-5-4",
        messages=[
            {"role": "system", "content": "你是资深短视频口播脚本改稿专家。你的任务是把脚本改得更口语化，尤其英文版。英文用短句、生动比喻、口语化用词。中文用人话，不要科普腔。"},
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
output_path = r"output\本周脚本_华为τ定律_v2.md"
import os
os.makedirs("output", exist_ok=True)
with open(output_path, "w", encoding="utf-8") as f:
    f.write("# 本周双平台脚本 — 华为韬(τ)定律 (v2 口语化)\n\n")
    f.write(result)
print(f"\n\n✅ 已保存到: {output_path}")
