"""生成3个TikTok封面 + 推送封面、视频、hashtags到Telegram"""
import os, requests
from playwright.sync_api import sync_playwright

# === 1. 截图3个封面 ===
html_path = os.path.abspath(r"output\华为τ定律\TikTok\covers.html")
out_dir = os.path.abspath(r"output\华为τ定律\TikTok")

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page(viewport={"width": 1200, "height": 2000})
    page.goto(f"file:///{html_path}", wait_until="networkidle")
    page.wait_for_timeout(2000)
    for cid, fname in [("cover-a", "CoverA_suspense"), ("cover-b", "CoverB_versus"), ("cover-c", "CoverC_news")]:
        el = page.locator(f"#{cid}")
        path = os.path.join(out_dir, f"{fname}.png")
        el.screenshot(path=path, timeout=60000)
        print(f"✅ {fname}.png")
    browser.close()

# === 2. 推送到 Telegram ===
TOKEN = "8215333535:AAHQFfKtFNvdEKt0NS5q-1ggaDOpB43nYPE"
CHAT_ID = "8483451023"
BASE = f"https://api.telegram.org/bot{TOKEN}"

def send_photo(path, caption=""):
    with open(path, "rb") as f:
        r = requests.post(f"{BASE}/sendPhoto", data={"chat_id": CHAT_ID, "caption": caption}, files={"photo": f})
    print(f"📸 Photo: {r.status_code} - {os.path.basename(path)}")

def send_video(path, caption=""):
    with open(path, "rb") as f:
        r = requests.post(f"{BASE}/sendVideo", data={"chat_id": CHAT_ID, "caption": caption}, files={"video": f})
    print(f"🎬 Video: {r.status_code} - {os.path.basename(path)}")

def send_msg(text):
    r = requests.post(f"{BASE}/sendMessage", data={"chat_id": CHAT_ID, "text": text, "parse_mode": "Markdown"})
    print(f"💬 Message: {r.status_code}")

# 推封面
for fname, label in [("CoverA_suspense", "Cover A — Suspense"), ("CoverB_versus", "Cover B — Versus"), ("CoverC_news", "Cover C — News")]:
    send_photo(os.path.join(out_dir, f"{fname}.png"), f"🎨 {label}")

# 推视频
video_path = os.path.join(out_dir, "output.mp4")
if os.path.exists(video_path):
    send_video(video_path, "🎬 TikTok τ Law — Draft")
else:
    print(f"⚠️ Video not found: {video_path}")

# 推 hashtags + 描述
send_msg("""*TikTok — Huawei τ Law*

📝 *Caption:*
Huawei just introduced "Tau Law" — a new way to think about chip progress as Moore's Law slows down. Instead of only making things smaller, make signals take shorter, faster paths. Logic Folding is the easiest part to picture.

*#️⃣ Hashtags:*
#TauLaw #MooresLaw #Huawei #ChipTech #LogicFolding

🕖 *Best posting:* Weekdays 6:30-9PM / Weekends 12-2PM or 7-10PM""")

print("\n✅ All done!")
