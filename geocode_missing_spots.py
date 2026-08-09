import json, urllib.request, urllib.parse

with open('/home/owen/.gemini/config/mcp_config.json') as f:
    cfg = json.load(f)
api_key = cfg['mcpServers']['google-maps']['env']['GOOGLE_MAPS_API_KEY']

with open('/home/owen/tokyo/navigation_links_dict.json', 'r', encoding='utf-8') as f:
    nav_dict = json.load(f)

MISSING = [
    ("吉野家 (吉野家 浅草橋店)", "吉野家 浅草橋店"),
    ("吉野家 浅草橋店", "吉野家 浅草橋店"),
    ("吉野家", "吉野家 浅草橋店"),
    ("松屋 (松屋 浅草橋店)", "松屋 浅草橋店"),
    ("松屋 浅草橋店", "松屋 浅草橋店"),
    ("拉麵 ろく月 (らーめん ろく月)", "らーめん ろく月"),
    ("拉麵 ろく月", "らーめん ろく月"),
    ("ろく月 雞白湯拉麵", "らーめん ろく月"),
    ("ろく月", "らーめん ろく月"),
    ("Cow Cow Kitchen (東京Milk Cheese Factory)", "東京ミルクチーズ工場 ルミネエスト新宿店"),
    ("Cow Cow Kitchen", "東京ミルクチーズ工場 ルミネエスト新宿店"),
    ("喫茶 Tricolore", "喫茶トリコロール 松坂屋上野店"),
    ("喫茶トリコロール", "喫茶トリコロール 松坂屋上野店"),
    ("燕子烤肉漢堡排 (つばめグリル 大丸東京店)", "つばめグリル 大丸東京店"),
    ("燕子烤肉漢堡排", "つばめグリル 大丸東京店"),
    ("だし茶漬け えん KITTE丸の内店", "だし茶漬け えん KITTE丸の内店"),
    ("だし茶漬け えん", "だし茶漬け えん KITTE丸の内店"),
    ("利久牛舌 (牛たん炭焼 利久 東京ソラマチ店)", "牛たん炭焼 利久 東京ソラマチ店"),
    ("利久牛舌 晴空塔店", "牛たん炭焼 利久 東京ソラマチ店"),
    ("利久牛舌", "牛たん炭焼 利久 東京ソラマチ店"),
    ("宮武讚岐烏龍麵 (宮武讃岐うどん 東京ソラマチ店)", "宮武讃岐うどん 東京ソラマチ店"),
    ("宮武讚岐烏龍麵", "宮武讃岐うどん 東京ソラマチ店"),
    ("一風堂 (一風堂 東京ソラマチ店)", "一風堂 東京ソラマチ店"),
    ("一風堂 晴空塔店", "一風堂 東京ソラマチ店"),
    ("一風堂 (一風堂 吉祥寺店)", "一風堂 吉祥寺店"),
    ("一風堂 吉祥寺店", "一風堂 吉祥寺店"),
    ("一風堂", "一風堂 吉祥寺店"),
    ("花丸烏龍麵 (はなまるうどん 吉祥寺南口店)", "はなまるうどん 吉祥寺南口店"),
    ("花丸烏龍麵 吉祥寺南口店", "はなまるうどん 吉祥寺南口店"),
    ("花丸烏龍麵", "はなまるうどん 吉祥寺南口店"),
    ("大戶屋 (大戸屋ごはん処 吉祥寺店)", "大戸屋ごはん処 吉祥寺店"),
    ("大戶屋 吉祥寺店", "大戸屋ごはん処 吉祥寺店"),
    ("大戶屋", "大戸屋ごはん処 吉祥寺店"),
    ("串家物語 (神楽食堂 串家物語 吉祥寺店)", "串家物語 吉祥寺店"),
    ("串家物語 吉祥寺店", "串家物語 吉祥寺店"),
    ("串家物語", "串家物語 吉祥寺店")
]

for label, jp_query in MISSING:
    if label in nav_dict:
        continue
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
            nav_dict[label] = can_url
            print(f"✓ Geocoded: {label} -> {can_url}")
        else:
            nav_dict[label] = f"https://www.google.com/maps/search/?api=1&query={q_enc}"
    except Exception as e:
        nav_dict[label] = f"https://www.google.com/maps/search/?api=1&query={q_enc}"

with open('/home/owen/tokyo/navigation_links_dict.json', 'w', encoding='utf-8') as f:
    json.dump(nav_dict, f, ensure_ascii=False, indent=2)

print(f"Updated navigation_links_dict.json with total {len(nav_dict)} entries!")
