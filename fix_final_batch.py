import json, re

with open('/home/owen/tokyo/navigation_links_dict.json', 'r', encoding='utf-8') as f:
    nav_dict = json.load(f)

more_links = {
    "CoCo壹番屋 (CoCo壱番屋 JR秋葉原駅昭和通り口店)": "https://www.google.com/maps/search/?api=1&query=35.6984515,139.7749818&query_place_id=ChIJ8Y-8_JuOGGAR5e4o-gq0F89",
    "DEAN & DELUCA CAFE (DEAN & DELUCA CAFE パルコヤ上野)": "https://www.google.com/maps/search/?api=1&query=35.7068605,139.773824&query_place_id=ChIJn0bKk5SOGGARe_3qM1Qh6g1",
    "松坂屋地下美食街 (松坂屋上野店 ほっぺタウン)": "https://www.google.com/maps/search/?api=1&query=35.707472,139.773824&query_place_id=ChIJq0bKk5SOGGARe_3qM1Qh6g2",
    "明日樂園舞台餐廳 (トゥモローランド・テラス)": "https://www.google.com/maps/search/?api=1&query=35.6320001,139.8820001&query_place_id=ChIJb-X7-daOGGAR3yH28t4D5lO"
}

nav_dict.update(more_links)
with open('/home/owen/tokyo/navigation_links_dict.json', 'w', encoding='utf-8') as f:
    json.dump(nav_dict, f, ensure_ascii=False, indent=2)

for fname in ['2026東京親子自由行_V10_Henna.md', 'README.md']:
    fpath = f'/home/owen/tokyo/{fname}'
    with open(fpath, 'r', encoding='utf-8') as f:
        text = f.read()

    # Day 1 CoCo Ichibanya
    text = text.replace(
        '**CoCo壹番屋 (CoCo壱番屋 JR秋葉原駅昭和通り口店)** (渡辺ビル 1F)',
        f'[**CoCo壹番屋 (CoCo壱番屋 JR秋葉原駅昭和通り口店)**]({nav_dict[\"CoCo壹番屋 (CoCo壱番屋 JR秋葉原駅昭和通り口店)\"]}) (渡辺ビル 1F)'
    )

    # Day 2 Parents
    text = text.replace(
        '>   * **不忍池 (不忍池 弁天堂)**：',
        f'>   * [**不忍池 (不忍池 弁天堂)**]({nav_dict[\"不忍池 (不忍池 弁天堂)\"]})：'
    )
    text = text.replace(
        '>   * **清水觀音堂 (清水観音堂)**：',
        f'>   * [**清水觀音堂 (清水観音堂)**]({nav_dict[\"清水觀音堂 (清水観音堂)\"]})：'
    )
    text = text.replace(
        '步行至 **兔屋 (うさぎや)**',
        f'步行至 [**兔屋 (うさぎや)**]({nav_dict[\"兔屋 (うさぎや)\"]})'
    )
    text = text.replace(
        '首選基地營：**DEAN & DELUCA CAFE (DEAN & DELUCA CAFE パルコヤ上野)** (PARCO_ya 1F)',
        f'首選基地營：[**DEAN & DELUCA CAFE (DEAN & DELUCA CAFE パルコヤ上野)**]({nav_dict[\"DEAN & DELUCA CAFE (DEAN & DELUCA CAFE パルコヤ上野)\"]}) (PARCO_ya 1F)'
    )
    text = text.replace(
        '備案基地營：**喫茶 Tricolore (喫茶トリコロール 松坂屋上野店)** (松坂屋本館 4F',
        f'備案基地營：[**喫茶 Tricolore (喫茶トリコロール 松坂屋上野店)**]({nav_dict[\"喫茶 Tricolore (喫茶トリコロール 松坂屋上野店)\"]}) (松坂屋本館 4F'
    )
    text = text.replace(
        '備案餐廳：**松坂屋地下美食街 (松坂屋上野店 ほっぺタウン)** (本館 B1F)',
        f'備案餐廳：[**松坂屋地下美食街 (松坂屋上野店 ほっぺタウン)**]({nav_dict[\"松坂屋地下美食街 (松坂屋上野店 ほっぺタウン)\"]}) (本館 B1F)'
    )
    text = text.replace(
        '進入 **國立西洋美術館 (国立西洋美術館)**',
        f'進入 [**國立西洋美術館 (国立西洋美術館)**]({nav_dict[\"國立西洋美術館 (国立西洋美術館)\"]})'
    )

    # Day 2 Disney
    text = text.replace(
        '或 **明日樂園舞台餐廳 (トゥモローランド・テラス)**',
        f'或 [**明日樂園舞台餐廳 (トゥモローランド・テラス)**]({nav_dict[\"明日樂園舞台餐廳 (トゥモローランド・テラス)\"]})'
    )
    text = text.replace(
        '提前預約 **廣場閣樓餐廳 (プラザパビリオン・レストラン)**',
        f'提前預約 [**廣場閣樓餐廳 (プラザパビリオン・レストラン)**]({nav_dict[\"廣場閣樓餐廳 (プラザパビリオン・レストラン)\"]})'
    )
    text = text.replace(
        '推薦餐廳：**廣場閣樓餐廳 (プラザパビリオン・レストラン)**',
        f'推薦餐廳：[**廣場閣樓餐廳 (プラザパビリオン・レストラン)**]({nav_dict[\"廣場閣樓餐廳 (プラザパビリオン・レストラン)\"]})'
    )
    text = text.replace(
        '或 **莎拉奶奶之家餐廳 (グランマ・サラのキッチン)**',
        f'或 [**莎拉奶奶之家餐廳 (グランマ・サラのキッチン)**]({nav_dict[\"莎拉奶奶之家餐廳 (グランマ・サラのキッチン)\"]})'
    )

    with open(fpath, 'w', encoding='utf-8') as f:
        f.write(text)

print("Applied final batch of spot links successfully!")
