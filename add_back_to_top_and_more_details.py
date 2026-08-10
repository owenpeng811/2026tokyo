import re

with open('/home/owen/tokyo/README.md', 'r', encoding='utf-8') as f:
    text = f.read()

# Add [⬆️ 回頂部] button to end of each Day section
day_headers = [
    '## **📅 Day 2（8/21 星期五 - 長輩組）',
    '## **📅 Day 2（8/21 星期五 - 親子組）',
    '## **📅 Day 3（8/22 星期六）',
    '## **�� Day 4（8/23 星期日）',
    '## **📅 Day 5（8/24 星期一）',
    '## **📅 Day 6（8/25 星期二）',
    '## **🎒 行前準備與實用資訊**'
]

for dh in day_headers:
    if f'\n\n[⬆️ 回頂部](#2026東京親子自由行-henna)\n\n---\n\n{dh}' not in text and dh in text:
        text = text.replace(dh, f'[⬆️ 回頂部](#2026東京親子自由行-henna)\n\n---\n\n{dh}')

# Add to the very bottom of the document
if not text.endswith('[⬆️ 回頂部](#2026東京親子自由行-henna)\n'):
    text = text.rstrip() + '\n\n[⬆️ 回頂部](#2026東京親子自由行-henna)\n'

# Wrap Day 5 Afternoon Branching in <details><summary>
d5_decision_old = """## **⭐ Day 5 下午/傍晚動態決策（水族館後）**

> * 方案 A（若體力佳且想看東京地標夜景）：依照原定計畫前往 **新宿** 逛街、吃甜點並登上 **東京都廳 45F 免費展望室** 俯瞰夜景。
> * 方案 B（若長輩或小孩想放慢腳步）：晴空塔逛街至 17:00 結束後，直接搭乘地鐵回淺草橋站，在飯店周邊享用晚餐（如居酒屋、拉麵）並悠閒整理行李。"""

d5_decision_new = """<details>
<summary>⭐ Day 5 下午/傍晚動態決策：方案 A（新宿夜景）/ 方案 B（淺草橋悠閒整備）（點擊展開）</summary>

> * **方案 A（體力充沛推薦）**：前往 **新宿** 逛街、品嚐 [**Cow Cow Kitchen**](https://www.google.com/maps/search/?api=1&query=35.6917502,139.7011419&query_place_id=ChIJr8RjHpyNGGAR-2K84o0P4sQ) 起司牛奶泡芙，並登上 [**東京都廳 45F 展望室**](https://www.google.com/maps/search/?api=1&query=35.6894807,139.6917769&query_place_id=ChIJ9T6uFtuMGGARn9aD9t5A4rA) 俯瞰新宿百萬夜景。  
> * **方案 B（放慢腳步放鬆）**：晴空塔逛街至 17:00 結束後，直接搭乘地鐵回淺草橋站，於飯店周邊品嚐 [**吉野家**](https://www.google.com/maps/search/?api=1&query=35.697878,139.786407&query_place_id=ChIJM2s0MnaPGGARLSDkTkqBlG4) 或 [**松屋**](https://www.google.com/maps/search/?api=1&query=35.696998,139.786388&query_place_id=ChIJW_fJurOOGGARyv4l77z-WHQ)，悠閒打包行李早點休息。  
</details>"""

text = text.replace(d5_decision_old, d5_decision_new)

# Wrap Day 2 DPA purchase recommendation in <details>
dpa_old = """### **🎟️ 建議購買 Disney Premier Access (依優先順序)**

1. **美女與野獸「城堡奇緣」**：極度熱門，入園後第一時間搶購。
2. **杯麵歡樂之旅 (Baymax)**：園區歡樂氣氛擔當，建議依現場排隊時間評估加購。
3. **飛濺山 (Splash Mountain)**：夏季消暑首選，若排隊超過 60 分鐘建議購買。

### **💰 迪士尼預估旅費 (3人)**

| 項目 | 金額 (JPY) | 說明 |
| :--- | :--- | :--- |
| 門票 (大人*2 + 小孩*1) | 約 ¥23,000 | 依官方浮動票價 |
| DPA 快速通關 (美女與野獸*3) | ¥6,000 | ¥2,000 / 人 |
| DPA 快速通關 (杯麵*3) | ¥4,500 | ¥1,500 / 人 |
| 園區餐飲 (午餐+晚餐+點心) | 約 ¥12,000 | 造型點心、火雞腿、正餐 |
| 紀念品與購物 | 約 ¥10,000 | 造型髮箍、限定爆米花桶、伴手禮 |
| **預估總花費** | **約 ¥55,500** | **約合台幣 12,000 元** |"""

dpa_new = """<details>
<summary>🎟️ 迪士尼 DPA 快速通關購買建議與 3 人預估預算表（點擊展開）</summary>

#### **建議購買 DPA 優先順序**：
1. **美女與野獸「城堡奇緣」**：極度熱門，入園後第一時間搶購。  
2. **杯麵歡樂之旅 (Baymax)**：園區歡樂氣氛擔當，建議依現場排隊時間評估加購。  
3. **飛濺山 (Splash Mountain)**：夏季消暑首選，若排隊超過 60 分鐘建議購買。  

#### **💰 迪士尼預估旅費 (3人)**

| 項目 | 金額 (JPY) | 說明 |
| :--- | :--- | :--- |
| 門票 (大人*2 + 小孩*1) | 約 ¥23,000 | 依官方浮動票價 |
| DPA 快速通關 (美女與野獸*3) | ¥6,000 | ¥2,000 / 人 |
| DPA 快速通關 (杯麵*3) | ¥4,500 | ¥1,500 / 人 |
| 園區餐飲 (午餐+晚餐+點心) | 約 ¥12,000 | 造型點心、火雞腿、正餐 |
| 紀念品與購物 | 約 ¥10,000 | 造型髮箍、限定爆米花桶、伴手禮 |
| **預估總花費** | **約 ¥55,500** | **約合台幣 12,000 元** |
</details>"""

text = text.replace(dpa_old, dpa_new)

with open('/home/owen/tokyo/README.md', 'w', encoding='utf-8') as f:
    f.write(text)

with open('/home/owen/tokyo/2026東京親子自由行_V10_Henna.md', 'w', encoding='utf-8') as f:
    f.write(text)

print("Applied back-to-top buttons, Day 5 decision fold, and DPA table fold successfully!")
