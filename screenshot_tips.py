"""截图新增的录制提示卡片"""
import os
from playwright.sync_api import sync_playwright

html_path = os.path.abspath(r"output\华为τ定律\cards_tau.html")
out_dir = os.path.abspath(r"output\华为τ定律")

cards = [
    ("tips-tk", "Tips_TikTok"),
    ("tips-dy", "Tips_Douyin"),
]

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page(viewport={"width": 1200, "height": 2000})
    page.goto(f"file:///{html_path}", wait_until="networkidle")
    page.wait_for_timeout(2000)

    for card_id, filename in cards:
        el = page.locator(f"#{card_id}")
        path = os.path.join(out_dir, f"{filename}.png")
        el.screenshot(path=path, timeout=60000)
        print(f"✅ {filename}.png")

    browser.close()

print("Done!")
