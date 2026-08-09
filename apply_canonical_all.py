import json
import re
import os
from bs4 import BeautifulSoup

with open('/home/owen/tokyo/navigation_links_dict.json', 'r', encoding='utf-8') as f:
    nav_dict = json.load(f)

print(f"Loaded {len(nav_dict)} canonical URLs from navigation_links_dict.json.")

# 1. Update 2026東京親子自由行_V10_Henna.md & README.md
for md_file in ['/home/owen/tokyo/2026東京親子自由行_V10_Henna.md', '/home/owen/tokyo/README.md']:
    with open(md_file, 'r', encoding='utf-8') as f:
        md_text = f.read()

    def replace_md_link(match):
        label = match.group(1)
        old_url = match.group(2)
        # Match label with dict
        for k in sorted(nav_dict.keys(), key=lambda x: -len(x)):
            if k in label:
                return f"[{label}]({nav_dict[k]})"
        return f"[{label}]({old_url})"

    new_md_text = re.sub(r'\[(.*?)\]\((https?://[^\)]+)\)', replace_md_link, md_text)
    
    with open(md_file, 'w', encoding='utf-8') as f:
        f.write(new_md_text)
    print(f"Updated {md_file} with canonical URLs.")

# 2. Update navigation_links.html
table_rows = ""
sorted_keys = sorted(nav_dict.keys())
for k in sorted_keys:
    url = nav_dict[k]
    table_rows += f"""        <tr>
      <td><strong>{k}</strong></td>
      <td><input type="text" class="link-input" value="{url}" readonly onclick="this.select()"></td>
      <td><a href="{url}" target="_blank" class="btn-preview">🔗 開啟地圖</a></td>
    </tr>\n"""

full_nav_html = f"""<!DOCTYPE html>
<html lang="zh-TW">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>2026 東京行程 導航連結對照基準表</title>
  <style>
    body {{
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
      background-color: #0f172a;
      color: #f8fafc;
      padding: 24px 16px;
      margin: 0;
    }}
    .container {{
      max-width: 960px;
      margin: 0 auto;
    }}
    h1 {{
      font-size: 1.5rem;
      color: #38bdf8;
      margin-bottom: 8px;
    }}
    p.desc {{
      color: #94a3b8;
      font-size: 0.9rem;
      margin-bottom: 20px;
    }}
    table {{
      width: 100%;
      border-collapse: collapse;
      background: #1e293b;
      border-radius: 12px;
      overflow: hidden;
      box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.2);
    }}
    th, td {{
      padding: 12px 14px;
      text-align: left;
      border-bottom: 1px solid #334155;
      font-size: 0.88rem;
    }}
    th {{
      background: #0f172a;
      color: #94a3b8;
      font-weight: 600;
    }}
    tr:hover {{
      background: rgba(56, 189, 248, 0.05);
    }}
    .link-input {{
      width: 100%;
      background: #0f172a;
      border: 1px solid #475569;
      color: #38bdf8;
      padding: 6px 8px;
      border-radius: 6px;
      font-size: 0.8rem;
    }}
    .btn-preview {{
      display: inline-block;
      background: #0284c7;
      color: #fff;
      text-decoration: none;
      padding: 6px 12px;
      border-radius: 6px;
      font-size: 0.8rem;
      font-weight: 500;
      white-space: nowrap;
    }}
    .btn-preview:hover {{
      background: #0369a1;
    }}
  </style>
</head>
<body>
  <div class="container">
    <h1>📍 2026 東京親子自由行 導航連結對照基準表 (官方永久定位版)</h1>
    <p class="desc">此表收錄全行程中所有景點、餐廳、飯店與車站之 Google Maps 永久定位連結（共 {len(sorted_keys)} 處，含 Place ID 與精確經緯度）。</p>
    <table>
      <thead>
        <tr>
          <th style="width: 32%;">景點 / 餐廳名稱 (Key)</th>
          <th style="width: 52%;">Google Maps 導航連結</th>
          <th style="width: 16%;">即時預覽</th>
        </tr>
      </thead>
      <tbody>
{table_rows}
      </tbody>
    </table>
  </div>
</body>
</html>
"""

with open('/home/owen/tokyo/navigation_links.html', 'w', encoding='utf-8') as f:
    f.write(full_nav_html)
print(f"Updated navigation_links.html with {len(sorted_keys)} canonical links.")

