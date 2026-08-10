import json, re

with open('/home/owen/tokyo/navigation_links_dict.json', 'r', encoding='utf-8') as f:
    nav_dict = json.load(f)

for fname in ['2026東京親子自由行_V10_Henna.md', 'README.md']:
    fpath = f'/home/owen/tokyo/{fname}'
    with open(fpath, 'r', encoding='utf-8') as f:
        text = f.read()

    # 1. Fix duplicate floor tag in Day 4
    text = text.replace('(ダイヤパレス吉祥寺 2F) (ダイヤパレス吉祥寺 2F)', '(ダイヤパレス吉祥寺 2F)')

    # 2. Add links to Day 4 Lunch
    url_ootoya = nav_dict.get("大戶屋 (大戶屋ごはん処 吉祥寺店)", "")
    url_hanamaru = nav_dict.get("花丸烏龍麵 (はなまるうどん 吉祥寺南口店)", "")
    text = text.replace(
        '首選餐廳：**大戶屋 (大戸屋ごはん処 吉祥寺店)** (ホワイトハウスビル 2F)',
        f'首選餐廳：[**大戶屋 (大戸屋ごはん処 吉祥寺店)**]({url_ootoya}) (ホワイトハウスビル 2F)'
    )
    text = text.replace(
        '備案餐廳：**花丸烏龍麵 (はなまるうどん 吉祥寺南口店)** (大竹ビル B1F)',
        f'備案餐廳：[**花丸烏龍麵 (はなまるうどん 吉祥寺南口店)**]({url_hanamaru}) (大竹ビル B1F)'
    )

    # 3. Add links to Day 4 Dinner
    url_kushiya = nav_dict.get("串家物語 (神楽食堂 串家物語 吉祥寺店)", "")
    url_ippudo = nav_dict.get("一風堂 (一風堂 吉祥寺店)", "")
    text = text.replace(
        '首選餐廳：**串家物語 (神楽食堂 串家物語 吉祥寺店)** (ダイヤパレス吉祥寺 2F)',
        f'首選餐廳：[**串家物語 (神楽食堂 串家物語 吉祥寺店)**]({url_kushiya}) (ダイヤパレス吉祥寺 2F)'
    )
    text = text.replace(
        '備案餐廳：**一風堂 (一風堂 吉祥寺店)**',
        f'備案餐廳：[**一風堂 (一風堂 吉祥寺店)**]({url_ippudo}) (古城ビル 1F)'
    )

    # 4. Add links to Day 5 Plan B Dinner
    url_miyatake = nav_dict.get("宮武讚岐烏龍麵 (宮武讃岐うどん 東京ソラマチ店)", "")
    url_ippudo_skytree = nav_dict.get("一風堂 (一風堂 東京ソラマチ店)", "")
    url_matsuya_oshiage = nav_dict.get("松屋 (松屋 押上店)", "")
    text = text.replace(
        '首選餐廳：**宮武讚岐烏龍麵 (宮武讃岐うどん 東京ソラマチ店)** (東京ソラマチ 西館 3F 美食街 タベテラス)',
        f'首選餐廳：[**宮武讚岐烏龍麵 (宮武讃岐うどん 東京ソラマチ店)**]({url_miyatake}) (東京ソラマチ 西館 3F 美食街 タベテラス)'
    )
    text = text.replace(
        '備案餐廳：**一風堂 (一風堂 東京ソラマチ店)** (東京ソラマチ 西館 3F 美食街 タベテラス)',
        f'備案餐廳：[**一風堂 (一風堂 東京ソラマチ店)**]({url_ippudo_skytree}) (東京ソラマチ 西館 3F 美食街 タベテラス)'
    )
    text = text.replace(
        '備案餐廳：**松屋 (松屋 押上店)** (押上站 A1 出口)',
        f'備案餐廳：[**松屋 (松屋 押上店)**]({url_matsuya_oshiage}) (押上站 A1 出口)'
    )

    # 5. Day 6 Tsukiji
    url_tsukiji_yamacho = nav_dict.get("築地山長 (つきぢ山長)", "")
    url_tsukiji_marutake = nav_dict.get("築地丸武 (丸武 玉子焼)", "")
    text = text.replace(
        '首選餐廳：**築地山長 (山長 玉子焼)**',
        f'首選餐廳：[**築地山長 (山長 玉子焼)**]({url_tsukiji_yamacho})'
    )
    text = text.replace(
        '首推 **築地山長 (山長 玉子焼)**',
        f'首推 [**築地山長 (山長 玉子焼)**]({url_tsukiji_yamacho})'
    )
    text = text.replace(
        '備選：**築地丸武 (丸武 玉子焼)**',
        f'備選：[**築地丸武 (丸武 玉子焼)**]({url_tsukiji_marutake})'
    )

    with open(fpath, 'w', encoding='utf-8') as f:
        f.write(text)

print("Synchronized all spot naming and navigation links across Markdown!")
