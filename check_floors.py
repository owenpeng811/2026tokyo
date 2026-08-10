import json, urllib.request, urllib.parse

with open('/home/owen/.gemini/config/mcp_config.json') as f:
    cfg = json.load(f)
api_key = cfg['mcpServers']['google-maps']['env']['GOOGLE_MAPS_API_KEY']

PLACES = [
    "ガシャポンのデパート 秋葉原店",
    "スシロー 秋葉原駅前店",
    "丸亀製麺 秋葉原店",
    "CoCo壱番屋 JR秋葉原駅昭和通り口店",
    "ガスト 新宿NOWAビル店",
    "ルミネエスト新宿 7&8 DINER",
    "喫茶トリコロール 松坂屋上野店",
    "大戸屋ごはん処 吉祥寺店",
    "串家物語 吉祥寺店",
    "はなまるうどん 吉祥寺南口店",
    "一風堂 吉祥寺店",
    "黒毛和牛専門店 さとう 吉祥寺店",
    "東京ミルクチーズ工場 ルミネエスト新宿店",
    "GiGO 秋葉原3号館",
    "天丼てんや 八重洲店",
    "だし茶漬け えん KITTE丸の内店",
    "つばめグリル 大丸東京店",
    "月島名物もんじゃ だるま 東京スカイツリータウン・ソラマチ店",
    "牛たん炭焼 利久 東京ソラマチ店",
    "宮武讃岐うどん 東京ソラマチ店",
    "一風堂 東京ソラマチ店",
    "マクドナルド 新宿西口店",
    "モスバーガー 新宿西口店"
]

for p in PLACES:
    q_enc = urllib.parse.quote(p)
    url = f"https://maps.googleapis.com/maps/api/place/findplacefromtext/json?input={q_enc}&inputtype=textquery&fields=name,formatted_address,place_id&language=ja&key={api_key}"
    try:
        req = urllib.request.urlopen(url, timeout=5)
        res = json.loads(req.read().decode('utf-8'))
        cands = res.get('candidates', [])
        if cands:
            c = cands[0]
            print(f"[{p}] -> {c.get('name')} | {c.get('formatted_address')}")
        else:
            print(f"[{p}] -> No candidate found")
    except Exception as e:
        print(f"[{p}] -> Error: {e}")
