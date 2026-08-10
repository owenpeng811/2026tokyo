import re

with open('/home/owen/tokyo/2026東京親子自由行_V10_Henna.md', 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Day 1 Gashapon Bandai -> いちご秋葉原駅前ビル 4F (namco秋葉原店 4F)
text = text.replace(
    "🪙 [萬代扭蛋百貨店 秋葉原店 (ガシャポンのデパート 秋葉原店)](https://maps.app.goo.gl/2F8a4mK7eUvB3H6x9)",
    "🪙 [萬代扭蛋百貨店 秋葉原店 (ガシャポンのデパート 秋葉原店)](https://maps.app.goo.gl/2F8a4mK7eUvB3H6x9) (いちご秋葉原駅前ビル 4F / namco 4F)"
)
text = text.replace(
    "前往全秋葉原規模最大之一的官方扭蛋專門店，擁有近千台最新動漫",
    "位於 **いちご秋葉原駅前ビル 4F (namco秋葉原店 4F)**，全秋葉原規模最大官方扭蛋專門店之一，擁有近千台最新動漫"
)

# 2. Day 1 Sushiro header/summary
text = text.replace(
    "#### **17:30－19:00 🍽️ 晚餐：壽司郎（90 分鐘寬裕大啖平價迴轉壽司）**",
    "#### **17:30－19:00 🍽️ 晚餐：壽司郎 秋葉原站前店 (BiTO AKIBA B1F)（90 分鐘寬裕大啖平價迴轉壽司）**"
)

# 3. Day 1 Gusto header
text = text.replace(
    "#### **17:40－18:35 🍽️ 晚餐：新宿東口家庭友善美食**",
    "#### **17:40－18:35 🍽️ 晚餐：新宿東口家庭友善美食 (Gusto 新宿NOWAビル 7F)**"
)

# 4. Day 2 Kissaten Tricolore floor fix (本館 4F)
text = text.replace(
    "(松坂屋本館 2F)",
    "(松坂屋上野店 本館 4F)"
)
text = text.replace(
    "松坂屋本館 2F",
    "松坂屋上野店 本館 4F"
)

# 5. Day 3 Tokyo Station Character Street shops floor
text = text.replace(
    "> * **寶可夢商店 (ポケモンストア 東京駅店)**：",
    "> * **寶可夢商店 (ポケモンストア 東京駅店)** (東京車站一番街 B1F 動漫人物街)："
)
text = text.replace(
    "> * **TOMICA專賣店 (トミカショップ 東京店)**：",
    "> * **TOMICA專賣店 (トミカショップ 東京店)** (東京車站一番街 B1F 動漫人物街)："
)
text = text.replace(
    "> * **橡子共和國 (ジブリがいっぱい どんぐり共和国 東京駅店)**：",
    "> * **橡子共和國 (ジブリがいっぱい どんぐり共和国 東京駅店)** (東京車站一番街 B1F 動漫人物街)："
)
text = text.replace(
    "> * **吉伊卡哇專賣店 (ちいかわらんど TOKYO Station)**：",
    "> * **吉伊卡哇專賣店 (ちいかわらんど TOKYO Station)** (東京車站一番街 B1F 動漫人物街)："
)
text = text.replace(
    "> * **迪士尼商店 (ディズニーストア 東京駅店)**：",
    "> * **迪士尼商店 (ディズニーストア 東京駅店)** (東京車站一番街 B1F 動漫人物街)："
)

# 6. Day 3 Tenya header & Yaesu Underground Mall floor
text = text.replace(
    "### **11:30－12:45 🍽️ 午餐（東京車站周邊）**",
    "### **11:30－12:45 🍽️ 午餐：天丼てんや (八重洲地下街 B1F 南1號)**"
)

# 7. Day 3 Cow Cow Kitchen floor
text = text.replace(
    "外帶 [**Cow Cow Kitchen (東京Milk Cheese Factory)**]",
    "外帶 [**Cow Cow Kitchen (東京Milk Cheese Factory)**] (ルミネエスト新宿 LUMINE EST 1F)"
)
text = text.replace(
    "外帶 **Cow Cow Kitchen (東京Milk Cheese Factory)**",
    "外帶 **Cow Cow Kitchen (東京Milk Cheese Factory)** (ルミネエスト新宿 LUMINE EST 1F)"
)

# 8. Day 4 Ootoya Kichijoji floor
text = text.replace(
    "### **13:00－14:10 🍽️ 午餐：大戶屋**",
    "### **13:00－14:10 🍽️ 午餐：大戶屋 (ホワイトハウスビル 2F)**"
)
text = text.replace(
    "首選餐廳：[**大戶屋 (大戸屋ごはん処 吉祥寺店)**]({nav_dict.get('大戶屋 (大戸屋ごはん処 吉祥寺店)', '')})",
    "首選餐廳：[**大戶屋 (大戸屋ごはん処 吉祥寺店)**]({nav_dict.get('大戶屋 (大戸屋ごはん処 吉祥寺店)', '')}) (ホワイトハウスビル 2F)"
) if '首選餐廳：[**大戶屋' in text else None
text = text.replace(
    "首選餐廳：**大戶屋 (大戸屋ごはん処 吉祥寺店)**",
    "首選餐廳：**大戶屋 (大戸屋ごはん処 吉祥寺店)** (ホワイトハウスビル 2F)"
)
text = text.replace(
    "備案餐廳 1：**一風堂 (一風堂 吉祥寺店)**",
    "備案餐廳 1：**一風堂 (一風堂 吉祥寺店)** (古城ビル 1F)"
)
text = text.replace(
    "備案餐廳 2：**花丸烏龍麵 (はなまるうどん 吉祥寺南口店)**",
    "備案餐廳 2：**花丸烏龍麵 (はなまるうどん 吉祥寺南口店)** (三河屋ビル B1F)"
)

# 9. Day 4 Kushiya Monogatari Kichijoji floor
text = text.replace(
    "### **17:00－18:30 🍽️ 晚餐：串家物語**",
    "### **17:00－18:30 🍽️ 晚餐：串家物語 (ダイヤパレス吉祥寺 2F)**"
)
text = text.replace(
    "首選餐廳：**串家物語 (神楽食堂 串家物語 吉祥寺店)**",
    "首選餐廳：**串家物語 (神楽食堂 串家物語 吉祥寺店)** (ダイヤパレス吉祥寺 2F)"
)

# 10. Day 4 SATOU floor
text = text.replace(
    "**SATOU (黒毛和牛専門店 さとう 吉祥寺店)**",
    "**SATOU (黒毛和牛専門店 さとう 吉祥寺店)** (1F 外帶炸牛肉丸櫃台 / 2F 鐵板牛排)"
)

# 11. Day 5 Skytree Dining floors
text = text.replace(
    "### **11:00－12:30 🍽️ 午餐：東京晴空街道(東京ソラマチ) 餐廳街**",
    "### **11:00－12:30 🍽️ 午餐：東京晴空街道 (東京ソラマチ 7F 餐廳街 / 達摩文字燒)**"
)
text = text.replace(
    "首選餐廳：[**達摩文字燒 (月島名物もんじゃ だるま 東京スカイツリータウン・ソラマチ店)**](https://maps.app.goo.gl/UaJR8NaOGGAR48j67) (東京ソラマチ 7F)",
    "首選餐廳：[**達摩文字燒 (月島名物もんじゃ だるま 東京スカイツリータウン・ソラマチ店)**](https://maps.app.goo.gl/UaJR8NaOGGAR48j67) (東京ソラマチ 東館 7F 餐廳街)"
)
text = text.replace(
    "備案餐廳 1：**利久牛舌 (牛たん炭焼 利久 東京ソラマチ店)** (東京ソラマチ 6F)",
    "備案餐廳 1：**利久牛舌 (牛たん炭焼 利久 東京ソラマチ店)** (東京ソラマチ 東館 6F 餐廳街)"
)
text = text.replace(
    "備案餐廳 2：**宮武讚岐烏龍麵 (宮武讃岐うどん 東京ソラマチ店)** (東京ソラマチ 3F タベテラス)",
    "備案餐廳 2：**宮武讚岐烏龍麵 (宮武讃岐うどん 東京ソラマチ店)** (東京ソラマチ 西館 3F 美食街 タベテラス)"
)
text = text.replace(
    "備案餐廳 3：**一風堂 (一風堂 東京ソラマチ店)**",
    "備案餐廳 3：**一風堂 (一風堂 東京ソラマチ店)** (東京ソラマチ 西館 3F 美食街 タベテラス)"
)

# 12. Day 5 Shinjuku West exit McDonald's / Mos Burger floor
text = text.replace(
    "首選餐廳：[**麥當勞 (マクドナルド 新宿西口店)**](https://maps.app.goo.gl/j8aWGtGMGGARxgm47) (西新宿 1-4-5)",
    "首選餐廳：[**麥當勞 (マクドナルド 新宿西口店)**](https://maps.app.goo.gl/j8aWGtGMGGARxgm47) (西新宿 1-4-5 1F點餐 / 2F-3F座位區)"
)
text = text.replace(
    "備案餐廳 1：[**摩斯漢堡 (モスバーガー 新宿西口店)**](https://maps.app.goo.gl/KdESUJGNGGAReuO_9) (西新宿 1-12-1 高倉第一ビル 1F)",
    "備案餐廳 1：[**摩斯漢堡 (モスバーガー 新宿西口店)**](https://maps.app.goo.gl/KdESUJGNGGAReuO_9) (西新宿 1-12-1 高倉第一ビル 1F/B1F)"
)

# 13. Day 5 Tokyo Metropolitan Government Building 45F observation deck
text = text.replace(
    "搭乘南展望室專用直達電梯直達 45 樓",
    "於 **第一本廳舍 1F 展望室專用電梯口** 搭乘直達高速電梯，直達 **45 樓南展望室**"
)

# 14. Day 6 Haneda Airport terminal floors
text = text.replace(
    "### **11:30－12:30 🛫 辦理登機與安檢**",
    "### **11:30－12:30 🛫 辦理登機與安檢 (羽田機場第3航廈 3F 出發大廳)**"
)
text = text.replace(
    "### **12:30－14:00 🍽️🛍️ 輕食午餐與免稅店最後採買**",
    "### **12:30－14:00 🍽️🛍️ 輕食午餐與免稅店最後採買 (第3航廈 4F 江戶小路 / 5F 展望台)**"
)

with open('/home/owen/tokyo/2026東京親子自由行_V10_Henna.md', 'w', encoding='utf-8') as f:
    f.write(text)

with open('/home/owen/tokyo/README.md', 'w', encoding='utf-8') as f:
    f.write(text)

print("Updated 2026東京親子自由行_V10_Henna.md and README.md with comprehensive building floor info!")
