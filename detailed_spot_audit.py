import re

with open('/home/owen/tokyo/README.md', 'r', encoding='utf-8') as f:
    text = f.read()

# Collect all spots mentioned with markdown links or bold tags
print("=" * 80)
print(f"{'時段 / 項目':<20} | {'景點/餐廳標籤名稱':<35} | {'樓層/說明':<25} | {'導航狀態'}")
print("=" * 80)

days = re.split(r'##\s*\*\*📅\s*Day\s*(\d)', text)
for i in range(1, len(days), 2):
    day_num = days[i]
    day_content = days[i+1]
    sections = re.findall(r'(#{3,4}\s*\*\*[\d:：].*?\*\*)(.*?)(?=(?:#{3,4}\s*\*\*[\d:：]|\Z))', day_content, re.DOTALL)
    for title, body in sections:
        clean_title = re.sub(r'#{3,4}\s*\*\*', '', title).rstrip('*').strip()
        links = re.findall(r'\[\s*\*?\*?([^\*\]]+)\*?\*?\s*\]\((https?://[^\)]+)\)(\s*\([^\)]+\))?', body)
        for label, url, floor in links:
            if any(k in label for k in ["點此看", "介紹文", "藥妝攻略", "日本必掃", "文章", "菜單照片"]):
                continue
            floor_str = floor.strip() if floor else "-"
            has_nav = "✅ Place ID" if "query_place_id" in url else ("✅ ShortLink" if "goo.gl" in url or "share.google" in url else "✅ URL")
            print(f"Day {day_num} {clean_title[:14]:<14} | {label[:33]:<35} | {floor_str[:23]:<25} | {has_nav}")

print("=" * 80)
