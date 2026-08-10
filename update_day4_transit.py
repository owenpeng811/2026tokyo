import json, re

# Update navigation dictionary if needed
with open('/home/owen/tokyo/navigation_links_dict.json', 'r', encoding='utf-8') as f:
    nav_dict = json.load(f)

nav_dict["三鷹站 (三鷹駅)"] = "https://www.google.com/maps/search/?api=1&query=35.7027878,139.5604169&query_place_id=ChIJ8Y-8_JuOGGAR5e4o-gq0F90"
nav_dict["吉祥寺站 (吉祥寺駅)"] = "https://www.google.com/maps/search/?api=1&query=35.7031125,139.5797825&query_place_id=ChIJe0e8kkfuGGARvH2cE14g_0I"
nav_dict["井之頭恩賜公園 (井の頭恩賜公園)"] = "https://www.google.com/maps/search/?api=1&query=35.7001429,139.5760205&query_place_id=ChIJo3N_X5yOGGARyv4l77z-WHQ"
nav_dict["井之頭池 (井の頭池)"] = "https://www.google.com/maps/search/?api=1&query=35.69974759999999,139.5769222&query_place_id=ChIJbfIujp-OGGARQpzhp7F2ocZ"

with open('/home/owen/tokyo/navigation_links_dict.json', 'w', encoding='utf-8') as f:
    json.dump(nav_dict, f, ensure_ascii=False, indent=2)

new_bus_section = """### **09:35－09:50 🚌 搭乘吉卜力接駁巴士**

> * 目標地點：[**三鷹之森吉卜力美術館 (三鷹の森ジブリ美術館)**](https://www.google.com/maps/search/?api=1&query=35.696238,139.5704317&query_place_id=ChIJLYwD5TTuGGARBZKEP5BV4U0)
> * 乘車地點：[**三鷹站 (三鷹駅)**](https://www.google.com/maps/search/?api=1&query=35.7027878,139.5604169&query_place_id=ChIJ8Y-8_JuOGGAR5e4o-gq0F90) 南口 9 號公車站（站體設有電梯與手扶梯；9 號站牌有龍貓與吉卜力彩繪，非常醒目）。
> * 目的地：直達吉卜力美術館（車程約 5 分鐘，約 10 分鐘一班）。

<details>
<summary>🔰 日本公車搭乘 3 大關鍵技巧（點擊展開）</summary>

> * **不用揮手**：人在站牌依序等候即可，公車到站會自動靠站開啟車門，不需要像在台灣一樣招手。  
> * **上下車刷卡**：請由**後門上車**感應 Suica ➔ 抵達後由**前門下車**再感應 Suica。  
> * **車停妥再站起來（最重要！）**：公車行進或減速時請絕對保持坐姿、切勿提前站立。請等公車完全停穩、車門開啟後，再起立走往前門下車即可，司機會非常耐心地等待全家，完全不用急著搶下車。  
</details>"""

new_kichijoji_transit = """### **12:15－12:50 🚌🚃 前往吉祥寺**

> * ✅ **Plan A（首選：接駁車 ＋ JR 電車，零腦力順暢轉乘）**：
>   * **第一段（接駁巴士回三鷹站）**：離開美術館後，直接至門口正前方公車站牌等候。門口進站的彩繪/黃色接駁巴士 100% 都是開往三鷹站，完全不用看路線，閉著眼睛上車即可（車程約 5 分鐘，後門上車嗶 Suica ➔ 前門下車嗶 Suica，車停妥再起立）。
>   * **第二段（轉乘 JR 至吉祥寺站）**：抵達三鷹站南口後搭電梯/手扶梯上樓刷 Suica 進站。於「新宿／東京」方向月台搭乘黃色中央・總武線或橘色中央線快速，僅搭 1 站（車程約 2 分鐘）即達 [**吉祥寺站 (吉祥寺駅)**](https://www.google.com/maps/search/?api=1&query=35.7031125,139.5797825&query_place_id=ChIJe0e8kkfuGGARvH2cE14g_0I)（建議由「公園口/南口」出站前往商圈與大戶屋）。
>   * **選擇優勢**：門口直接原線接駁車上車，完全不需要在路口判斷一般公車路線，對新手與家庭來說最簡單直覺且全冷氣。

<details>
<summary>🌲 Plan B 備案：井之頭恩賜公園林蔭散步（點擊展開）</summary>

> * 若當天微風涼爽且全家體力充沛，可選擇由美術館一路往下坡漫步穿過 [**井之頭恩賜公園 (井の頭恩賜公園)**](https://www.google.com/maps/search/?api=1&query=35.7001429,139.5760205&query_place_id=ChIJo3N_X5yOGGARyv4l77z-WHQ) 往吉祥寺方向，樹蔭多、湖景漂亮。途中於 [**井之頭池 (井の頭池)**](https://www.google.com/maps/search/?api=1&query=35.69974759999999,139.5769222&query_place_id=ChIJbfIujp-OGGARQpzhp7F2ocZ) 停留約 10～15 分鐘拍照、欣賞湖景，但不建議租船（因後面還有商圈行程）。  
</details>"""

for fname in ['README.md', '2026東京親子自由行_V10_Henna.md']:
    fpath = f'/home/owen/tokyo/{fname}'
    with open(fpath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Replace Bus section
    content = re.sub(
        r'### \*\*09:35－09:50 🚌 搭乘吉卜力接駁巴士\*\*.*?(?=### \*\*09:50－12:15)',
        new_bus_section + '\n\n',
        content,
        flags=re.DOTALL
    )

    # Replace Transit to Kichijoji section
    content = re.sub(
        r'### \*\*12:15－12:50 🚌🚶‍♂️ 前往吉祥寺\*\*.*?(?=### \*\*13:00－14:10)',
        new_kichijoji_transit + '\n\n',
        content,
        flags=re.DOTALL
    )

    with open(fpath, 'w', encoding='utf-8') as f:
        f.write(content)

print("Updated Day 4 Ghibli & Kichijoji transit in both Markdown files!")
