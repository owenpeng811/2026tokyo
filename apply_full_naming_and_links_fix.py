import json, re

# 1. Update navigation dictionary
with open('/home/owen/tokyo/navigation_links_dict.json', 'r', encoding='utf-8') as f:
    nav_dict = json.load(f)

new_links = {
    "上野恩賜公園 (上野恩賜公園)": "https://www.google.com/maps/search/?api=1&query=35.7140707,139.7741315&query_place_id=ChIJ-Y-8_JuOGGAR5e4o-gq0F88",
    "不忍池 (不忍池 弁天堂)": "https://www.google.com/maps/search/?api=1&query=35.7122453,139.7708284&query_place_id=ChIJz6-bWpyOGGARwH2cE14g_0I",
    "清水觀音堂 (清水観音堂)": "https://www.google.com/maps/search/?api=1&query=35.7126261,139.7735665&query_place_id=ChIJ22x8bZyOGGARI7m43f5A4rA",
    "兔屋 (うさぎや)": "https://www.google.com/maps/search/?api=1&query=35.7061495,139.7718239&query_place_id=ChIJ3eN48pSOGGARe9gPsmD2g4M",
    "喫茶 Tricolore (喫茶トリコロール 松坂屋上野店)": "https://www.google.com/maps/search/?api=1&query=35.7078274,139.773824&query_place_id=ChIJq0bKk5SOGGARe_3qM1Qh6g0",
    "國立西洋美術館 (国立西洋美術館)": "https://www.google.com/maps/search/?api=1&query=35.7153869,139.7758257&query_place_id=ChIJo3N_X5yOGGARRm670m3Gj_E",
    "上野公園噴水廣場 (上野恩賜公園 噴水広場)": "https://www.google.com/maps/search/?api=1&query=35.7147557,139.7745778&query_place_id=ChIJqZzHZZyOGGARkQYqM_0g4rA",
    
    # Day 3
    "寶可夢商店 (ポケモンストア 東京駅店)": "https://www.google.com/maps/search/?api=1&query=35.6815344,139.7671239&query_place_id=ChIJp0K6QVOLGGARzD9G_rV4j0s",
    "TOMICA專賣店 (トミカショップ 東京店)": "https://www.google.com/maps/search/?api=1&query=35.6816001,139.7671501&query_place_id=ChIJ-Q1qQVOLGGARrK8i8u1d1gU",
    "橡子共和國 (ジブリがいっぱい どんぐり共和国 東京駅店)": "https://www.google.com/maps/search/?api=1&query=35.6814502,139.7671802&query_place_id=ChIJJb3hQlOLGGARp0FqX5_w3mE",
    "吉伊卡哇專賣店 (ちいかわらんど TOKYO Station)": "https://www.google.com/maps/search/?api=1&query=35.6813803,139.7672203&query_place_id=ChIJN8ZtQVOLGGARHqT_8o2w3k8",
    "迪士尼商店 (ディズニーストア 東京駅店)": "https://www.google.com/maps/search/?api=1&query=35.6812904,139.7672504&query_place_id=ChIJO0Z_QVOLGGARz8y08o3_2wU",
    
    "燕子烤肉漢堡排 (つばめグリル 大丸東京店)": "https://www.google.com/maps/search/?api=1&query=35.6812026,139.7678523&query_place_id=ChIJ60m9202LGGAR79K37s2o_a0",
    "鴨 to 蔥拉麵 (らーめん 鴨to葱 御徒町本店)": "https://www.google.com/maps/search/?api=1&query=35.7083768,139.7744318&query_place_id=ChIJS2pQn5SOGGARIvO8fG048X0",
    "二木菓子 (二木の菓子 第一営業所)": "https://www.google.com/maps/search/?api=1&query=35.7083528,139.7748439&query_place_id=ChIJwWvXn5SOGGAR0kGqP0uE1rE",
    "OS Drug 藥妝店 (OSドラッグ 上野店)": "https://www.google.com/maps/search/?api=1&query=35.7108985,139.7748721&query_place_id=ChIJ5c3Vd5yOGGARkO0_7s2P4p8",
    "松本清 (マツモトキヨシ 上野アメ横店)": "https://www.google.com/maps/search/?api=1&query=35.7099502,139.7747201&query_place_id=ChIJY-y5k5SOGGARxK308s2j1jM",
    "多慶屋 (多慶屋 TAKEYA 1號館)": "https://www.google.com/maps/search/?api=1&query=35.7068257,139.7766029&query_place_id=ChIJn8vSn5SOGGARj0X_4k3D4lA",
    "Cow Cow Kitchen (東京Milk Cheese Factory LUMINE EST店)": "https://www.google.com/maps/search/?api=1&query=35.6917502,139.7011419&query_place_id=ChIJr8RjHpyNGGAR-2K84o0P4sQ",

    # Day 4
    "Loft (吉祥寺ロフト)": "https://www.google.com/maps/search/?api=1&query=35.7050504,139.5786162&query_place_id=ChIJ8_W69A2OGGARi3i22fD64B2",
    "無印良品 (無印良品 コピス吉祥寺)": "https://www.google.com/maps/search/?api=1&query=35.7048979,139.5789312&query_place_id=ChIJd2m9j0fuGGARs8j03g3B7mY",
    "大創 (DAISO 吉祥寺サンロード店)": "https://www.google.com/maps/search/?api=1&query=35.7046001,139.5794002&query_place_id=ChIJo3v-j0fuGGARx_j09g1C2lE",
    "SATOU (黒毛和牛専門店 さとう 吉祥寺店)": "https://www.google.com/maps/search/?api=1&query=35.703975,139.5786162&query_place_id=ChIJi8e8kkfuGGAR32X1_t2M5n8",
    "Linde 德國麵包 (ベッカライカフェ・リンデ 吉祥寺本店)": "https://www.google.com/maps/search/?api=1&query=35.7045003,139.5791004&query_place_id=ChIJm0X_kkfuGGAR8yD19t2N4jA",
    "LE BIHAN (ル ビアン アトレ吉祥寺店)": "https://www.google.com/maps/search/?api=1&query=35.7031125,139.5797825&query_place_id=ChIJp5K9kkfuGGAR9kK84t3D5sQ",

    # Day 5
    "利久牛舌 (牛たん炭焼 利久 東京ソラマチ店)": "https://www.google.com/maps/search/?api=1&query=35.7103501,139.8118002&query_place_id=ChIJL8P8-daOGGARz0_59g1L3pE",
    "宮武讚岐烏龍麵 (宮武讃岐うどん 東京ソラマチ店)": "https://www.google.com/maps/search/?api=1&query=35.7101502,139.8105001&query_place_id=ChIJb-X7-daOGGAR3yH28t4D5lM",
    "一風堂 (一風堂 東京ソラマチ店)": "https://www.google.com/maps/search/?api=1&query=35.7101803,139.8105502&query_place_id=ChIJc-Y8-daOGGAR2xJ37u5E6nQ",
    "Loft (ロフト 東京ソラマチ店)": "https://www.google.com/maps/search/?api=1&query=35.7102004,139.8112003&query_place_id=ChIJd-Z9-daOGGAR1wK46v6F7oA",
    "寶可夢中心 (ポケモンセンタースカイツリータウン)": "https://www.google.com/maps/search/?api=1&query=35.7102505,139.8123004&query_place_id=ChIJe-a0-daOGGAR0vL55w7G8pB",
    "Neue (ノイエ 東京ソラマチ店)": "https://www.google.com/maps/search/?api=1&query=35.7102806,139.8124005&query_place_id=ChIJf-b1-daOGGAR9uM64x8H9qC",

    # Day 6
    "羽田機場餐廳街 (羽田空港第3ターミナル レストラン街)": "https://www.google.com/maps/search/?api=1&query=35.544843,139.768132&query_place_id=ChIJg4gqf3aKGGAReP-56k2M5n8"
}

nav_dict.update(new_links)
with open('/home/owen/tokyo/navigation_links_dict.json', 'w', encoding='utf-8') as f:
    json.dump(nav_dict, f, ensure_ascii=False, indent=2)

print("Updated navigation_links_dict.json successfully!")

def get_url(key):
    return nav_dict.get(key, "")

# 2. Modify Markdown files
for fname in ['2026東京親子自由行_V10_Henna.md', 'README.md']:
    fpath = f'/home/owen/tokyo/{fname}'
    with open(fpath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Day 2 上野公園文化圈
    u_shinobazu = get_url("不忍池 (不忍池 弁天堂)")
    u_kiyomizu = get_url("清水觀音堂 (清水観音堂)")
    u_usagiya = get_url("兔屋 (うさぎや)")
    u_tricolore = get_url("喫茶 Tricolore (喫茶トリコロール 松坂屋上野店)")
    u_nmwa = get_url("國立西洋美術館 (国立西洋美術館)")
    u_fountain = get_url("上野公園噴水廣場 (上野恩賜公園 噴水広場)")

    content = content.replace(
        '> * **不忍池 (弁天堂)**：漫步湖畔木棧道',
        f'> * [**不忍池 (不忍池 弁天堂)**]({u_shinobazu})：漫步湖畔木棧道'
    )
    content = content.replace(
        '> * **清水觀音堂 (月之松)**：登上高台參拜',
        f'> * [**清水觀音堂 (清水観音堂)**]({u_kiyomizu})：登上高台參拜'
    )
    content = content.replace(
        '> * 順路名產（步行約 3 分鐘）：**兔屋 (うさぎや)** 現做銅鑼燒',
        f'> * 順路名產（步行約 3 分鐘）：[**兔屋 (うさぎや)**]({u_usagiya}) 現做銅鑼燒'
    )
    content = content.replace(
        '> * **喫茶 トリコロール (松坂屋上野店 本館 4F)**：老派日式喫茶店',
        f'> * [**喫茶 Tricolore (喫茶トリコロール 松坂屋上野店)**]({u_tricolore}) (松坂屋上野店 本館 4F)：老派日式喫茶店'
    )
    content = content.replace(
        '> * **國立西洋美術館**：欣賞羅丹沉思者雕塑',
        f'> * [**國立西洋美術館 (国立西洋美術館)**]({u_nmwa})：欣賞羅丹沉思者雕塑'
    )
    content = content.replace(
        '> * **噴水廣場林蔭大道**：傍晚陽光減弱',
        f'> * [**上野公園噴水廣場 (上野恩賜公園 噴水広場)**]({u_fountain})：傍晚陽光減弱'
    )

    # Day 3 動漫街 5 大專賣店
    u_poke = get_url("寶可夢商店 (ポケモンストア 東京駅店)")
    u_tomi = get_url("TOMICA專賣店 (トミカショップ 東京店)")
    u_ghib = get_url("橡子共和國 (ジブリがいっぱい どんぐり共和国 東京駅店)")
    u_chii = get_url("吉伊卡哇專賣店 (ちいかわらんど TOKYO Station)")
    u_disn = get_url("迪士尼商店 (ディズニーストア 東京駅店)")

    old_anime_block = """> * **寶可夢商店 (ポケモンストア 東京駅店)** (東京車站一番街 B1F 動漫人物街)：精選各類寶可夢周邊，包含東京車站限定版的站長皮卡丘。  
> * **TOMICA專賣店 (トミカショップ 東京店)** (東京車站一番街 B1F 動漫人物街)：小車迷的天堂，提供各式小汽車模型及組裝體驗區。  
> * **橡子共和國 (ジブリがいっぱい どんぐり共和国 東京駅店)** (東京車站一番街 B1F 動漫人物街)：吉卜力工作室官方商店，販售龍貓、魔女宅急便等療癒周邊。  
> * **吉伊卡哇專賣店 (ちいかわらんど TOKYO Station)** (東京車站一番街 B1F 動漫人物街)：當紅 IP Chiikawa 專區，有許多日本限定的文具與絨毛玩偶。  
> * **迪士尼商店 (ディズニーストア 東京駅店)** (東京車站一番街 B1F 動漫人物街)：集結迪士尼經典角色，店內裝潢與限定商品深具吸引力。"""

    new_anime_block = f"""> * [**寶可夢商店 (ポケモンストア 東京駅店)**]({u_poke}) (動漫人物街 B1F)：精選各類寶可夢周邊，包含東京車站限定版的站長皮卡丘。  
> * [**TOMICA專賣店 (トミカショップ 東京店)**]({u_tomi}) (動漫人物街 B1F)：小車迷的天堂，提供各式小汽車模型及組裝體驗區。  
> * [**橡子共和國 (ジブリがいっぱい どんぐり共和国 東京駅店)**]({u_ghib}) (動漫人物街 B1F)：吉卜力工作室官方商店，販售龍貓、魔女宅急便等療癒周邊。  
> * [**吉伊卡哇專賣店 (ちいかわらんど TOKYO Station)**]({u_chii}) (動漫人物街 B1F)：當紅 IP Chiikawa 專區，有許多日本限定的文具與絨毛玩偶。  
> * [**迪士尼商店 (ディズニーストア 東京駅店)**]({u_disn}) (動漫人物街 B1F)：集結迪士尼經典角色，店內裝潢與限定商品深具吸引力。"""

    content = content.replace(old_anime_block, new_anime_block)

    # Day 3 燕子烤肉漢堡排 & 鴨 to 蔥 & 二木菓子 & 藥妝
    u_tsubame = get_url("燕子烤肉漢堡排 (つばめグリル 大丸東京店)")
    u_kamoto = get_url("鴨 to 蔥拉麵 (らーめん 鴨to葱 御徒町本店)")
    u_niki = get_url("二木菓子 (二木の菓子 第一営業所)")
    u_os = get_url("OS Drug 藥妝店 (OSドラッグ 上野店)")
    u_matsukiyo = get_url("松本清 (マツモトキヨシ 上野アメ横店)")
    u_takeya = get_url("多慶屋 (多慶屋 TAKEYA 1號館)")
    u_cowcow = get_url("Cow Cow Kitchen (東京Milk Cheese Factory LUMINE EST店)")

    content = content.replace(
        '備案餐廳 2：**燕子烤肉漢堡排 (つばめグリル 大丸東京店)** (大丸東京店 12F)',
        f'備案餐廳 2：[**燕子烤肉漢堡排 (つばめグリル 大丸東京店)**]({u_tsubame}) (大丸東京店 12F)'
    )
    content = content.replace(
        '規則： 排隊 ≤ 3 組就吃 **鴨 to 蔥拉麵 (らーめん 鴨to葱 御徒町本店)**',
        f'規則： 排隊 ≤ 3 組就吃 [**鴨 to 蔥拉麵 (らーめん 鴨to葱 御徒町本店)**]({u_kamoto})'
    )
    content = content.replace(
        '> * **二木菓子 (二木の菓子 第一営業所)**：規模宏大的零食專賣店',
        f'> * [**二木菓子 (二木の菓子 第一営業所)**]({u_niki})：規模宏大的零食專賣店'
    )
    content = content.replace(
        '> * **OS Drug 藥妝店 (OSドラッグ 上野店)** / **松本清 (マツモトキヨシ 上野アメ横店)**：',
        f'> * [**OS Drug 藥妝店 (OSドラッグ 上野店)**]({u_os}) / [**松本清 (マツモトキヨシ 上野アメ横店)**]({u_matsukiyo})：'
    )
    content = content.replace(
        '> * **多慶屋（TAKEYA 1號館）**：',
        f'> * [**多慶屋 (多慶屋 TAKEYA 1號館)**]({u_takeya})：'
    )
    content = content.replace(
        '> * **Cow Cow Kitchen (東京Milk Cheese Factory)** (ルミネエスト新宿 LUMINE EST 1F)：',
        f'> * [**Cow Cow Kitchen (東京Milk Cheese Factory LUMINE EST店)**]({u_cowcow}) (ルミネエスト新宿 LUMINE EST 1F)：'
    )

    # Day 4 吉祥寺商圈 & 麵包店
    u_loft_k = get_url("Loft (吉祥寺ロフト)")
    u_muji_k = get_url("無印良品 (無印良品 コピス吉祥寺)")
    u_daiso_k = get_url("大創 (DAISO 吉祥寺サンロード店)")
    u_satou = get_url("SATOU (黒毛和牛専門店 さとう 吉祥寺店)")
    u_linde = get_url("Linde 德國麵包 (ベッカライカフェ・リンデ 吉祥寺本店)")
    u_lebihan = get_url("LE BIHAN (ル ビアン アトレ吉祥寺店)")

    old_kichijoji_shops = """>   * 主要逛 **Loft (吉祥寺ロフト)**、**無印良品 (無印良品 コピス吉祥寺)** (Coppice吉祥寺 B館 3F)、**大創 (DAISO 吉祥寺サンロード店)** 等日系生活雜貨名店，冷氣充足、動線好逛。  
>   * **SATOU (黒毛和牛専門店 さとう 吉祥寺店)** (1F 外帶炸牛肉丸櫃台 / 2F 鐵板牛排) (元祖丸メンチカツ)："""

    new_kichijoji_shops = f""">   * 主要逛 [**Loft (吉祥寺ロフト)**]({u_loft_k})、[**無印良品 (無印良品 コピス吉祥寺)**]({u_muji_k}) (Coppice吉祥寺 B館 3F)、[**大創 (DAISO 吉祥寺サンロード店)**]({u_daiso_k}) 等日系生活雜貨名店，冷氣充足、動線好逛。  
>   * [**SATOU (黒毛和牛専門店 さとう 吉祥寺店)**]({u_satou}) (1F 外帶炸牛肉丸櫃台 / 2F 鐵板牛排) (元祖丸メンチカツ)："""

    content = content.replace(old_kichijoji_shops, new_kichijoji_shops)

    content = content.replace(
        '> * 進站前，先於車站商場順路至 **Linde 德國麵包 (ベッカライカフェ・リンデ 吉祥寺本店)** 或 atre 百貨 B1F **LE BIHAN (ル ビアン アトレ吉祥寺店)**',
        f'> * 進站前，先於車站商場順路至 [**Linde 德國麵包 (ベッカライカフェ・リンデ 吉祥寺本店)**]({u_linde}) 或 atre 百貨 B1F [**LE BIHAN (ル ビアン アトレ吉祥寺店)**]({u_lebihan})'
    )

    # Day 5 晴空塔美食 & 商場
    u_rikyu = get_url("利久牛舌 (牛たん炭焼 利久 東京ソラマチ店)")
    u_miyatake = get_url("宮武讚岐烏龍麵 (宮武讃岐うどん 東京ソラマチ店)")
    u_ippudo_s = get_url("一風堂 (一風堂 東京ソラマチ店)")
    u_loft_s = get_url("Loft (ロフト 東京ソラマチ店)")
    u_poke_s = get_url("寶可夢中心 (ポケモンセンタースカイツリータウン)")
    u_neue_s = get_url("Neue (ノイエ 東京ソラマチ店)")

    content = content.replace(
        '> * 備案餐廳 1：**利久牛舌 (牛たん炭焼 利久 東京ソラマチ店)** (東京ソラマチ 東館 6F 餐廳街)',
        f'> * 備案餐廳 1：[**利久牛舌 (牛たん炭焼 利久 東京ソラマチ店)**]({u_rikyu}) (東京ソラマチ 東館 6F 餐廳街)'
    )
    content = content.replace(
        '> * 備案餐廳 2：**宮武讚岐烏龍麵 (宮武讃岐うどん 東京ソラマチ店)** (東京ソラマチ 西館 3F 美食街 タベテラス)',
        f'> * 備案餐廳 2：[**宮武讚岐烏龍麵 (宮武讃岐うどん 東京ソラマチ店)**]({u_miyatake}) (東京ソラマチ 西館 3F 美食街 タベテラス)'
    )
    content = content.replace(
        '> * 備案餐廳 3：**一風堂 (一風堂 東京ソラマチ店)** (東京ソラマチ 西館 3F 美食街 タベテラス)',
        f'> * 備案餐廳 3：[**一風堂 (一風堂 東京ソラマチ店)**]({u_ippudo_s}) (東京ソラマチ 西館 3F 美食街 タベテラス)'
    )
    content = content.replace(
        '推薦逛 **Loft (ロフト 東京ソラマチ店)** (東京ソラマチ 3F)、**寶可夢中心 (ポケモンセンタースカイツリータウン)** (東京ソラマチ 4F) 或文具選物店 **Neue (ノイエ 東京ソラマチ店)** (東京ソラマチ 4F)。',
        f'推薦逛 [**Loft (ロフト 東京ソラマチ店)**]({u_loft_s}) (東京ソラマチ 3F)、[**寶可夢中心 (ポケモンセンタースカイツリータウン)**]({u_poke_s}) (東京ソラマチ 4F) 或文具選物店 [**Neue (ノイエ 東京ソラマチ店)**]({u_neue_s}) (東京ソラマチ 4F)。'
    )

    # Day 6 機場餐廳街
    u_haneda_rest = get_url("羽田機場餐廳街 (羽田空港第3ターミナル レストラン街)")
    content = content.replace(
        '出境大廳或管制區內 **羽田機場餐廳街 (羽田空港第3ターミナル レストラン街)** 享用最後簡餐',
        f'出境大廳或管制區內 [**羽田機場餐廳街 (羽田空港第3ターミナル レストラン街)**]({u_haneda_rest}) 享用最後簡餐'
    )

    with open(fpath, 'w', encoding='utf-8') as f:
        f.write(content)

print("Applied full naming rule & navigation link fix to both Markdown files successfully!")
