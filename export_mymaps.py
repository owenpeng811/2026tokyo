# -*- coding: utf-8 -*-
"""
把行程表的導航點分天匯出成 CSV，供 Google My Maps 匯入（每天一個圖層）。

⚠️ 重要：My Maps **不吃 Place ID**，它只用「經緯度」或「名稱／地址地理編碼」定位。
   因此本工具輸出經緯度欄位；少數只有名稱查詢、沒有座標的地點，
   請改用「定位用名稱」欄讓 My Maps 自行地理編碼。

用法
  python3 export_mymaps.py            # 產生 exports/Day1.csv ~ Day6.csv
  python3 export_mymaps.py --merged   # 另外產生含全部天數的 exports/All.csv

My Maps 匯入步驟見 BUILD.md。
"""

import csv
import os
import re
import sys

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
README = os.path.join(BASE_DIR, 'README.md')
OUT_DIR = os.path.join(BASE_DIR, 'exports')

DAY_RE = re.compile(r'^## \*\*📅 (Day \d)（([^）]+)）：(.+?)\*\*')
SLOT_RE = re.compile(r'^#{3,4} \*\*(.+?)\*\*')
LINK_RE = re.compile(
    r'\[\*{0,2}([^\]]+?)\*{0,2}\]\((https://www\.google\.com/maps/search/\?api=1&query=[^)]+)\)')

# 類別判斷用關鍵字
TRANSPORT = ('站 (', '駅)', '車站', '機場', '空港', 'バスターミナル', '巴士總站', '公車站', '月台')
STAY = ('酒店', 'ホテル', '飯店')
SHOP = ('商店街', '橫丁', '横丁', '百貨', '藥妝', 'マツモトキヨシ', 'Loft', 'ロフト', '無印', '大創', 'DAISO',
        '唐吉訶德', '友都八喜', 'BicCamera', '多慶屋', '二木', '市場', 'Sunroad', 'サンロード',
        'GRANSTA', 'グランスタ', '菓子樂園', 'おかしランド', '扭蛋', 'ガシャポン', 'THANK YOU MART',
        'サンキューマート', 'Dream Market', 'ドリームマーケット', 'DiverCity', 'ダイバーシティ',
        'PARCO', '松坂屋', 'KITTE', 'コピス', 'Coppice', '晴空街道', 'ソラマチ', 'ROUND1', 'GiGO')
MEAL_SLOT = ('早餐', '午餐', '晚餐', '下午茶', '宵夜', '點心', '基地營')
MEAL_PREFIX = ('首選餐廳', '備案餐廳', '次備案餐廳', '首選店家', '備選店家')
# 店名本身就看得出是吃的（用於不在用餐時段、但屬小吃甜點的店家）
FOOD_NAME = ('たい焼き', 'たい菓子', '鯛魚燒', '和菓子', '最中', 'もなか', '玉子焼', '玉子燒',
             '拉麵', 'ラーメン', '烏龍麵', 'うどん', '蕎麥', 'そば', '咖啡', '珈琲', 'コーヒー',
             '銅鑼燒', 'うさぎや', '文字燒', 'もんじゃ', '壽司', '寿司', '牛丼', '天丼', '鰻',
             'メンチカツ', '炸牛肉', 'ベーカリー', 'パン', '麵包')

ICON = {
    'restaurant': '🍜 餐廳',
    'transport': '🚉 交通',
    'stay': '🏨 住宿',
    'shopping': '🛍️ 購物',
    'sight': '⛩️ 景點',
}


def classify(label, slot_title, line):
    """判斷類別。餐廳優先由『行首標記』與『時段名稱』判定，避免餐廳被誤分為購物。"""
    if any(p in line for p in MEAL_PREFIX):
        return 'restaurant'
    if any(k in label for k in STAY):
        return 'stay'
    if any(k in label for k in TRANSPORT):
        return 'transport'
    if any(k in slot_title for k in MEAL_SLOT):
        return 'restaurant'
    if any(k in label for k in SHOP):
        return 'shopping'
    if any(k in label for k in FOOD_NAME):
        return 'restaurant'
    return 'sight'


def split_label(label):
    """把『中文名 (官方日文名)』拆成兩欄。"""
    m = re.match(r'^(.*?)\s*[（(]([^（()]+)[)）]\s*$', label)
    if m:
        return m.group(1).strip(), m.group(2).strip()
    return label.strip(), ''


def parse():
    with open(README, encoding='utf-8') as f:
        lines = f.read().split('\n')

    days, cur, slot = [], None, ''
    for line in lines:
        m = DAY_RE.match(line)
        if m:
            # 同一天可能有多個區塊（Day 2 分長輩組／親子組），取標題括號內的組別當後綴
            group = re.search(r'[（(]([^）)]{2,6}組)[）)]', m.group(3))
            cur = {'day': m.group(1), 'date': m.group(2),
                   'group': group.group(1) if group else '',
                   'rows': [], 'seen': set()}
            days.append(cur)
            slot = ''
            continue
        m = SLOT_RE.match(line)
        if m:
            slot = re.sub(r'\[|\]|\(https[^)]*\)|\*', '', m.group(1)).strip()
            continue
        if not cur:
            continue
        for label, url in LINK_RE.findall(line):
            label = label.strip()
            if label in cur['seen']:
                continue
            q = re.search(r'query=([^&]+)', url)
            query = q.group(1) if q else ''
            lat = lng = ''
            if ',' in query:
                try:
                    a, b = query.split(',', 1)
                    lat, lng = f'{float(a):.7f}', f'{float(b):.7f}'
                except ValueError:
                    lat = lng = ''
            zh, ja = split_label(label)
            cat = classify(label, slot, line)
            cur['seen'].add(label)
            cur['rows'].append({
                '名稱': f'{ICON[cat].split()[0]} {zh}',
                '類別': ICON[cat],
                '天數': cur['day'] + (f'（{cur["group"]}）' if cur['group'] else ''),
                '日期': cur['date'],
                '時段': slot,
                '緯度': lat,
                '經度': lng,
                '定位用名稱': ja or zh,
                '官方日文名': ja,
                '導航連結': url,
            })
    return days


FIELDS = ['名稱', '類別', '天數', '日期', '時段', '緯度', '經度', '定位用名稱', '官方日文名', '導航連結']


def write_csv(path, rows):
    # UTF-8 with BOM：My Maps 與 Excel 才能正確辨識中文
    with open(path, 'w', encoding='utf-8-sig', newline='') as f:
        w = csv.DictWriter(f, fieldnames=FIELDS)
        w.writeheader()
        w.writerows(rows)


def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    days = parse()
    if not days:
        sys.exit('❌ 沒有從 README.md 解析到任何 Day 區塊')

    all_rows = []
    print(f'{"檔案":<14}{"筆數":>4}   類別分佈')
    for d in days:
        rows = d['rows']
        all_rows.extend(rows)
        name = d['day'].replace(' ', '') + (f'_{d["group"]}' if d['group'] else '')
        path = os.path.join(OUT_DIR, f'{name}.csv')
        write_csv(path, rows)
        dist = {}
        for r in rows:
            dist[r['類別']] = dist.get(r['類別'], 0) + 1
        print(f'{os.path.basename(path):<14}{len(rows):>4}   '
              + '、'.join(f'{k}×{v}' for k, v in sorted(dist.items())))

    if '--merged' in sys.argv:
        write_csv(os.path.join(OUT_DIR, 'All.csv'), all_rows)
        print(f'{"All.csv":<14}{len(all_rows):>4}   （全部天數合併）')

    no_coord = sorted({r['名稱'] for r in all_rows if not r['緯度']})
    if no_coord:
        print(f'\n⚠️ {len(no_coord)} 筆沒有座標，匯入時請改選「定位用名稱」欄定位：')
        for n in no_coord:
            print(f'   • {n}')
    print(f'\n✅ 已輸出至 {OUT_DIR}/　My Maps 匯入步驟見 BUILD.md')


if __name__ == '__main__':
    main()
