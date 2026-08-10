import re

with open('/home/owen/tokyo/README.md', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Day 1: Airport to Asakusabashi
content = content.replace(
    '搭乘「京急機場線 (直通都營淺草線往成田空港/青砥方向)」直達',
    '搭乘「京急機場線 (直通都營淺草線，紅色/玫瑰紅色列車，往成田空港/青砥方向)」直達'
)

# 2. Day 2 Seniors: Return from Okachimachi
content = content.replace(
    '搭乘 JR 山手線 1 站至秋葉原 ➔ 轉乘 JR 中央・總武線 1 站返回 淺草橋站',
    '搭乘 JR 山手線 (綠色列車) 1 站至秋葉原 ➔ 轉乘 JR 中央・總武線 (黃色列車) 1 站返回 淺草橋站'
)

# 3. Day 2 Kids: Plan B return train colors
content = content.replace(
    '由舞濱站搭乘 [**JR 京葉線 (JR京葉線)**](https://www.google.com/maps/search/?api=1&query=35.635834,139.883584&query_place_id=ChIJo3N_X5yOGGARyv4l77z-WHQ) 前往「2 號月台（往東京方向）」上車 ➔ 抵達 [**八丁堀站 (八丁堀駅)**](https://www.google.com/maps/search/?api=1&query=35.674998,139.777402&query_place_id=ChIJe0e8kkfuGGARvH2cE14g_0J)（車程約 12 分鐘）。',
    '由舞濱站搭乘 [**JR 京葉線 (JR京葉線)**](https://www.google.com/maps/search/?api=1&query=35.635834,139.883584&query_place_id=ChIJo3N_X5yOGGARyv4l77z-WHQ) (紅色列車) 前往「2 號月台（往東京方向）」上車 ➔ 抵達 [**八丁堀站 (八丁堀駅)**](https://www.google.com/maps/search/?api=1&query=35.674998,139.777402&query_place_id=ChIJe0e8kkfuGGARvH2cE14g_0J)（車程約 12 分鐘）。'
)
content = content.replace(
    '八丁堀站轉乘 [**東京地鐵日比谷線 (東京メトロ日比谷線)**](https://www.google.com/maps/search/?api=1&query=35.674998,139.777402&query_place_id=ChIJe0e8kkfuGGARvH2cE14g_0J) ➔ 前往「2 號月台（往北千住方向）」上車 ➔ 抵達 [**秋葉原站 (秋葉原駅)**](https://www.google.com/maps/search/?api=1&query=35.698383,139.7731315&query_place_id=ChIJ8Y-8_JuOGGAR5e4o-gq0F88)（車程約 8 分鐘）。',
    '八丁堀站轉乘 [**東京地鐵日比谷線 (東京メトロ日比谷線)**](https://www.google.com/maps/search/?api=1&query=35.674998,139.777402&query_place_id=ChIJe0e8kkfuGGARvH2cE14g_0J) (銀灰色列車) ➔ 前往「2 號月台（往北千住方向）」上車 ➔ 抵達 [**秋葉原站 (秋葉原駅)**](https://www.google.com/maps/search/?api=1&query=35.698383,139.7731315&query_place_id=ChIJ8Y-8_JuOGGAR5e4o-gq0F88)（車程約 8 分鐘）。'
)
content = content.replace(
    '抵達秋葉原站後，於同站轉乘 JR 中央・總武線 1 站返抵淺草橋站飯店休息。',
    '抵達秋葉原站後，於同站轉乘 JR 中央・總武線 (黃色列車) 1 站返抵淺草橋站飯店休息。'
)

# 4. Day 3: Tokyo Station to Ueno
content = content.replace(
    '前往 **4 號月台（JR 山手線・上野／池袋方向）**，搭車直達',
    '前往 **4 號月台搭乘 JR 山手線 (綠色列車，往上野／池袋方向)**，搭車直達'
)

# Day 3: Return from Okachimachi
content = content.replace(
    'JR 御徒町站 (JR 御徒町駅)（站內設有手扶梯） ➔ JR 山手線 ➔ JR 秋葉原站 (JR 秋葉原駅) ➔ 轉乘 JR 中央・總武線 1 站至 淺草橋站 (浅草橋駅)。',
    'JR 御徒町站 (JR 御徒町駅)（站內設有手扶梯） ➔ 搭乘 JR 山手線 (綠色列車) ➔ JR 秋葉原站 (JR 秋葉原駅) ➔ 同站轉乘 JR 中央・總武線 (黃色列車) 1 站至 淺草橋站 (浅草橋駅)。'
)

# 5. Day 4: Ghibli to Kichijoji Plan A
content = content.replace(
    '於「新宿／東京」方向月台搭乘黃色中央・總武線或橘色中央線快速，僅搭 1 站（車程約 2 分鐘）即達',
    '於「新宿／東京」方向月台搭乘 JR 中央・總武線 (黃色列車) 或 JR 中央線快速 (橘色列車)，僅搭 1 站（車程約 2 分鐘）即達'
)

# 6. Day 5: Asakusabashi to Asakusa
content = content.replace(
    '交通：都營淺草線  \n> * 步行至 都營淺草線 淺草橋站（走 A1/A3 進站） ➔ 搭乘往淺草方向列車 ➔ 淺草站 (浅草駅) (僅 2 站，免轉車約 3 分鐘)。',
    '交通：都營淺草線 (玫瑰紅色列車)  \n> * 步行至 都營淺草線 淺草橋站（走 A1/A3 進站） ➔ 搭乘 都營淺草線 (玫瑰紅色列車，往淺草/押上方向) ➔ 淺草站 (浅草駅) (僅 2 站，免轉車約 3 分鐘)。'
)

# Day 5: Oshiage to Shinjuku
content = content.replace(
    '從 押上站 搭乘 都營淺草線 至 淺草橋站（約 6 分鐘），同站轉乘 JR 中央・總武線 (黃色列車) 至 御茶之水站',
    '從 押上站 搭乘 都營淺草線 (玫瑰紅色列車) 至 淺草橋站（約 6 分鐘），同站轉乘 JR 中央・總武線 (黃色列車) 至 御茶之水站'
)

# Day 5: Shinjuku to Asakusabashi
content = content.replace(
    '於都廳前站 (都庁前駅) 搭乘 都營大江戶線 直達 藏前站 (蔵前駅)（車程約 25 分鐘，出站後散步約 8 分鐘返回飯店）；或至「新宿西口站」搭乘都營大江戶線。',
    '於都廳前站 (都庁前駅) 搭乘 都營大江戶線 (紫紅色列車，往六本木/大門方向) 直達 藏前站 (蔵前駅)（車程約 25 分鐘，出站後散步約 8 分鐘返回飯店）；或至 JR 新宿站搭乘 JR 中央・總武線 (黃色列車) 直達淺草橋站。'
)

# 7. Day 6: Asakusabashi to Tsukiji
content = content.replace(
    '步行 2 分鐘至 都營淺草線 淺草橋站 (A1 電梯口) ➔ 搭乘 都營淺草線（往西馬込/羽田機場方向，僅 4 站，車程約 7 分鐘）直達 東銀座站 (東銀座駅)',
    '步行 2 分鐘至 都營淺草線 淺草橋站 (A1 電梯口) ➔ 搭乘 都營淺草線 (玫瑰紅色列車，往西馬込/羽田機場方向，僅 4 站，車程約 7 分鐘）直達 東銀座站 (東銀座駅)'
)

# Day 6: Tsukiji back to Hotel
content = content.replace(
    '由 東銀座站 (東銀座駅) 搭乘 都營淺草線 4 站直達 淺草橋站 (浅草橋駅) (車程約 7 分鐘)。走 A1 出口無障礙電梯回飯店領取行李。',
    '由 東銀座站 (東銀座駅) 搭乘 都營淺草線 (玫瑰紅色列車，往淺草/押上方向) 4 站直達 淺草橋站 (浅草橋駅) (車程約 7 分鐘)。走 A1 出口無障礙電梯回飯店領取行李。'
)

# Day 6: Hotel to Haneda Airport
content = content.replace(
    '從 都營淺草線 淺草橋站（走 A1 出口無障礙電梯）進站，搭乘 都營淺草線直通京急機場線 的「機場特快 (エアポート快特) / 快特」列車直達 羽田機場第3航廈站(羽田空港第3ターミナル駅)',
    '從 都營淺草線 淺草橋站（走 A1 出口無障礙電梯）進站，搭乘 都營淺草線直通京急機場線 (紅色/玫瑰紅色列車) 的「機場特快 (エアポート快特) / 快特」列車直達 羽田機場第3航廈站(羽田空港第3ターミナル駅)'
)

# Write to both files
for fname in ['README.md', '2026東京親子自由行_V10_Henna.md']:
    fpath = f'/home/owen/tokyo/{fname}'
    with open(fpath, 'w', encoding='utf-8') as f:
        f.write(content)

print("Standardized all rail, subway, and train line names and vehicle colors across Day 1 to Day 6!")
