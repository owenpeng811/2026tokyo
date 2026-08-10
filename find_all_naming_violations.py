import re, json

with open('/home/owen/tokyo/README.md', 'r', encoding='utf-8') as f:
    text = f.read()

print("=" * 80)
print("🔍 正在逐行深入掃描 README.md 所有未符合 Naming Rule 或 遺漏導航超連結 之處...")
print("=" * 80)

# Pattern to find all bold text that looks like a spot/shop/restaurant
# E.g. **名稱 (日文)** or **名稱**
lines = text.splitlines()

violations = []

# Exclude overview tables at the top
in_daily_itinerary = False

for line_idx, line in enumerate(lines, 1):
    if "## **📅 Day 1" in line:
        in_daily_itinerary = True
    if not in_daily_itinerary:
        continue
    
    # 1. Check Section headings
    if line.startswith("### ") or line.startswith("#### "):
        # Check if heading has bracket or raw store names
        if "(" in line and ")" in line and not any(k in line for k in ["若下午未吃拉麵", "若下午已吃拉麵", "CI221", "未吃"]):
            violations.append((
                line_idx,
                "時段標題包含括號/細節",
                line.strip(),
                "時段標題應為純活動導向，細節移至內文第一行"
            ))

    # 2. Find bold items that are NOT links: e.g. **中文 (日文)** or **純中文店名/景點**
    # But exclude common labels like **交通：**, **建議順序：**, **消費預估：**, **亮點特色：**, **點餐祕訣：**, **首選餐廳：**, **備案餐廳：**, **核心體驗：**, **目標地點：**
    labels_to_ignore = [
        "交通：", "建議順序：", "消費預估：", "亮點特色：", "點餐祕訣：", "首選餐廳：", "備案餐廳：",
        "核心體驗：", "目標地點：", "全家合影紀念：", "趣味塗鴉：", "現場取件：", "重要避坑警示：",
        "點餐與用餐祕訣：", "時間評估與行程建議：", "避暑與歇腳備案：", "出站動線推薦：",
        "大行李進站唯一動線：", "必玩設施：", "選玩設施：", "設施說明：", "建議路線：", "景點與商店說明：",
        "推薦必吃：", "備註：", "注意事項：", "重點提示：", "用餐指南：", "避熱提醒：", "入園策略：",
        "方案比較：", "重要提醒：", "交通建議：", "推薦順序：", "排隊規則：", "營業時間：", "必買推薦："
    ]
    
    # Find all **something**
    bolds = re.findall(r'\*\*([^\*]+)\*\*', line)
    for b in bolds:
        b_clean = b.strip()
        if any(b_clean.startswith(lbl) or b_clean == lbl.rstrip('：') for lbl in labels_to_ignore):
            continue
        if re.match(r'^\d+[\.:]', b_clean) or re.match(r'^\d+:\d+', b_clean) or "Plan A" in b_clean or "Plan B" in b_clean or "Option" in b_clean:
            continue
        if b_clean in ["免排隊時段", "零語言壓力", "90 分鐘寬裕時間", "商場散策", "30/31F 高空景觀", "時間彈性", "舒適補眠電車移動", "長輩小孩充能"]:
            continue
        
        # Check if this bold item is inside a link [**b**](url) or **[b](url)**
        is_in_link = False
        link_matches = re.finditer(r'\[([^\]]*)\]\(([^\)]+)\)', line)
        for lm in link_matches:
            if b in lm.group(0):
                is_in_link = True
                break
        
        if not is_in_link:
            # Check if this looks like a spot, restaurant, or shop
            # (has japanese brackets, or known shop names like 二木菓子, 寶可夢, etc.)
            has_japanese = bool(re.search(r'[\u3040-\u30ff]', b_clean))
            is_spot_like = has_japanese or any(k in b_clean for k in ["商店", "專賣店", "大樓", "神社", "寺", "館", "水族館", "超市", "市場", "公園", "牛排", "拉麵", "烏龍麵", "牛舌", "文字燒", "咖啡", "麵包", "藥妝", "堂", "池", "橋"])
            
            if is_spot_like:
                violations.append((
                    line_idx,
                    "實體地點/店家缺少 Google Maps 超連結",
                    f"**{b_clean}** (在行: {line.strip()[:60]}...)",
                    "應轉換為 [**中文 (日文)**](Google Maps URL) (樓層)"
                ))

print(f"掃描完成！共發現 {len(violations)} 個不符合處 / 遺漏連結處：\n")
for idx, vtype, target, solution in violations:
    print(f"[{vtype}] Line {idx}:")
    print(f"   內容: {target}")
    print(f"   建議: {solution}\n")

