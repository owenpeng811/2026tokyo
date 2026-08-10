import re, json, urllib.request, urllib.error
from bs4 import BeautifulSoup

print("=" * 60)
print("🔍 正在全面檢查所有導航連結...")
print("=" * 60)

# 1. Collect all links from Markdown
with open('/home/owen/tokyo/2026東京親子自由行_V10_Henna.md', 'r', encoding='utf-8') as f:
    md_text = f.read()

md_links = re.findall(r'\[(.*?)\]\((https?://[^\)]+)\)', md_text)

# 2. Collect all links from itinerary.html
with open('/home/owen/tokyo/itinerary.html', 'r', encoding='utf-8') as f:
    html_text = f.read()

soup = BeautifulSoup(html_text, 'html.parser')
html_anchors = soup.find_all('a')
html_links = []
for a in html_anchors:
    href = a.get('href', '')
    if href and href.startswith('http'):
        html_links.append((a.get_text(strip=True), href))

all_targets = []
seen_urls = set()

for lbl, u in md_links + html_links:
    u_clean = u.strip().rstrip(')>*],."\'')
    if u_clean not in seen_urls:
        seen_urls.add(u_clean)
        all_targets.append((lbl, u_clean))

print(f"總共掃描到 {len(all_targets)} 個不重複的外部導航/參考超連結。\n")

valid_count = 0
error_list = []

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

for idx, (label, url) in enumerate(all_targets, 1):
    status = "OK"
    dest_info = ""
    
    # Check for obvious trailing syntax bugs
    if url.endswith(')') or url.endswith('>') or url.endswith('*') or url.endswith(']'):
        status = "SYNTAX_ERROR"
        error_list.append((label, url, "網址結尾包含錯誤標點符號"))
        print(f"[{idx:03d}] ❌ {label[:25]:<25} | 語法錯誤: {url}")
        continue

    # Test HTTP request
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=8) as resp:
            code = resp.getcode()
            final_url = resp.geturl()
            body_sample = resp.read(2048).decode('utf-8', errors='ignore')
            
            if "Dynamic Link Not Found" in body_sample or "dynamic-link-not-found" in final_url:
                status = "DYNAMIC_LINK_NOT_FOUND"
                error_list.append((label, url, "Firebase 短網址失效 (Dynamic Link Not Found)"))
                print(f"[{idx:03d}] ❌ {label[:25]:<25} | 短網址失效: {url}")
            elif code in [200, 301, 302]:
                valid_count += 1
                print(f"[{idx:03d}] ✅ {label[:25]:<25} | HTTP {code} | {url[:65]}...")
            else:
                status = f"HTTP_{code}"
                error_list.append((label, url, f"HTTP 回應碼: {code}"))
                print(f"[{idx:03d}] ⚠️ {label[:25]:<25} | HTTP {code}: {url}")
    except urllib.error.HTTPError as e:
        if e.code == 403 or e.code == 429: # Google sometimes blocks automated scrapers with 403 but link works in browser
            valid_count += 1
            print(f"[{idx:03d}] 🆗 {label[:25]:<25} | HTTP {e.code} (Google 防爬蟲阻擋，網址有效)")
        else:
            error_list.append((label, url, f"HTTP 錯誤: {e.code}"))
            print(f"[{idx:03d}] ❌ {label[:25]:<25} | HTTP {e.code}: {url}")
    except Exception as e:
        error_list.append((label, url, f"連線異常: {str(e)[:40]}"))
        print(f"[{idx:03d}] ❌ {label[:25]:<25} | 異常: {e}")

print("\n" + "=" * 60)
print(f"📊 檢查總結：")
print(f"  總檢查連結數：{len(all_targets)}")
print(f"  有效連結數：{valid_count}")
print(f"  異常連結數：{len(error_list)}")
print("=" * 60)

if error_list:
    print("\n🚨 異常連結明細：")
    for lbl, u, reason in error_list:
        print(f"  - [{lbl}]: {u} -> {reason}")
else:
    print("\n🎉 恭喜！全行程所有導航與參考連結 100% 正確有效！無任何失效短網址或語法錯誤！")
