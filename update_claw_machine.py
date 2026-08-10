with open('/home/owen/tokyo/README.md', 'r', encoding='utf-8') as f:
    text = f.read()

target = """#### **16:30－16:50 🎮 秋葉原大型電玩體驗**

> * 目標地點：[**GiGO 秋葉原3號館 (GiGO 秋葉原3号館)**](https://www.google.com/maps/search/?api=1&query=35.6992456,139.7709552&query_place_id=ChIJR-PMBx2MGGARPFrgtULaJB0)
> * 體驗日本大型電玩中心、日式夾娃娃機（UFO Catcher）、全家感受秋葉原熱鬧的次文化遊樂氛圍。  
> * 💡 **消費預估**：夾娃娃機體驗約 ¥500～¥1,000 / 全家，小試身手即可。"""

replacement = """#### **16:30－16:50 🕹️ 日式夾娃娃機體驗**

> * 目標地點：[**GiGO 秋葉原3號館 (GiGO 秋葉原3号館)**](https://www.google.com/maps/search/?api=1&query=35.6992456,139.7709552&query_place_id=ChIJR-PMBx2MGGARPFrgtULaJB0) (1F/2F 夾娃娃機專區)  
> * **核心體驗（1F/2F）**：專注體驗日式夾娃娃機（UFO Catcher），全家感受秋葉原熱鬧的動漫周邊、人氣公仔與玩偶夾娃娃樂趣。  
> * 💡 **消費預估**：夾娃娃機體驗約 ¥500～¥1,000 / 全家，小試身手體驗日式機台手感即可。  
> * （Option：若想參觀其他樓層大型電玩，3F 為音樂節奏遊戲、7F 為懷舊復古遊戲專區 RETRO:G，可視時間與興趣順路搭手扶梯快閃參觀）。"""

text = text.replace(target, replacement)

with open('/home/owen/tokyo/README.md', 'w', encoding='utf-8') as f:
    f.write(text)

print("Updated README.md claw machine section!")
