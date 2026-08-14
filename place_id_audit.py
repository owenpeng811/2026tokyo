# -*- coding: utf-8 -*-
"""
Google Place ID 離線偽造偵測。

不需要 API key、不需要網路，靠結構性特徵找出捏造或張冠李戴的導航連結。
起因：2026-08 稽核發現大量偽造 Place ID，而驗證管線的 HTTP 200 檢查完全抓不到
（Google 對任何 place_id 都回 200，然後靜默退回用座標定位）。

可獨立執行：  python3 place_id_audit.py
也可被匯入：  from place_id_audit import audit_files, format_report
"""

import json
import os
import re
from collections import defaultdict
from datetime import date

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# 日本本土概略範圍（含沖繩與北海道），用來抓「座標跑到國外」
JP_LAT = (24.0, 46.0)
JP_LNG = (122.0, 154.0)

# Place ID 允許的字元集（Google 使用 base64url 變體）
PLACE_ID_RE = re.compile(r'^[A-Za-z0-9_-]{20,}$')

URL_RE = re.compile(
    r'https://www\.google\.com/maps/search/\?api=1&query=([^&\s\)"\']+)'
    r'(?:&query_place_id=([A-Za-z0-9_-]+))?'
)

# 這些標籤天生共用同一座標／Place ID（同棟大樓、同車站的不同出入口），不算異常
SHARED_OK = (
    '淺草橋站', '浅草橋駅', '松坂屋', 'PARCO_ya', 'DEAN & DELUCA',
    'DiverCity', 'ダイバーシティ', '東京迪士尼樂園', '東京ディズニーランド',
    '晴空街道', '東京ソラマチ', '羽田機場', '羽田空港', '吉豚屋', 'かつや',
    # 同一車站的多個別名／出入口，本來就共用座標
    '秋葉原站', '秋葉原駅', '多慶屋', 'TAKEYA',
    # 劇場與在該劇場上演的節目，共用場館座標屬正常
    '劇院', '劇場', 'シアター',
)


def _load_sources():
    """回傳 [(來源檔名, 標籤, 網址), ...]，涵蓋 README 與所有導航字典。"""
    out = []

    readme = os.path.join(BASE_DIR, 'README.md')
    if os.path.exists(readme):
        with open(readme, encoding='utf-8') as f:
            text = f.read()
        for label, url in re.findall(
                r'\[\*{0,2}([^\]]+?)\*{0,2}\]\((https://www\.google\.com/maps[^)]+)\)', text):
            out.append(('README.md', label.strip(), url))

    for name in ('navigation_links_dict.json', 'first_destinations.json', 'canonical_nav_map.json'):
        path = os.path.join(BASE_DIR, name)
        if not os.path.exists(path):
            continue
        with open(path, encoding='utf-8') as f:
            data = json.load(f)
        for k, v in data.items():
            if isinstance(v, str) and 'google.com/maps' in v:
                out.append((name, k, v))

    path = os.path.join(BASE_DIR, 'text_entities.json')
    if os.path.exists(path):
        with open(path, encoding='utf-8') as f:
            for pair in json.load(f):
                if len(pair) == 2 and 'google.com/maps' in pair[1]:
                    out.append(('text_entities.json', pair[0], pair[1]))

    html = os.path.join(BASE_DIR, 'navigation_links.html')
    if os.path.exists(html):
        with open(html, encoding='utf-8') as f:
            content = f.read()
        for label, url in re.findall(
                r'<td><strong>(.*?)</strong></td>\s*<td><input[^>]*value="([^"]+)"', content):
            out.append(('navigation_links.html', label, url))

    return out


def _parse(url):
    """從網址取出 (lat, lng, place_id)；純店名查詢者座標為 None。"""
    m = URL_RE.search(url)
    if not m:
        return None, None, None
    query, pid = m.group(1), m.group(2)
    lat = lng = None
    if ',' in query:
        try:
            a, b = query.split(',', 1)
            lat, lng = float(a), float(b)
        except ValueError:
            pass
    return lat, lng, pid


def _shared_ok(labels):
    """同一組標籤是否屬於「本來就該共用」的情況。"""
    joined = ' '.join(labels)
    return any(tok in joined for tok in SHARED_OK)


def _close_ids(a, b):
    """兩個等長 Place ID 是否僅差 1~2 個字元（序列偽造特徵）。"""
    if len(a) != len(b) or a == b:
        return False
    diff = sum(1 for x, y in zip(a, b) if x != y)
    return diff <= 2


def audit_files():
    """執行全部規則，回傳 (問題清單, 掃描筆數)。"""
    rows = _load_sources()
    issues = []

    by_pid = defaultdict(set)         # place_id -> {標籤}
    by_pid_coords = defaultdict(set)  # place_id -> {(緯度, 經度)}
    by_lng = defaultdict(set)         # 經度 -> {(緯度, 標籤)}
    by_lat = defaultdict(set)

    for src, label, url in rows:
        lat, lng, pid = _parse(url)

        if pid:
            by_pid[pid].add(label)
            # R0：格式檢查
            if not PLACE_ID_RE.match(pid):
                issues.append(('R0 格式異常', f'{label}（{src}）', f'place_id 不符合格式：{pid}'))

        if lat is not None and lng is not None:
            # R4：座標跑出日本
            if not (JP_LAT[0] <= lat <= JP_LAT[1] and JP_LNG[0] <= lng <= JP_LNG[1]):
                issues.append(('R4 座標不在日本', f'{label}（{src}）', f'{lat},{lng}'))
            by_lng[lng].add((lat, label))
            by_lat[lat].add((lng, label))
            if pid:
                by_pid_coords[pid].add((lat, lng))

    # R1：同一經度配上 3 個以上不同緯度（或反之）＝ 座標複製貼上
    for lng, pairs in by_lng.items():
        lats = {p[0] for p in pairs}
        labels = [p[1] for p in pairs]
        if len(lats) >= 3 and not _shared_ok(labels):
            issues.append(('R1 座標疑似複製', f'經度 {lng}',
                           f'{len(lats)} 個不同緯度共用此經度：' + '、'.join(sorted(set(labels))[:6])))
    for lat, pairs in by_lat.items():
        lngs = {p[0] for p in pairs}
        labels = [p[1] for p in pairs]
        if len(lngs) >= 3 and not _shared_ok(labels):
            issues.append(('R1 座標疑似複製', f'緯度 {lat}',
                           f'{len(lngs)} 個不同經度共用此緯度：' + '、'.join(sorted(set(labels))[:6])))

    # R2：Place ID 尾碼僅差 1~2 字元的群組 ＝ 手動遞增偽造
    pids = sorted(by_pid)
    seen = set()
    for i, a in enumerate(pids):
        if a in seen:
            continue
        group = [a]
        for b in pids[i + 1:]:
            if _close_ids(a, b):
                group.append(b)
        if len(group) >= 2:
            seen.update(group)
            names = [f'{g} → ' + '／'.join(sorted(by_pid[g])[:2]) for g in group]
            issues.append(('R2 ID 疑似序列偽造', f'{len(group)} 個相近 ID', '｜'.join(names)))

    # R3：同一個 Place ID 卻標了相距過遠的座標 ＝ 資料自相矛盾（張冠李戴）
    #     只比座標不比字面，避免「Hanamasa vs 肉のハナマサ」這類跨語言別名被誤判。
    FAR = 0.005  # 約 500 公尺
    for pid, coords in by_pid_coords.items():
        pts = sorted(coords)
        if len(pts) < 2:
            continue
        lats = [p[0] for p in pts]
        lngs = [p[1] for p in pts]
        if (max(lats) - min(lats)) > FAR or (max(lngs) - min(lngs)) > FAR:
            issues.append((
                'R3 ID 座標自相矛盾', pid,
                f'同一 Place ID 標到相距過遠的座標：{pts[0]} 與 {pts[-1]}｜'
                '共用者：' + '、'.join(sorted(by_pid[pid])[:6])))

    # R5：places.json 若存在，檢查驗證日期是否過期（Google 官方建議 12 個月）
    places = os.path.join(BASE_DIR, 'places.json')
    if os.path.exists(places):
        with open(places, encoding='utf-8') as f:
            data = json.load(f)
        today = date.today()
        stale = []
        for label, rec in data.get('places', {}).items():
            v = rec.get('verified_at')
            if not v:
                stale.append(f'{label}（未記錄）')
                continue
            try:
                y, m, d = (int(x) for x in v.split('-'))
                if (today - date(y, m, d)).days > 365:
                    stale.append(f'{label}（{v}）')
            except ValueError:
                stale.append(f'{label}（日期格式錯誤 {v}）')
        if stale:
            issues.append(('R5 驗證已逾期', f'{len(stale)} 筆超過 12 個月',
                           '、'.join(stale[:8]) + ('…' if len(stale) > 8 else '')))

        # R6：查證地址沒有番地門牌 ＝ 疑似被降級成行政區（町名）而非商家 POI
        #     成因：用 Geocoding 而非 Places Text Search 查詢，遇到「店名≒町名」會靜默降級。
        #     只檢查有記錄 verified_address 的條目；沒記錄者無從判斷，略過。
        degraded = []
        for label, rec in data.get('places', {}).items():
            addr = rec.get('verified_address')
            if not addr:
                continue
            # 已誠實宣告 poi_level=container 者豁免：它本來就只能導到建物／園區層級
            if rec.get('poi_level') == 'container':
                continue
            # 先移除郵遞區號（〒123-4567 或裸的 123-4567），再看還有沒有數字
            stripped = re.sub(r'〒?\d{3}-\d{4}', '', addr)
            if not re.search(r'\d', stripped):
                degraded.append(f'{label}（{addr}）')
        if degraded:
            issues.append((
                'R6 疑似降級為行政區', f'{len(degraded)} 筆地址無番地門牌',
                '這通常代表查到的是町名而非店家，請改用 Places Text Search 重查；'
                '若該地點在 Google 上確實沒有獨立 POI，請宣告 poi_level="container"：'
                + '、'.join(degraded[:6]) + ('…' if len(degraded) > 6 else '')))

        # R7：verified_* 欄位出現人工填寫的痕跡 ＝ 佐證造假
        #     這兩個欄位必須是 API 原封不動的回傳值，手寫會讓離線稽核完全失去意義。
        FAKE_MARKERS = ('fallback', 'manual', '手動', '手工', 'unknown',
                        'n/a', 'tbd', 'placeholder', '暫定')
        faked = []
        for label, rec in data.get('places', {}).items():
            blob = f"{rec.get('verified_name') or ''} {rec.get('verified_address') or ''}".lower()
            if any(m in blob for m in FAKE_MARKERS):
                faked.append(f'{label}（{rec.get("verified_name")}）')
        if faked:
            issues.append((
                'R7 佐證欄位疑似人工填寫', f'{len(faked)} 筆',
                'verified_name／verified_address 必須是 API 原始回傳值、不可手寫；'
                '若該地點沒有獨立 POI，正確做法是宣告 poi_level="container" 並保留容器的真實回傳值：'
                + '、'.join(faked[:6]) + ('…' if len(faked) > 6 else '')))

    return issues, len(rows)


def format_report(issues, total):
    lines = [f'掃描 {total} 筆導航連結（README 與全部字典檔）']
    if not issues:
        lines.append('✅ 偽造偵測 8 項規則全數通過，未發現可疑的 Place ID 或座標。')
        return '\n'.join(lines)
    lines.append(f'❌ 發現 {len(issues)} 項可疑：')
    for rule, subject, detail in issues:
        lines.append(f'  [{rule}] {subject}')
        lines.append(f'      {detail}')
    return '\n'.join(lines)


if __name__ == '__main__':
    import sys
    found, count = audit_files()
    print(format_report(found, count))
    sys.exit(1 if found else 0)
