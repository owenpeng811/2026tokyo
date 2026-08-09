#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
import os
import urllib.parse
from bs4 import BeautifulSoup

def update_navigation_links():
    with open('/home/owen/tokyo/2026東京親子自由行_V10_Henna.md', 'r', encoding='utf-8') as f:
        md_content = f.read()

    links_found = re.findall(r'\[(.*?)\]\((https://[^\)]+)\)', md_content)
    
    extracted_links = {}
    for text, url in links_found:
        clean_text = text.replace('*', '').strip()
        clean_text = re.sub(r'\(.*?\)', '', clean_text).strip()
        if len(clean_text) > 1 and not clean_text.startswith('http'):
            extracted_links[clean_text] = url

    print(f"Extracted {len(extracted_links)} links from V10 markdown.")
    
    existing_links = {}
    if os.path.exists('/home/owen/tokyo/navigation_links.html'):
        with open('/home/owen/tokyo/navigation_links.html', 'r', encoding='utf-8') as f:
            html_content = f.read()
        soup = BeautifulSoup(html_content, 'html.parser')
        for row in soup.find_all('tr'):
            cols = row.find_all('td')
            if len(cols) >= 2:
                name = cols[0].get_text(strip=True)
                inp = cols[1].find('input')
                if inp and inp.get('value'):
                    existing_links[name] = inp.get('value')

    for k, v in extracted_links.items():
        existing_links[k] = v

    sorted_keys = sorted(existing_links.keys())
    
    table_rows = ""
    for k in sorted_keys:
        url = existing_links[k]
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
    <h1>📍 2026 東京親子自由行 導航連結對照基準表</h1>
    <p class="desc">此表收錄全行程中所有景點、餐廳、飯店與車站之精準 Google Maps 導航連結（共 {len(sorted_keys)} 處）。</p>
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
    print(f"✅ Successfully updated navigation_links.html with {len(sorted_keys)} links.")

if __name__ == '__main__':
    update_navigation_links()
