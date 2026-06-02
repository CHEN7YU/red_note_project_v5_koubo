"""用 Playwright 截图 cards_tau.html 的 8 张卡片"""
import os
from playwright.sync_api import sync_playwright

html_path = os.path.abspath(r"output\cards_tau.html")
out_dir = os.path.abspath(r"output\images_tau")
os.makedirs(out_dir, exist_ok=True)

cards = [
    ("tk1", "TK1_core_concept"),
    ("tk2", "TK2_city_metaphor"),
    ("tk3", "TK3_logic_folding"),
    ("dy1", "DY1_hook"),
    ("dy2", "DY2_house_road_metaphor"),
    ("dy3", "DY3_comparison"),
    ("dy4", "DY4_results_timeline"),
    ("cover-tk", "Cover_TikTok"),
    ("cover-dy", "Cover_Douyin"),
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

print(f"\n全部完成，保存在: {out_dir}")
