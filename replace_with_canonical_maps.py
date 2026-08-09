import json
import urllib.request
import urllib.parse
import re

with open('/home/owen/.gemini/config/mcp_config.json') as f:
    cfg = json.load(f)
api_key = cfg['mcpServers']['google-maps']['env']['GOOGLE_MAPS_API_KEY']

# Master dictionary of Place -> Canonical URL
GEOCODE_CACHE = {}

def get_canonical_url(jp_query):
    if jp_query in GEOCODE_CACHE:
        return GEOCODE_CACHE[jp_query]
    
    q_enc = urllib.parse.quote(jp_query)
    url = f"https://maps.googleapis.com/maps/api/geocode/json?address={q_enc}&language=ja&key={api_key}"
    try:
        req = urllib.request.urlopen(url, timeout=5)
        res = json.loads(req.read().decode('utf-8'))
        results = res.get('results', [])
        if results:
            r = results[0]
            place_id = r.get('place_id', '')
            loc = r.get('geometry', {}).get('location', {})
            can_url = f"https://www.google.com/maps/search/?api=1&query={loc.get('lat')},{loc.get('lng')}&query_place_id={place_id}"
            GEOCODE_CACHE[jp_query] = can_url
            return can_url
    except Exception as e:
        print(f"Error geocoding {jp_query}: {e}")
    
    fallback = f"https://www.google.com/maps/search/?api=1&query={q_enc}"
    GEOCODE_CACHE[jp_query] = fallback
    return fallback

# Map keyword in link label to Japanese search query
KEYWORD_TO_JP = [
    ("GiGO 秋葉原3號館", "GiGO 秋葉原3号館"),
    ("拍貼機", "GiGO 秋葉原3号館"),
    ("萬代扭蛋百貨店", "ガシャポンのデパート 秋葉原店"),
    ("秋葉原扭蛋會館", "秋葉原ガチャポン会館"),
    ("友都八喜", "ヨドバシカメラ マルチメディアAkiba"),
    ("壽司郎", "スシロー 秋葉原駅前店"),
    ("丸龜製麵", "丸亀製麺 アトレ秋葉原1"),
    ("CoCo壹番屋", "CoCo壱番屋 JR秋葉原駅昭和通り口店"),
    ("3D 巨貓", "クロス新宿ビジョン"),
    ("Cross Shinjuku", "クロス新宿ビジョン"),
    ("Gusto", "ガスト 新宿NOWAビル店"),
    ("LUMINE EST", "ルミネエスト新宿"),
    ("Hanamasa", "肉のハナマサ 浅草橋店"),
    ("肉之Hanamasa", "肉のハナマサ 浅草橋店"),
    ("松坂屋上野店", "松坂屋 上野店"),
    ("DEAN & DELUCA", "DEAN & DELUCA CAFE パルコヤ上野"),
    ("喫茶 トリコロール", "喫茶トリコロール 松坂屋上野店"),
    ("不忍池", "不忍池"),
    ("清水觀音堂", "清水観音堂"),
    ("兔屋", "うさぎや 上野"),
    ("すき家", "すき家 上野三丁目店"),
    ("國立西洋美術館", "国立西洋美術館"),
    ("宇奈とと", "名代 宇奈とと 上野店"),
    ("松屋 上野店", "松屋 上野店"),
    ("松屋 浅草橋店", "松屋 浅草橋店"),
    ("松屋 押上店", "松屋 押上店"),
    ("東京迪士尼樂園", "東京ディズニーランド"),
    ("美女與野獸", "美女と野獣“魔法のものがたり”"),
    ("小熊維尼", "プーさんのハニーハント"),
    ("巨雷山", "ビッグサンダー・マウンテン"),
    ("紅心皇后", "クイーン・オブ・ハートのバンケットホール"),
    ("廣場閣樓", "プラザパビリオン・レストラン"),
    ("明日樂園舞台", "トゥモローランド・テラス"),
    ("莎拉奶奶", "グランマ・サラのキッチン"),
    ("紅連火箭筒", "パン・ギャラクティック・ピザ・ポート"),
    ("東京車站丸之內站舍", "東京駅丸の内駅舎"),
    ("東京車站一番街", "東京駅一番街"),
    ("KITTE花園", "KITTEガーデン"),
    ("天丼てんや", "天丼てんや 八重洲店"),
    ("だし茶漬け", "だし茶漬け えん KITTE丸の内店"),
    ("燕子烤肉漢堡排", "つばめグリル 大丸東京店"),
    ("國立科學博物館", "国立科学博物館"),
    ("鴨 to 蔥", "らーめん 鴨to葱"),
    ("鴨to蔥", "らーめん 鴨to葱"),
    ("二木菓子", "二木の菓子 第一営業所"),
    ("OS Drug", "OSドラッグ 上野店"),
    ("肉之大山", "肉の大山 上野店"),
    ("みなとや", "みなとや食品 本店"),
    ("多慶屋", "多慶屋 TAKEYA 1"),
    ("三鷹之森吉卜力美術館", "三鷹の森ジブリ美術館"),
    ("吉卜力", "三鷹の森ジブリ美術館"),
    ("井之頭恩賜公園", "井の頭恩賜公園"),
    ("大戶屋", "大戸屋ごはん処 吉祥寺店"),
    ("花丸烏龍麵", "はなまるうどん 吉祥寺南口店"),
    ("吉祥寺 Sunroad", "吉祥寺サンロード商店街"),
    ("Loft", "吉祥寺ロフト"),
    ("無印良品", "無印良品 コピス吉祥寺"),
    ("大創", "DAISO 吉祥寺サンロード店"),
    ("哈莫尼卡橫丁", "ハーモニカ横丁"),
    ("SATOU", "吉祥寺 さとう"),
    ("串家物語", "串家物語 吉祥寺店"),
    ("一風堂 吉祥寺", "一風堂 吉祥寺店"),
    ("一風堂 晴空塔", "一風堂 東京ソラマチ店"),
    ("一風堂", "一風堂 吉祥寺店"),
    ("Linde 德國麵包", "ベッカライカフェ リンデ 吉祥寺本店"),
    ("Jyonetsu Bakery", "Jyonetsu Bakery 吉祥寺"),
    ("淺草寺", "浅草寺"),
    ("雷門", "雷門"),
    ("仲見世商店街", "仲見世商店街"),
    ("淺草文化觀光中心", "浅草文化観光センター"),
    ("東京晴空塔", "東京スカイツリー"),
    ("達摩文字燒", "月島名物もんじゃ だるま 東京スカイツリータウン・ソラマチ店"),
    ("利久牛舌", "牛たん炭焼 利久 東京ソラマチ店"),
    ("宮武讚岐烏龍麵", "宮武讃岐うどん 東京ソラマチ店"),
    ("墨田水族館", "すみだ水族館"),
    ("東京都廳", "東京都庁"),
    ("麥當勞", "マクドナルド 新宿西口店"),
    ("摩斯漢堡", "モスバーガー 新宿西口店"),
    ("築地場外市場", "築地場外市場"),
    ("築地山長", "つきぢ山長"),
    ("築地丸武", "丸武 築地本店"),
    ("波除稻荷神社", "波除神社"),
    ("海茵娜酒店", "変なホテル東京 浅草橋")
]

print("Prefetching canonical Google Maps URLs...")
CANONICAL_MAP = {}
for kw, jp_name in KEYWORD_TO_JP:
    url = get_canonical_url(jp_name)
    CANONICAL_MAP[kw] = url
    print(f"  ✓ {kw} -> {url}")

# Save full mapping to json
with open('/home/owen/tokyo/canonical_nav_map.json', 'w', encoding='utf-8') as f:
    json.dump(CANONICAL_MAP, f, ensure_ascii=False, indent=2)

print("\nUpdating 2026東京親子自由行_V10_Henna.md with canonical URLs...")
with open('/home/owen/tokyo/2026東京親子自由行_V10_Henna.md', 'r', encoding='utf-8') as f:
    v10_content = f.read()

def replace_md_link(match):
    label = match.group(1)
    old_url = match.group(2)
    # find best canonical URL
    for kw, jp in KEYWORD_TO_JP:
        if kw in label:
            return f"[{label}]({CANONICAL_MAP[kw]})"
    return f"[{label}]({old_url})"

v10_new = re.sub(r'\[(.*?)\]\((https?://maps\.app\.goo\.gl/[^\)]+|https?://share\.google/[^\)]+)\)', replace_md_link, v10_content)

with open('/home/owen/tokyo/2026東京親子自由行_V10_Henna.md', 'w', encoding='utf-8') as f:
    f.write(v10_new)

# Copy to README.md
with open('/home/owen/tokyo/README.md', 'w', encoding='utf-8') as f:
    f.write(v10_new)

print("Updated Markdown files!")
