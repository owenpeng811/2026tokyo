import json

with open('/home/owen/tokyo/navigation_links_dict.json', 'r', encoding='utf-8') as f:
    nav_dict = json.load(f)

FIRST_DESTINATIONS = {
    # Day 1
    (1, "機場整備與購票"): nav_dict.get("羽田機場第3航廈"),
    (1, "前往飯店"): nav_dict.get("海茵娜酒店"),
    (1, "Check-in"): nav_dict.get("海茵娜酒店"),
    (1, "前往秋葉原"): nav_dict.get("淺草橋站"),
    (1, "秋葉原大型電玩體驗"): nav_dict.get("GiGO 秋葉原3號館"),
    (1, "日系拍貼機全家合影體驗"): nav_dict.get("日系拍貼機體驗 (Purikura / GiGO 拍貼機專區)"),
    (1, "萬代官方扭蛋體驗"): nav_dict.get("萬代扭蛋百貨店 秋葉原店"),
    (1, "晚餐：壽司郎"): nav_dict.get("壽司郎 (スシロー 秋葉原駅前店)"),
    (1, "返回淺草橋"): nav_dict.get("秋葉原站"),
    (1, "前往新宿東口"): nav_dict.get("淺草橋站"),
    (1, "欣賞新宿 3D 巨貓"): nav_dict.get("Cross Shinjuku 3D 巨貓 (クロス新宿ビジョン)"),
    (1, "晚餐：Gusto 家庭餐廳"): nav_dict.get("Gusto (ガスト 新宿NOWAビル店)"),
    (1, "生鮮超市採買"): nav_dict.get("肉之Hanamasa超市"),
    (1, "回飯店休息"): nav_dict.get("海茵娜酒店"),
    (1, "準時就寢"): nav_dict.get("海茵娜酒店"),

    # Day 2 Parents
    (2, "前往上野御徒町"): nav_dict.get("淺草橋站"),
    (2, "晨間不忍池與清水觀音堂散步"): nav_dict.get("不忍池"),
    (2, "室內基地營避暑"): nav_dict.get("DEAN & DELUCA CAFE (PARCO_ya 1F)"),
    (2, "午餐：すき家"): nav_dict.get("すき家 (すき家 上野三丁目店)"),
    (2, "參觀國立西洋美術館"): nav_dict.get("國立西洋美術館"),
    (2, "傍晚噴水廣場林蔭散步"): nav_dict.get("上野公園噴水廣場"),
    (2, "晚餐：宇奈とと鰻魚飯"): nav_dict.get("名代 宇奈とと (名代 宇奈とと 上野店)"),
    (2, "返回淺草橋"): nav_dict.get("御徒町站"),

    # Day 2 Kids
    (2, "前往東京迪士尼樂園"): nav_dict.get("淺草橋站"),
    (2, "抵達樂園入園"): nav_dict.get("東京迪士尼樂園"),
    (2, "暢玩熱門遊樂設施"): nav_dict.get("美女與野獸：魔法物語"),
    (2, "欣賞日間遊行與午後設施"): nav_dict.get("東京迪士尼樂園"),
    (2, "午餐：園區主題餐廳"): nav_dict.get("東京迪士尼樂園"),
    (2, "晚餐：主題餐廳"): nav_dict.get("廣場閣樓餐廳"),
    (2, "城堡夜間點燈拍照與遊行卡位"): nav_dict.get("東京迪士尼樂園"),
    (2, "欣賞電子大遊行「夢之光」"): nav_dict.get("東京迪士尼樂園"),
    (2, "欣賞城堡高空投影秀"): nav_dict.get("東京迪士尼樂園"),
    (2, "世界市集紀念品採買與出園"): nav_dict.get("東京迪士尼樂園"),
    (2, "返回淺草橋"): nav_dict.get("東京迪士尼樂園"),

    # Day 3
    (3, "前往東京車站"): nav_dict.get("淺草橋站"),
    (3, "欣賞東京車站丸之內站舍建築"): nav_dict.get("東京車站丸之內站舍 (東京駅丸の内駅舎)"),
    (3, "移動至東京車站一番街"): nav_dict.get("東京車站一番街 (東京駅一番街)"),
    (3, "逛東京車站一番街動漫街"): nav_dict.get("東京車站一番街 (東京駅一番街)"),
    (3, "KITTE頂樓花園眺望東京車站"): nav_dict.get("KITTE花園 (ＫＩＴＴＥガーデン)"),
    (3, "午餐：天丼てんや"): nav_dict.get("天丼てんや (天丼てんや 八重洲店)"),
    (3, "前往上野"): nav_dict.get("東京站"),
    (3, "參觀國立科學博物館"): nav_dict.get("國立科學博物館 (国立科学博物館)"),
    (3, "晚餐：鴨 to 蔥拉麵"): nav_dict.get("鴨 to 蔥拉麵 (らーめん 鴨to葱 御徒町本店)"),
    (3, "阿美橫丁逛街採買"): nav_dict.get("二木菓子 (二木の菓子 第一営業所)"),
    (3, "前往御徒町站搭車"): nav_dict.get("御徒町站"),
    (3, "晚餐：吉野家（若下午未吃拉麵）"): nav_dict.get("吉野家 (吉野家 浅草橋店)"),
    (3, "外帶點心宵夜（若下午已吃拉麵）"): nav_dict.get("Cow Cow Kitchen (東京Milk Cheese Factory)"),

    # Day 4
    (4, "前往三鷹"): nav_dict.get("淺草橋站"),
    (4, "搭乘吉卜力接駁巴士"): nav_dict.get("三鷹站"),
    (4, "參觀三鷹之森吉卜力美術館"): nav_dict.get("三鷹之森吉卜力美術館 (三鷹の森ジブリ美術館)"),
    (4, "前往吉祥寺"): nav_dict.get("井之頭恩賜公園"),
    (4, "午餐：大戶屋"): nav_dict.get("大戶屋 (大戶屋ごはん処 吉祥寺店)"),
    (4, "吉祥寺商圈漫遊與下午茶"): nav_dict.get("吉祥寺 Sunroad 商店街"),
    (4, "晚餐：串家物語"): nav_dict.get("串家物語 (神楽食堂 串家物語 吉祥寺店)"),
    (4, "返回淺草橋"): nav_dict.get("吉祥寺站"),
    (4, "回飯店休息"): nav_dict.get("海茵娜酒店"),

    # Day 5
    (5, "前往淺草"): nav_dict.get("淺草橋站"),
    (5, "參觀淺草寺與雷門散策"): nav_dict.get("雷門 (雷門)"),
    (5, "淺草文化觀光中心眺望晴空塔"): nav_dict.get("淺草文化觀光中心 (浅草文化観光センター)"),
    (5, "前往東京晴空塔"): nav_dict.get("淺草站"),
    (5, "午餐：達摩文字燒"): nav_dict.get("達摩文字燒 (月島名物もんじゃ だるま 東京スカイツリータウン・ソラマチ店)"),
    (5, "參觀墨田水族館"): nav_dict.get("墨田水族館 (すみだ水族館)"),
    (5, "晴空街道散策與高空景觀"): nav_dict.get("東京晴空街道 (東京ソラマチ)"),
    (5, "前往新宿西口"): nav_dict.get("東京晴空塔站"),
    (5, "晚餐：麥當勞"): nav_dict.get("麥當勞 (マクドナルド 新宿西口店)"),
    (5, "登上東京都廳俯瞰百萬夜景"): nav_dict.get("東京都廳第一本廳舍 (東京都庁舎)"),
    (5, "晴空街道伴手禮採買"): nav_dict.get("東京晴空街道 (東京ソラマチ)"),
    (5, "晚餐：晴空街道美食街"): nav_dict.get("宮武讚岐烏龍麵 (宮武讃岐うどん 東京ソラマチ店)"),
    (5, "返回淺草橋"): nav_dict.get("押上站"),
    (5, "回飯店打包行李"): nav_dict.get("海茵娜酒店"),

    # Day 6
    (6, "早餐與整理行李"): nav_dict.get("海茵娜酒店"),
    (6, "飯店退房與寄放行李"): nav_dict.get("海茵娜酒店"),
    (6, "前往築地場外市場"): nav_dict.get("淺草橋站"),
    (6, "築地場外市場美食散策"): nav_dict.get("築地山長 (つきぢ山長)"),
    (6, "返回淺草橋飯店"): nav_dict.get("東銀座站"),
    (6, "領取行李並前往車站"): nav_dict.get("海茵娜酒店"),
    (6, "前往羽田機場"): nav_dict.get("淺草橋站"),
    (6, "辦理登機與行李託運"): nav_dict.get("羽田機場第3航廈"),
    (6, "機場輕食午餐與免稅採買"): nav_dict.get("羽田機場第3航廈"),
    (6, "搭機返台"): nav_dict.get("羽田機場第3航廈")
}

with open('/home/owen/tokyo/first_destinations.json', 'w', encoding='utf-8') as f:
    json.dump({f"{d}_{k}": v for (d, k), v in FIRST_DESTINATIONS.items() if v}, f, ensure_ascii=False, indent=2)

print("Updated first_destinations.json with activity names!")
