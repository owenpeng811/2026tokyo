# -*- coding: utf-8 -*-
"""
places.json 單一真相來源的同步工具。

背景：同一個地點的導航網址原本散落在 5 個檔案，彼此無同步機制，
2026-08 稽核發現大量偽造 Place ID 與座標漂移。改為以 places.json 為唯一真相，
其餘字典檔一律由本工具生成，不再手工維護。

五個模式
  --bootstrap  由現有檔案彙整出 places.json（只需執行一次，之後別再用）
  --adopt      收編只存在於 README、尚未登錄的「孤兒連結」
  --generate   由 places.json 生成 navigation_links.html 與三個字典 JSON
  --check      掃描 README.md 內文網址，列出與 places.json 不符者
  --fix        直接改寫 README.md 中不符的網址

⚠️ README.md 由 Docsify 直接渲染，必須保持完成品、不能使用佔位符，
   因此 README 只能「被檢查／被修正」，不能被生成。
"""

import json
import os
import re
import sys
from datetime import date

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PLACES = os.path.join(BASE_DIR, 'places.json')

NAV_DICT = os.path.join(BASE_DIR, 'navigation_links_dict.json')
FIRST_DEST = os.path.join(BASE_DIR, 'first_destinations.json')
TEXT_ENT = os.path.join(BASE_DIR, 'text_entities.json')
CANONICAL = os.path.join(BASE_DIR, 'canonical_nav_map.json')
NAV_HTML = os.path.join(BASE_DIR, 'navigation_links.html')
README = os.path.join(BASE_DIR, 'README.md')

MAPS_LINK_RE = re.compile(r'\[(\*{0,2})([^\]]+?)\1\]\((https://www\.google\.com/maps[^)]+)\)')


def _read_json(path, default):
    if not os.path.exists(path):
        return default
    with open(path, encoding='utf-8') as f:
        return json.load(f)


def _write_json(path, data):
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        f.write('\n')


def _canonical_label(labels):
    """從同一組別名中挑出主標籤：優先取含括號日文名者，其次取最長。"""
    with_paren = [x for x in labels if '(' in x or '（' in x]
    pool = with_paren or list(labels)
    return sorted(pool, key=lambda s: (-len(s), s))[0]


def bootstrap():
    """把現有來源彙整成 places.json。

    以網址分組視為同一地點，但**精確保留每個檔案原本的鍵名**，
    生成時可 100% 還原，不做跨檔合併（跨檔合併會讓 text_entities 之類的清單暴增）。
    """
    by_url = {}
    conflicts = []

    def add(url, field, key):
        rec = by_url.setdefault(url, {'nav_dict': set(), 'text_entities': set(),
                                      'first_dest': set(), 'html': set()})
        rec[field].add(key)

    seen = {}  # (field, key) -> url，用來偵測同一鍵在同一檔案指向不同網址

    def track(field, key, url):
        prev = seen.get((field, key))
        if prev and prev != url:
            conflicts.append((field, key, prev, url))
        seen[(field, key)] = url

    for label, url in _read_json(NAV_DICT, {}).items():
        add(url, 'nav_dict', label)
        track('nav_dict', label, url)
    for key, url in _read_json(FIRST_DEST, {}).items():
        add(url, 'first_dest', key)
        track('first_dest', key, url)
    for pair in _read_json(TEXT_ENT, []):
        if len(pair) == 2:
            add(pair[1], 'text_entities', pair[0])
            track('text_entities', pair[0], pair[1])
    if os.path.exists(NAV_HTML):
        with open(NAV_HTML, encoding='utf-8') as f:
            html = f.read()
        for label, url in re.findall(
                r'<td><strong>(.*?)</strong></td>\s*<td><input[^>]*value="([^"]+)"', html):
            add(url, 'html', label)
            track('html', label, url)
    # canonical_nav_map.json 只是舊的校準參考，不再生成，僅用來補主標籤名稱
    canon_labels = {}
    for label, url in _read_json(CANONICAL, {}).items():
        canon_labels.setdefault(url, label)

    today = date.today().isoformat()
    places = {}
    for url, rec in by_url.items():
        all_labels = rec['nav_dict'] | rec['html'] | rec['text_entities']
        if not all_labels:
            all_labels = {canon_labels.get(url, url[:40])}
        main = _canonical_label(all_labels)
        while main in places:
            main += '＋'
        places[main] = {
            'url': url,
            'nav_dict': sorted(rec['nav_dict']),
            'text_entities': sorted(rec['text_entities']),
            'first_dest': sorted(rec['first_dest']),
            'html': sorted(rec['html']),
            'verified_at': today,
        }

    _write_json(PLACES, {
        'schema': 2,
        'note': ('唯一真相來源。修改地點只改這裡，再執行 python3 sync_places.py --generate。'
                 'nav_dict／text_entities／first_dest／html 四個欄位記錄該地點在各衍生檔中的鍵名。'),
        'places': dict(sorted(places.items())),
    })
    print(f'✅ 已建立 places.json，共 {len(places)} 個地點')
    if conflicts:
        print(f'⚠️ 發現 {len(conflicts)} 組同鍵不同網址的衝突，已各自獨立成筆，請人工確認：')
        for field, key, a, b in conflicts[:10]:
            print(f'  [{field}] {key}\n      {a}\n      {b}')


def adopt():
    """把只存在於 README、尚未登錄 places.json 的「孤兒連結」收編進來。

    這類連結過去完全在管理之外：稽核規則因為找不到同伴而抓不到它們，
    `--check` 也因為查無標籤而略過。收編後即納入單一真相來源。
    """
    data = _read_json(PLACES, None)
    if not data:
        sys.exit('❌ 找不到 places.json，請先執行 --bootstrap')
    places = data['places']

    known = set()
    for rec in places.values():
        known.update(rec.get('nav_dict', []))
        known.update(rec.get('html', []))
        known.update(rec.get('text_entities', []))

    with open(README, encoding='utf-8') as f:
        text = f.read()

    added = []
    for _, label, url in MAPS_LINK_RE.findall(text):
        label = label.strip()
        if label in known or label in places:
            continue
        known.add(label)
        places[label] = {
            'url': url,
            'nav_dict': [label],
            'text_entities': [],
            'first_dest': [],
            'html': [label],
            'verified_at': date.today().isoformat(),
        }
        added.append(label)

    if not added:
        print('✅ 沒有孤兒連結，README 的地點皆已登錄於 places.json')
        return 0

    data['places'] = dict(sorted(places.items()))
    _write_json(PLACES, data)
    print(f'✅ 已收編 {len(added)} 個孤兒連結進 places.json：')
    for a in added:
        print(f'  • {a}')
    print('\n⚠️ 收編只是納管，並未驗證這些 Place ID 是否真實有效；'
          '請以 Place ID Finder 逐一查證後更新 verified_at。')
    print('接著執行 python3 sync_places.py --generate')
    return 0


def _load_places():
    data = _read_json(PLACES, None)
    if not data:
        sys.exit('❌ 找不到 places.json，請先執行 python3 sync_places.py --bootstrap')
    return data['places']


def generate():
    """由 places.json 生成全部衍生檔。"""
    places = _load_places()

    nav_dict, text_entities, first_dest, html_rows = {}, [], {}, []
    for rec in places.values():
        url = rec['url']
        for n in rec.get('nav_dict', []):
            nav_dict[n] = url
        for n in rec.get('text_entities', []):
            text_entities.append([n, url])
        for key in rec.get('first_dest', []):
            first_dest[key] = url
        for n in rec.get('html', []):
            html_rows.append((n, url))

    _write_json(NAV_DICT, dict(sorted(nav_dict.items())))
    _write_json(FIRST_DEST, first_dest)
    _write_json(TEXT_ENT, sorted(text_entities, key=lambda p: -len(p[0])))

    rows_html = '\n'.join(
        '        <tr>\n'
        f'      <td><strong>{label}</strong></td>\n'
        f'      <td><input type="text" class="link-input" value="{url}" readonly onclick="this.select()"></td>\n'
        f'      <td><a href="{url}" target="_blank" class="btn-preview">🔗 開啟地圖</a></td>\n'
        '    </tr>'
        for label, url in sorted(set(html_rows))
    )
    with open(NAV_HTML, 'w', encoding='utf-8') as f:
        f.write(_HTML_TEMPLATE.format(count=len(set(html_rows)),
                                      generated=date.today().isoformat(), rows=rows_html))

    print(f'✅ 已生成 navigation_links_dict.json（{len(nav_dict)} 筆）、'
          f'first_destinations.json（{len(first_dest)} 筆）、'
          f'text_entities.json（{len(text_entities)} 筆）、'
          f'navigation_links.html（{len(set(html_rows))} 列）')


def _readme_mismatches():
    """回傳 README 中與 places.json 不符的連結 [(標籤, 現有網址, 應為網址)]。"""
    places = _load_places()
    lookup = {}
    for rec in places.values():
        for n in rec.get('nav_dict', []) + rec.get('html', []):
            lookup.setdefault(n, rec['url'])

    with open(README, encoding='utf-8') as f:
        text = f.read()

    bad = []
    for _, label, url in MAPS_LINK_RE.findall(text):
        label = label.strip()
        want = lookup.get(label)
        if want and want != url:
            bad.append((label, url, want))
    return bad


def check():
    bad = _readme_mismatches()
    if not bad:
        print('✅ README.md 的導航連結與 places.json 完全一致')
        return 0
    print(f'❌ README.md 有 {len(bad)} 個連結與 places.json 不符：')
    for label, url, want in bad:
        print(f'  • {label}\n      現有：{url}\n      應為：{want}')
    print('\n執行 python3 sync_places.py --fix 可自動修正。')
    return 1


def fix():
    bad = _readme_mismatches()
    if not bad:
        print('✅ README.md 無需修正')
        return 0
    with open(README, encoding='utf-8') as f:
        text = f.read()
    for _, url, want in bad:
        text = text.replace(url, want)
    with open(README, 'w', encoding='utf-8') as f:
        f.write(text)
    print(f'✅ 已修正 README.md 中 {len(bad)} 個連結（請重新執行 build_pwa.py）')
    return 0


_HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="zh-TW">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>2026 東京行程 導航連結對照基準表</title>
  <style>
    body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
           background-color: #0f172a; color: #f8fafc; padding: 24px 16px; margin: 0; }}
    .container {{ max-width: 960px; margin: 0 auto; }}
    h1 {{ font-size: 1.5rem; color: #38bdf8; margin-bottom: 8px; }}
    p.desc {{ color: #94a3b8; font-size: 0.9rem; margin-bottom: 20px; line-height: 1.6; }}
    table {{ width: 100%; border-collapse: collapse; background: #1e293b; border-radius: 12px;
            overflow: hidden; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.2); }}
    th, td {{ padding: 12px 14px; text-align: left; border-bottom: 1px solid #334155; }}
    th {{ background: #334155; color: #e2e8f0; font-size: 0.85rem; }}
    .link-input {{ width: 100%; background: #0f172a; color: #cbd5e1; border: 1px solid #334155;
                  border-radius: 6px; padding: 6px 8px; font-size: 0.78rem; }}
    .btn-preview {{ display: inline-block; background: #38bdf8; color: #0f172a; padding: 6px 12px;
                   border-radius: 6px; text-decoration: none; font-size: 0.82rem;
                   font-weight: 600; white-space: nowrap; }}
  </style>
</head>
<body>
  <div class="container">
    <h1>2026 東京行程 導航連結對照基準表</h1>
    <p class="desc">
      ⚠️ 本頁由 <code>sync_places.py --generate</code> 自動生成，共 {count} 列，最後生成日 {generated}。<br>
      請勿直接編輯本檔，任何修改都會在下次生成時被覆蓋；要改連結請編輯 <code>places.json</code>。
    </p>
    <table>
      <tr><th>網頁行程標籤文字</th><th>導航網址</th><th>預覽</th></tr>
{rows}
    </table>
  </div>
</body>
</html>
"""


if __name__ == '__main__':
    mode = sys.argv[1] if len(sys.argv) > 1 else ''
    if mode == '--bootstrap':
        bootstrap()
    elif mode == '--generate':
        generate()
    elif mode == '--adopt':
        sys.exit(adopt())
    elif mode == '--check':
        sys.exit(check())
    elif mode == '--fix':
        sys.exit(fix())
    else:
        print(__doc__)
        sys.exit(2)
