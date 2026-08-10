import re

new_day3_tokyo_section = """### **09:10 🚇 前往東京車站**

JR 淺草橋站 ➔ 搭乘 JR 中央・總武線 1 站至 秋葉原站 ➔ 同站轉乘 **JR 山手線 (綠色列車，往東京方向)** 至 [**東京站 (東京駅)**](https://www.google.com/maps/search/?api=1&query=35.6812996,139.7670659&query_place_id=ChIJn0PtQVOLGGARqZ-06r4mC70)（車程約 8 分鐘）。  
🚶‍♂️ **出站指引**：下月台後請跟隨頭頂黃色指標前往 1F **「丸之內中央口 / 丸之內南口」** 閘門出站，一走出站體正前方即為開闊的「丸之內站前廣場」。

### **09:25－09:45 �� 欣賞東京車站丸之內站舍建築**

> * 目標地點：[**東京車站丸之內站舍 (東京駅丸の内駅舎)**](https://www.google.com/maps/search/?api=1&query=35.6814247,139.7659944&query_place_id=ChIJE9qjZ0-LGGARQiAs8hULJsg)
> * 拍全家福、欣賞東京車站百年經典紅磚文藝復興式建築（清晨氣溫舒適、陽光順光，最適合戶外合影）。

### **09:45－10:00 🚶‍♂️ 移動至東京車站一番街動漫街（室內無腦走法）**

> * 🚶‍♂️ **室內零迷路步行動線（全程不需 GPS，抬頭看指標）**：
>   1. 在丸之內廣場拍完照後，面向紅磚站舍往**左手邊（北側）**走入 **「丸之內北口」**。
>   2. **切勿刷卡進 JR 閘門**！在閘門前搭乘手扶梯/電梯**下至 B1F**。
>   3. 抬頭看到黃底黑字標示 **「北地下自由通路 (North Underground Passage)」**，沿著這條寬敞筆直的冷氣地下通道直走到底（約 3 分鐘）。
>   4. 出通道即抵達 **「八重洲地下中央口」**，正前方與兩側整條就是 [**東京車站一番街 (東京駅一番街)**](https://www.google.com/maps/search/?api=1&query=%E6%9D%B1%E4%BA%AC%E9%A7%85%E4%B8%80%E7%95%AA%E8%A1%97) 的「東京動漫人物街」！

### **10:00－11:05 🛍️ 逛東京車站一番街動漫街**

> * 目標地點：[**東京車站一番街 (東京駅一番街)**](https://www.google.com/maps/search/?api=1&query=%E6%9D%B1%E4%BA%AC%E9%A7%85%E4%B8%80%E7%95%AA%E8%A1%97) (八重洲地下中央口 B1F)
> * 10:00 店家開始營業，整條動漫街為直線單純動線，依照優先順序輕鬆逛：
> * [**寶可夢商店 (ポケモンストア 東京駅店)**](https://www.google.com/maps/search/?api=1&query=35.6815344,139.7671239&query_place_id=ChIJp0K6QVOLGGARzD9G_rV4j0s) (動漫人物街 B1F)：精選寶可夢周邊，包含東京車站限定版站長皮卡丘。  
> * [**TOMICA專賣店 (トミカショップ 東京店)**](https://www.google.com/maps/search/?api=1&query=35.6816001,139.7671501&query_place_id=ChIJ-Q1qQVOLGGARrK8i8u1d1gU) (動漫人物街 B1F)：小車迷天堂，各式合金小車與組裝工廠。  
> * [**橡子共和國 (ジブリがいっぱい どんぐり共和国 東京駅店)**](https://www.google.com/maps/search/?api=1&query=35.6814502,139.7671802&query_place_id=ChIJJb3hQlOLGGARp0FqX5_w3mE) (動漫人物街 B1F)：吉卜力工作室官方周邊。  
> * [**吉伊卡哇專賣店 (ちいかわらんど TOKYO Station)**](https://www.google.com/maps/search/?api=1&query=35.6813803,139.7672203&query_place_id=ChIJN8ZtQVOLGGARHqT_8o2w3k8) (動漫人物街 B1F)：超人氣 Chiikawa 日本限定文具與玩偶。  
> * [**迪士尼商店 (ディズニーストア 東京駅店)**](https://www.google.com/maps/search/?api=1&query=35.6812904,139.7672504&query_place_id=ChIJO0Z_QVOLGGARz8y08o3_2wU) (動漫人物街 B1F)：迪士尼限定商品專區。

### **11:05－11:25 🌇 KITTE頂樓花園眺望東京車站**

> * 目標地點：[**KITTE花園 (ＫＩＴＴＥガーデン)**](https://www.google.com/maps/search/?api=1&query=35.6795336,139.7654445&query_place_id=ChIJtZRvRvqLGGARdS57rQP2NEk) (KITTE 6F)
> * 🚶‍♂️ **移動動線**：從一番街 B1F 往南側地下通道直通 [**KITTE丸之內 (KITTE丸の内)**](https://www.google.com/maps/search/?api=1&query=35.6795336,139.7654445&query_place_id=ChIJtZRvRvqLGGARdS57rQP2NEk) B1F 連通道，搭乘館內中庭電梯直達 6F 免費屋頂花園，俯瞰東京車站紅磚全景與新幹線進出站。

### **11:30－12:45 🍽️ 午餐：天丼てんや**

> * 首選餐廳：[**天丼てんや (天丼てんや 八重洲店)**](https://www.google.com/maps/search/?api=1&query=35.6790668,139.7679772&query_place_id=ChIJzQEVm_yLGGAR1QSl3jr9CNU) (八重洲地下街 南1號) 享用日式炸蝦天丼（人均 ¥560～¥850）。出餐極快、平價美味、長輩小孩皆愛！
<details>
<summary>🍽️ 查看東京車站午餐備案（KITTE茶泡飯 / 燕子漢堡排）（點擊展開）</summary>

> * 備案餐廳 1：[**だし茶漬け えん (だし茶漬け＋肉うどん えん KITTE丸の内店)**](https://www.google.com/maps/search/?api=1&query=35.6792913,139.7653382&query_place_id=ChIJqVS6VgCLGGAR-5BoRnVee14) (KITTE丸の内 B1F) 和風高湯茶泡飯（人均 ¥850～¥1,100，就在 KITTE 6F 下方 B1F）。  
> * 備案餐廳 2：[**燕子烤肉漢堡排 (つばめグリル 大丸東京店)**](https://www.google.com/maps/search/?api=1&query=35.6812026,139.7678523&query_place_id=ChIJ60m9202LGGAR79K37s2o_a0) (大丸東京店 12F) 經典洋食漢堡排。  
</details>

### **12:50 🚇 前往上野**

🚶‍♂️ **進站指引**：從天丼てんや（八重洲地下街）搭手扶梯上至 1F **「JR 八重洲南口」** 閘門，刷 Suica 卡進站，前往 **4 號月台（JR 山手線・上野／池袋方向）**，搭車直達 [**上野站 (上野駅)**](https://www.google.com/maps/search/?api=1&query=35.7141672,139.7774091&query_place_id=ChIJqZzHZZyOGGAR0M4X5P7X77A)（車程約 8 分鐘）。"""

for fname in ['README.md', '2026東京親子自由行_V10_Henna.md']:
    fpath = f'/home/owen/tokyo/{fname}'
    with open(fpath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Replace Day 3 Tokyo Station sections
    content = re.sub(
        r'### \*\*09:10 🚇 前往東京車站\*\*.*?(?=### \*\*13:25－15:25)',
        new_day3_tokyo_section + '\n\n',
        content,
        flags=re.DOTALL
    )

    with open(fpath, 'w', encoding='utf-8') as f:
        f.write(content)

print("Updated Day 3 Tokyo Station navigation and walking instructions in both Markdown files!")
