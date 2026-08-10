import re

new_disney_bus_section = """### **21:50－22:45 🚌🚆 返回淺草橋**

> * 目標地點：[**秋葉原站東口 (秋葉原駅東口交通広場)**](https://www.google.com/maps/search/?api=1&query=35.698383,139.7741315&query_place_id=ChIJ8Y-8_JuOGGAR5e4o-gq0F92)
> * ✅ **Plan A（首選：直達高速巴士，免轉乘一路睡回秋葉原）**：
>   * **乘車地點**：出園剪票口後往右前方步行約 2 分鐘，至迪士尼樂園正門外「東巴士總站東面（Bus Terminal East）」[**東京迪士尼樂園東巴士總站 1 號站牌 (東京ディズニーランド・バスターミナル・イースト 1番のりば)**](https://www.google.com/maps/search/?api=1&query=35.6364946,139.8807661&query_place_id=ChIJ3w8y8xN9GGARe5_gvaqDCMo)（地面與立柱有明顯標示「1番：秋葉原駅行」；可參考 [巴士總站設施與動線介紹文](https://secure.j-bus.co.jp/busrepo/2025/06/23/post-32156/)）。  
>     ![東京迪士尼樂園東巴士總站 1 號公車站牌](https://secure.j-bus.co.jp/busrepo/wp-content/uploads/2025/06/IMG20250513080949-1024x768.jpg)
>   * **巴士特徵與路線**：搭乘京成巴士 (Keisei Bus) 或東京灣城市交通 (Tokyo Bay City Bus) 高速巴士直達 **秋葉原站東口**。車程約 35～45 分鐘，全家每人皆有獨立舒適大座席，免除深夜帶著疲憊小孩擠電車與轉乘的辛苦。  
>   * **抵達與轉乘**：抵達秋葉原站東口後，步行 1 分鐘進 JR 閘門搭乘中央・總武線 1 站（2 分鐘）即返抵淺草橋站。

<details>
<summary>🔰 迪士尼回程高速巴士搭乘 3 大關鍵技巧（點擊展開）</summary>

> * **先到先排隊免預約**：採現場排隊上車制（無需提前購票或劃位，客滿即發車或等下一班車）。  
> * **前門上車感應刷卡**：票價為大人 ¥1,000 / 兒童 ¥500。上車時由**前門上車**並直接以手機/實體 Suica 感應付款即可。  
> * **嬰兒車與戰利品放行李艙**：若有折疊嬰兒車或大包戰利品，上車前可請司機開啟車側下層行李艙免費放置。  
> * **行駛高速公路嚴禁站立**：高速巴士行駛首都高速道路，上車後請務必全程繫好安全帶，等車輛停妥開門後再起立下車。  
</details>

<details>
<summary>🚆 Plan B 備案：電車轉乘路線（若巴士滿載或班次無法配合）（點擊展開）</summary>

> 1. 由舞濱站搭乘 [**JR 京葉線 (JR京葉線)**](https://www.google.com/maps/search/?api=1&query=35.635834,139.883584&query_place_id=ChIJo3N_X5yOGGARyv4l77z-WHQ) 前往「2 號月台（往東京方向）」上車 ➔ 抵達 [**八丁堀站 (八丁堀駅)**](https://www.google.com/maps/search/?api=1&query=35.674998,139.777402&query_place_id=ChIJe0e8kkfuGGARvH2cE14g_0J)（車程約 12 分鐘）。  
> 2. 八丁堀站轉乘 [**東京地鐵日比谷線 (東京メトロ日比谷線)**](https://www.google.com/maps/search/?api=1&query=35.674998,139.777402&query_place_id=ChIJe0e8kkfuGGARvH2cE14g_0J) ➔ 前往「2 號月台（往北千住方向）」上車 ➔ 抵達 [**秋葉原站 (秋葉原駅)**](https://www.google.com/maps/search/?api=1&query=35.698383,139.7731315&query_place_id=ChIJ8Y-8_JuOGGAR5e4o-gq0F88)（車程約 8 分鐘）。  
> 3. 抵達秋葉原站後，於同站轉乘 JR 中央・總武線 1 站返抵淺草橋站飯店休息。  
</details>"""

for fname in ['README.md', '2026東京親子自由行_V10_Henna.md']:
    fpath = f'/home/owen/tokyo/{fname}'
    with open(fpath, 'r', encoding='utf-8') as f:
        content = f.read()

    content = re.sub(
        r'### \*\*21:50－22:45 🚌🚆 返回淺草橋\*\*.*?(?=### \*\*🎟️ 建議購買 Disney Premier Access)',
        new_disney_bus_section + '\n\n',
        content,
        flags=re.DOTALL
    )

    with open(fpath, 'w', encoding='utf-8') as f:
        f.write(content)

print("Added J-Bus introductory blog link to both Markdown files!")
