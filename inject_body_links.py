import json, re

with open('/home/owen/tokyo/navigation_links_dict.json', 'r', encoding='utf-8') as f:
    nav_dict = json.load(f)

for fpath in ['/home/owen/tokyo/2026東京親子自由行_V10_Henna.md', '/home/owen/tokyo/README.md']:
    with open(fpath, 'r', encoding='utf-8') as f:
        text = f.read()

    # 1. Day 1 GiGO 3
    text = text.replace(
        "#### **16:30－16:50 🎮 秋葉原大型電玩體驗**\n\n> * 體驗日本大型電玩中心",
        f"#### **16:30－16:50 🎮 秋葉原大型電玩體驗**\n\n> * 目標地點：[**GiGO 秋葉原3號館 (GiGO 秋葉原3号館)**]({nav_dict['GiGO 秋葉原3號館']})\n> * 體驗日本大型電玩中心"
    )

    # 2. Day 1 Purikura
    text = text.replace(
        "#### **16:50－17:10 📸 日系拍貼機全家合影體驗**\n\n> * **全家合影紀念**：走進日本最新",
        f"#### **16:50－17:10 �� 日系拍貼機全家合影體驗**\n\n> * 目標地點：[**日系拍貼機體驗 (Purikura / GiGO 拍貼機專區)**]({nav_dict['日系拍貼機體驗 (Purikura / GiGO 拍貼機專區)']})\n> * **全家合影紀念**：走進日本最新"
    )

    # 3. Day 1 Gashapon
    text = text.replace(
        "#### **17:10－17:30 🪙 萬代官方扭蛋體驗**\n\n> * 前往全秋葉原規模最大",
        f"#### **17:10－17:30 🪙 萬代官方扭蛋體驗**\n\n> * 目標地點：[**萬代扭蛋百貨店 秋葉原店 (ガシャポンのデパート 秋葉原店)**]({nav_dict['萬代扭蛋百貨店 秋葉原店']}) (いちご秋葉原駅前ビル 4F / namco 4F)\n> * 前往全秋葉原規模最大"
    )

    # 4. Day 1 Shinjuku 3D Cat
    text = text.replace(
        "#### **17:15－17:40 🐈 欣賞新宿 3D 巨貓**\n\n> * **亮點特色**：從新宿東口一出站",
        f"#### **17:15－17:40 🐈 欣賞新宿 3D 巨貓**\n\n> * 目標地點：[**Cross Shinjuku 3D 巨貓 (クロス新宿ビジョン)**]({nav_dict['Cross Shinjuku 3D 巨貓 (クロス新宿ビジョン)']})\n> * **亮點特色**：從新宿東口一出站"
    )

    # 5. Day 3 Tokyo Station Marunouchi
    text = text.replace(
        "### **09:25－09:45 📸 欣賞東京車站丸之內站舍建築**\n\n拍全家福、欣賞東京車站經典紅磚建築",
        f"### **09:25－09:45 📸 欣賞東京車站丸之內站舍建築**\n\n> * 目標地點：[**東京車站丸之內站舍 (東京駅丸の内駅舎)**]({nav_dict['東京車站丸之內站舍 (東京駅丸の内駅舎)']})\n> * 拍全家福、欣賞東京車站經典紅磚建築"
    )

    # 6. Day 3 Tokyo Character Street
    text = text.replace(
        "### **10:00－11:05 🛍️ 逛東京車站一番街動漫街**\n\n10:00 店家開始營業",
        f"### **10:00－11:05 🛍️ 逛東京車站一番街動漫街**\n\n> * 目標地點：[**東京車站一番街 (東京駅一番街)**]({nav_dict['東京車站一番街 (東京駅一番街)']}) (八重洲地下中央口 B1F)\n> * 10:00 店家開始營業"
    )

    # 7. Day 3 KITTE Garden
    text = text.replace(
        "### **11:05－11:25 🌇 KITTE頂樓花園眺望東京車站**\n\n11:00 頂樓花園剛開門",
        f"### **11:05－11:25 🌇 KITTE頂樓花園眺望東京車站**\n\n> * 目標地點：[**KITTE花園 (ＫＩＴＴＥガーデン)**]({nav_dict['KITTE花園 (ＫＩＴＴＥガーデン)']}) (KITTE 6F)\n> * 11:00 頂樓花園剛開門"
    )

    # 8. Day 3 Science Museum
    text = text.replace(
        "### **13:25－15:25 🦕 參觀國立科學博物館**\n\n",
        f"### **13:25－15:25 🦕 參觀國立科學博物館**\n\n> * 目標地點：[**國立科學博物館 (国立科学博物館)**]({nav_dict['國立科學博物館 (国立科学博物館)']})\n"
    )

    # 9. Day 4 Ghibli Museum
    text = text.replace(
        "### **09:50－12:15 🌳 參觀三鷹之森吉卜力美術館**\n\n",
        f"### **09:50－12:15 🌳 參觀三鷹之森吉卜力美術館**\n\n> * 目標地點：[**三鷹之森吉卜力美術館 (三鷹の森ジブリ美術館)**]({nav_dict['三鷹之森吉卜力美術館 (三鷹の森ジブリ美術館)']})\n"
    )

    # 10. Day 5 Sensoji
    text = text.replace(
        "### **08:45－10:15 ⛩️ 參觀淺草寺與雷門散策**\n\n",
        f"### **08:45－10:15 ⛩️ 參觀淺草寺與雷門散策**\n\n> * 目標地點：[**雷門 (雷門)**]({nav_dict['雷門 (雷門)']}) ➔ [**仲見世商店街 (仲見世商店街)**]({nav_dict['仲見世商店街 (仲見世商店街)']}) ➔ [**淺草寺 (浅草寺)**]({nav_dict['淺草寺 (浅草寺)']})\n"
    )

    # 11. Day 5 Asakusa Culture Tourist Info Center
    text = text.replace(
        "### **10:15－10:35 🌇 淺草文化觀光中心眺望晴空塔**\n\n",
        f"### **10:15－10:35 🌇 淺草文化觀光中心眺望晴空塔**\n\n> * 目標地點：[**淺草文化觀光中心 (浅草文化観光センター)**]({nav_dict['淺草文化觀光中心 (浅草文化観光センター)']}) (8F 展望台)\n"
    )

    # 12. Day 5 Sumida Aquarium
    text = text.replace(
        "### **12:30－14:45 🐧 參觀墨田水族館**\n\n",
        f"### **12:30－14:45 🐧 參觀墨田水族館**\n\n> * 目標地點：[**墨田水族館 (すみだ水族館)**]({nav_dict['墨田水族館 (すみだ水族館)']}) (東京晴空塔城 5F/6F)\n"
    )

    # 13. Day 5 Solamachi Shopping
    text = text.replace(
        "### **14:45－15:30 🛍️ 晴空街道散策與高空景觀**\n\n",
        f"### **14:45－15:30 🛍️ 晴空街道散策與高空景觀**\n\n> * 目標地點：[**東京晴空街道 (東京ソラマチ)**]({nav_dict['東京晴空街道 (東京ソラマチ)']}) (東館 30F/31F 高空景觀)\n"
    )

    # 14. Day 5 Tokyo Metropolitan Government
    text = text.replace(
        "#### **18:00－19:15 🌇 登上東京都廳俯瞰百萬夜景**\n\n",
        f"#### **18:00－19:15 🌇 登上東京都廳俯瞰百萬夜景**\n\n> * 目標地點：[**東京都廳 (東京都庁)**]({nav_dict['東京都廳第一本廳舍 (東京都庁舎)']}) (第一本廳舍 45F 南展望室)\n"
    )

    with open(fpath, 'w', encoding='utf-8') as f:
        f.write(text)

print("Injected all explicit destination navigation links into markdown bodies!")
