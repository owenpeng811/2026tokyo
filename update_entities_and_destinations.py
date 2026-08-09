import json
import re

with open('/home/owen/tokyo/navigation_links_dict.json', 'r', encoding='utf-8') as f:
    nav_dict = json.load(f)

# Specific First Destination mapping per (day, slot_title_pattern)
FIRST_DESTINATIONS = {
    # Day 1
    (1, "機場整備與購票"): nav_dict.get("羽田機場第3航廈"),
    (1, "前往飯店"): nav_dict.get("海茵娜酒店"),
    (1, "Check-in"): nav_dict.get("海茵娜酒店"),
    (1, "前往秋葉原"): nav_dict.get("淺草橋站"),
    (1, "GiGO 秋葉原3號館"): nav_dict.get("GiGO 秋葉原3號館"),
    (1, "日系拍貼機體驗"): nav_dict.get("日系拍貼機體驗 (Purikura / GiGO 拍貼機專區)"),
    (1, "萬代扭蛋百貨店"): nav_dict.get("萬代扭蛋百貨店 秋葉原店"),
    (1, "壽司郎"): nav_dict.get("壽司郎 (スシロー 秋葉原駅前店)"),
    (1, "返回淺草橋"): nav_dict.get("秋葉原站"),
    (1, "交通出發與轉乘"): nav_dict.get("淺草橋站"),
    (1, "Cross Shinjuku"): nav_dict.get("Cross Shinjuku 3D 巨貓 (クロス新宿ビジョン)"),
    (1, "新宿東口家庭友善美食"): nav_dict.get("Gusto (ガスト 新宿NOWAビル店)"),
    (1, "地方生鮮超市採買"): nav_dict.get("肉之Hanamasa超市"),
    (1, "回飯店休息"): nav_dict.get("海茵娜酒店"),
    (1, "準時就寢"): nav_dict.get("海茵娜酒店"),

    # Day 2 Parents
    (2, "出發前往上野御徒町"): nav_dict.get("淺草橋站"),
    (2, "晨間清涼戶外散步"): nav_dict.get("不忍池"),  # <<--- First destination is 不忍池!
    (2, "進入室內基地營避暑"): nav_dict.get("DEAN & DELUCA CAFE (PARCO_ya 1F)"),
    (2, "午餐"): nav_dict.get("すき家 (すき家 上野三丁目店)"),
    (2, "正午酷暑亮點：國立西洋美術館"): nav_dict.get("國立西洋美術館"),
    (2, "傍晚戶外悠閒漫步"): nav_dict.get("上野公園噴水廣場"),
    (2, "晚餐"): nav_dict.get("名代 宇奈とと (名代 宇奈とと 上野店)"),
    (2, "回程：前往JR 御徒町站"): nav_dict.get("御徒町站"),

    # Day 2 Kids
    (2, "迪士尼交通動線"): nav_dict.get("淺草橋站"),
    (2, "抵達樂園門口"): nav_dict.get("東京迪士尼樂園"),
    (2, "必玩設施與行程建議"): nav_dict.get("美女與野獸：魔法物語"),
    (2, "午後行程與遊行"): nav_dict.get("東京迪士尼樂園"),
    (2, "主題餐廳時間"): nav_dict.get("廣場閣樓餐廳"),
    (2, "城堡點燈拍照"): nav_dict.get("東京迪士尼樂園"),
    (2, "電子大遊行"): nav_dict.get("東京迪士尼樂園"),
    (2, "城堡高空投影秀"): nav_dict.get("東京迪士尼樂園"),
    (2, "世界市集"): nav_dict.get("東京迪士尼樂園"),
    (2, "親子組回程交通"): nav_dict.get("東京迪士尼樂園"),

    # Day 3
    (3, "搭乘 JR 前往東京車站"): nav_dict.get("淺草橋站"),
    (3, "東京車站丸之內站舍"): nav_dict.get("東京車站丸之內站舍 (東京駅丸の内駅舎)"),
    (3, "返回東京車站一番街入口"): nav_dict.get("東京車站一番街 (東京駅一番街)"),
    (3, "東京車站一番街"): nav_dict.get("東京車站一番街 (東京駅一番街)"),
    (3, "KITTE花園"): nav_dict.get("KITTE花園 (ＫＩＴＴＥガーデン)"),
    (3, "午餐"): nav_dict.get("天丼てんや (天丼てんや 八重洲店)"),
    (3, "前往上野"): nav_dict.get("東京站"),
    (3, "國立科學博物館"): nav_dict.get("國立科學博物館 (国立科学博物館)"),
    (3, "鴨 to 蔥拉麵"): nav_dict.get("鴨 to 蔥拉麵 (らーめん 鴨to葱 御徒町本店)"),
    (3, "阿美橫丁採買"): nav_dict.get("二木菓子 (二木の菓子 第一営業所)"), # <<--- First shopping destination is 二木菓子!
    (3, "前往JR 御徒町站"): nav_dict.get("御徒町站"),
    (3, "宵夜／點心"): nav_dict.get("海茵娜酒店"),

    # Day 4
    (4, "前往三鷹"): nav_dict.get("淺草橋站"),
    (4, "吉卜力接駁巴士"): nav_dict.get("三鷹站"),
    (4, "三鷹之森吉卜力美術館"): nav_dict.get("三鷹之森吉卜力美術館 (三鷹の森ジブリ美術館)"),
    (4, "前往吉祥寺"): nav_dict.get("井之頭恩賜公園"),
    (4, "午餐：大戶屋"): nav_dict.get("大戶屋 (大戶屋ごはん処 吉祥寺店)"),
    (4, "吉祥寺商圈慢活"): nav_dict.get("吉祥寺 Sunroad 商店街"),
    (4, "晚餐：串家物語"): nav_dict.get("串家物語 (神楽食堂 串家物語 吉祥寺店)"),
    (4, "返回淺草橋"): nav_dict.get("吉祥寺站"),
    (4, "回飯店休息"): nav_dict.get("海茵娜酒店"),

    # Day 5
    (5, "前往淺草"): nav_dict.get("淺草橋站"),
    (5, "淺草寺"): nav_dict.get("雷門 (雷門)"), # <<--- First destination in Asakusa is 雷門!
    (5, "淺草文化觀光中心"): nav_dict.get("淺草文化觀光中心 (浅草文化観光センター)"),
    (5, "前往東京晴空塔"): nav_dict.get("淺草站"),
    (5, "午餐：東京晴空街道"): nav_dict.get("達摩文字燒 (月島名物もんじゃ だるま 東京スカイツリータウン・ソラマチ店)"),
    (5, "墨田水族館"): nav_dict.get("墨田水族館 (すみだ水族館)"),
    (5, "東京晴空街道"): nav_dict.get("東京晴空街道 (東京ソラマチ)"),
    (5, "前往新宿西口"): nav_dict.get("東京晴空塔站"),
    (5, "晚餐：新宿西口平價美食"): nav_dict.get("麥當勞 (マクドナルド 新宿西口店)"),
    (5, "東京都廳第一本廳舍"): nav_dict.get("東京都廳第一本廳舍 (東京都庁舎)"),
    (5, "晚餐：東京晴空街道 3F 美食街"): nav_dict.get("宮武讚岐烏龍麵 (宮武讃岐うどん 東京ソラマチ店)"),

    # Day 6
    (6, "早餐與整理行李"): nav_dict.get("海茵娜酒店"),
    (6, "退房"): nav_dict.get("海茵娜酒店"),
    (6, "前往築地場外市場"): nav_dict.get("淺草橋站"),
    (6, "築地場外市場（早餐）"): nav_dict.get("築地山長 (つきぢ山長)"), # <<--- First food destination is 築地山長!
    (6, "前往東銀座站回飯店"): nav_dict.get("東銀座站"),
    (6, "領行李與車站移動"): nav_dict.get("海茵娜酒店"),
    (6, "前往羽田機場"): nav_dict.get("淺草橋站"),
    (6, "辦理登機與安檢"): nav_dict.get("羽田機場第3航廈"),
    (6, "輕食午餐與免稅店最後採買"): nav_dict.get("羽田機場第3航廈"),
    (6, "搭機返台"): nav_dict.get("羽田機場第3航廈")
}

# In-text Entities to auto-link
TEXT_ENTITIES = [
    ("不忍池 (不忍池 弁天堂)", nav_dict.get("不忍池")),
    ("不忍池", nav_dict.get("不忍池")),
    ("清水觀音堂 (清水観音堂)", nav_dict.get("清水觀音堂")),
    ("清水觀音堂", nav_dict.get("清水觀音堂")),
    ("兔屋 (うさぎや)", nav_dict.get("兔屋 (うさぎや)")),
    ("兔屋", nav_dict.get("兔屋 (うさぎや)")),
    ("松坂屋上野店", nav_dict.get("松坂屋上野店")),
    ("PARCO_ya", nav_dict.get("PARCO_ya")),
    ("國立西洋美術館", nav_dict.get("國立西洋美術館")),
    ("上野恩賜公園 噴水広場", nav_dict.get("上野公園噴水廣場")),
    ("上野公園中央噴水廣場", nav_dict.get("上野公園噴水廣場")),
    ("噴水廣場", nav_dict.get("上野公園噴水廣場")),
    ("舊岩崎邸庭園", nav_dict.get("舊岩崎邸庭園")),
    ("上野東照宮", nav_dict.get("上野東照宮")),
    ("二木菓子（二木の菓子 第一営業所）", nav_dict.get("二木菓子 (二木の菓子 第一営業所)")),
    ("二木菓子", nav_dict.get("二木菓子 (二木の菓子 第一営業所)")),
    ("OS Drug 上野店", nav_dict.get("OS Drug 上野店")),
    ("OS Drug", nav_dict.get("OS Drug 上野店")),
    ("肉之大山 (肉の大山 上野店)", nav_dict.get("肉之大山 (肉の大山 上野店)")),
    ("肉之大山", nav_dict.get("肉之大山 (肉の大山 上野店)")),
    ("みなとや食品 (みなとや食品 本店)", nav_dict.get("みなとや食品")),
    ("みなとや食品", nav_dict.get("みなとや食品")),
    ("多慶屋 (多慶屋 TAKEYA1)", nav_dict.get("多慶屋 (多慶屋 TAKEYA 1)")),
    ("多慶屋 (多慶屋 TAKEYA 1)", nav_dict.get("多慶屋 (多慶屋 TAKEYA 1)")),
    ("多慶屋（TAKEYA）", nav_dict.get("多慶屋 (多慶屋 TAKEYA 1)")),
    ("多慶屋", nav_dict.get("多慶屋 (多慶屋 TAKEYA 1)")),
    ("雷門 (雷門)", nav_dict.get("雷門 (雷門)")),
    ("雷門", nav_dict.get("雷門 (雷門)")),
    ("仲見世商店街 (仲見世商店街)", nav_dict.get("仲見世商店街 (仲見世商店街)")),
    ("仲見世商店街", nav_dict.get("仲見世商店街 (仲見世商店街)")),
    ("淺草寺 (浅草寺)", nav_dict.get("淺草寺 (浅草寺)")),
    ("淺草寺", nav_dict.get("淺草寺 (浅草寺)")),
    ("淺草文化觀光中心 (浅草文化観光センター)", nav_dict.get("淺草文化觀光中心 (浅草文化観光センター)")),
    ("淺草文化觀光中心", nav_dict.get("淺草文化觀光中心 (浅草文化観光センター)")),
    ("東京晴空塔 (東京スカイツリー)", nav_dict.get("東京晴空塔 (東京スカイツリー)")),
    ("東京晴空塔", nav_dict.get("東京晴空塔 (東京スカイツリー)")),
    ("晴空塔", nav_dict.get("東京晴空塔 (東京スカイツリー)")),
    ("墨田水族館 (すみだ水族館)", nav_dict.get("墨田水族館 (すみだ水族館)")),
    ("墨田水族館", nav_dict.get("墨田水族館 (すみだ水族館)")),
    ("東京晴空街道 (東京ソラマチ)", nav_dict.get("東京晴空街道 (東京ソラマチ)")),
    ("東京晴空街道", nav_dict.get("東京晴空街道 (東京ソラマチ)")),
    ("晴空街道", nav_dict.get("東京晴空街道 (東京ソラマチ)")),
    ("東京都廳 (東京都庁)", nav_dict.get("東京都廳第一本廳舍 (東京都庁舎)")),
    ("東京都廳", nav_dict.get("東京都廳第一本廳舍 (東京都庁舎)")),
    ("東京都庁", nav_dict.get("東京都廳第一本廳舍 (東京都庁舎)")),
    ("東京車站丸之內站舍 (東京駅丸の内駅舎)", nav_dict.get("東京車站丸之內站舍 (東京駅丸の内駅舎)")),
    ("東京車站丸之內站舍", nav_dict.get("東京車站丸之內站舍 (東京駅丸の内駅舎)")),
    ("東京車站一番街 (東京駅一番街)", nav_dict.get("東京車站一番街 (東京駅一番街)")),
    ("東京車站一番街", nav_dict.get("東京車站一番街 (東京駅一番街)")),
    ("一番街", nav_dict.get("東京車站一番街 (東京駅一番街)")),
    ("KITTE花園 (ＫＩＴＴＥガーデン)", nav_dict.get("KITTE花園 (ＫＩＴＴＥガーデン)")),
    ("KITTE花園", nav_dict.get("KITTE花園 (ＫＩＴＴＥガーデン)")),
    ("KITTE丸の内", nav_dict.get("KITTE花園 (ＫＩＴＴＥガーデン)")),
    ("三鷹之森吉卜力美術館 (三鷹の森ジブリ美術館)", nav_dict.get("三鷹之森吉卜力美術館 (三鷹の森ジブリ美術館)")),
    ("三鷹之森吉卜力美術館", nav_dict.get("三鷹之森吉卜力美術館 (三鷹の森ジブリ美術館)")),
    ("井之頭恩賜公園", nav_dict.get("井之頭恩賜公園")),
    ("吉祥寺 Sunroad 商店街", nav_dict.get("吉祥寺 Sunroad 商店街")),
    ("Sunroad 商店街", nav_dict.get("吉祥寺 Sunroad 商店街")),
    ("吉祥寺ロフト", nav_dict.get("Loft (吉祥寺ロフト)")),
    ("Loft 文具旗艦店", nav_dict.get("Loft (吉祥寺ロフト)")),
    ("無印良品 コピス吉祥寺", nav_dict.get("無印良品 (無印良品 コピス吉祥寺)")),
    ("無印良品", nav_dict.get("無印良品 (無印良品 コピス吉祥寺)")),
    ("大創", nav_dict.get("大創 (DAISO 吉祥寺サンロード店)")),
    ("哈莫尼卡橫丁 (ハーモニカ横丁)", nav_dict.get("哈莫尼卡橫丁 (ハーモニカ横丁)")),
    ("哈莫尼卡橫丁", nav_dict.get("哈莫尼卡橫丁 (ハーモニカ横丁)")),
    ("SATOU (黒毛和牛専門店 さとう 吉祥寺店)", nav_dict.get("SATOU (黒毛和牛専門店 さとう 吉祥寺店)")),
    ("SATOU 黑毛和牛炸牛肉丸", nav_dict.get("SATOU (黒毛和牛専門店 さとう 吉祥寺店)")),
    ("SATOU", nav_dict.get("SATOU (黒毛和牛専門店 さとう 吉祥寺店)")),
    ("Linde 德國麵包", nav_dict.get("Linde 德國麵包 (ベッカライカフェ・リンデ 吉祥寺本店)")),
    ("Jyonetsu Bakery", nav_dict.get("Jyonetsu Bakery")),
    ("築地場外市場 (築地場外市場)", nav_dict.get("築地場外市場 (築地場外市場)")),
    ("築地場外市場", nav_dict.get("築地場外市場 (築地場外市場)")),
    ("築地山長 (つきぢ山長)", nav_dict.get("築地山長 (つきぢ山長)")),
    ("「築地山長」現做玉子燒", nav_dict.get("築地山長 (つきぢ山長)")),
    ("築地山長", nav_dict.get("築地山長 (つきぢ山長)")),
    ("波除稻荷神社", nav_dict.get("波除稻荷神社")),
    ("肉之Hanamasa超市 (肉のハナマサ 浅草橋店)", nav_dict.get("肉之Hanamasa超市")),
    ("肉之Hanamasa超市", nav_dict.get("肉之Hanamasa超市")),
    ("海茵娜酒店东京浅草桥", nav_dict.get("海茵娜酒店")),
    ("海茵娜酒店", nav_dict.get("海茵娜酒店"))
]

# Write out mapping to json for build_pwa.py
with open('/home/owen/tokyo/first_destinations.json', 'w', encoding='utf-8') as f:
    json.dump({f"{d}_{k}": v for (d, k), v in FIRST_DESTINATIONS.items() if v}, f, ensure_ascii=False, indent=2)

with open('/home/owen/tokyo/text_entities.json', 'w', encoding='utf-8') as f:
    json.dump(TEXT_ENTITIES, f, ensure_ascii=False, indent=2)

print("Saved first_destinations.json and text_entities.json!")
