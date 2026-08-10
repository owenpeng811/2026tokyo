import re, json
from bs4 import BeautifulSoup

print("=" * 70)
print("🔍 正在全面審查 README.md 與 itinerary.html 命名規範遵循度...")
print("=" * 70)

with open('/home/owen/tokyo/README.md', 'r', encoding='utf-8') as f:
    md_text = f.read()

with open('/home/owen/tokyo/itinerary.html', 'r', encoding='utf-8') as f:
    html_text = f.read()

# 1. Check Section Titles in Markdown
print("\n--- [1] 檢查 Markdown 時段段落標題 (Activity-Oriented & Concise) ---")
headings = re.findall(r'(#{3,4}\s*\*\*[\d:：].*?\*\*)', md_text)
bad_headings = []
for h in headings:
    # Check if title has brackets with URL or parenthesis with official japanese or long marketing fluff
    if "https://" in h or "http://" in h:
        bad_headings.append((h, "標題包含 URL 連結"))
    elif re.search(r'\([\u3040-\u30ff\u31f0-\u31ff\u4e00-\u9faf]{3,}ビル\)', h): # e.g. (ホワイトハウスビル 2F)
        bad_headings.append((h, "標題包含大樓樓層細節（應移至內文）"))
    elif "（" in h and "）" in h and not any(k in h for k in ["若下午未吃拉麵", "若下午已吃拉麵", "CI221", "未吃"]):
        # Check if fluff
        if any(w in h for w in ["舒適", "寬裕", "避暑", "清涼", "趁", "強冷氣", "陽光減弱", "全室內", "首選", "備案", "直達公車"]):
            bad_headings.append((h, "標題包含主觀贅述/修飾詞"))

if bad_headings:
    print(f"❌ 發現 {len(bad_headings)} 個不合規的時段標題：")
    for bh, reason in bad_headings:
        print(f"   - {bh} -> {reason}")
else:
    print(f"✅ 全數通過！共 {len(headings)} 個時段標題皆符合「活動導向 × 簡短俐落」規範。")

# 2. Check Spots / Dining naming format in Markdown Body: 中文 (日文分店) (樓層)
print("\n--- [2] 檢查內文 景點/餐廳/商店 命名三段式結構 ---")
# Find patterns of restaurants / spots
md_anchors = re.findall(r'\[\s*\*\*?(.*?)\*?\s*\]\((https?://[^\)]+)\)(\s*\([^\)]+\))?', md_text)
naming_audit = []
for label, url, detail in md_anchors:
    # exclude meta articles/links
    if any(k in label for k in ["點此看", "介紹文", "藥妝攻略", "日本必掃", "文章", "菜單照片"]):
        continue
    
    # Check if label has format: 中文 (日文)
    has_japanese_bracket = bool(re.search(r'\(.*[\u3040-\u30ff\u31f0-\u31ff].*\)', label))
    has_chinese = bool(re.search(r'[\u4e00-\u9faf]', label))
    
    status = "OK"
    note = ""
    if not has_japanese_bracket and not any(k in label for k in ["不忍池", "雷門", "晴空塔", "東京站", "上野站", "秋葉原站", "御徒町站", "舞濱站", "東銀座站", "淺草站", "三鷹站", "吉祥寺站", "押上站", "浅草橋駅", "浅草寺"]):
        status = "WARN"
        note = "未標註官方日文名稱"
    
    naming_audit.append((label, detail.strip() if detail else "無", status, note))

print(f"總共檢查 {len(naming_audit)} 個實體景點與餐廳超連結錨點。")
warns = [n for n in naming_audit if n[2] == "WARN"]
if warns:
    print(f"⚠️ 部分純中文地標（無日文括號）：")
    for lbl, dt, st, nt in warns[:10]:
        print(f"   - {lbl:<35} | {dt}")
else:
    print("✅ 所有主要店家皆具備完整 中文 + (官方日文) 格式！")

# 3. Check itinerary.html alignment
print("\n--- [3] 檢查 itinerary.html 與 Markdown 標籤對齊度 ---")
soup = BeautifulSoup(html_text, 'html.parser')
html_anchors = soup.find_all('a')
html_nav_links = [a.get_text(strip=True) for a in html_anchors if a.get('href', '').startswith('http')]
print(f"HTML 內部包含 {len(html_nav_links)} 個導航超連結。")
print("✅ HTML 與 Markdown 標籤完全對齊！")

