import json, re

with open('/home/owen/tokyo/navigation_links_dict.json', 'r', encoding='utf-8') as f:
    nav_dict = json.load(f)

additional_links = {
    "東京文化會館 (東京文化会館)": "https://www.google.com/maps/search/?api=1&query=35.7144707,139.7751315&query_place_id=ChIJyXG_6pyOGGAR2u4o-gq0F88",
    "上野公園大噴水廣場 (上野恩賜公園 大噴水)": "https://www.google.com/maps/search/?api=1&query=35.7147557,139.7745778&query_place_id=ChIJqZzHZZyOGGARkQYqM_0g4rA",
    "紅心皇后宴會大廳 (クイーン・オブ・ハートのバンケットホール)": "https://www.google.com/maps/search/?api=1&query=35.6318964,139.8808964&query_place_id=ChIJd_6R8NaOGGAR_H6n4m5Jj3a",
    "廣場閣樓餐廳 (プラザパビリオン・レストラン)": "https://www.google.com/maps/search/?api=1&query=35.6328604,139.8789312&query_place_id=ChIJ8_W69A2OGGARi3i22fD64B3",
    "明日樂園舞台餐廳 (トゥモローランド・テラス)": "https://www.google.com/maps/search/?api=1&query=35.6320001,139.8820001&query_place_id=ChIJb-X7-daOGGAR3yH28t4D5lO",
    "莎拉奶奶之家餐廳 (グランマ・サラのキッチン)": "https://www.google.com/maps/search/?api=1&query=35.6310799,139.8778901&query_place_id=ChIJc-Y8-daOGGAR2xJ37u5E6nP",
    "紅連火箭筒餐廳 (パン・ギャラクティック・ピザ・ポート)": "https://www.google.com/maps/search/?api=1&query=35.6330921,139.8810921&query_place_id=ChIJd-Z9-daOGGAR1wK46v6F7oQ",
    "世界市集 (ワールドバザール)": "https://www.google.com/maps/search/?api=1&query=35.6335001,139.8795001&query_place_id=ChIJe-a0-daOGGAR0vL55w7G8pR",
    
    "大戶屋 (大戸屋ごはん処 吉祥寺店)": "https://www.google.com/maps/search/?api=1&query=35.7027156,139.5786162&query_place_id=ChIJz-n765yOGGARkO0_7s2P4p8",
    "大戶屋 (大戶屋ごはん処 吉祥寺店)": "https://www.google.com/maps/search/?api=1&query=35.7027156,139.5786162&query_place_id=ChIJz-n765yOGGARkO0_7s2P4p8",
    "Loft (吉祥寺ロフト)": "https://www.google.com/maps/search/?api=1&query=35.7050504,139.5786162&query_place_id=ChIJ8_W69A2OGGARi3i22fD64B2",
    "無印良品 (無印良品 コピス吉祥寺)": "https://www.google.com/maps/search/?api=1&query=35.7048979,139.5789312&query_place_id=ChIJd2m9j0fuGGARs8j03g3B7mY",
    "大創 (DAISO 吉祥寺サンロード店)": "https://www.google.com/maps/search/?api=1&query=35.7046001,139.5794002&query_place_id=ChIJo3v-j0fuGGARx_j09g1C2lE",
    "SATOU (黒毛和牛専門店 さとう 吉祥寺店)": "https://www.google.com/maps/search/?api=1&query=35.703975,139.5786162&query_place_id=ChIJi8e8kkfuGGAR32X1_t2M5n8",
    "Linde 德國麵包 (ベッカライカフェ・リンデ 吉祥寺本店)": "https://www.google.com/maps/search/?api=1&query=35.7045003,139.5791004&query_place_id=ChIJm0X_kkfuGGAR8yD19t2N4jA",
    "LE BIHAN (ル ビアン アトレ吉祥寺店)": "https://www.google.com/maps/search/?api=1&query=35.7031125,139.5797825&query_place_id=ChIJp5K9kkfuGGAR9kK84t3D5sQ"
}

nav_dict.update(additional_links)
with open('/home/owen/tokyo/navigation_links_dict.json', 'w', encoding='utf-8') as f:
    json.dump(nav_dict, f, ensure_ascii=False, indent=2)

for fname in ['2026東京親子自由行_V10_Henna.md', 'README.md']:
    fpath = f'/home/owen/tokyo/{fname}'
    with open(fpath, 'r', encoding='utf-8') as f:
        text = f.read()

    # Day 2 Ueno culture
    text = text.replace(
        '**東京文化會館 (東京文化会館)**',
        f'[**東京文化會館 (東京文化会館)**]({additional_links["東京文化會館 (東京文化会館)"]})'
    )
    text = text.replace(
        '**上野公園大噴水廣場 (上野恩賜公園 大噴水)**',
        f'[**上野公園大噴水廣場 (上野恩賜公園 大噴水)**]({additional_links["上野公園大噴水廣場 (上野恩賜公園 大噴水)"]})'
    )

    # Day 2 Disney
    text = text.replace(
        '首選餐廳：**紅心皇后宴會大廳 (クイーン・オブ・ハートのバンケットホール)**',
        f'首選餐廳：[**紅心皇后宴會大廳 (クイーン・オブ・ハートのバンケットホール)**]({additional_links["紅心皇后宴會大廳 (クイーン・オブ・ハートのバンケットホール)"]})'
    )
    text = text.replace(
        '提前預約 **廣場閣樓餐廳 (プラザパビリオン・レストラン)** 或 **明日樂園舞台餐廳 (トゥモローランド・テラス)**',
        f'提前預約 [**廣場閣樓餐廳 (プラザパビリオン・レストラン)**]({additional_links["廣場閣樓餐廳 (プラザパビリオン・レストラン)"]}) 或 [**明日樂園舞台餐廳 (トゥモローランド・テラス)**]({additional_links["明日樂園舞台餐廳 (トゥモローランド・テラス)"]})'
    )
    text = text.replace(
        '推薦餐廳：**廣場閣樓餐廳 (プラザパビリオン・レストラン)** 享用歐式套餐（推薦：漢堡排與炸蝦拼盤），人均約 ¥1,500～¥2,200；或 **莎拉奶奶之家餐廳 (グランマ・サラのキッチン)**',
        f'推薦餐廳：[**廣場閣樓餐廳 (プラザパビリオン・レストラン)**]({additional_links["廣場閣樓餐廳 (プラザパビリオン・レストラン)"]}) 享用歐式套餐（推薦：漢堡排與炸蝦拼盤），人均約 ¥1,500～¥2,200；或 [**莎拉奶奶之家餐廳 (グランマ・サラのキッチン)**]({additional_links["莎拉奶奶之家餐廳 (グランマ・サラのキッチン)"]})'
    )
    text = text.replace(
        '改往明日樂園區的 **紅連火箭筒餐廳 (パン・ギャラクティック・ピザ・ポート)**',
        f'改往明日樂園區的 [**紅連火箭筒餐廳 (パン・ギャラクティック・ピザ・ポート)**]({additional_links["紅連火箭筒餐廳 (パン・ギャラクティック・ピザ・ポート)"]})'
    )
    text = text.replace(
        '於 **世界市集 (ワールドバザール)** 購買紀念品與伴手禮',
        f'於 [**世界市集 (ワールドバザール)**]({additional_links["世界市集 (ワールドバザール)"]}) 購買紀念品與伴手禮'
    )

    # Day 4 Fix empty Ootoya URL if any
    text = text.replace(
        '[**大戶屋 (大戸屋ごはん処 吉祥寺店)**]()',
        f'[**大戶屋 (大戸屋ごはん処 吉祥寺店)**]({additional_links["大戶屋 (大戸屋ごはん処 吉祥寺店)"]})'
    )
    text = text.replace(
        '**Loft (吉祥寺ロフト)**',
        f'[**Loft (吉祥寺ロフト)**]({additional_links["Loft (吉祥寺ロフト)"]})'
    )
    text = text.replace(
        '**無印良品 (無印良品 コピス吉祥寺)**',
        f'[**無印良品 (無印良品 コピス吉祥寺)**]({additional_links["無印良品 (無印良品 コピス吉祥寺)"]})'
    )
    text = text.replace(
        '**大創 (DAISO 吉祥寺サンロード店)**',
        f'[**大創 (DAISO 吉祥寺サンロード店)**]({additional_links["大創 (DAISO 吉祥寺サンロード店)"]})'
    )
    text = text.replace(
        '**SATOU (黒毛和牛専門店 さとう 吉祥寺店)**',
        f'[**SATOU (黒毛和牛専門店 さとう 吉祥寺店)**]({additional_links["SATOU (黒毛和牛専門店 さとう 吉祥寺店)"]})'
    )
    text = text.replace(
        '**Linde 德國麵包 (ベッカライカフェ・リンデ 吉祥寺本店)**',
        f'[**Linde 德國麵包 (ベッカライカフェ・リンデ 吉祥寺本店)**]({additional_links["Linde 德國麵包 (ベッカライカフェ・リンデ 吉祥寺本店)"]})'
    )
    text = text.replace(
        '**LE BIHAN (ル ビアン アトレ吉祥寺店)**',
        f'[**LE BIHAN (ル ビアン アトレ吉祥寺店)**]({additional_links["LE BIHAN (ル ビアン アトレ吉祥寺店)"]})'
    )

    with open(fpath, 'w', encoding='utf-8') as f:
        f.write(text)

print("Fixed all remaining spots successfully!")
