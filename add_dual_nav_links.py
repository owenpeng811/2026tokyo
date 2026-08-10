import re

new_bus_line = """  * **乘車地點**：出園剪票口後往右前方步行約 2 分鐘，至迪士尼樂園正門外「東巴士總站東面（Bus Terminal East）」[**東京迪士尼樂園東巴士總站 1 號站牌 (東京ディズニーランド・バスターミナル・イースト 1番のりば)**](https://www.google.com/maps/search/?api=1&query=35.6364946,139.8807661&query_place_id=ChIJ3w8y8xN9GGARe5_gvaqDCMo)（[短網址備用導航 🔗](https://maps.app.goo.gl/EkzBtj7Q6RDJCh2C6)；地面與立柱有明顯標示「1番：秋葉原駅行」；可參考 [巴士總站設施與動線介紹文](https://secure.j-bus.co.jp/busrepo/2025/06/23/post-32156/)）。  
    ![東京迪士尼樂園東巴士總站 1 號公車站牌](https://secure.j-bus.co.jp/busrepo/wp-content/uploads/2025/06/IMG20250513080949-1024x768.jpg)"""

for fname in ['README.md', '2026東京親子自由行_V10_Henna.md']:
    fpath = f'/home/owen/tokyo/{fname}'
    with open(fpath, 'r', encoding='utf-8') as f:
        content = f.read()

    content = re.sub(
        r'  \* \*\*乘車地點\*\*：出園剪票口後往右前方步行約 2 分鐘.*?\!\[東京迪士尼樂園東巴士總站 1 號公車站牌\]\(https://secure\.j-bus\.co\.jp/busrepo/wp-content/uploads/2025/06/IMG20250513080949-1024x768\.jpg\)',
        new_bus_line,
        content,
        flags=re.DOTALL
    )

    with open(fpath, 'w', encoding='utf-8') as f:
        f.write(content)

print("Dual navigation links (Place ID URL + maps.app.goo.gl shortlink) added successfully!")
