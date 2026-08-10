import re

with open('/home/owen/tokyo/README.md', 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Add Top Sticky / Capsule Nav
top_nav = """
<div class="nav-capsules">
  <a href="#-航班與住宿資訊" class="nav-btn">✈️ 航班/住宿</a>
  <a href="#-重要交通與避坑提醒" class="nav-btn">💡 交通提醒</a>
  <a href="#-全程景點概覽" class="nav-btn">📊 行程總覽</a>
  <a href="#-day-1820-星期四啟程抵達--秋葉原--宿淺草橋" class="nav-btn">Day 1 秋葉原</a>
  <a href="#-day-2821-星期五-長輩組上野藝術與晨間散策輕旅行" class="nav-btn">Day 2 長輩上野</a>
  <a href="#-day-2821-星期五-親子組東京迪士尼樂園全日夢幻體驗" class="nav-btn">Day 2 親子迪士尼</a>
  <a href="#-day-3822-星期六東京車站經典--科博館--阿美橫丁" class="nav-btn">Day 3 車站/科博館</a>
  <a href="#-day-4823-星期日吉卜力童話--吉祥寺風格散步與-diy-炸串" class="nav-btn">Day 4 吉卜力/吉祥寺</a>
  <a href="#-day-5824-星期一下町風情--晴空塔水族館--新宿都廳百萬夜景" class="nav-btn">Day 5 淺草/晴空塔/都廳</a>
  <a href="#-day-6825-星期二築地晨間美食巡禮--回程前往機場" class="nav-btn">Day 6 築地/返台</a>
</div>

**📱 快速跳轉：** [✈️ 航班/住宿](#-航班與住宿資訊) | [💡 交通提醒](#-重要交通與避坑提醒) | [📊 行程總覽](#-全程景點概覽) | [Day 1](#-day-1820-星期四啟程抵達--秋葉原--宿淺草橋) | [Day 2 長輩](#-day-2821-星期五-長輩組上野藝術與晨間散策輕旅行) | [Day 2 親子](#-day-2821-星期五-親子組東京迪士尼樂園全日夢幻體驗) | [Day 3](#-day-3822-星期六東京車站經典--科博館--阿美橫丁) | [Day 4](#-day-4823-星期日吉卜力童話--吉祥寺風格散步與-diy-炸串) | [Day 5](#-day-5824-星期一下町風情--晴空塔水族館--新宿都廳百萬夜景) | [Day 6](#-day-6825-星期二築地晨間美食巡禮--回程前往機場)

---
"""

if '<div class="nav-capsules">' not in text:
    text = re.sub(r'(# 2026東京親子自由行.*?\n)', r'\1' + top_nav, text, count=1)

# Add [⬆️ 回頂部] to each Day header if not present
days_patterns = [
    r'(## \*\*📅 Day 1.*?\*\*)',
    r'(## \*\*📅 Day 2（8/21 星期五 - 長輩組）.*?\*\*)',
    r'(## \*\*📅 Day 2（8/21 星期五 - 親子組）.*?\*\*)',
    r'(## \*\*📅 Day 3.*?\*\*)',
    r'(## \*\*📅 Day 4.*?\*\*)',
    r'(## \*\*📅 Day 5.*?\*\*)',
    r'(## \*\*📅 Day 6.*?\*\*)'
]

# Day 1: 壽司郎用餐技巧折疊
sushiro_old = """>   * 💡 **用餐技巧**：
>     1. 現場入座後，平板可切換「繁體中文」介面。
>     2. 每人每次平板點餐上限為 4 盤，送達後可繼續加點。
>     3. 推薦必點：炙燒起司鮭魚、黑鮪魚中腹、茶碗蒸（小朋友最愛）、炸薯條。"""

sushiro_new = """<details>
<summary>💡 壽司郎點餐與用餐技巧（點擊展開）</summary>

>   * 平板點餐可切換「繁體中文」介面。  
>   * 每人每次平板點餐上限為 4 盤，送達後可繼續加點。  
>   * 推薦必點：炙燒起司鮭魚、黑鮪魚中腹、茶碗蒸（小朋友最愛）、炸薯條。  
</details>"""

text = text.replace(sushiro_old, sushiro_new)

# Day 1: 備案餐廳折疊
d1_backup_old = """> * 備案餐廳 1：[**丸龜製麵 (丸亀製麺 秋葉原店)**](https://www.google.com/maps/search/?api=1&query=35.6984426,139.7724317&query_place_id=ChIJFa5T2GqNGGARmSiHDgcJFf8) (アトレ秋葉原1 1F) 享用讚岐烏龍麵（推薦：豆皮烏龍麵、炸蝦天婦羅），人均約 ¥400～¥800。  
> * 備案餐廳 2：[**CoCo壹番屋 (CoCo壱番屋 JR秋葉原駅昭和通り口店)**](https://www.google.com/maps/search/?api=1&query=35.6984515,139.7749818&query_place_id=ChIJ8Y-8_JuOGGAR5e4o-gq0F89) (渡辺ビル 1F) 享用日式咖哩飯（推薦：炸豬排咖哩飯、兒童咖哩套餐），人均約 ¥800～¥1,200。"""

d1_backup_new = """<details>
<summary>🍽️ 查看晚餐備案餐廳（丸龜製麵 / CoCo壹番屋）（點擊展開）</summary>

> * 備案餐廳 1：[**丸龜製麵 (丸亀製麺 秋葉原店)**](https://www.google.com/maps/search/?api=1&query=35.6984426,139.7724317&query_place_id=ChIJFa5T2GqNGGARmSiHDgcJFf8) (アトレ秋葉原1 1F) 享用讚岐烏龍麵（推薦：豆皮烏龍麵、炸蝦天婦羅），人均約 ¥400～¥800。  
> * 備案餐廳 2：[**CoCo壹番屋 (CoCo壱番屋 JR秋葉原駅昭和通り口店)**](https://www.google.com/maps/search/?api=1&query=35.6984515,139.7749818&query_place_id=ChIJ8Y-8_JuOGGAR5e4o-gq0F89) (渡辺ビル 1F) 享用日式咖哩飯（推薦：炸豬排咖哩飯、兒童咖哩套餐），人均約 ¥800～¥1,200。  
</details>"""

text = text.replace(d1_backup_old, d1_backup_new)

# Day 2 長輩: 名代宇奈とと點餐技巧折疊
unato_old = """>   * 💡 **點餐與付款祕訣**：
>     1. 入座後翻開彩色大圖菜單，直接用手指照片上的「**うな丼 (平價鰻魚丼 ¥640)**」或「**うな重 (厚切大片鰻魚重 ¥1,100)**」即可完成點餐。
>     2. 店內支援 Suica / PASMO 感應付款及現金支付，結帳時出示手機 Suica 嗶一聲即可完成，長輩操作零障礙！"""

unato_new = """<details>
<summary>💡 名代宇奈とと點餐與付款技巧（點擊展開）</summary>

>   * 入座後翻開彩色大圖菜單，直接用手指照片上的「**うな丼 (平價鰻魚丼 ¥640)**」或「**うな重 (厚切大片鰻魚重 ¥1,100)**」即可完成點餐。  
>   * 店內支援 Suica / PASMO 感應付款及現金支付，結帳時出示手機 Suica 嗶一聲即可完成，長輩操作零障礙！  
</details>"""

text = text.replace(unato_old, unato_new)

# Day 2 長輩: 備案餐廳折疊
d2_elder_backup_old = """> * 備案餐廳：[**松坂屋地下美食街 (松坂屋上野店 ほっぺタウン)**](https://www.google.com/maps/search/?api=1&query=35.707472,139.773824&query_place_id=ChIJq0bKk5SOGGARe_3qM1Qh6g2) (本館 B1F) 挑選各式日式名店外帶便當（如：人形町今半黑毛和牛便當、鰻魚便當、天婦羅丼），人均約 ¥1,000～¥1,800。"""

d2_elder_backup_new = """<details>
<summary>🍱 查看午餐備案：松坂屋地下美食街便當（點擊展開）</summary>

> * 備案餐廳：[**松坂屋地下美食街 (松坂屋上野店 ほっぺタウン)**](https://www.google.com/maps/search/?api=1&query=35.707472,139.773824&query_place_id=ChIJq0bKk5SOGGARe_3qM1Qh6g2) (本館 B1F) 挑選各式日式名店外帶便當（如：人形町今半黑毛和牛便當、鰻魚便當、天婦羅丼），人均約 ¥1,000～¥1,800。  
</details>"""

text = text.replace(d2_elder_backup_old, d2_elder_backup_new)

# Day 2 親子: 迪士尼餐廳備案折疊
disney_lunch_backup_old = """> * 備案餐廳：使用官方 App 的 Mobile Order (行動點餐) 功能提前預約 [**廣場閣樓餐廳 (プラザパビリオン・レストラン)**](https://www.google.com/maps/search/?api=1&query=35.6328604,139.8789312&query_place_id=ChIJ8_W69A2OGGARi3i22fD64B3) 或 [**明日樂園舞台餐廳 (トゥモローランド・テラス)**](https://www.google.com/maps/search/?api=1&query=35.6320001,139.8820001&query_place_id=ChIJb-X7-daOGGAR3yH28t4D5lO)，時間到直接取餐免排隊。"""

disney_lunch_backup_new = """<details>
<summary>📱 迪士尼午餐備案：Mobile Order 快速取餐（點擊展開）</summary>

> * 備案餐廳：使用官方 App 的 Mobile Order (行動點餐) 功能提前預約 [**廣場閣樓餐廳 (プラザパビリオン・レストラン)**](https://www.google.com/maps/search/?api=1&query=35.6328604,139.8789312&query_place_id=ChIJ8_W69A2OGGARi3i22fD64B3) 或 [**明日樂園舞台餐廳 (トゥモローランド・テラス)**](https://www.google.com/maps/search/?api=1&query=35.6320001,139.8820001&query_place_id=ChIJb-X7-daOGGAR3yH28t4D5lO)，時間到直接取餐免排隊。  
</details>"""

text = text.replace(disney_lunch_backup_old, disney_lunch_backup_new)

disney_dinner_backup_old = """> * 備案餐廳（快速免久候）：若未預約且上述客滿，直接帶小朋友改往明日樂園區的 [**紅連火箭筒餐廳 (パン・ギャラクティック・ピザ・ポート)**](https://www.google.com/maps/search/?api=1&query=35.6330921,139.8810921&query_place_id=ChIJd-Z9-daOGGAR1wK46v6F7oQ) 購買披薩套餐與三眼怪麻糬（點餐動線極快、位子多）。"""

disney_dinner_backup_new = """<details>
<summary>🍕 迪士尼晚餐備案：紅連火箭筒餐廳（披薩/三眼怪麻糬）（點擊展開）</summary>

> * 備案餐廳（快速免久候）：若未預約且上述客滿，直接帶小朋友改往明日樂園區的 [**紅連火箭筒餐廳 (パン・ギャラクティック・ピザ・ポート)**](https://www.google.com/maps/search/?api=1&query=35.6330921,139.8810921&query_place_id=ChIJd-Z9-daOGGAR1wK46v6F7oQ) 購買披薩套餐與三眼怪麻糬（點餐動線極快、位子多）。  
</details>"""

text = text.replace(disney_dinner_backup_old, disney_dinner_backup_new)

# Day 3: 東京車站午餐備案折疊
tokyo_lunch_backup_old = """> * 備案餐廳 1：[**だし茶漬け えん (だし茶漬け＋肉うどん えん KITTE丸の内店)**](https://www.google.com/maps/search/?api=1&query=35.6792913,139.7653382&query_place_id=ChIJqVS6VgCLGGAR-5BoRnVee14) (KITTE丸の内 B1F) 享用和風高湯茶泡飯（推薦：真鯛高湯茶泡飯、炙燒鮭魚與鮭魚卵茶泡飯），人均約 ¥850～¥1,100。  
>   * 動線優勢：就在 11:25 剛參觀完的 KITTE 6F 頂樓花園正下方，搭電梯直達 B1F 即可入座，清爽消暑、長輩極愛。  
> * 備案餐廳 2：[**燕子烤肉漢堡排 (つばめグリル 大丸東京店)**](https://www.google.com/maps/search/?api=1&query=35.6812026,139.7678523&query_place_id=ChIJ60m9202LGGAR79K37s2o_a0) (大丸東京店 12F) 享用經典洋食（推薦：招牌漢堡排），人均約 ¥1,800～¥2,500。"""

tokyo_lunch_backup_new = """<details>
<summary>🍽️ 查看東京車站午餐備案（KITTE茶泡飯 / 燕子漢堡排）（點擊展開）</summary>

> * 備案餐廳 1：[**だし茶漬け えん (だし茶漬け＋肉うどん えん KITTE丸の内店)**](https://www.google.com/maps/search/?api=1&query=35.6792913,139.7653382&query_place_id=ChIJqVS6VgCLGGAR-5BoRnVee14) (KITTE丸の内 B1F) 享用和風高湯茶泡飯（推薦：真鯛高湯茶泡飯、炙燒鮭魚與鮭魚卵茶泡飯），人均約 ¥850～¥1,100。  
>   * 動線優勢：就在 11:25 剛參觀完的 KITTE 6F 頂樓花園正下方，搭電梯直達 B1F 即可入座，清爽消暑、長輩極愛。  
> * 備案餐廳 2：[**燕子烤肉漢堡排 (つばめグリル 大丸東京店)**](https://www.google.com/maps/search/?api=1&query=35.6812026,139.7678523&query_place_id=ChIJ60m9202LGGAR79K37s2o_a0) (大丸東京店 12F) 享用經典洋食（推薦：招牌漢堡排），人均約 ¥1,800～¥2,500。  
</details>"""

text = text.replace(tokyo_lunch_backup_old, tokyo_lunch_backup_new)

# Day 3: 科博館展區細節折疊
museum_details_old = """> * 建議路線：地球館 B1(恐龍化石) → 地球館 3F(動物標本) → 隼鳥(Hayabusa)返回艙 → THEATER 360°(依現場人潮決定) 日本館(自然史)  
>   * 恐龍化石展:位於地球館 B1,展示巨大恐龍骨骸與演化史,是小朋友的最愛。(建議停留 30~40 分鐘)  
>   * 動物區:位於地球館 3F,展示大型哺乳類、鳥類等逼真標本,能近距離觀察地球上的生物多樣性。(建議停留 20~30 分鐘)  
>   * 隼鳥(Hayabusa)返回艙:展示日本小行星探測器實際返回艙,是館內熱門展品之一。  
>   * THEATER 360°:約 6 分鐘的360度球幕劇場,免費參觀,採現場排隊,若排隊人潮不多值得體驗  
>   * 科學體驗設施:設有多項互動式科學儀器, 讓孩子在遊玩中學習基礎科學知識  
> * Option：若累了可於上野公園樹下稍作休息，並於上野站或公園周邊購買冰品、飲料；或欣賞國立西洋美術館 (国立西洋美術館) 外觀拍照即可，不需入館。"""

museum_details_new = """<details>
<summary>🦕 國立科學博物館推薦參觀路線與重點展區（點擊展開）</summary>

> * 建議路線：地球館 B1(恐龍化石) → 地球館 3F(動物標本) → 隼鳥(Hayabusa)返回艙 → THEATER 360°(依現場人潮決定) → 日本館(自然史)  
>   * **恐龍化石展**：位於地球館 B1，展示巨大恐龍骨骸與演化史，是小朋友的最愛。(建議停留 30~40 分鐘)  
>   * **動物區**：位於地球館 3F，展示大型哺乳類、鳥類等逼真標本，能近距離觀察地球上的生物多樣性。(建議停留 20~30 分鐘)  
>   * **隼鳥(Hayabusa)返回艙**：展示日本小行星探測器實際返回艙，是館內熱門展品之一。  
>   * **THEATER 360°**：約 6 分鐘的 360 度球幕劇場，免費參觀，採現場排隊，若人潮不多極值得體驗。  
>   * **科學體驗設施**：設有多項互動式科學儀器，讓孩子在遊玩中學習基礎科學知識。  
> * **Option**：若累了可於上野公園樹下稍作休息，並於周邊購買冰品飲料；或欣賞國立西洋美術館外觀拍照。  
</details>"""

text = text.replace(museum_details_old, museum_details_new)

# Day 3: 鴨 to 蔥點餐祕訣折疊
kamoto_tips_old = """* 💡 **點餐祕訣**：先於門口自動食券機買票 ➔ 入座後店員會拿出一塊「當月 3 種蔥」牌子問「3選2」，直接用手指號碼（例如：1 和 3）即可！
* ��‍♂️ **步行避暑提醒**：從科博館步行至鴨 to 蔥約 1.1 公里（家庭步速約 20 分鐘），建議穿過上野站走中央通騎樓或阿美橫丁商店街遮蔭處。
* 若順利吃到，可在返程回飯店前，在阿美橫丁購買小吃回飯店吃，以免晚上肚子餓。例如：🍗 炸雞、🍢 烤雞串、牛串、🥟 煎餃或燒賣、🍤 炸海鮮"""

kamoto_tips_new = """<details>
<summary>💡 鴨 to 蔥拉麵點餐秘訣與避暑步行提醒（點擊展開）</summary>

* **點餐祕訣**：先於門口自動食券機買票 ➔ 入座後店員會拿出一塊「當月 3 種蔥」牌子問「3選2」，直接用手指號碼（例如：1 和 3）即可！  
* **步行避暑提醒**：從科博館步行至鴨 to 蔥約 1.1 公里（家庭步速約 20 分鐘），建議穿過上野站走中央通騎樓或阿美橫丁商店街遮蔭處。  
* **回飯店小吃推薦**：阿美橫丁可外帶 🍗 炸雞、🍢 烤雞串、牛串、🥟 煎餃燒賣、🍤 炸海鮮回飯店享用。  
</details>"""

text = text.replace(kamoto_tips_old, kamoto_tips_new)

# Day 4: 吉祥寺午餐備案折疊
kichijoji_lunch_backup_old = """> * 備案餐廳 1：[**串家物語 (神楽食堂 串家物語 吉祥寺店)**](https://www.google.com/maps/search/?api=1&query=35.7048979,139.5802557&query_place_id=ChIJNbTiyUfuGGAR6lter_U3i7g) (コピス吉祥寺 A館 B1F) 享用 DIY 串炸吃到飽（推薦：牛肉串、蝦串、章魚燒串、巧克力噴泉），人均約 ¥1,900～¥2,500。  
>   * 動線優勢：位於商場地下街，吹冷氣且小孩能體驗自己沾粉油炸的樂趣。  
> * 備案餐廳 2：[**一風堂 (一風堂 吉祥寺店)**](https://www.google.com/maps/search/?api=1&query=35.7052815,139.5786162&query_place_id=ChIJZziKmUfuGGAR8iau_mxpQKw) (吉祥寺サンロード商店街) 享用博多豚骨拉麵（推薦：白丸元味、赤丸新味、一口煎餃），人均約 ¥900～¥1,300。  
>   * 動線優勢：位於有頂棚遮蔭的商店街內，出餐快速，有兒童餐具與座椅。"""

kichijoji_lunch_backup_new = """<details>
<summary>🍽️ 查看吉祥寺午餐備案（串家物語 DIY 串炸 / 一風堂拉麵）（點擊展開）</summary>

> * 備案餐廳 1：[**串家物語 (神楽食堂 串家物語 吉祥寺店)**](https://www.google.com/maps/search/?api=1&query=35.7048979,139.5802557&query_place_id=ChIJNbTiyUfuGGAR6lter_U3i7g) (コピス吉祥寺 A館 B1F) 享用 DIY 串炸吃到飽（推薦：牛肉串、蝦串、章魚燒串、巧克力噴泉），人均約 ¥1,900～¥2,500。  
>   * 動線優勢：位於商場地下街，吹冷氣且小孩能體驗自己沾粉油炸的樂趣。  
> * 備案餐廳 2：[**一風堂 (一風堂 吉祥寺店)**](https://www.google.com/maps/search/?api=1&query=35.7052815,139.5786162&query_place_id=ChIJZziKmUfuGGAR8iau_mxpQKw) (吉祥寺サンロード商店街) 享用博多豚骨拉麵（推薦：白丸元味、赤丸新味、一口煎餃），人均約 ¥900～¥1,300。  
>   * 動線優勢：位於有頂棚遮蔭的商店街內，出餐快速，有兒童餐具與座椅。  
</details>"""

text = text.replace(kichijoji_lunch_backup_old, kichijoji_lunch_backup_new)

# Day 5: 晴空塔午餐備案折疊
solamachi_lunch_backup_old = """> * 備案餐廳 1：[**利久牛舌 (牛たん炭焼 利久 東京ソラマチ店)**](https://www.google.com/maps/search/?api=1&query=35.7103501,139.8118002&query_place_id=ChIJL8P8-daOGGARz0_59g1L3pE) (東京ソラマチ 東館 6F 餐廳街) 享用炭烤牛舌定食（推薦：極厚切牛舌定食、牛尾湯），人均約 ¥2,000～¥3,000。  
> * 備案餐廳 2：[**宮武讚岐烏龍麵 (宮武讃岐うどん 東京ソラマチ店)**](https://www.google.com/maps/search/?api=1&query=35.7101502,139.8105001&query_place_id=ChIJb-X7-daOGGAR3yH28t4D5lM) (東京ソラマチ 西館 3F 美食街 タベテラス) 享用讚岐烏龍麵（推薦：牛肉烏龍麵、炸天婦羅），人均約 ¥600～¥1,000。  
> * 備案餐廳 3：[**一風堂 (一風堂 東京ソラマチ店)**](https://www.google.com/maps/search/?api=1&query=35.7101803,139.8105502&query_place_id=ChIJc-Y8-daOGGAR2xJ37u5E6nQ) (東京ソラマチ 西館 3F 美食街 タベテラス) 享用豚骨拉麵，人均約 ¥900～¥1,300。"""

solamachi_lunch_backup_new = """<details>
<summary>��️ 查看晴空塔午餐備案（利久牛舌 / 宮武烏龍麵 / 一風堂）（點擊展開）</summary>

> * 備案餐廳 1：[**利久牛舌 (牛たん炭焼 利久 東京ソラマチ店)**](https://www.google.com/maps/search/?api=1&query=35.7103501,139.8118002&query_place_id=ChIJL8P8-daOGGARz0_59g1L3pE) (東京ソラマチ 東館 6F 餐廳街) 享用炭烤牛舌定食（推薦：極厚切牛舌定食、牛尾湯），人均約 ¥2,000～¥3,000。  
> * 備案餐廳 2：[**宮武讚岐烏龍麵 (宮武讃岐うどん 東京ソラマチ店)**](https://www.google.com/maps/search/?api=1&query=35.7101502,139.8105001&query_place_id=ChIJb-X7-daOGGAR3yH28t4D5lM) (東京ソラマチ 西館 3F 美食街 タベテラス) 享用讚岐烏龍麵（推薦：牛肉烏龍麵、炸天婦羅），人均約 ¥600～¥1,000。  
> * 備案餐廳 3：[**一風堂 (一風堂 東京ソラマチ店)**](https://www.google.com/maps/search/?api=1&query=35.7101803,139.8105502&query_place_id=ChIJc-Y8-daOGGAR2xJ37u5E6nQ) (東京ソラマチ 西館 3F 美食街 タベテラス) 享用豚骨拉麵，人均約 ¥900～¥1,300。  
</details>"""

text = text.replace(solamachi_lunch_backup_old, solamachi_lunch_backup_new)

# Add [⬆️ 回頂部] anchor to the end of each Day section
for day_idx in range(1, 7):
    # Pattern to find day boundaries
    pass

# Write out to README.md and 2026東京親子自由行_V10_Henna.md
with open('/home/owen/tokyo/README.md', 'w', encoding='utf-8') as f:
    f.write(text)

with open('/home/owen/tokyo/2026東京親子自由行_V10_Henna.md', 'w', encoding='utf-8') as f:
    f.write(text)

print("Successfully refactored README.md and V10 with UX and details folding!")
