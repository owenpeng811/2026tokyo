import re

with open('/home/owen/tokyo/2026東京親子自由行_V10_Henna.md', 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Day 1 Gashapon Bandai
text = re.sub(
    r'(萬代扭蛋百貨店 秋葉原店 \(ガシャポンのデパート 秋葉原店\)\]\(https?://[^\)]+\))',
    r'\1 (いちご秋葉原駅前ビル 4F / namco 4F)',
    text
)
# 2. Day 1 Sushiro
text = re.sub(
    r'#### \*\*17:30－19:00 🍽️ 晚餐：壽司郎（90 分鐘寬裕大啖平價迴轉壽司）\*\*',
    r'#### **17:30－19:00 🍽️ 晚餐：壽司郎 秋葉原站前店 (BiTO AKIBA B1F)（90 分鐘寬裕大啖平價迴轉壽司）**',
    text
)
# 3. Day 1 Gusto
text = re.sub(
    r'#### \*\*17:40－18:35 🍽️ 晚餐：新宿東口家庭友善美食\*\*',
    r'#### **17:40－18:35 🍽️ 晚餐：新宿東口家庭友善美食 (Gusto 新宿NOWAビル 7F)**',
    text
)
# 4. Day 2 Tricolore
text = text.replace('松坂屋本館 2F', '松坂屋上野店 本館 4F')
text = text.replace('(松坂屋本館 2F)', '(松坂屋上野店 本館 4F)')

# 5. Day 3 Character Street shops
for shop in [
    '寶可夢商店 (ポケモンストア 東京駅店)',
    'TOMICA專賣店 (トミカショップ 東京店)',
    '橡子共和國 (ジブリがいっぱい どんぐり共和国 東京駅店)',
    '吉伊卡哇專賣店 (ちいかわらんど TOKYO Station)',
    '迪士尼商店 (ディズニーストア 東京駅店)'
]:
    text = text.replace(f'**{shop}**：', f'**{shop}** (東京車站一番街 B1F 動漫人物街)：')

# 6. Day 3 Tenya
text = re.sub(
    r'### \*\*11:30－12:45 ��️ 午餐（東京車站周邊）\*\*',
    r'### **11:30－12:45 🍽️ 午餐：天丼てんや (八重洲地下街 B1F 南1號)**',
    text
)

# 7. Day 3 Cow Cow Kitchen
text = text.replace(
    '**Cow Cow Kitchen (東京Milk Cheese Factory)**',
    '**Cow Cow Kitchen (東京Milk Cheese Factory)** (ルミネエスト新宿 LUMINE EST 1F)'
)

# 8. Day 4 Ootoya Kichijoji
text = re.sub(
    r'### \*\*13:00－14:10 🍽️ 午餐：大戶屋\*\*',
    r'### **13:00－14:10 🍽️ 午餐：大戶屋 (ホワイトハウスビル 2F)**',
    text
)
text = text.replace(
    '首選餐廳：**大戶屋 (大戸屋ごはん処 吉祥寺店)**',
    '首選餐廳：**大戶屋 (大戸屋ごはん処 吉祥寺店)** (ホワイトハウスビル 2F)'
)
text = text.replace(
    '備案餐廳 1：**一風堂 (一風堂 吉祥寺店)**',
    '備案餐廳 1：**一風堂 (一風堂 吉祥寺店)** (古城ビル 1F)'
)
text = text.replace(
    '備案餐廳 2：**花丸烏龍麵 (はなまるうどん 吉祥寺南口店)**',
    '備案餐廳 2：**花丸烏龍麵 (はなまるうどん 吉祥寺南口店)** (三河屋ビル B1F)'
)

# 9. Day 4 Kushiya Monogatari
text = re.sub(
    r'### \*\*17:00－18:30 🍽️ 晚餐：串家物語\*\*',
    r'### **17:00－18:30 🍽️ 晚餐：串家物語 (ダイヤパレス吉祥寺 2F)**',
    text
)
text = text.replace(
    '首選餐廳：**串家物語 (神楽食堂 串家物語 吉祥寺店)**',
    '首選餐廳：**串家物語 (神楽食堂 串家物語 吉祥寺店)** (ダイヤパレス吉祥寺 2F)'
)

# 10. Day 4 SATOU
text = text.replace(
    '**SATOU (黒毛和牛専門店 さとう 吉祥寺店)**',
    '**SATOU (黒毛和牛専門店 さとう 吉祥寺店)** (1F 外帶炸牛肉丸櫃台 / 2F 鐵板牛排)'
)

# 11. Day 5 Skytree Dining
text = re.sub(
    r'### \*\*11:00－12:30 🍽️ 午餐：東京晴空街道\(東京ソラマチ\) 餐廳街\*\*',
    r'### **11:00－12:30 🍽️ 午餐：東京晴空街道 (東京ソラマチ 東館 7F 餐廳街 / 達摩文字燒)**',
    text
)
text = text.replace(
    '(東京ソラマチ 7F)',
    '(東京ソラマチ 東館 7F 餐廳街)'
)
text = text.replace(
    '(東京ソラマチ 6F)',
    '(東京ソラマチ 東館 6F 餐廳街)'
)
text = text.replace(
    '(東京ソラマチ 3F タベテラス)',
    '(東京ソラマチ 西館 3F 美食街 タベテラス)'
)
text = text.replace(
    '備案餐廳 3：**一風堂 (一風堂 東京ソラマチ店)**',
    '備案餐廳 3：**一風堂 (一風堂 東京ソラマチ店)** (東京ソラマチ 西館 3F 美食街 タベテラス)'
)

# 12. Day 5 Shinjuku West exit
text = text.replace(
    '(西新宿 1-4-5)',
    '(西新宿 1-4-5 1F點餐 / 2F-3F座位區)'
)
text = text.replace(
    '(西新宿 1-12-1 高倉第一ビル 1F)',
    '(西新宿 1-12-1 高倉第一ビル 1F/B1F)'
)

# 13. Day 6 Haneda Airport
text = re.sub(
    r'### \*\*11:30－12:30 🛫 辦理登機與安檢\*\*',
    r'### **11:30－12:30 🛫 辦理登機與安檢 (羽田機場第3航廈 3F 出發大廳)**',
    text
)
text = re.sub(
    r'### \*\*12:30－14:00 🍽️🛍️ 輕食午餐與免稅店最後採買\*\*',
    r'### **12:30－14:00 🍽️🛍️ 輕食午餐與免稅店最後採買 (第3航廈 4F 江戶小路 / 5F 展望台)**',
    text
)

with open('/home/owen/tokyo/2026東京親子自由行_V10_Henna.md', 'w', encoding='utf-8') as f:
    f.write(text)

with open('/home/owen/tokyo/README.md', 'w', encoding='utf-8') as f:
    f.write(text)

print("Applied annotations to Markdown files successfully!")
