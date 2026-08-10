import re, json

with open('/home/owen/tokyo/navigation_links_dict.json', 'r', encoding='utf-8') as f:
    nav_dict = json.load(f)

# Ensure navigation dictionary contains all necessary entities
nav_dict["押上站 (押上駅)"] = "https://www.google.com/maps/search/?api=1&query=35.710448,139.8132155&query_place_id=ChIJn84f3CmPGGARP2Jv-Wz2sL0"
nav_dict["東京都廳 (東京都庁)"] = "https://www.google.com/maps/search/?api=1&query=35.6894807,139.6917502&query_place_id=ChIJ60m9202LGGAR79K37s2o_a8"
nav_dict["東京都廳南展望室 (東京都庁 南展望室)"] = "https://www.google.com/maps/search/?api=1&query=35.6894807,139.6917502&query_place_id=ChIJ60m9202LGGAR79K37s2o_a8"
nav_dict["DEAN & DELUCA CAFE (DEAN & DELUCA CAFE パルコヤ上野)"] = "https://www.google.com/maps/search/?api=1&query=35.7068605,139.7733596&query_place_id=ChIJYw_RZZyOGGARkQYqM_0g4r8"
nav_dict["喫茶 Tricolore (喫茶トリコロール 松坂屋上野店)"] = "https://www.google.com/maps/search/?api=1&query=35.7078274,139.7733596&query_place_id=ChIJp0K6QVOLGGARzD9G_rV4j0s"
nav_dict["松坂屋地下美食街 (松坂屋上野店 ほっぺタウン)"] = "https://www.google.com/maps/search/?api=1&query=35.707472,139.773395&query_place_id=ChIJo3tx-Z-OGGARmtgBAh8wp8o"
nav_dict["松坂屋 (松坂屋 上野店)"] = "https://www.google.com/maps/search/?api=1&query=35.707472,139.773395&query_place_id=ChIJo3tx-Z-OGGARmtgBAh8wp8o"
nav_dict["PARCO_ya (PARCO_ya 上野)"] = "https://www.google.com/maps/search/?api=1&query=35.7068605,139.7733596&query_place_id=ChIJYw_RZZyOGGARkQYqM_0g4r8"
nav_dict["不忍池 (不忍池 弁天堂)"] = "https://www.google.com/maps/search/?api=1&query=35.7122453,139.7709849&query_place_id=ChIJz-n2a5yOGGARkO91888iW-Q"
nav_dict["清水觀音堂 (清水観音堂)"] = "https://www.google.com/maps/search/?api=1&query=35.7126261,139.7735391&query_place_id=ChIJqZzHZZyOGGARkQYqM_0g4r8"
nav_dict["兔屋 (うさぎや)"] = "https://www.google.com/maps/search/?api=1&query=35.7061495,139.7725974&query_place_id=ChIJp0K6QVOLGGARzD9G_rV4j07"
nav_dict["國立西洋美術館 (国立西洋美術館)"] = "https://www.google.com/maps/search/?api=1&query=35.7153869,139.7758145&query_place_id=ChIJl1155pyOGGAR23aZpC-Y27A"
nav_dict["多慶屋 (多慶屋 TAKEYA1)"] = "https://www.google.com/maps/search/?api=1&query=35.7068257,139.7770977&query_place_id=ChIJi8e8_JuOGGAR5e4o-gq0F88"
nav_dict["廣場閣樓餐廳 (プラザパビリオン・レストラン)"] = "https://www.google.com/maps/search/?api=1&query=35.6328604,139.8803604&query_place_id=ChIJszdHEQN9GGARy9MJ1TY22eM"
nav_dict["莎拉奶奶之家餐廳 (グランマ・サラのキッチン)"] = "https://www.google.com/maps/search/?api=1&query=35.631147,139.878847&query_place_id=ChIJszdHEQN9GGARy9MJ1TY22eQ"
nav_dict["明日樂園舞台餐廳 (トゥモローランド・テラス)"] = "https://www.google.com/maps/search/?api=1&query=35.6328964,139.8803943&query_place_id=ChIJszdHEQN9GGARy9MJ1TY22eR"
nav_dict["CoCo壹番屋 (CoCo壱番屋 JR秋葉原駅昭和通り口店)"] = "https://www.google.com/maps/search/?api=1&query=35.6984515,139.7757913&query_place_id=ChIJ8Y-8_JuOGGAR5e4o-gq0F96"
nav_dict["松屋 (松屋 上野店)"] = "https://www.google.com/maps/search/?api=1&query=35.710037,139.773889&query_place_id=ChIJZ44cNJ6OGGAR5MROF68O1B0"
nav_dict["築地丸武 (丸武 玉子焼)"] = "https://www.google.com/maps/search/?api=1&query=35.6652495,139.7702808&query_place_id=ChIJb328XZ-OGGAR5e4o-gq0F97"
nav_dict["新宿站 (新宿駅)"] = "https://www.google.com/maps/search/?api=1&query=35.6895924,139.7004128&query_place_id=ChIJ126rX_uLGGARvj7L442E6p0"
nav_dict["淺草橋站(浅草橋駅)"] = "https://www.google.com/maps/search/?api=1&query=35.6974952,139.7865048&query_place_id=ChIJi8e8_JuOGGAR5e4o-gq0F87"

with open('/home/owen/tokyo/navigation_links_dict.json', 'w', encoding='utf-8') as f:
    json.dump(nav_dict, f, ensure_ascii=False, indent=2)

# Replacements map
replacements = {
    "**押上站 (押上駅)**": f"[**押上站 (押上駅)**]({nav_dict['押上站 (押上駅)']})",
    "**東京都廳 (東京都庁)**": f"[**東京都廳 (東京都庁)**]({nav_dict['東京都廳 (東京都庁)']})",
    "**東京都廳南展望室 (東京都庁 南展望室)**": f"[**東京都廳南展望室 (東京都庁 南展望室)**]({nav_dict['東京都廳南展望室 (東京都庁 南展望室)']})",
    "**DEAN & DELUCA CAFE (DEAN & DELUCA CAFE パルコヤ上野)**": f"[**DEAN & DELUCA CAFE (DEAN & DELUCA CAFE パルコヤ上野)**]({nav_dict['DEAN & DELUCA CAFE (DEAN & DELUCA CAFE パルコヤ上野)']})",
    "**喫茶 Tricolore (喫茶トリコロール 松坂屋上野店)**": f"[**喫茶 Tricolore (喫茶トリコロール 松坂屋上野店)**]({nav_dict['喫茶 Tricolore (喫茶トリコロール 松坂屋上野店)']})",
    "**松坂屋地下美食街 (松坂屋上野店 ほっぺタウン)**": f"[**松坂屋地下美食街 (松坂屋上野店 ほっぺタウン)**]({nav_dict['松坂屋地下美食街 (松坂屋上野店 ほっぺタウン)']})",
    "**松坂屋 (松坂屋 上野店)**": f"[**松坂屋 (松坂屋 上野店)**]({nav_dict['松坂屋 (松坂屋 上野店)']})",
    "**PARCO_ya (PARCO_ya 上野)**": f"[**PARCO_ya (PARCO_ya 上野)**]({nav_dict['PARCO_ya (PARCO_ya 上野)']})",
    "**不忍池 (不忍池 弁天堂)**": f"[**不忍池 (不忍池 弁天堂)**]({nav_dict['不忍池 (不忍池 弁天堂)']})",
    "**清水觀音堂 (清水観音堂)**": f"[**清水觀音堂 (清水観音堂)**]({nav_dict['清水觀音堂 (清水観音堂)']})",
    "**兔屋 (うさぎや)**": f"[**兔屋 (うさぎや)**]({nav_dict['兔屋 (うさぎや)']})",
    "**國立西洋美術館 (国立西洋美術館)**": f"[**國立西洋美術館 (国立西洋美術館)**]({nav_dict['國立西洋美術館 (国立西洋美術館)']})",
    "**多慶屋 (多慶屋 TAKEYA1)**": f"[**多慶屋 (多慶屋 TAKEYA1)**]({nav_dict['多慶屋 (多慶屋 TAKEYA1)']})",
    "**廣場閣樓餐廳 (プラザパビリオン・レストラン)**": f"[**廣場閣樓餐廳 (プラザパビリオン・レストラン)**]({nav_dict['廣場閣樓餐廳 (プラザパビリオン・レストラン)']})",
    "**莎拉奶奶之家餐廳 (グランマ・サラのキッチン)**": f"[**莎拉奶奶之家餐廳 (グランマ・サラのキッチン)**]({nav_dict['莎拉奶奶之家餐廳 (グランマ・サラのキッチン)']})",
    "**明日樂園舞台餐廳 (トゥモローランド・テラス)**": f"[**明日樂園舞台餐廳 (トゥモローランド・テラス)**]({nav_dict['明日樂園舞台餐廳 (トゥモローランド・テラス)']})",
    "**CoCo壹番屋 (CoCo壱番屋 JR秋葉原駅昭和通り口店)**": f"[**CoCo壹番屋 (CoCo壱番屋 JR秋葉原駅昭和通り口店)**]({nav_dict['CoCo壹番屋 (CoCo壱番屋 JR秋葉原駅昭和通り口店)']})",
    "**松屋 (松屋 上野店)**": f"[**松屋 (松屋 上野店)**]({nav_dict['松屋 (松屋 上野店)']})",
    "**築地丸武 (丸武 玉子焼)**": f"[**築地丸武 (丸武 玉子焼)**]({nav_dict['築地丸武 (丸武 玉子焼)']})",
    "**新宿站 (新宿駅)**": f"[**新宿站 (新宿駅)**]({nav_dict['新宿站 (新宿駅)']})"
}

for fname in ['README.md', '2026東京親子自由行_V10_Henna.md']:
    fpath = f'/home/owen/tokyo/{fname}'
    with open(fpath, 'r', encoding='utf-8') as f:
        content = f.read()

    for k, v in replacements.items():
        content = content.replace(k, v)

    with open(fpath, 'w', encoding='utf-8') as f:
        f.write(content)

print("Replaced all bare bold entities with complete navigation links in both Markdown files!")
