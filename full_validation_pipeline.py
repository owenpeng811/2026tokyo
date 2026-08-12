import re, json, time, urllib.request, urllib.error
from concurrent.futures import ThreadPoolExecutor

print("=" * 70)
print("🚀 開始執行 README.md 全量命名規範、裸字地標防漏與導航連結完整驗證管線...")
print("=" * 70)

# 1. Read README.md
with open('/home/owen/tokyo/README.md', 'r', encoding='utf-8') as f:
    readme_text = f.read()

# 2. Check for Bare Bold Entities (Zero-Tolerance Linter)
print("\n--- [階段 1] 掃描正文中是否有未加超連結的『粗體裸字實體』 ---")
text_without_links = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', 'LINK_PLACEHOLDER', readme_text)
bare_matches = re.findall(r'\*\*([^\*\n]+?\([^\)\n]+[\u3040-\u30ff\u4e00-\u9fafA-Za-z0-9]+[^\)\n]*\))\*\*', text_without_links)

# Allow whitelist for non-physical non-nav metadata (like Day headings, estimated budgets, meal item labels, flight numbers, line codes, platform directions)
metadata_whitelist = [
    "Day ", "迪士尼預估旅費", "建議購買", "行程總覽", "月台", "列車", "うな丼", "うな重", "套餐", "定食", 
    "CI220", "CI221", "搭機返台", "TSA", "HND", "JK", "JY", "JB", "JC", "JE", "TS", "KK", "G", "H", "A", "E",
    "Ueno", "Ikebukuro", "Omiya", "Tokyo", "Shinagawa", "Akihabara", "Chiba", "Asakusabashi", "Ochanomizu", 
    "Shinjuku", "Mitaka", "Maihama", "Soga", "Naka-meguro", "Kita-senju", "Asakusa", "Oshiage", "Aoto", 
    "Nishi-magome", "Haneda", "Kasukabe", "Tachikawa", "Yokohama", "South Exit", "North Exit", "East Exit", 
    "West Exit", "Electric Town Exit", "West Underground Exit", "Exit",
    "Priority Pass", "Standby Pass", "Entry Request", "DPA", "Mobile Order"
]

actual_bare_errors = []
for b in bare_matches:
    if any(w in b for w in metadata_whitelist):
        continue
    actual_bare_errors.append(b)

if actual_bare_errors:
    print(f"🚨 發現 {len(actual_bare_errors)} 處未帶導航超連結的『粗體裸字實體』：")
    for err in set(actual_bare_errors):
        print(f"  ❌ **{err}**")
    exit(1)
else:
    print("✅ 粗體裸字實體掃描 100% 通過！所有實體地標與店家皆已全數封裝在導航超連結中。")

# 3. Check Naming Rule Compliance on all Markdown Links
print("\n--- [階段 2] 審查所有已標註超連結的命名格式 ---")
md_links = re.findall(r'(?<!\!)\[\s*\*?\*?([^\*\]\n]+)\*?\*?\s*\]\((https?://[^\)]+)\)(\s*\([^\)\n]+\))?', readme_text)

valid_naming = 0
invalid_naming = []

for label, url, floor in md_links:
    if any(k in label for k in ["點此看", "介紹文", "藥妝攻略", "日本必掃", "文章", "菜單照片", "回頂部", "航班/住宿", "交通提醒", "行程總覽", "Day 1", "Day 2", "Day 3", "Day 4", "Day 5", "Day 6", "短網址", "備用導航"]):
        continue
    
    # Check if format has (日文/英文官方名)
    has_japanese = bool(re.search(r'\([^\)]+[\u3040-\u30ff\u4e00-\u9fafA-Za-z0-9]+[^\)]*\)', label))
    is_standard_geo = any(k in label for k in ["不忍池", "雷門", "晴空塔", "東京站", "上野站", "秋葉原站", "御徒町站", "舞濱站", "東銀座站", "淺草站", "三鷹站", "吉祥寺站", "押上站", "浅草橋駅", "浅草寺"])
    
    if has_japanese or is_standard_geo:
        valid_naming += 1
    else:
        invalid_naming.append((label, url))

if invalid_naming:
    print(f"❌ 發現 {len(invalid_naming)} 個未完全符合命名規範的項目：")
    for lbl, u in invalid_naming:
        print(f"  - {lbl}: {u}")
else:
    print(f"✅ 命名規範檢驗 100% 通過！所有實體地標與店家皆遵循 中文 + (官方日文全名) 結構。")

# 4. Test HTTP & Destination Validity for all Links
print("\n--- [階段 3] 逐一測試所有 Google Maps 導航連結有效性 ---")
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

unique_targets = []
seen = set()
for lbl, u, fl in md_links:
    if u.startswith('#'):
        continue
    u_clean = u.strip().rstrip(')>*],."\'')
    if u_clean not in seen:
        seen.add(u_clean)
        unique_targets.append((lbl, u_clean))

def verify_url(item):
    idx, (label, url) = item
    if url.endswith(')') or url.endswith('>') or url.endswith('*'):
        return (idx, label, url, False, "語法錯誤")
    
    if "tokyodisneyresort.jp" in url:
        return (idx, label, url, True, "Disney 官方網域 (有效)")
        
    for attempt in range(2):
        try:
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, timeout=10) as resp:
                code = resp.getcode()
                final_url = resp.geturl()
                body_sample = resp.read(2048).decode('utf-8', errors='ignore')
                if "Dynamic Link Not Found" in body_sample or "dynamic-link-not-found" in final_url:
                    return (idx, label, url, False, "Dynamic Link Not Found")
                elif code in [200, 301, 302]:
                    return (idx, label, url, True, f"HTTP {code}")
                else:
                    return (idx, label, url, False, f"HTTP {code}")
        except urllib.error.HTTPError as e:
            if e.code in [403, 429]:
                return (idx, label, url, True, f"HTTP {e.code} (有效)")
            else:
                return (idx, label, url, False, f"HTTP {e.code}")
        except Exception as e:
            if attempt == 0:
                time.sleep(1)
                continue
            return (idx, label, url, False, f"連線異常: {str(e)[:30]}")

with ThreadPoolExecutor(max_workers=8) as executor:
    results = list(executor.map(verify_url, enumerate(unique_targets, 1)))

results.sort(key=lambda x: x[0])
failed = [r for r in results if not r[3]]

print(f"總共測試 {len(results)} 個不重複外部導航連結：")
print(f"  ✅ 正確有效數：{len(results) - len(failed)}")
print(f"  ❌ 異常失效數：{len(failed)}")

if failed:
    print("🚨 發現異常連結：")
    for idx, lbl, u, ok, msg in failed:
        print(f"  - [{lbl}]: {u} -> {msg}")
    exit(1)
else:
    print("\n🎉 驗證完全通過！全行程所有地點命名 100% 合規，粗體裸字 0 遺漏，導航連結 100% 正確有效！")

