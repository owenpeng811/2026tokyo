import re
import os

CUSTOM_SUMMARIES = {
    # Day 1
    (1, "機場整備與購票"): "洗手間整備、ATM提款、整理行李。<strong>建議直接於機場辦理 2 張兒童 Welcome Suica</strong>（需出示護照，後續搭車最省事），每張建議先儲值 ¥2,000～3,000。",
    (1, "前往淺草橋飯店"): "<strong>搭乘首選（直達）：</strong>從羽田機場第3航廈站 搭乘「京急機場線 (直通都營淺草線)」直達 淺草橋站。車程約 40-45 分鐘，免提行李換車。",
    (1, "飯店 Check-in"): "步行抵達飯店，辦理 Check-in、置放行李、稍作休息，更換舒適鞋衣。",
    (1, "晚餐：鳥良商店 (新宿西口店)"): "雞肉料理名店（人均 ¥2,500-3,500）。推薦點選：<strong>雞肉串燒、唐揚雞、親子丼</strong>。已訂位 17:00。<br><strong>大戶屋新宿西口HALC店：</strong><a class=\"map-link-inline\" href=\"https://www.google.com/maps/search/?api=1&query=大戸屋+新宿西口ハルク店\" target=\"_blank\">🍽️ 導航</a> 備案餐廳，位於 HALC 商場 B3F，主打經典家庭日式定食，人均約 ¥1,000-1,500。",
    (1, "東京都廳南展望室"): "參觀東京都廳南展望室與都民廣場拍照。欣賞 8 月下旬東京白天、黃昏與夜景的漸層變化，21:00 前返回飯店。",
    (1, "秋葉原慢遊"): "秋葉原商圈漫步：<strong>GiGO 秋葉原</strong>玩夾娃娃、扭蛋店（預算 ¥400-600/人），以及<strong>友都八喜 Yodobashi</strong>玩具與 Switch 樓層參觀體驗。",
    (1, "晚餐 (秋葉原)"): "秋葉原晚餐選擇：首選<strong>丸龜製麵秋葉原店</strong>（烏龍麵，人均 ¥500-900）；備案為<strong>CoCo壹番屋秋葉原站前店</strong>（咖哩飯）或<strong>壽司郎秋葉原站前店</strong>（迴轉壽司）。",
    (1, "地方超市採買 (Plan A / B 共通)"): "慢步前往飯店附近的 24 小時大型生鮮超市 <strong>肉のハナマサ (Hanamasa 淺草橋店)</strong> 採買：翌日早餐、高優質鮮乳、礦泉水，以及日本當季盛產水果（價格比超商更經濟實惠）。",
    (1, "回飯店"): "步行回飯店。整理明日裝備：門票、Welcome Suica、行動電源。全家輪流洗澡休息。<strong>建議最晚於 21:30 前入睡</strong>。",
    
    # Day 2 Parents
    (2, "出發前往上野御徒町"): "從淺草橋搭 JR 總武線至秋葉原，轉乘山手線或京濱東北線 1 站，在<strong>御徒町站</strong>出站，車程僅 5 分鐘。",
    (2, "尋找基地營咖啡廳與會合點"): "<strong>首選基地營：</strong>DEAN & DELUCA CAFE (PARCO_ya 1F)（人均 ¥500-800）。方便室內組頁腳，與戶外散步組會合。<br><strong>備案基地營：</strong><a class=\"map-link-inline\" href=\"https://www.google.com/maps/search/?api=1&query=喫茶+トリコロール+松坂屋上野店\" target=\"_blank\">🍵 導航</a> 喫茶 トリコロール (松坂屋本館 2F)（人均 ¥800-1,200），日系復古環境幽靜。",
    (2, "上午自由活動"): "<strong>室內組：</strong>在基地營悠閒放鬆或逛松坂屋百貨與 PARCO_ya 百貨。<br><strong>戶外組：</strong>建議路線從松坂屋出發 ➔ 不忍池（賞荷花） ➔ 清水觀音堂（看月之松）。<br><strong>隱藏版美食：</strong><a class=\"map-link-inline\" href=\"https://www.google.com/maps/search/?api=1&query=うさぎや+上野\" target=\"_blank\">🍽️ 導航</a> 可順路步行至「兔屋 (うさぎや)」採買現做百年銅鑼燒。<br><strong>體力充沛備案景點：</strong>上野東照宮、舊岩崎邸庭園。",
    (2, "午餐會合"): "首選餐廳：<strong>KATOREYA (松坂屋本館 M2F)</strong> 經典日式家庭餐廳，人均約 ¥1,500-2,000。<strong>請在 11:30 提早入座避開排隊！</strong><br>備案：<a class=\"map-link-inline\" href=\"https://www.google.com/maps/search/?api=1&query=手打ちそば+みや川+パルコヤ上野店\" target=\"_blank\">🍽️ 導航</a> 手打ちそば みや川 (PARCO_ya 6F) 享用天婦羅蕎麥麵。",
    (2, "下午自由活動"): "<strong>室內組：</strong>繼續於室內或基地營悠遊，或在松坂屋本館休息。<br><strong>戶外組：</strong>建議路線從東京文化會館 ➔ 國立西洋美術館（看羅丹雕塑） ➔ 上野公園中央噴水廣場。<br><strong>避暑備案：</strong><a class=\"map-link-inline\" href=\"https://www.google.com/maps/search/?api=1&query=国際子ども図書館\" target=\"_blank\">📍 導航</a> 國際兒童圖書館，可進入這座近百年的磚紅色老建築，享受優美安靜的室內空調。",
    (2, "晚餐會合"): "首選餐廳：步行至御徒町站附近的 <strong>松屋</strong> 享用平價美味牛丼（人均 ¥500-900）。<br>備案：<a class=\"map-link-inline\" href=\"https://www.google.com/maps/search/?api=1&query=松坂屋上野店+ほっぺタウン\" target=\"_blank\">🍽️ 導航</a> 松坂屋地下美食街（ほっぺタウン）自由外帶各式便當。",
    (2, "返回飯店"): "由御徒町搭乘山手線至秋葉原，轉總武線 1 站返抵淺草橋飯店，早點洗熱水澡舒緩雙腿。",
    
    # Day 2 Kids
    (2, "迪士尼交通動線"): "<strong>特選輕鬆電車路線：</strong>淺草橋 ➔ 秋葉原 (總武線) ➔ 八丁堀 (地鐵日比谷線) ➔ 舞濱 (JR京葉線)。避開東京車站複雜轉乘。",
    (2, "抵達樂園門口"): "開園排隊。入園後立即開啟 Disney App：搶購「美女與野獸 (DPA)」或預約免費「Priority Pass (PP)」。<br>第一必玩：<strong>美女與野獸：魔法物語</strong> (推薦 DPA)<br>第二必玩：<strong>小熊維尼獵蜜記</strong> (搶 Priority Pass)<br>第三推薦：<strong>巨雷山</strong> (過 130cm 小朋友必玩)",
    (2, "午餐"): "首選餐廳：<strong>紅心皇后宴會大廳</strong>（無行動點餐，需排 45-60 分）。<br><strong>🚀 救星備案（App 行動點餐）：</strong>廣場閣樓餐廳（<a class=\"map-link-inline\" href=\"https://www.google.com/maps/search/?api=1&query=プラザパビリオン・レストラン\" target=\"_blank\">🍽️ 導航</a> 歐風漢堡排）或明日樂園舞台餐廳（<a class=\"map-link-inline\" href=\"https://www.google.com/maps/search/?api=1&query=トゥモローランド・テラス\" target=\"_blank\">🍽️ 導航</a> 漢堡/三明治），免排隊！",
    (2, "午後行程與遊行"): "<strong>必看日間遊行：</strong>提前 30 分鐘於遊行路線旁卡位休息。<br><strong>熱門推薦設施：</strong>幽靈公館、加勒比海盜、飛濺山（夏日消暑首選）。備選：怪獸電力公司、小小世界。",
    (2, "晚餐：主題餐廳時間"): "<strong>首選：</strong>廣場閣樓餐廳（<a class=\"map-link-inline\" href=\"https://www.google.com/maps/search/?api=1&query=プラザパビリオン・レストラン\" target=\"_blank\">🍽️ 導航</a> 漢堡排炸蝦盤）或 莎拉奶奶之之家（<a class=\"map-link-inline\" href=\"https://www.google.com/maps/search/?api=1&query=グランマ・サラのキッチン\" target=\"_blank\">🍽️ 導航</a> 蛋包飯）。<br><strong>快速備案：</strong><a class=\"map-link-inline\" href=\"https://www.google.com/maps/search/?api=1&query=パン+ギャラクティック+ピザ+ポート\" target=\"_blank\">🍽️ 導航</a> 紅連火箭筒餐廳（披薩與烤餅）。",
    (2, "城堡點燈拍照、購買夜間點心與遊行卡位"): "灰姑娘城堡夜間點燈拍照，留下夢幻全家福。購買吉事果或米奇冰棒作為夜間點心。19:30 前往圓環區域或明日樂園通道邊卡位休息。",
    (2, "東京迪士尼樂園電子大遊行「夢之光」"): "全長約 45 分鐘，欣賞璀璨燈光花車與經典迪士尼音樂，全家可坐著休息放鬆雙腿。",
    (2, "城堡高空投影秀「Reach for the Stars: Everlasting Dreams」"): "2026 夏季特別版（約 25 分鐘），於灰姑娘城堡前欣賞結合漫威、大英雄天團與迪士尼經典動畫的 3D 燈光投影與焰火秀。",
    (2, "世界市集（World Bazaar）最後補貨與出園"): "於世界市集購買紀念品與伴手禮，約 21:50 離開樂園前往 JR 舞濱站。",
    (2, "親子組回程交通（首選巴士 / 備案電車）"): "<strong>首選（直達巴士）：</strong>出園直接去巴士總站搭乘往<strong>秋葉原站東口</strong>的高速巴士（車程約 35-45m，上車即有座位，小孩可以一路睡回秋葉原）。到秋葉原轉總武線 1 站至淺草橋。<br><strong>電車備案：</strong>舞濱站 ➔ 八丁堀站 (京葉線 2號月台) ➔ 秋葉原站 (地鐵日比谷線 2號月台) ➔ 淺草橋。",
    
    # Day 3
    (3, "搭乘 JR 前往東京車站"): "淺草橋 ➔ 秋葉原 ➔ 東京站 (JR 山手線)。前往西側廣場，在清晨涼風中與壯麗的百年紅磚站舍拍照合影。",
    (3, "東京車站丸之內紅磚站舍"): "拍全家福、欣賞東京車站經典紅磚建築（清晨較涼爽，最適合戶外拍照）。",
    (3, "返回東京車站一番街入口等待開門"): "<strong>避坑指南：</strong>從丸之內（西側）跨越到八重洲（東側地下）時，<strong>請走站外的「北自由通路」</strong>！千萬別刷 Suica 誤進站！<br>10:00 一開門優先逛：寶可夢商店（站長皮卡丘）、TOMICA、橡子共和國、吉伊卡哇商店、迪士尼商店。",
    (3, "東京車站一番街"): "10:00 店家開始營業，依照目標店家優先順序慢慢逛，不需每間店都慢慢逛，保留時間欣賞東京車站地面景觀。",
    (3, "KITTE花園展望台"): "搭乘 KITTE 商場電梯上 6 樓，這片綠化屋頂花園可免費進入。是鋪瞰東京車站紅磚站舍、新幹線與城市景觀，順便吹冷氣休息。",
    (3, "午餐（東京車站）"): "首選餐廳：<strong>燕子烤肉漢堡排 (大丸東京店)</strong> 經典鐵箔包烤漢堡排，空間寬敞可賞高空景觀，人均約 ¥1,800-2,500。<br><strong>備案：</strong>大丸東京店「三代目泰明軒」（<a class=\"map-link-inline\" href=\"https://www.google.com/maps/search/?api=1&query=たいめいけん+大丸東京店\" target=\"_blank\">🍽️ 導航</a> 蛋包飯）或東京站「極味屋」（<a class=\"map-link-inline\" href=\"https://www.google.com/maps/search/?api=1&query=極味や+東京駅店\" target=\"_blank\">🍽️ 導航</a> 鐵板漢堡排，但人擠油煙大、不推薦長輩小孩排隊）。",
    (3, "前往上野"): "搭乘 JR 山手線 8 分鐘抵達上野站。",
    (3, "國立科學博物館"): "參觀國立科學博物館，打卡地球館 B1 恐龍化石、3F 世界野生動物標本及 THEATER 360°。若累了可在公園樹下休息或欣賞西洋美術館外觀。",
    (3, "離開國立科學博物館"): "慢慢步行往御徒町站方向，不趕行程。",
    (3, "晚餐 or 點心：鴨 to 蔥拉麵"): "主打香濃鴨肉醬油拉麵。<strong>規則：排隊在 3 組內就吃；超過直接跳過</strong>，將名額留給阿美橫丁或秋葉原晚餐，不耗費站立體力。",
    (3, "阿美橫丁(アメ横)採買"): "<strong>必掃店家與名產：</strong><br>二木菓子（<a class=\"map-link-inline\" href=\"https://www.google.com/maps/search/?api=1&query=二木の菓子+第一営業所\" target=\"_blank\">🛒 導航</a> 掃零食，Calbee、干貝糖）；OS Drug（<a class=\"map-link-inline\" href=\"https://www.google.com/maps/search/?api=1&query=OSドラッグ+上野店\" target=\"_blank\">🛒 導航</a> 藥妝價格之冠）；街邊小吃（肉の大山<a class=\"map-link-inline\" href=\"https://www.google.com/maps/search/?api=1&query=肉の大山+上野店\" target=\"_blank\">🍽️ 導航</a>、みなとや章魚燒<a class=\"map-link-inline\" href=\"https://www.google.com/maps/search/?api=1&query=みなとや+食品\" target=\"_blank\">🍽️ 導航</a>）；多慶屋（<a class=\"map-link-inline\" href=\"https://www.google.com/maps/search/?api=1&query=多慶屋\" target=\"_blank\">🛒 導航</a> 紫色商場備案）。",
    (3, "返回淺草橋"): "搭電車返回淺草橋，順路買 RusaRuka 麵包作早餐。晚餐（若沒吃拉麵）吃 <strong>烤牛肉大野 (秋葉原店)</strong>。<br>備案：名代 宇奈とと 上野店（<a class=\"map-link-inline\" href=\"https://www.google.com/maps/search/?api=1&query=名代+宇奈とと+上野店\" target=\"_blank\">🍽️ 導航</a> 鰻魚飯）或 九州じゃんがら拉麵。宵夜可吃 Cow Cow Kitchen 牛奶泡芙（<a class=\"map-link-inline\" href=\"https://www.google.com/maps/search/?api=1&query=東京ミルクチーズ工場+Cow+Cow+Kitchen+アトレ秋葉原1店\" target=\"_blank\">🍽️ 導航</a>）。",
    
    # Day 4
    (4, "前往三鷹"): "淺草橋 ➔ 御茶之水 (總武線)。<strong>在御茶之水站「月台正對面」無縫平行換乘</strong> JR 中央線快速直達三鷹站，省下 15 分鐘。",
    (4, "吉卜力接駁巴士"): "三鷹站南口 9 號公車站搭乘彩繪接駁巴士前往美術館。",
    (4, "三鷹之森吉卜力美術館 (三鷹の森ジブリ美術館)"): "參觀吉卜力美術館（大龍貓售票亭、龍貓接駁巴士、屋頂天空之城巨神兵機械人）。已購票 10:00 入場。",
    (4, "前往吉祥寺"): "<strong>首選 Plan A (防中暑公車)：</strong>美術館旁的「萬助橋」站牌直接坐公車直達吉祥寺站南口（5 分鐘）。避開正午曝曬。<br><strong>備案 Plan B (涼爽散步)：</strong>走林蔭步道穿過「井之頭恩賜公園」（<a class=\"map-link-inline\" href=\"https://www.google.com/maps/search/?api=1&query=井の頭恩賜公園\" target=\"_blank\">📍 導航</a>），可在井之頭池畔合影。",
    (4, "午餐：大戶屋"): "首選餐廳：<strong>大戶屋 吉祥寺店</strong>。備案：Kirarina 商場 9 樓 <strong>手打烏龍麵 杵屋</strong>（<a class=\"map-link-inline\" href=\"https://www.google.com/maps/search/?api=1&query=実演手打ちうどん+杵屋+吉祥寺キラリーナ店\" target=\"_blank\">🍽️ 導航</a>）環境舒適不用曬太陽。",
    (4, "吉祥寺商圈慢活 + 下午茶：SATOU 炸牛肉丸"): "逛 Sunroad 商店街（<a class=\"map-link-inline\" href=\"https://www.google.com/maps/search/?api=1&query=吉祥寺サンロード商店街\" target=\"_blank\">🛒 導航</a>），主力造訪 Loft、無印良品、大創及藥妝店，感受哈莫尼卡橫丁（<a class=\"map-link-inline\" href=\"https://www.google.com/maps/search/?api=1&query=ハーモニカ横丁\" target=\"_blank\">📍 導航</a>）昭和巷弄。排隊 10 人以下買 SATOU 炸牛肉丸（<a class=\"map-link-inline\" href=\"https://www.google.com/maps/search/?api=1&query=吉祥寺さとう\" target=\"_blank\">🍽️ 導航</a>）。",
    (4, "晚餐：串家物語"): "預約 17:00 <strong>串家物語 吉祥寺店</strong>，全家享受 DIY 炸串樂趣。<br>備案：大阪王將吉祥寺店（<a class=\"map-link-inline\" href=\"https://www.google.com/maps/search/?api=1&query=大阪王将+吉祥寺店\" target=\"_blank\">🍽️ 導航</a>）或 杵屋烏龍麵。",
    (4, "返回淺草橋"): "進站前外帶「Jyonetsu Bakery」（<a class=\"map-link-inline\" href=\"https://www.google.com/maps/search/?api=1&query=Jyonetsu+Bakery+吉祥寺\" target=\"_blank\">🍽️ 導航</a>）人氣麵包。搭慢車直達淺草橋，或搭中央快速線到御茶之水站同月台換總武線。",
    
    # Day 5
    (5, "前往淺草"): "都營淺草線：淺草橋站 ➔ 淺草站 (直達僅 2 站，車程 3 分鐘)。由 1 號或 3 號出口步行 1 分鐘即可看見雷門紅燈籠。",
    (5, "淺草寺"): "清晨人少好拍照，遊覽及參拜路線：雷門 ➔ 仲見世商店街（買人形燒） ➔ 寶藏門 ➔ 五重塔 ➔ 觀音本堂參拜祈福。",
    (5, "展望台：淺草文化觀光中心"): "免費搭電梯到 8 樓半露天觀景台，居高臨下完整俯瞰雷門、仲見世街紅色屋頂長廊及淺草寺，還能正面遠眺隅田川與晴空塔。",
    (5, "前往東京晴空塔"): "步行 3 分鐘至「東武淺草站」，搭東武晴空塔線火車 3 分鐘抵達「東京晴空塔站」，慢步搭電梯橫跨商場至 6 樓餐廳區。",
    (5, "午餐：東京晴空街道 餐廳街"): "首選：<strong>利久牛舌 晴空塔店</strong> 享用仙台碳烤厚切牛舌定食，人均約 ¥2,000-3,000。請派代表先去抽號碼牌！<br>備案：名古屋備長鰻魚飯 (6F，<a class=\"map-link-inline\" href=\"https://www.google.com/maps/search/?api=1&query=ひつまぶし名古屋備長+東京スカイツリータウン・ソラマチ店\" target=\"_blank\">🍽️ 導航</a> 鰻魚三吃）或 3 樓美食街「宮武讚岐烏龍麵 / 一風堂」。",
    (5, "墨田水族館"): "參觀墨田水族館（看企鵝池、水母區）。館內設有許多沙發座椅，長輩能在此放鬆休憩，隨後悠閒逛晴空街道商場。",
    (5, "晚餐"): "在 3 樓美食街享用宮武讚岐烏龍麵（<a class=\"map-link-inline\" href=\"https://www.google.com/maps/search/?api=1&query=宮武讃岐うどん+東京ソラマチ店\" target=\"_blank\">🍽️ 導航</a>）或一風堂（<a class=\"map-link-inline\" href=\"https://www.google.com/maps/search/?api=1&query=一風堂+東京ソラマチ店\" target=\"_blank\">🍽️ 導航</a>），或去押上站前松屋（<a class=\"map-link-inline\" href=\"https://www.google.com/maps/search/?api=1&query=松屋+押上店\" target=\"_blank\">🍽️ 導航</a>）快餐。隨後搭淺草線回淺草橋。",
    
    # Day 6
    (6, "整理行李與退房"): "整理行李，辦理 Check-out 並將全部大件行李寄放在海茵娜酒店櫃檯。",
    (6, "前往築地場外市場"): "都營淺草線：淺草橋站 ➔ 東銀座站 (直達免轉車，僅 8 分鐘)。出站後步行 3 分鐘即達築地。",
    (6, "築地場外市場（早餐）"): "享用現做熱騰騰小吃：<strong>「築地山長」現做玉子燒</strong>（<a class=\"map-link-inline\" href=\"https://www.google.com/maps/search/?api=1&query=築地山長\" target=\"_blank\">🍽️ 導航</a> 一份 ¥150-200）、現烤和牛串、新鮮草莓大福。隨後參訪波除稻荷神社（<a class=\"map-link-inline\" href=\"https://www.google.com/maps/search/?api=1&query=波除稲荷神社\" target=\"_blank\">📍 導航</a>）。",
    (6, "前往羽田機場 (超便利直達)"): "回飯店提領行李後，在<strong>都營淺草線 淺草橋站</strong>搭乘機場快特直達羽田機場第 3 航廈，全程約 40-45 分鐘，免轉乘最省力。",
    (6, "辦理登機與安檢"): "起飛前 3 小時抵達辦理登機。管制區內餐廳享用簡餐（烏龍麵/定食），最後在免稅店採買白色戀人、東京香蕉等伴手禮後登機（CI221，14:30 起飛）。"
}

def markdown_to_html(text):
    if not text:
        return ""
    
    # Preprocess list items
    lines = text.split('\n')
    html_lines = []
    in_list = False
    in_quote = False
    
    for line in lines:
        line = line.strip()
        if not line:
            if in_list:
                html_lines.append('</ul>')
                in_list = False
            if in_quote:
                html_lines.append('</div>')
                in_quote = False
            continue
            
        # Handle Blockquotes
        if line.startswith('>'):
            if not in_quote:
                html_lines.append('<div class="original-quote">')
                in_quote = True
            line = line.lstrip('>').strip()
            # Remove leading bullet if in quote
            if line.startswith('*') or line.startswith('-'):
                line = line.lstrip('*-').strip()
        
        # Handle Lists
        if line.startswith('*') or line.startswith('-') or line.startswith('1\\.') or re.match(r'^\d+\.', line):
            if not in_list:
                html_lines.append('<ul class="original-list">')
                in_list = True
            # Clean list marker
            clean_line = re.sub(r'^[\*\-\d\.]+\s*', '', line).strip()
            # Apply bold & link formatting
            clean_line = format_inline_markdown(clean_line)
            html_lines.append(f'<li>{clean_line}</li>')
            continue
        else:
            if in_list:
                html_lines.append('</ul>')
                in_list = False
                
        # Handle regular line
        formatted = format_inline_markdown(line)
        if in_quote:
            html_lines.append(f'<p>{formatted}</p>')
        else:
            html_lines.append(f'<p class="original-p">{formatted}</p>')
            
    if in_list:
        html_lines.append('</ul>')
    if in_quote:
        html_lines.append('</div>')
        
    return '\n'.join(html_lines)

def format_inline_markdown(text):
    # Bold
    text = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', text)
    # Inline links
    text = re.sub(r'\[(.*?)\]\((.*?)\)', r'<a class="map-link-inline" href="\2" target="_blank">\1 🔗</a>', text)
    # Map query links
    text = re.sub(r'(?<!href=")(https://www\.google\.com/maps/search/\?api=1&query=[^\s\)]+|https://maps\.google\S+|https://maps\.app\S+)', r'<a class="map-link-inline" href="\1" target="_blank">地圖導航 📍</a>', text)
    return text

def parse_readme():
    with open('/home/owen/tokyo/README.md', 'r', encoding='utf-8') as f:
        content = f.read()

    content = content.replace('\r\n', '\n')

    # Extract Meta
    meta = {}
    member_match = re.search(r'## \*\*👨‍👩‍👧‍👦 旅遊成員\*\*\n+\s*>\s*\* (.*?)\n', content)
    meta['member'] = member_match.group(1) if member_match else "我/ 父親/ 母親/ 女兒（9歲，150cm）/兒子（7歲，130cm）"

    flight_match = re.search(r'## \*\*✈️ 航班資訊\*\*\n+\s*>\s*\* 去程：(.*?)\n\s*>\s*\* 回程：(.*?)\n', content)
    if flight_match:
        meta['flight_go'] = flight_match.group(1).strip()
        meta['flight_back'] = flight_match.group(2).strip()
    else:
        meta['flight_go'] = "CI220 松山(TSA) → 羽田(HND) 09:00－13:10"
        meta['flight_back'] = "CI221 羽田(HND) → 松山(TSA) 14:30－16:55"

    stay_match = re.search(r'## \*\*🏨 住宿資訊\*\*\n+\s*\*\*(.*?)\*\*\s*\(住宿 \d+ 晚\)\n+\s*地址：(.*?)\n', content)
    if stay_match:
        meta['hotel_name'] = stay_match.group(1).strip()
        meta['hotel_addr'] = stay_match.group(2).strip()
    else:
        meta['hotel_name'] = "海茵娜酒店东京浅草桥 (Henn na Hotel Tokyo Asakusabashi)"
        meta['hotel_addr'] = "1-10-5 Asakusabashi, Taito-ku, Tokyo 111-0053, JAPAN"

    # Split into days/sections
    sections = re.split(r'\n(## \*\*.*?)\n', content)
    
    days_data = {1: [], 2: {'parents': [], 'kids': []}, 3: [], 4: [], 5: [], 6: []}
    
    current_day = None
    day2_group = None
    
    for i in range(1, len(sections), 2):
        header = sections[i]
        body = sections[i+1] if i+1 < len(sections) else ""
        
        if 'Day 1' in header:
            current_day = 1
        elif 'Day 2' in header:
            current_day = 2
            if '長輩組' in header:
                day2_group = 'parents'
            elif '親子組' in header:
                day2_group = 'kids'
        elif 'Day 3' in header:
            current_day = 3
        elif 'Day 4' in header:
            current_day = 4
        elif 'Day 5' in header:
            current_day = 5
        elif 'Day 6' in header:
            current_day = 6
        elif 'Check-in 後行程' in header and current_day == 1:
            pass
        else:
            continue
            
        slots = re.split(r'\n(### \*\*.*?)\n', body)
        
        for j in range(1, len(slots), 2):
            slot_header = slots[j]
            slot_body = slots[j+1] if j+1 < len(slots) else ""
            
            header_clean = slot_header.replace('###', '').replace('**', '').strip()
            
            time_match = re.match(r'^([\d:：]+－[\d:：]+|[\d:：]+)\s*(.*)', header_clean)
            if time_match:
                slot_time = time_match.group(1)
                slot_title = time_match.group(2)
            else:
                slot_time = ""
                slot_title = header_clean
                
            maps_links = re.findall(r'https://www\.google\.com/maps/search/\?api=1&query=[^\s\)]+|https://maps\.google\S+|https://maps\.app\S+', slot_title + " " + slot_body)
            maps_link = maps_links[0] if maps_links else f"https://www.google.com/maps/search/?api=1&query={slot_title.split('(')[0]}"
            
            title_display = re.sub(r'\[(.*?)\]\(.*?\)', r'\1', slot_title)
            title_display = re.sub(r'\([^\)]*maps[^\)]*\)', '', title_display).strip()
            
            title_display = title_display.replace('✈️', '').replace('🚇', '').replace('🏨', '').replace('🍽️', '').replace('跑', '').replace('🏃', '').replace('🦕', '').replace('🌳', '').replace('🚌', '').replace('📸', '').replace('🍜', '').replace('🍪', '').replace('🛒', '').replace('⛪', '').replace('🌅', '').strip()

            category = 'attraction'
            title_lower = title_display.lower()
            if any(x in title_lower for x in ['餐', '食', '吃', '拉麵', '燒', '飲', '咖啡', '麵', '丼', '牛舌', '丸子', '甜點', '泡芙', '銅鑼燒', '炸牛肉丸']):
                category = 'food'
            elif any(x in title_lower for x in ['車', '航', '抵達', '交通', '公車', '地鐵', '捷運', '飛機', '前往', '返回', '機場線', '京急', '總武線', '山手線', '電車']):
                category = 'transport'
            elif any(x in title_lower for x in ['飯店', '住宿', 'check', '入住', '海茵娜', '就寢', '睡覺']):
                category = 'stay'
                
            html_content = markdown_to_html(slot_body.strip())
            
            # Check Custom Summaries
            summary = CUSTOM_SUMMARIES.get((current_day, title_display))
            has_modal = True
            
            if not summary:
                # If no custom summary, check if original is short or identical
                body_clean = slot_body.strip()
                # Parse to simple text and clean markdown markers for summary
                summary_text = re.sub(r'\[(.*?)\]\(.*?\)', r'\1', body_clean)
                summary_text = re.sub(r'\*\*(.*?)\*\*', r'\1', summary_text)
                summary_text = re.sub(r'^>\s*\*?\s*', '', summary_text)
                
                # If original body is short or just one line, show it directly without modal button
                lines = [l.strip() for l in body_clean.split('\n') if l.strip()]
                if len(lines) <= 1 and not body_clean.startswith('*') and not body_clean.startswith('-'):
                    summary = format_inline_markdown(body_clean)
                    has_modal = False
                else:
                    # Create a default summary (first non-blockquote line)
                    summary = ""
                    for line in body_clean.split('\n'):
                        line = line.strip()
                        if line and not line.startswith('>') and not line.startswith('*') and not line.startswith('-'):
                            summary = format_inline_markdown(line)
                            break
                    if not summary:
                        summary = format_inline_markdown(lines[0]) if lines else ""
            
            slot_item = {
                'time': slot_time,
                'title': title_display,
                'category': category,
                'summary': summary,
                'html_content': html_content,
                'maps_link': maps_link,
                'has_modal': has_modal
            }
            
            if current_day == 2:
                days_data[2][day2_group].append(slot_item)
            else:
                if 'Plan A' in slot_body or 'Plan A' in slot_header or 'Plan A' in title_display:
                    slot_item['plan'] = 'A'
                elif 'Plan B' in slot_body or 'Plan B' in slot_header or 'Plan B' in title_display:
                    slot_item['plan'] = 'B'
                else:
                    slot_item['plan'] = 'common'
                days_data[current_day].append(slot_item)

    return meta, days_data

def generate_html(meta, days_data):
    html_template = """<!DOCTYPE html>
<html lang="zh-TW">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
  <meta name="apple-mobile-web-app-capable" content="yes">
  <meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
  <title>2026 東京 6天5夜親子自由行</title>
  
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700&family=Noto+Sans+TC:wght@300;400;500;700&display=swap" rel="stylesheet">
  
  <style>
    :root {
      --bg-dark: #12141c;
      --card-bg: rgba(26, 29, 41, 0.8);
      --card-border: rgba(255, 255, 255, 0.08);
      --accent-coral: #E45F56;
      --accent-blue: #3b82f6;
      --accent-green: #10b981;
      --accent-purple: #8b5cf6;
      --text-main: #f3f4f6;
      --text-muted: #9ca3af;
      --text-dark: #1f2937;
      --shadow-premium: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
      --blur-strength: 16px;
      --transition-smooth: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    }

    * {
      box-sizing: border-box;
      margin: 0;
      padding: 0;
      -webkit-tap-highlight-color: transparent;
    }

    body {
      font-family: 'Outfit', 'Noto Sans TC', sans-serif;
      background-color: var(--bg-dark);
      background-image: 
        radial-gradient(at 0% 0%, rgba(228, 95, 86, 0.1) 0px, transparent 50%),
        radial-gradient(at 100% 100%, rgba(59, 130, 246, 0.1) 0px, transparent 50%);
      background-attachment: fixed;
      color: var(--text-main);
      line-height: 1.6;
      padding-bottom: 90px;
      overflow-x: hidden;
    }

    ::-webkit-scrollbar {
      width: 6px;
      height: 6px;
    }
    ::-webkit-scrollbar-track {
      background: transparent;
    }
    ::-webkit-scrollbar-thumb {
      background: rgba(255, 255, 255, 0.1);
      border-radius: 3px;
    }

    .top-banner {
      padding: 24px 20px 16px;
      background: linear-gradient(180deg, rgba(18, 20, 28, 0.95) 0%, rgba(18, 20, 28, 0) 100%);
      border-bottom: 1px solid rgba(255, 255, 255, 0.05);
      position: relative;
    }

    .logo-container {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 8px;
    }

    .badge-year {
      background: var(--accent-coral);
      color: white;
      font-weight: 700;
      padding: 2px 8px;
      border-radius: 20px;
      font-size: 0.75rem;
      letter-spacing: 1px;
    }

    .trip-title {
      font-size: 1.4rem;
      font-weight: 700;
      letter-spacing: -0.5px;
      background: linear-gradient(135deg, #fff 0%, #a5b4fc 100%);
      -webkit-background-clip: text;
      background-clip: text;
      -webkit-text-fill-color: transparent;
    }

    .trip-meta {
      display: flex;
      flex-wrap: wrap;
      gap: 12px;
      margin-top: 10px;
      font-size: 0.85rem;
      color: var(--text-muted);
    }

    .trip-meta span {
      display: flex;
      align-items: center;
      gap: 4px;
    }

    .trip-meta a {
      color: var(--text-main);
      text-decoration: none;
      border-bottom: 1px dashed var(--text-muted);
    }

    .info-strip {
      margin: 0 16px 20px;
      padding: 12px 16px;
      background: rgba(255, 255, 255, 0.03);
      border: 1px solid var(--card-border);
      border-radius: 12px;
      font-size: 0.8rem;
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 12px;
    }

    .flight-side {
      display: flex;
      flex-direction: column;
    }

    .flight-side .title {
      color: var(--accent-blue);
      font-weight: 600;
      margin-bottom: 2px;
    }

    .sticky-nav-container {
      position: sticky;
      top: 0;
      z-index: 100;
      background: rgba(18, 20, 28, 0.85);
      backdrop-filter: blur(var(--blur-strength));
      -webkit-backdrop-filter: blur(var(--blur-strength));
      border-bottom: 1px solid var(--card-border);
      padding: 10px 0;
    }

    .day-tabs {
      display: flex;
      overflow-x: auto;
      padding: 0 16px;
      gap: 8px;
      scroll-snap-type: x mandatory;
      scrollbar-width: none;
    }

    .day-tabs::-webkit-scrollbar {
      display: none;
    }

    .tab-btn {
      flex: 0 0 auto;
      scroll-snap-align: start;
      background: rgba(255, 255, 255, 0.04);
      border: 1px solid var(--card-border);
      color: var(--text-muted);
      padding: 8px 16px;
      border-radius: 30px;
      font-size: 0.9rem;
      font-weight: 600;
      cursor: pointer;
      transition: var(--transition-smooth);
    }

    .tab-btn.active {
      background: var(--text-main);
      color: var(--bg-dark);
      border-color: var(--text-main);
      box-shadow: 0 4px 12px rgba(255, 255, 255, 0.15);
    }

    .progress-bar-container {
      margin: 8px 16px 0;
      height: 4px;
      background: rgba(255, 255, 255, 0.05);
      border-radius: 2px;
      overflow: hidden;
    }

    .progress-bar-fill {
      height: 100%;
      width: 0%;
      background: linear-gradient(90deg, var(--accent-blue), var(--accent-green));
      transition: width 0.4s ease;
    }

    .filter-bar {
      display: flex;
      overflow-x: auto;
      padding: 12px 16px;
      gap: 6px;
      scrollbar-width: none;
    }

    .filter-bar::-webkit-scrollbar {
      display: none;
    }

    .filter-pill {
      flex: 0 0 auto;
      background: rgba(255, 255, 255, 0.02);
      border: 1px solid rgba(255, 255, 255, 0.05);
      color: var(--text-muted);
      padding: 6px 12px;
      border-radius: 20px;
      font-size: 0.75rem;
      font-weight: 500;
      cursor: pointer;
      transition: var(--transition-smooth);
      display: flex;
      align-items: center;
      gap: 4px;
    }

    .filter-pill.active {
      background: rgba(255, 255, 255, 0.12);
      color: var(--text-main);
      border-color: rgba(255, 255, 255, 0.2);
    }

    .sub-toggle-container {
      display: none;
      margin: 0 16px 16px;
      background: rgba(0, 0, 0, 0.2);
      border-radius: 30px;
      padding: 4px;
      border: 1px solid var(--card-border);
    }

    .sub-toggle {
      display: flex;
      width: 100%;
    }

    .sub-toggle-btn {
      flex: 1;
      background: transparent;
      border: none;
      color: var(--text-muted);
      padding: 8px 12px;
      font-size: 0.85rem;
      font-weight: 600;
      border-radius: 26px;
      cursor: pointer;
      transition: var(--transition-smooth);
      display: flex;
      justify-content: center;
      align-items: center;
      gap: 6px;
    }

    .sub-toggle-btn.active {
      background: rgba(255, 255, 255, 0.08);
      color: var(--text-main);
      box-shadow: inset 0 1px 1px rgba(255, 255, 255, 0.1);
    }

    .timeline {
      padding: 0 16px;
      position: relative;
    }

    .timeline-item {
      display: flex;
      margin-bottom: 20px;
      position: relative;
      animation: fadeIn 0.4s ease forwards;
    }

    @keyframes fadeIn {
      from { opacity: 0; transform: translateY(12px); }
      to { opacity: 1; transform: translateY(0); }
    }

    .timeline-check {
      flex: 0 0 40px;
      display: flex;
      flex-direction: column;
      align-items: center;
      position: relative;
    }

    .timeline-line {
      position: absolute;
      top: 36px;
      bottom: -20px;
      width: 2px;
      background: rgba(255, 255, 255, 0.08);
      z-index: 1;
    }

    .timeline-item:last-child .timeline-line {
      display: none;
    }

    .check-wrapper {
      position: relative;
      width: 26px;
      height: 26px;
      margin-top: 4px;
      z-index: 2;
    }

    .check-wrapper input {
      position: absolute;
      opacity: 0;
      cursor: pointer;
      height: 0;
      width: 0;
    }

    .checkmark {
      position: absolute;
      top: 0;
      left: 0;
      height: 26px;
      width: 26px;
      background-color: rgba(255, 255, 255, 0.05);
      border: 2px solid rgba(255, 255, 255, 0.15);
      border-radius: 50%;
      transition: var(--transition-smooth);
      display: flex;
      align-items: center;
      justify-content: center;
    }

    .check-wrapper:hover input ~ .checkmark {
      border-color: var(--text-muted);
    }

    .check-wrapper input:checked ~ .checkmark {
      background-color: var(--accent-green);
      border-color: var(--accent-green);
    }

    .checkmark:after {
      content: "";
      display: none;
      width: 5px;
      height: 10px;
      border: solid white;
      border-width: 0 2px 2px 0;
      transform: rotate(45deg);
      margin-bottom: 2px;
    }

    .check-wrapper input:checked ~ .checkmark:after {
      display: block;
    }

    .timeline-card {
      flex: 1;
      background: var(--card-bg);
      border: 1px solid var(--card-border);
      border-radius: 16px;
      padding: 16px;
      box-shadow: var(--shadow-premium);
      backdrop-filter: blur(var(--blur-strength));
      -webkit-backdrop-filter: blur(var(--blur-strength));
      transition: var(--transition-smooth);
      position: relative;
      overflow: hidden;
    }

    .timeline-card.checked {
      border-color: rgba(16, 185, 129, 0.3);
      opacity: 0.75;
    }

    .card-header {
      display: flex;
      justify-content: space-between;
      align-items: flex-start;
      margin-bottom: 8px;
    }

    .card-time {
      font-size: 0.85rem;
      font-weight: 700;
      color: var(--accent-blue);
      letter-spacing: 0.5px;
    }

    .card-tags {
      display: flex;
      gap: 4px;
    }

    .tag {
      font-size: 0.65rem;
      font-weight: 600;
      padding: 2px 8px;
      border-radius: 20px;
      text-transform: uppercase;
    }

    .tag-attraction { background: rgba(59, 130, 246, 0.15); color: #93c5fd; }
    .tag-food { background: rgba(228, 95, 86, 0.15); color: #fca5a5; }
    .tag-transport { background: rgba(16, 185, 129, 0.15); color: #6ee7b7; }
    .tag-stay { background: rgba(139, 92, 246, 0.15); color: #c4b5fd; }

    .card-title {
      font-size: 1.05rem;
      font-weight: 600;
      margin-bottom: 8px;
      display: flex;
      align-items: center;
      flex-wrap: wrap;
      gap: 6px;
    }

    .map-link {
      display: inline-flex;
      align-items: center;
      gap: 2px;
      background: rgba(255, 255, 255, 0.05);
      border: 1px solid rgba(255, 255, 255, 0.08);
      color: var(--text-main);
      padding: 2px 8px;
      border-radius: 6px;
      font-size: 0.7rem;
      text-decoration: none;
      transition: var(--transition-smooth);
    }

    .map-link:active {
      background: rgba(255, 255, 255, 0.15);
    }

    .card-body {
      font-size: 0.85rem;
      color: var(--text-muted);
    }

    .card-body p {
      margin-bottom: 8px;
    }

    .card-body p:last-child {
      margin-bottom: 0;
    }

    .view-original-btn {
      display: inline-flex;
      align-items: center;
      gap: 4px;
      background: rgba(59, 130, 246, 0.15);
      border: 1px solid rgba(59, 130, 246, 0.20);
      color: #93c5fd;
      padding: 6px 12px;
      border-radius: 8px;
      font-size: 0.75rem;
      font-weight: 600;
      cursor: pointer;
      margin-top: 10px;
      transition: var(--transition-smooth);
    }

    .view-original-btn:active {
      background: rgba(59, 130, 246, 0.25);
    }

    .emergency-bar {
      position: fixed;
      bottom: 0;
      left: 0;
      right: 0;
      background: rgba(26, 29, 41, 0.95);
      backdrop-filter: blur(20px);
      -webkit-backdrop-filter: blur(20px);
      border-top: 1px solid var(--card-border);
      padding: 12px 16px;
      z-index: 1000;
      box-shadow: 0 -4px 20px rgba(0,0,0,0.4);
    }

    .emergency-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
    }

    .emergency-header span {
      display: flex;
      align-items: center;
      gap: 8px;
      font-weight: 700;
      color: var(--accent-coral);
    }

    .emergency-header button {
      background: rgba(255, 255, 255, 0.08);
      border: 1px solid var(--card-border);
      color: var(--text-main);
      padding: 4px 12px;
      border-radius: 20px;
      font-size: 0.75rem;
      cursor: pointer;
    }

    .emergency-drawer {
      display: none;
      margin-top: 16px;
      max-height: 70vh;
      overflow-y: auto;
      border-top: 1px solid rgba(255, 255, 255, 0.05);
      padding-top: 16px;
      font-size: 0.8rem;
    }

    .emergency-section {
      margin-bottom: 16px;
    }

    .emergency-section h4 {
      color: var(--accent-coral);
      margin-bottom: 6px;
      font-size: 0.85rem;
      display: flex;
      align-items: center;
      gap: 4px;
    }

    .emergency-section p {
      color: var(--text-muted);
      margin-bottom: 4px;
    }

    .weather-chip {
      background: rgba(255, 255, 255, 0.05);
      border: 1px solid rgba(255, 255, 255, 0.08);
      border-radius: 12px;
      padding: 10px;
      margin: 0 16px 16px;
      display: flex;
      justify-content: space-between;
      align-items: center;
      font-size: 0.8rem;
    }

    .weather-icon {
      font-size: 1.5rem;
    }

    .decision-banner {
      background: linear-gradient(135deg, rgba(228, 95, 86, 0.2) 0%, rgba(59, 130, 246, 0.1) 100%);
      border: 1px solid var(--accent-coral);
      padding: 12px;
      border-radius: 12px;
      margin-bottom: 16px;
      font-size: 0.8rem;
    }

    .decision-banner strong {
      color: var(--accent-coral);
    }

    .modal-overlay {
      position: fixed;
      top: 0;
      left: 0;
      right: 0;
      bottom: 0;
      background: rgba(0, 0, 0, 0.7);
      z-index: 2000;
      opacity: 0;
      visibility: hidden;
      transition: var(--transition-smooth);
      backdrop-filter: blur(6px);
      -webkit-backdrop-filter: blur(6px);
    }

    .modal-overlay.active {
      opacity: 1;
      visibility: visible;
    }

    .modal-sheet {
      position: fixed;
      bottom: 0;
      left: 0;
      right: 0;
      background: #181b29;
      border-top-left-radius: 24px;
      border-top-right-radius: 24px;
      border-top: 1px solid rgba(255, 255, 255, 0.1);
      z-index: 2001;
      transform: translateY(100%);
      transition: transform 0.4s cubic-bezier(0.16, 1, 0.3, 1);
      max-height: 85vh;
      display: flex;
      flex-direction: column;
      box-shadow: 0 -8px 40px rgba(0, 0, 0, 0.6);
    }

    .modal-sheet.active {
      transform: translateY(0);
    }

    .modal-drag-bar {
      width: 40px;
      height: 4px;
      background: rgba(255, 255, 255, 0.2);
      border-radius: 2px;
      margin: 12px auto 6px;
    }

    .modal-header {
      padding: 16px 20px;
      border-bottom: 1px solid rgba(255, 255, 255, 0.05);
      display: flex;
      justify-content: space-between;
      align-items: center;
    }

    .modal-title-container {
      flex: 1;
    }

    .modal-time {
      font-size: 0.8rem;
      color: var(--accent-blue);
      font-weight: 700;
      margin-bottom: 2px;
    }

    .modal-title {
      font-size: 1.15rem;
      font-weight: 700;
    }

    .modal-close-btn {
      background: rgba(255, 255, 255, 0.05);
      border: 1px solid rgba(255, 255, 255, 0.08);
      color: var(--text-main);
      width: 32px;
      height: 32px;
      border-radius: 50%;
      font-size: 1.1rem;
      cursor: pointer;
      display: flex;
      align-items: center;
      justify-content: center;
    }

    .modal-body {
      padding: 20px;
      overflow-y: auto;
      flex: 1;
      font-size: 0.95rem;
    }

    .original-quote {
      background: rgba(228, 95, 86, 0.1);
      border-left: 4px solid var(--accent-coral);
      padding: 12px 16px;
      margin-bottom: 16px;
      border-radius: 4px;
      font-size: 0.9rem;
    }

    .original-quote p {
      margin-bottom: 6px !important;
    }

    .original-quote p:last-child {
      margin-bottom: 0 !important;
    }

    .original-list {
      margin: 0 0 16px 20px;
    }

    .original-list li {
      margin-bottom: 6px;
    }

    .original-p {
      margin-bottom: 12px;
    }

    .map-link-inline {
      display: inline-flex;
      align-items: center;
      gap: 2px;
      background: rgba(59, 130, 246, 0.15);
      color: #93c5fd;
      padding: 2px 6px;
      border-radius: 4px;
      text-decoration: none;
      font-size: 0.8rem;
    }
  </style>
</head>
<body>

  <!-- Top Header Banner -->
  <div class="top-banner">
    <div class="logo-container">
      <h1 class="trip-title">東京親子自由行</h1>
      <span class="badge-year">2026 SUMMER</span>
    </div>
    <p style="font-size: 0.85rem; opacity: 0.9; margin-bottom: 6px;">🇯🇵 6天5夜 · 住宿與行程原始完整版</p>
    <div class="trip-meta">
      <span>🏨 海茵娜酒店 東京淺草橋</span>
      <span>📍 <a href="https://www.google.com/maps/search/?api=1&query={hotel_query}" target="_blank">地圖導航 🔗</a></span>
    </div>
  </div>

  <!-- Flight Quick Details -->
  <div class="info-strip">
    <div class="flight-side">
      <span class="title">🛫 CI220 去程</span>
      <span>{flight_go}</span>
    </div>
    <div class="flight-side" style="border-left: 1px solid rgba(255,255,255,0.08); padding-left: 12px;">
      <span class="title" style="color: var(--accent-green)">🛬 CI221 回程</span>
      <span>{flight_back}</span>
    </div>
  </div>

  <!-- Weather & Reminder Info -->
  <div class="weather-chip">
    <div>
      <strong>💡 乘車直覺提醒</strong>
      <p style="color: var(--text-muted); font-size: 0.75rem; margin-top: 2px;">認顏色月台比認日文快！總武線=黃色、山手線=綠色</p>
    </div>
    <span class="weather-icon">🚄</span>
  </div>

  <!-- Sticky Days & Progress -->
  <div class="sticky-nav-container">
    <div class="day-tabs" id="dayTabs">
      <button class="tab-btn active" onclick="switchDay(1)">Day 1</button>
      <button class="tab-btn" onclick="switchDay(2)">Day 2</button>
      <button class="tab-btn" onclick="switchDay(3)">Day 3</button>
      <button class="tab-btn" onclick="switchDay(4)">Day 4</button>
      <button class="tab-btn" onclick="switchDay(5)">Day 5</button>
      <button class="tab-btn" onclick="switchDay(6)">Day 6</button>
    </div>
    <div class="progress-bar-container">
      <div class="progress-bar-fill" id="progressFill"></div>
    </div>
  </div>

  <!-- Filters -->
  <div class="filter-bar">
    <button class="filter-pill active" onclick="setFilter('all')">全部</button>
    <button class="filter-pill" onclick="setFilter('attraction')">📍 景點</button>
    <button class="filter-pill" onclick="setFilter('food')">🍽️ 美食</button>
    <button class="filter-pill" onclick="setFilter('transport')">🚃 交通</button>
    <button class="filter-pill" onclick="setFilter('stay')">🏨 住宿</button>
  </div>

  <!-- Day 2 Split Itinerary Selector -->
  <div class="sub-toggle-container" id="day2GroupToggle">
    <div class="sub-toggle">
      <button class="sub-toggle-btn active" onclick="setGroup('parents')">👵 長輩休閒組</button>
      <button class="sub-toggle-btn" onclick="setGroup('kids')">👦 迪士尼親子組</button>
    </div>
  </div>

  <!-- Day 1 Plan A / B Selector -->
  <div class="sub-toggle-container" id="day1PlanToggle">
    <div class="sub-toggle">
      <button class="sub-toggle-btn active" onclick="setDay1Plan('A')">✅ Plan A (都廳夜景)</button>
      <button class="sub-toggle-btn" onclick="setDay1Plan('B')">✅ Plan B (秋葉原慢遊)</button>
    </div>
  </div>

  <!-- Timeline Itinerary Cards -->
  <div class="timeline" id="timelineContainer">
{timeline_html}
  </div>

  <!-- Bottom Drawer Modal for Original Content -->
  <div class="modal-overlay" id="modalOverlay" onclick="closeModal()"></div>
  <div class="modal-sheet" id="modalSheet">
    <div class="modal-drag-bar"></div>
    <div class="modal-header">
      <div class="modal-title-container">
        <div class="modal-time" id="modalTime">13:10 - 14:10</div>
        <h4 class="modal-title" id="modalTitle">抵達羽田機場第 3 航廈</h4>
      </div>
      <button class="modal-close-btn" onclick="closeModal()">×</button>
    </div>
    <div class="modal-body" id="modalBody">
      <!-- Injected by JS -->
    </div>
  </div>

  <!-- Emergency Footer Bar -->
  <div class="emergency-bar">
    <div class="emergency-header">
      <span>🚨 點擊展開緊急求助與防丟指南</span>
      <button onclick="toggleEmergency()">展開</button>
    </div>
    <div class="emergency-drawer" id="emergencyDrawer">
      <div class="emergency-section">
        <h4>🏨 飯店資訊</h4>
        <p>名稱：Henn na Hotel Tokyo Asakusabashi</p>
        <p>地址：1-10-5 Asakusabashi, Taito-ku, Tokyo 111-0053</p>
        <p>電話：+81 3-5829-9810</p>
      </div>
      <div class="emergency-section">
        <h4>☎️ 常用緊急求助熱線</h4>
        <p>警局撥打：<strong>110</strong> (免費/支援中文服務)</p>
        <p>救護車/火警撥打：<strong>119</strong></p>
        <p>台北駐日經濟文化代表處：<strong>+81 3-3280-7811</strong> (緊急聯絡電話：<strong>+81 80-6557-8796</strong>)</p>
      </div>
      <div class="emergency-section">
        <h4>🛂 護照遺失緊急處理流程</h4>
        <p>1. 立即去最近的派出所（交番 koban）報案，取得「遺失申報證明書」（紛失届出証明書）。</p>
        <p>2. 拍攝白底大頭照 2 張。</p>
        <p>3. 攜帶身分證、報案證明前往駐日代表處辦理「入國證明書」或補發護照。</p>
      </div>
    </div>
  </div>

  <script>
    let currentDay = 1;
    let currentFilter = 'all';
    let currentGroup = 'parents';
    let currentDay1Plan = 'A';

    document.addEventListener("DOMContentLoaded", () => {
      document.querySelectorAll(".check-wrapper input").forEach(input => {
        const isChecked = localStorage.getItem(input.id) === 'true';
        input.checked = isChecked;
        if (isChecked) {
          document.getElementById('card-' + input.id)?.classList.add('checked');
        }
      });
      
      updateProgressBar();
      renderItinerary();
    });

    function toggleCheck(id) {
      const checkbox = document.getElementById(id);
      const card = document.getElementById('card-' + id);
      
      if (checkbox.checked) {
        card.classList.add('checked');
        localStorage.setItem(id, 'true');
      } else {
        card.classList.remove('checked');
        localStorage.setItem(id, 'false');
      }
      updateProgressBar();
    }

    function updateProgressBar() {
      const visibleCheckboxes = Array.from(document.querySelectorAll(`#day${currentDay}-section input[type="checkbox"]`))
        .filter(cb => {
          const item = cb.closest('.timeline-item');
          if (!item) return false;
          
          if (currentDay === 2) {
            const isParents = cb.id.includes('d2p');
            const isKids = cb.id.includes('d2k');
            if (isParents && currentGroup !== 'parents') return false;
            if (isKids && currentGroup !== 'kids') return false;
          }
          if (currentDay === 1) {
            const isPlanA = cb.id.includes('d1a');
            const isPlanB = cb.id.includes('d1b');
            if (isPlanA && currentDay1Plan !== 'A') return false;
            if (isPlanB && currentDay1Plan !== 'B') return false;
          }
          
          return true;
        });

      if (visibleCheckboxes.length === 0) {
        document.getElementById('progressFill').style.width = '0%';
        return;
      }

      const checkedCount = visibleCheckboxes.filter(cb => cb.checked).length;
      const percentage = (checkedCount / visibleCheckboxes.length) * 100;
      document.getElementById('progressFill').style.width = percentage + '%';
    }

    function switchDay(dayNum) {
      currentDay = dayNum;
      
      const tabs = document.querySelectorAll('#dayTabs .tab-btn');
      tabs.forEach((tab, index) => {
        if (index === dayNum - 1) {
          tab.classList.add('active');
        } else {
          tab.classList.remove('active');
        }
      });

      for (let i = 1; i <= 6; i++) {
        const sec = document.getElementById(`day${i}-section`);
        if (sec) sec.style.display = (i === dayNum) ? 'block' : 'none';
      }

      document.getElementById('day2GroupToggle').style.display = (dayNum === 2) ? 'block' : 'none';
      document.getElementById('day1PlanToggle').style.display = (dayNum === 1) ? 'block' : 'none';

      renderItinerary();
      updateProgressBar();
      
      window.scrollTo({ top: 180, behavior: 'smooth' });
    }

    function setFilter(category) {
      currentFilter = category;
      const pills = document.querySelectorAll('.filter-bar .filter-pill');
      pills.forEach(pill => {
        if (pill.getAttribute('onclick').includes(category)) {
          pill.classList.add('active');
        } else {
          pill.classList.remove('active');
        }
      });
      renderItinerary();
    }

    function setGroup(groupName) {
      currentGroup = groupName;
      const btns = document.querySelectorAll('#day2GroupToggle .sub-toggle-btn');
      btns[0].classList.toggle('active', groupName === 'parents');
      btns[1].classList.toggle('active', groupName === 'kids');
      
      renderItinerary();
      updateProgressBar();
    }

    function setDay1Plan(plan) {
      currentDay1Plan = plan;
      const btns = document.querySelectorAll('#day1PlanToggle .sub-toggle-btn');
      btns[0].classList.toggle('active', plan === 'A');
      btns[1].classList.toggle('active', plan === 'B');
      
      renderItinerary();
      updateProgressBar();
    }

    function renderItinerary() {
      const parentsSec = document.querySelector('.day2-parents-itinerary');
      const kidsSec = document.querySelector('.day2-kids-itinerary');
      if (parentsSec && kidsSec) {
        parentsSec.style.display = (currentDay === 2 && currentGroup === 'parents') ? 'block' : 'none';
        kidsSec.style.display = (currentDay === 2 && currentGroup === 'kids') ? 'block' : 'none';
      }

      const planASec = document.querySelector('.day1-plan-A');
      const planBSec = document.querySelector('.day1-plan-B');
      if (planASec && planBSec) {
        planASec.style.display = (currentDay === 1 && currentDay1Plan === 'A') ? 'block' : 'none';
        planBSec.style.display = (currentDay === 1 && currentDay1Plan === 'B') ? 'block' : 'none';
      }

      const currentSection = document.getElementById(`day${currentDay}-section`);
      if (currentSection) {
        const items = currentSection.querySelectorAll('.timeline-item');
        items.forEach(item => {
          const category = item.getAttribute('data-category');
          if (currentFilter === 'all' || category === currentFilter) {
            item.style.display = 'flex';
          } else {
            item.style.display = 'none';
          }
        });
      }
    }

    function openOriginalModal(cardId) {
      const card = document.getElementById(cardId);
      if (!card) return;
      
      const time = card.querySelector('.card-time').innerText;
      const title = card.querySelector('.card-title').innerText.replace('📍 導航', '').trim();
      const originalHtml = card.querySelector('.original-content-holder').innerHTML;
      
      document.getElementById('modalTime').innerText = time;
      document.getElementById('modalTitle').innerText = title;
      document.getElementById('modalBody').innerHTML = originalHtml;
      
      document.getElementById('modalOverlay').classList.add('active');
      document.getElementById('modalSheet').classList.add('active');
      document.body.style.overflow = 'hidden';
    }

    function closeModal() {
      document.getElementById('modalOverlay').classList.remove('active');
      document.getElementById('modalSheet').classList.remove('active');
      document.body.style.overflow = '';
    }

    function toggleEmergency() {
      const drawer = document.getElementById('emergencyDrawer');
      const btn = document.querySelector('.emergency-header button');
      if (drawer.style.display === 'block') {
        drawer.style.display = 'none';
        btn.innerText = '展開';
      } else {
        drawer.style.display = 'block';
        btn.innerText = '收合';
        drawer.scrollIntoView({ behavior: 'smooth' });
      }
    }
  </script>
</body>
</html>
"""

    # Generate the timeline items
    timeline_html = ""
    
    for day in range(1, 7):
        timeline_html += f'    <!-- Day {day} Section -->\n'
        timeline_html += f'    <div class="day-section" id="day{day}-section" style="{"display: none;" if day > 1 else ""}">\n'
        
        if day == 1:
            timeline_html += """      <div class="decision-banner">
        <strong>🎯 關鍵決策點（16:20 離開飯店）</strong>：<br>
        16:20 前出發走 <strong>Plan A (新宿西口鳥良商店 & 都廳夜景)</strong>；<br>
        16:20 後出發走 <strong>Plan B (秋葉原商圈漫步)</strong>。
      </div>\n"""
            
            day1_items = days_data[1]
            common_before = [x for x in day1_items if x.get('plan') == 'common' and day1_items.index(x) < 4]
            plan_a = [x for x in day1_items if x.get('plan') == 'A']
            plan_b = [x for x in day1_items if x.get('plan') == 'B']
            common_after = [x for x in day1_items if x.get('plan') == 'common' and day1_items.index(x) >= 4]
            
            for idx, item in enumerate(common_before):
                timeline_html += make_card_html(f"d1-c{idx}", item)
                
            timeline_html += '      <div class="day1-plan-A">\n'
            for idx, item in enumerate(plan_a):
                timeline_html += make_card_html(f"d1-a{idx}", item)
            timeline_html += '      </div>\n'
            
            timeline_html += '      <div class="day1-plan-B" style="display: none;">\n'
            for idx, item in enumerate(plan_b):
                timeline_html += make_card_html(f"d1-b{idx}", item)
            timeline_html += '      </div>\n'
            
            for idx, item in enumerate(common_after):
                timeline_html += make_card_html(f"d1-ca{idx}", item)
                
        elif day == 2:
            timeline_html += '      <div class="day2-parents-itinerary">\n'
            for idx, item in enumerate(days_data[2]['parents']):
                timeline_html += make_card_html(f"d2p-{idx}", item)
            timeline_html += '      </div>\n'
            
            timeline_html += '      <div class="day2-kids-itinerary" style="display: none;">\n'
            for idx, item in enumerate(days_data[2]['kids']):
                timeline_html += make_card_html(f"d2k-{idx}", item)
            timeline_html += '      </div>\n'
            
        else:
            for idx, item in enumerate(days_data[day]):
                timeline_html += make_card_html(f"d{day}-{idx}", item)
                
        timeline_html += '    </div>\n\n'
        
    hotel_query = meta['hotel_name'].replace(' ', '+')
    final_html = html_template.replace('{hotel_query}', hotel_query)
    final_html = final_html.replace('{flight_go}', meta['flight_go'])
    final_html = final_html.replace('{flight_back}', meta['flight_back'])
    final_html = final_html.replace('{timeline_html}', timeline_html)
    
    with open('/home/owen/tokyo/itinerary.html', 'w', encoding='utf-8') as f:
        f.write(final_html)
    print("Successfully generated itinerary.html!")

def make_card_html(item_id, item):
    btn_html = ""
    if item['has_modal']:
        btn_html = f'<button class="view-original-btn" onclick="openOriginalModal(\'card-item-{item_id}\')">📖 完整原始說明</button>'
        
    return f"""      <div class="timeline-item" data-category="{item['category']}">
        <div class="timeline-check">
          <label class="check-wrapper">
            <input type="checkbox" id="item-{item_id}" onchange="toggleCheck('item-{item_id}')">
            <span class="checkmark"></span>
          </label>
          <div class="timeline-line"></div>
        </div>
        <div class="timeline-card" id="card-item-{item_id}">
          <div class="card-header">
            <span class="card-time">{item['time']}</span>
            <div class="card-tags"><span class="tag tag-{item['category']}">{get_category_zh(item['category'])}</span></div>
          </div>
          <h3 class="card-title">
            {item['title']}
            <a class="map-link" href="{item['maps_link']}" target="_blank">📍 導航</a>
          </h3>
          <div class="card-body">
            <p>{item['summary']}</p>
            {btn_html}
            <div class="original-content-holder" style="display: none;">
              {item['html_content']}
            </div>
          </div>
        </div>
      </div>\n"""

def get_category_zh(cat):
    return {
        'attraction': '景點',
        'food': '美食',
        'transport': '交通',
        'stay': '住宿'
    }.get(cat, '景點')

if __name__ == '__main__':
    meta, days_data = parse_readme()
    generate_html(meta, days_data)
