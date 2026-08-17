#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
import os
import json
import urllib.parse

def clean_url(url):
    if not url:
        return ""
    u = url.strip()
    u = re.sub(r'[\)\>\*\]\,\.\s\"\']+$', '', u)
    return u

def clean_title(title_raw):
    t = re.sub(r'\[(.*?)\]\(.*?\)', r'\1', title_raw)
    t = re.sub(r'\([^\)]*maps[^\)]*\)', '', t)
    t = re.sub(r'^[#\s\*\-]+', '', t)
    t = t.replace('✈️', '').replace('🚇', '').replace('🏨', '').replace('🍽️', '').replace('🏃', '').replace('🦕', '').replace('🌳', '').replace('🚌', '').replace('📸', '').replace('🍜', '').replace('🍪', '').replace('🛒', '').replace('⛪', '').replace('🌅', '').replace('🪙', '').replace('🎮', '').replace('🥞', '').replace('🍔', '').replace('🎡', '').replace('🏰', '').replace('🎢', '').replace('🎠', '').replace('🎆', '').replace('🛍️', '').replace('🚶‍♂️', '').replace('🐧', '').replace('🛬', '').replace('🧳', '').replace('🍳', '').replace('🌿', '').replace('☕', '').replace('🏛️', '').replace('🍩', '').replace('🐟', '').replace('🛫', '').replace('🏮', '').replace('🥩', '')
    t = re.sub(r'[\*\#]', '', t)
    return t.strip()

def get_category_info(title):
    t_lower = title.lower()
    if any(x in t_lower for x in ['餐', '食', '吃', '拉麵', '燒', '飲', '咖啡', '麵', '丼', '牛舌', '丸子', '甜點', '泡芙', '銅鑼燒', '炸牛肉丸', '壽司', '文字燒', '麥當勞', '摩斯', '大戶屋', '串家物語', 'すき家', '宇奈とと', '天丼', '玉子燒', '早午餐', '宵夜', '下午茶']):
        return 'food', '美食', '🍜'
    elif any(x in t_lower for x in ['車', '航', '抵達', '交通', '公車', '地鐵', '捷運', '飛機', '前往', '返回', '機場線', '京急', '總武線', '山手線', '電車', '出發', '回程']):
        return 'transport', '交通', '🚆'
    elif any(x in t_lower for x in ['飯店', '住宿', 'check', '入住', '海茵娜', '就寢', '睡覺', '退房', '行李']):
        return 'stay', '住宿', '🏨'
    else:
        return 'attraction', '景點', '⛩️'

# Load canonical map dictionary and entities
NAV_DICT_PATH = '/home/owen/tokyo/navigation_links_dict.json'
if os.path.exists(NAV_DICT_PATH):
    with open(NAV_DICT_PATH, 'r', encoding='utf-8') as f:
        MASTER_NAV_MAP = json.load(f)
else:
    MASTER_NAV_MAP = {}

FIRST_DEST_PATH = '/home/owen/tokyo/first_destinations.json'
if os.path.exists(FIRST_DEST_PATH):
    with open(FIRST_DEST_PATH, 'r', encoding='utf-8') as f:
        FIRST_DESTINATIONS = json.load(f)
else:
    FIRST_DESTINATIONS = {}

TEXT_ENTITIES_PATH = '/home/owen/tokyo/text_entities.json'
if os.path.exists(TEXT_ENTITIES_PATH):
    with open(TEXT_ENTITIES_PATH, 'r', encoding='utf-8') as f:
        TEXT_ENTITIES = json.load(f)
else:
    TEXT_ENTITIES = []

def is_non_nav_slot(day, title, body=""):
    t = clean_title(title).strip()
    
    # 1. Any meal with a designated restaurant MUST have navigation
    if any(k in t for k in ['午餐', '晚餐', '拉麵', '壽司', 'すき家', '宇奈とと', '大戶屋', '串家物語', '文字燒', '天丼', '吉野家', '麥當勞', 'Gusto']):
        return False
        
    # 2. Specific outdoor / shopping destinations that MUST have navigation
    if any(k in t for k in ['築地場外市場', '二木菓子', '阿美橫丁', '不忍池', '淺草寺', '吉卜力', '都廳']):
        return False

    # 3. Strictly in-hotel or static non-movement activities
    static_exact = [
        '早餐', '早餐與整理行李', '退房', '準時就寢', '就寢',
        '回飯店休息', '回飯店休息整備', '飯店 Check-in 與休息', 'Check-in 與休息',
        '機場整備與購票', '返回東京車站一番街入口等待開門', '等待開門', '整理行李',
        '輕食午餐與免稅店最後採買', '搭機返台 (CI221)', '搭機返台'
    ]
    
    for s in static_exact:
        if t == s or t.startswith(s):
            return True
            
    # 4. Disney park internal shows/rides
    disney_rides = [
        '必玩設施與行程建議', '午後行程與遊行', '城堡點燈拍照',
        '東京迪士尼樂園電子大遊行', '城堡高空投影秀', '世界市集（World Bazaar）最後補貨與出園',
        'DPA 與 Priority Pass 快速通關'
    ]
    if any(k in t for k in disney_rides):
        return True

    return False

def get_first_destination_map_link(day, title, body=""):
    # If this is a static / non-movement slot, return empty (no nav button!)
    if is_non_nav_slot(day, title, body):
        return ""
        
    # 1. Check FIRST_DESTINATIONS dictionary by day and matching key
    for k, url in FIRST_DESTINATIONS.items():
        if k.startswith(f"{day}_"):
            kw = k[len(f"{day}_"):]
            if kw in title:
                return url

    # 2. Search in body for first explicit markdown link
    md_links = re.findall(r'\[(.*?)\]\((https?://[^\)]+)\)', body)
    if md_links:
        lbl, u = md_links[0]
        for k in sorted(MASTER_NAV_MAP.keys(), key=lambda x: -len(x)):
            if k in lbl:
                return MASTER_NAV_MAP[k]
        return clean_url(u)

    # 3. Fallback to longest match in MASTER_NAV_MAP
    for k in sorted(MASTER_NAV_MAP.keys(), key=lambda x: -len(x)):
        if k in title:
            return MASTER_NAV_MAP[k]

    return ""

def autolink_text_entities(html_text):
    if not html_text:
        return ""
    
    sorted_entities = sorted(TEXT_ENTITIES, key=lambda x: -len(x[0]))
    
    for name, url in sorted_entities:
        if not url or len(name) < 2:
            continue
        escaped_name = re.escape(name)
        # 同時保護既有 <a> 與 <summary>：摺疊標題若被塞進連結，
        # 點擊時會開地圖而不是展開區塊。
        parts = re.split(r'(<a\b[^>]*>.*?</a>|<summary\b[^>]*>.*?</summary>)',
                         html_text, flags=re.DOTALL)
        new_parts = []
        remaining = 2
        for p in parts:
            if (p.startswith('<a') and p.endswith('</a>')) or \
               (p.startswith('<summary') and p.endswith('</summary>')):
                new_parts.append(p)
                continue
            # 再依標籤切一次，只在文字節點取代；否則像 <img alt="…不忍池…">
            # 這種屬性值會被塞進 <a>，導致引號提前結束、HTML 破損
            for seg in re.split(r'(<[^>]+>)', p):
                if seg.startswith('<') or remaining <= 0:
                    new_parts.append(seg)
                    continue
                seg_sub, n = re.subn(r'(?<![="\'/])' + escaped_name,
                                     f'<a class="map-link-inline" href="{url}" target="_blank">{name} 🔗</a>',
                                     seg, count=remaining)
                remaining -= n
                new_parts.append(seg_sub)
        html_text = "".join(new_parts)
        
    return html_text

def format_inline_markdown(text):
    if not text:
        return ""
    text = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', text)
    
    # 1. Handle Markdown Image Syntax: ![alt](url) (supports http/https and local ./assets/)
    def replace_md_img(match):
        alt = match.group(1)
        url = match.group(2).strip()
        return f'<div class="itinerary-img-wrapper" style="margin: 10px 0; text-align: center;"><img src="{url}" alt="{alt}" class="itinerary-img" style="max-width: 100%; height: auto; border-radius: 8px; box-shadow: 0 2px 8px rgba(0,0,0,0.12);" /><p style="font-size: 0.82rem; color: #64748b; margin-top: 4px; font-style: italic;">{alt}</p></div>'
    text = re.sub(r'!\[(.*?)\]\(([^)]+)\)', replace_md_img, text)

    # 2. Handle Markdown Link Syntax: [label](url)
    def replace_md_link(match):
        lbl = match.group(1)
        raw_url = match.group(2)
        clean_u = clean_url(raw_url)
        # If the URL is already an explicit external resource or doc (e.g. tokyodisneyresort.jp, komeda menu, etc.) or label contains reference words, keep raw URL!
        if any(k in lbl for k in ["點此看", "官網", "菜單", "介紹文", "指南", "短網址", "備用導航"]) or "tokyodisneyresort.jp" in raw_url or "komeda.co.jp" in raw_url or not ("google.com/maps" in raw_url or "maps.app.goo.gl" in raw_url or "maps.google" in raw_url):
            return f'<a class="map-link-inline" href="{clean_u}" target="_blank">{lbl} 🔗</a>'
            
        for k in sorted(MASTER_NAV_MAP.keys(), key=lambda x: -len(x)):
            if k in lbl:
                clean_u = MASTER_NAV_MAP[k]
                break
        return f'<a class="map-link-inline" href="{clean_u}" target="_blank">{lbl} 🔗</a>'
    text = re.sub(r'(?<!\!)\[(.*?)\]\((https?://[^\)]+)\)', replace_md_link, text)
    
    def replace_bare_url(match):
        raw_url = match.group(0)
        clean_u = clean_url(raw_url)
        return f'<a class="map-link-inline" href="{clean_u}" target="_blank">地圖導航 📍</a>'
    text = re.sub(r'(?<!href=")(https://www\.google\.com/maps/search/\?api=1&query=[^\s\)\"\']+|https://maps\.google\S+|https://maps\.app\S+|https://share\.google\S+)', replace_bare_url, text)
    return text

def clean_markdown_for_summary(md_text):
    if not md_text:
        return ""
    lines = [l.strip() for l in md_text.split('\n') if l.strip()]
    summary_parts = []
    for line in lines:
        cleaned = re.sub(r'^>\s*\*?\s*', '', line)
        cleaned = re.sub(r'\[(.*?)\]\((https?://[^\)]+)\)', r'<strong>\1</strong>', cleaned)
        cleaned = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', cleaned)
        if cleaned.startswith('💡') or cleaned.startswith('首選餐廳') or cleaned.startswith('推薦') or cleaned.startswith('交通') or cleaned.startswith('亮點') or cleaned.startswith('參觀重點'):
            summary_parts.append(cleaned)
        elif not summary_parts and len(cleaned) > 8:
            summary_parts.append(cleaned)
        if len(summary_parts) >= 2:
            break
    if not summary_parts and lines:
        first = re.sub(r'^>\s*\*?\s*', '', lines[0])
        first = re.sub(r'\[(.*?)\]\((https?://[^\)]+)\)', r'<strong>\1</strong>', first)
        first = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', first)
        return autolink_text_entities(first)
    return autolink_text_entities("<br>".join(summary_parts))

def render_md_table(rows):
    """把連續的 Markdown 表格行轉成 HTML；沿用行前頁籤的 .prep-table 樣式。"""
    cells = [[c.strip() for c in r.strip().strip('|').split('|')] for r in rows]
    header, body = cells[0], [r for r in cells[1:] if set(''.join(r)) - set(': -')]
    html = '<div class="prep-table-wrap"><table class="prep-table"><thead><tr>'
    html += ''.join(f'<th>{format_inline_markdown(c)}</th>' for c in header)
    html += '</tr></thead><tbody>'
    for r in body:
        html += '<tr>' + ''.join(f'<td>{format_inline_markdown(c)}</td>' for c in r) + '</tr>'
    return html + '</tbody></table></div>'


def strip_orphan_details(text):
    """剝除跨時段殘留的孤兒 <details>／</details>。

    README 為了 Docsify 用 <details><summary>☔ 雨天備案…</summary> 包住整個分支，
    該開頭標籤會被切進「前一個時段」的本文，在 PWA 產生一個點開沒有內容的空摺疊；
    對應的 </details> 則落在分支最後一個時段。時段內自己成對的 <details> 不受影響。
    """
    lines = text.split('\n')
    # README 兩種寫法都要認：獨立成行的 <details>，以及單行的
    # <details><summary>…</summary>。只比對 == '<details>' 會漏掉後者，
    # 使它的 </details> 被誤判成孤兒結尾刪掉，摺疊區永遠關不起來。
    opens = [i for i, l in enumerate(lines) if l.strip().startswith('<details>')]
    closes = [i for i, l in enumerate(lines) if l.strip() == '</details>']
    drop = set()
    # 由後往前配對：每個 </details> 找它前面最近、尚未被配對的 <details>
    unpaired_opens = list(opens)
    for c in closes:
        prior = [o for o in unpaired_opens if o < c]
        if prior:
            unpaired_opens.remove(prior[-1])
        else:
            drop.add(c)                      # 沒有開頭的孤兒結尾
    for o in unpaired_opens:                 # 沒有結尾的孤兒開頭
        drop.add(o)
        nxt = o + 1
        while nxt < len(lines) and not lines[nxt].strip():
            nxt += 1
        if nxt < len(lines) and lines[nxt].strip().startswith('<summary>'):
            drop.add(nxt)
    return '\n'.join(l for i, l in enumerate(lines) if i not in drop)


BACKUP_BULLET_RE = re.compile(r'^\*\s*次?備案餐廳')


def _quote_line(line):
    """把引用行拆成 (是否引用行, 縮排量, 去空白內容)。非引用行回傳 (False, None, None)。"""
    if not line.startswith('>'):
        return False, None, None
    after = line[1:]
    return True, len(after) - len(after.lstrip()), after.strip()


def collapse_backup_restaurants(text):
    """把每一家「備案餐廳」各自收進預設收合的 <details>，摘要列店名與人均。

    備案往往佔掉時段本文一半以上篇幅，但現場多半只看首選。一家一個區塊，
    摘要就能比較（誰便宜、誰貴），不必全部展開。
    只改 PWA 呈現，README 不動（Docsify 仍為攤平樣式）。
    """
    lines = text.split('\n')
    out, i = [], 0
    while i < len(lines):
        is_q, indent, content = _quote_line(lines[i])
        if not (is_q and indent is not None and indent <= 1
                and BACKUP_BULLET_RE.match(content or '')):
            out.append(lines[i])
            i += 1
            continue
        # 連續的備案條列：逐筆各自包成一個 <details>
        while i < len(lines):
            is_q2, indent2, content2 = _quote_line(lines[i])
            if not is_q2 or indent2 is None:
                break
            if indent2 > 1:              # 理論上不會單獨出現，保險起見原樣輸出
                out.append(lines[i])
                i += 1
                continue
            if not BACKUP_BULLET_RE.match(content2 or ''):
                break
            start = i
            m = re.search(r'\[\*\*(.+?)\*\*\]', content2)
            name = m.group(1).split(' (')[0].strip() if m else '備案餐廳'
            pm = re.search(r'人均約\s*([^，。]+)', content2)
            hint = f'人均 {pm.group(1)}・' if pm else ''
            i += 1
            while i < len(lines):        # 縮排更深者屬於這一筆，一併收入
                is_q3, indent3, _ = _quote_line(lines[i])
                if not is_q3 or indent3 is None or indent3 <= 1:
                    break
                i += 1
            out += ['<details>',
                    f'<summary>🍽️ 備案：{name}（{hint}點擊展開）</summary>', '']
            out += lines[start:i]
            out += ['', '</details>']
    return '\n'.join(out)


def markdown_to_html(text):
    if not text:
        return ""
    text = strip_orphan_details(text)
    text = collapse_backup_restaurants(text)
    lines = text.split('\n')
    html_lines = []
    in_list = False
    in_quote = False
    table = []

    def flush_table():
        if table:
            html_lines.append(render_md_table(table))
            table.clear()

    for raw_line in lines:
        line = raw_line.strip()
        # 表格：`| a | b |`，或引用區塊內的 `> | a | b |`
        cell_line = line.lstrip('>').strip() if line.startswith('>') else line
        if cell_line.startswith('|') and cell_line.endswith('|'):
            if in_list:
                html_lines.append('</ul>')
                in_list = False
            table.append(cell_line)
            continue
        flush_table()
        if not line:
            if in_list:
                html_lines.append('</ul>')
                in_list = False
            if in_quote:
                html_lines.append('</div>')
                in_quote = False
            continue
            
        if line.startswith('>'):
            if not in_quote:
                html_lines.append('<div class="modal-quote">')
                in_quote = True
            content = line.lstrip('>').strip()
            # 項目符號後面必須有空白。只比對 startswith('*') 會把 `**粗體**`
            # 開頭的行當成清單，且 lstrip('*-') 連兩個星號一起吃掉，
            # 渲染成「文字**」——粗體失效、尾端多一個 **。
            # README 目前沒有任何無空格的清單寫法，加這個條件不會誤傷既有清單。
            if re.match(r'^[*-]\s', content):
                if not in_list:
                    html_lines.append('<ul class="modal-list">')
                    in_list = True
                item_text = content[1:].strip()
                html_lines.append(f'<li>{format_inline_markdown(item_text)}</li>')
            else:
                if in_list:
                    html_lines.append('</ul>')
                    in_list = False
                html_lines.append(f'<p>{format_inline_markdown(content)}</p>')
        elif line.startswith('*') or line.startswith('-'):
            if in_quote:
                html_lines.append('</div>')
                in_quote = False
            if not in_list:
                html_lines.append('<ul class="modal-list">')
                in_list = True
            item_text = line.lstrip('*-').strip()
            html_lines.append(f'<li>{format_inline_markdown(item_text)}</li>')
        else:
            if in_list:
                html_lines.append('</ul>')
                in_list = False
            if in_quote:
                html_lines.append('</div>')
                in_quote = False
            if line.startswith('<'):
                # 原始 HTML（<details>／<summary> 等）直接輸出，
                # 不要包進 <p>，否則要靠瀏覽器容錯才顯示得對。
                html_lines.append(line)
            elif line.startswith('###') or line.startswith('####'):
                h_text = line.lstrip('#').strip()
                html_lines.append(f'<h4 class="modal-subheading">{format_inline_markdown(h_text)}</h4>')
            else:
                html_lines.append(f'<p>{format_inline_markdown(line)}</p>')
                
    flush_table()
    if in_list:
        html_lines.append('</ul>')
    if in_quote:
        html_lines.append('</div>')

    full_html = '\n'.join(html_lines)
    return autolink_text_entities(full_html)

CUSTOM_SUMMARIES_V10 = {
    # Day 1
    (1, "機場整備與 Suica 交通卡辦理"): f"洗手間整備、ATM提款、整理行李。<strong>建議直接於機場辦理 2 張兒童 Welcome Suica</strong>（需出示護照，後續搭車最省事），每張建議先儲值 ¥2,000～3,000。",
    (1, "前往飯店 (Henn na Hotel)"): f"<strong>搭乘首選（直達）：</strong>從 <a class=\"map-link-inline\" href=\"{MASTER_NAV_MAP.get('羽田機場第3航廈', '')}\" target=\"_blank\">羽田機場第3航廈站 🔗</a> 搭乘「京急機場線 (直通都營淺草線)」直達 淺草橋站（A1 電梯出口）。車程約 40-45 分鐘，免提行李換車。",
    (1, "飯店 Check-in 與休息"): f"步行抵達 <a class=\"map-link-inline\" href=\"{MASTER_NAV_MAP.get('海茵娜酒店', '')}\" target=\"_blank\">海茵娜酒店 🔗</a> 辦理 Check-in、置放行李、稍作休息，更換舒適鞋衣。",
    (1, "出發前往秋葉原"): f"🚪 <strong>西口進站</strong>。慢步 2 分鐘至 JR 淺草橋站，搭乘 JR 中央・總武線 (黃色列車) 1 站直達 <a class=\"map-link-inline\" href=\"{MASTER_NAV_MAP.get('秋葉原站', '')}\" target=\"_blank\">秋葉原站 🔗</a> (車程僅 2 分鐘)。",
    (1, "🕹️ 日式夾娃娃機體驗"): f"日本大型電玩中心，日式夾娃娃機（UFO Catcher），預算約 ¥500～¥1,000。",
    (1, "日系拍貼機全家合影體驗"): f"<strong>全家合影紀念：</strong>全家 5 人拍貼，觸控塗鴉並現場列印全彩貼紙（¥500/次）。",
    (1, "晚餐：壽司郎（90 分鐘寬裕大啖平價迴轉壽司）"): f"<strong>首選餐廳：</strong><a class=\"map-link-inline\" href=\"{MASTER_NAV_MAP.get('壽司郎 (スシロー 秋葉原駅前店)', '')}\" target=\"_blank\">🍣 壽司郎 秋葉原駅前店 (BiTO AKIBA B1F) 🔗</a> 享用平價迴轉壽司（人均 ¥1,000～¥1,800）。<strong>已訂位</strong>。全中文觸控平板、現點現做軌道直送，90 分鐘寬裕用餐！<br><strong>備案 1：</strong><a class=\"map-link-inline\" href=\"{MASTER_NAV_MAP.get('丸龜製麵 (丸亀製麺 秋葉原店)', '')}\" target=\"_blank\">丸龜製麵 秋葉原店 🔗</a> (烏龍麵，¥500-900)<br><strong>備案 2：</strong><a class=\"map-link-inline\" href=\"{MASTER_NAV_MAP.get('CoCo壹番屋 (CoCo壱番屋 JR秋葉原駅昭和通り口店)', '')}\" target=\"_blank\">CoCo壹番屋 秋葉原站前店 🔗</a> (咖哩飯，¥800-1,200)",
    (1, "返回淺草橋"): f"步行至 JR <a class=\"map-link-inline\" href=\"{MASTER_NAV_MAP.get('秋葉原站', '')}\" target=\"_blank\">秋葉原站 🔗</a>，搭乘 JR 中央・總武線 1 站直達 淺草橋站 (車程 2 分鐘)。",
    (1, "🐈 欣賞新宿 3D 巨貓"): f"新宿東口站前廣場抬頭觀賞巨大 3D 三花貓演出，廣場平坦。",
    (1, "晚餐：Gusto 家庭餐廳"): f"<strong>首選餐廳：</strong><a class=\"map-link-inline\" href=\"{MASTER_NAV_MAP.get('Gusto (ガスト 新宿NOWAビル店)', '')}\" target=\"_blank\">🍽️ Gusto 新宿NOWAビル店 (7F) 🔗</a> 享用平價日式家庭料理（漢堡排定食，人均 ¥800～¥1,200），全中文平板點餐、貓咪送餐機器人。<br><strong>備案：</strong><a class=\"map-link-inline\" href=\"{MASTER_NAV_MAP.get('LUMINE EST 餐廳街 (ルミネエスト新宿 7&8 DINER)', '')}\" target=\"_blank\">LUMINE EST 餐廳街 🔗</a> (7F/8F 蛋包飯/日式洋食)。",
    (1, "地方生鮮超市採買"): f"前往飯店旁 <a class=\"map-link-inline\" href=\"{MASTER_NAV_MAP.get('肉之Hanamasa超市', '')}\" target=\"_blank\"><strong>肉之Hanamasa超市 (肉のハナマサ 浅草橋店)</strong> 🔗</a> 採買：翌日早餐鮮乳、麵包、優格、礦泉水與當季水果。",
    (1, "回飯店休息整備"): f"回到 <a class=\"map-link-inline\" href=\"{MASTER_NAV_MAP.get('海茵娜酒店', '')}\" target=\"_blank\">海茵娜酒店 🔗</a>。整理明日迪士尼裝備（門票、Welcome Suica、行動電源）。全家輪流洗澡泡澡放鬆。",
    (1, "準時就寢"): f"<strong>21:00－21:30 準時就寢</strong>，隔天 06:20 起床睡滿 9 小時，充足體力迎戰東京迪士尼！",

    # Day 2 Parents
    (2, "前往上野"): f"🚪 <strong>西口進站</strong>。從淺草橋搭 🟡 JR 總武線 1 站至秋葉原，站內轉🟢 JR 山手線往上野方向再搭 2 站至 <a class=\"map-link-inline\" href=\"{MASTER_NAV_MAP.get('JR 上野站 (上野駅)', '')}\" target=\"_blank\"><strong>上野站</strong> 🔗</a>。<br><strong>☀️ 晴天</strong>：走「不忍口」出站，直接往不忍池散步。<br><strong>☔ 雨天</strong>：走「公園口」出站，正對上野恩賜公園，步行 12 分鐘直達東京國立博物館。",
    (2, "晨間不忍池與清水觀音堂散步"): f"<a class=\"map-link-inline\" href=\"{MASTER_NAV_MAP.get('JR 上野站 (上野駅)', '')}\" target=\"_blank\">上野站不忍口 🔗</a> 出發 ➔ <a class=\"map-link-inline\" href=\"{MASTER_NAV_MAP.get('不忍池 (不忍池 弁天堂)', '')}\" target=\"_blank\">不忍池 🔗</a>（賞荷花） ➔ <a class=\"map-link-inline\" href=\"{MASTER_NAV_MAP.get('清水觀音堂 (清水観音堂)', '')}\" target=\"_blank\">清水觀音堂 🔗</a>（看月之松）➔ 走回上野站。實走約 1.5 公里、純走路 29 分鐘；走不動可只到不忍池就折返。",
    (2, "午餐：松屋 / 吉野家"): f"<strong>首選餐廳：</strong><a class=\"map-link-inline\" href=\"{MASTER_NAV_MAP.get('松屋 (松屋 上野浅草口店)', '')}\" target=\"_blank\">松屋 上野浅草口店 🔗</a>（上野站浅草口步行 1 分鐘，有桌席、24 小時營業，人均 ¥500～¥900）。<strong>門口自動售票機可切換語言，全程不需與店員對話。</strong><br><strong>備案：</strong><a class=\"map-link-inline\" href=\"{MASTER_NAV_MAP.get('吉野家 (吉野家 上野駅前店)', '')}\" target=\"_blank\">吉野家 上野駅前店 🔗</a>（就在隔壁一棟，人均 ¥500～¥900，以吧台席為主）。",
    (2, "參觀國立西洋美術館"): f"<strong>室內避暑亮點：</strong><a class=\"map-link-inline\" href=\"{MASTER_NAV_MAP.get('國立西洋美術館 (国立西洋美術館)', '')}\" target=\"_blank\">🏛️ 國立西洋美術館 🔗</a> 欣賞羅丹雕塑與莫內睡蓮（<strong>滿 65 歲長輩出示護照常設展免費入場</strong>，冷氣極強！）。",
    (2, "美術館戶外庭園"): f"就在美術館館外前庭，免票、不用另外走路。免費近距離欣賞羅丹名作「地獄之門」與「沉思者」。若還有餘裕，<a class=\"map-link-inline\" href=\"{MASTER_NAV_MAP.get('東京文化會館 (東京文化会館)', '')}\" target=\"_blank\">東京文化會館 🔗</a> 與 <a class=\"map-link-inline\" href=\"{MASTER_NAV_MAP.get('上野公園大噴水廣場 (上野恩賜公園 大噴水)', '')}\" target=\"_blank\">大噴水廣場 🔗</a> 都在旁邊。15:00 仍有 32～34 度，不久留。",
    (2, "下午茶與逛街（兩案擇一）"): f"<strong>長輩自己挑，兩案都成立：</strong><br><strong>🛍️ 方案 1</strong>：搭 🟢 山手線 1 站到御徒町（含移動約 20 分），逛 <a class=\"map-link-inline\" href=\"{MASTER_NAV_MAP.get('松坂屋 (松坂屋 上野店)', '')}\" target=\"_blank\">松坂屋 🔗</a>／PARCO_ya，順路買 <a class=\"map-link-inline\" href=\"{MASTER_NAV_MAP.get('兔屋 (うさぎや)', '')}\" target=\"_blank\">兔屋 🔗</a> 銅鑼燒；咖啡廳 4 家可選（客美多沙發座／聖瑪克／松坂屋 8F 免費休憩所／麥當勞 24 小時）。<br><strong>☕ 方案 2</strong>：<strong>完全不用移動</strong>，就在上野站周邊 3 家擇一——<a class=\"map-link-inline\" href=\"{MASTER_NAV_MAP.get('羅多倫咖啡 (ドトールコーヒーショップ アトレ上野店)', '')}\" target=\"_blank\">羅多倫 アトレ上野店 🔗</a>（車站直結、最便宜）、<a class=\"map-link-inline\" href=\"{MASTER_NAV_MAP.get('雷諾瓦咖啡 (喫茶室ルノアール 上野しのばず口店)', '')}\" target=\"_blank\">雷諾瓦咖啡 🔗</a>（最能久坐）、<a class=\"map-link-inline\" href=\"{MASTER_NAV_MAP.get('三橋餡蜜 (あんみつ みはし アトレ上野店)', '')}\" target=\"_blank\">三橋餡蜜 🔗</a>（和風甜點）。",
    (2, "晚餐：宇奈とと鰻魚飯"): f"<strong>首選餐廳：</strong><a class=\"map-link-inline\" href=\"{MASTER_NAV_MAP.get('名代 宇奈とと (名代 宇奈とと 上野店)', '')}\" target=\"_blank\">🐟 名代 宇奈とと 上野店 🔗</a> (JR高架旁) 平價鰻魚飯（うな丼 ¥640、うな重 ¥1,060）。<br><strong>備案：</strong><a class=\"map-link-inline\" href=\"{MASTER_NAV_MAP.get('松屋 (松屋 上野店)', '')}\" target=\"_blank\">松屋 上野店 🔗</a> (日式定食附熱味噌湯，人均 ¥550-950)。",
    (2, "返回淺草橋（長輩組）"): f"<strong>就近進站：</strong>宇奈とと步行 2 分鐘直達 <a class=\"map-link-inline\" href=\"{MASTER_NAV_MAP.get('JR 上野站 (上野駅)', '')}\" target=\"_blank\">JR 上野站不忍口 🔗</a>（或從松坂屋步行 2 分鐘至 <a class=\"map-link-inline\" href=\"{MASTER_NAV_MAP.get('JR 御徒町站 (御徒町駅)', '')}\" target=\"_blank\">JR 御徒町站 🔗</a>），搭山手線至秋葉原轉總武線 1 站回淺草橋。",

    # Day 2 Kids (Disney)
    (2, "前往東京迪士尼樂園"): f"🚪 <strong>西口進站</strong>。淺草橋 ➔ 秋葉原 (總武線) ➔ 八丁堀 (地鐵日比谷線) ➔ <a class=\"map-link-inline\" href=\"{MASTER_NAV_MAP.get('JR 舞濱站 (舞浜駅)', '')}\" target=\"_blank\">舞濱站 🔗</a> (JR京葉線)。全程設有手扶梯與電梯，避開東京車站巨型轉乘。",
    (2, "抵達樂園門口排隊與入園"): f"<strong>核心策略：免費＋合理視野＋最大化遊樂時間</strong>。入園後以 <strong>40周年 Priority Pass（免費 PP）</strong> 為主要導航，搭配 Entry Request 與周邊設施動態遊玩。",
    (2, "動態遊玩主時段"): f"<strong>本日主體：遊樂設施</strong>。以免費 PP 為核心導航，擴散遊玩所在區域周邊設施。搭配 Notion「迪士尼體驗 Database」即時查看推薦項目與排隊時間。",
    (2, "午餐窗口（彈性不跨區）"): f"<strong>遊玩 > 吃飯，不預約、不跨區</strong>。使用 Disney App Mobile Order 就近點餐取餐，或找附近行動餐車解決。",
    (2, "午餐窗口"): f"<strong>遊玩 > 吃飯，不預約、不跨區</strong>。使用 Disney App Mobile Order 就近點餐取餐，或找附近行動餐車解決。",
    (2, "米奇魔法音樂世界"): f"全室內劇場演出，雨天亦非常適合。<strong>抽到合理時段才去，不為其破壞遊樂節奏</strong>。",
    (2, "🌈 日間遊行「迪士尼眾彩交融」 (ディズニー・ハーモニー・イン・カラー)｜OPTION"): f"<strong>17:00 一天只有一場</strong>，全程約 45 分鐘。<strong>要看就站起點側</strong>（<a class=\"map-link-inline\" href=\"{MASTER_NAV_MAP.get('幽靈公館 (ホーンテッドマンション)', '')}\" target=\"_blank\">幽靈公館 🔗</a> 旁到西部樂園一帶），看完就能走、接得上 17:30 晚餐；站城堡前或卡通城會結束得晚很多。<strong>有空且晴天才看</strong>，雨天優先放棄，不提前長時間卡位。",
    (2, "晚餐窗口（快速補充體力）"): f"<strong>快速補充體力</strong>。目前位置附近以 App Mobile Order 下單或買行動餐車，不為吃飯特別跑遠。",
    (2, "晚餐窗口"): f"<strong>快速補充體力</strong>。目前位置附近以 App Mobile Order 下單或買行動餐車，不為吃飯特別跑遠。",
    (2, "跳跳熱舞"): f"戶外舞台演出，<strong>僅優先考慮 18:00 場次</strong>，雨天降低優先度。",
    (2, "夜間遊行「夢之光」免費卡位"): f"<strong>18:15～18:30 開始卡位</strong>。<a class=\"map-link-inline\" href=\"{MASTER_NAV_MAP.get('灰姑娘城堡 (シンデレラ城)', '')}\" target=\"_blank\">灰姑娘城堡 🔗</a> 前 <a class=\"map-link-inline\" href=\"{MASTER_NAV_MAP.get('城堡前廣場 (プラザ)', '')}\" target=\"_blank\">Plaza 廣場 🔗</a> 附近免費區，以合理視野換取下午遊玩時間。",
    (2, "東京迪士尼樂園電子大遊行「夢之光」"): f"<strong>固定核心／建議必看</strong>。全長約 45 分鐘，璀璨燈光花車與經典音樂遊行，全家坐著放鬆休息。",
    (2, "前往 Reach for the Stars 免費鑑賞區"): f"遊行結束後直接移動至 <a class=\"map-link-inline\" href=\"{MASTER_NAV_MAP.get('夥伴雕像 (パートナーズ像)', '')}\" target=\"_blank\"><strong>Partners Statue（夥伴銅像）</strong> 🔗</a> 附近或 <a class=\"map-link-inline\" href=\"{MASTER_NAV_MAP.get('城堡前廣場 (プラザ)', '')}\" target=\"_blank\">Plaza 廣場 🔗</a> 中後方免費區。",
    (2, "城堡投影秀 Reach for the Stars"): f"<strong>固定核心（雨天正常演出才看）</strong>。Everlasting Dreams 夏季特別版，3D 燈光投影與焰火震撼演出。",
    (2, "世界市集紀念品採買與出園"): f"於 <a class=\"map-link-inline\" href=\"{MASTER_NAV_MAP.get('世界市集 (ワールドバザール)', '')}\" target=\"_blank\">世界市集 🔗</a> 採買紀念品與伴手禮，前往東巴士總站搭車。",
    (2, "返回淺草橋（親子組）"): f"<strong>首選（直達巴士）：</strong>出園至巴士總站 11 號站牌搭乘直達 <a class=\"map-link-inline\" href=\"{MASTER_NAV_MAP.get('秋葉原站東口 (秋葉原駅東口交通広場)', '')}\" target=\"_blank\"><strong>秋葉原站東口</strong> 🔗</a> 的高速巴士（車程約 35-45 分鐘，上車有座位一路睡回秋葉原），轉總武線 1 站回淺草橋。<br><strong>備案：</strong>舞濱 ➔ 八丁堀 (京葉線) ➔ 秋葉原 (日比谷線) ➔ 淺草橋。",
    (2, "返回淺草橋"): f"<strong>首選（直達巴士）：</strong>出園至巴士總站 11 號站牌搭乘直達 <a class=\"map-link-inline\" href=\"{MASTER_NAV_MAP.get('秋葉原站東口 (秋葉原駅東口交通広場)', '')}\" target=\"_blank\"><strong>秋葉原站東口</strong> 🔗</a> 的高速巴士（車程約 35-45 分鐘，上車有座位一路睡回秋葉原），轉總武線 1 站回淺草橋。<br><strong>備案：</strong>舞濱 ➔ 八丁堀 (京葉線) ➔ 秋葉原 (日比谷線) ➔ 淺草橋。",

    # Day 3
    (3, "搭乘 JR 前往東京車站"): f"🚪 <strong>西口進站</strong>。淺草橋 ➔ 秋葉原 ➔<a class=\"map-link-inline\" href=\"{MASTER_NAV_MAP.get('東京站', '')}\" target=\"_blank\">東京站 🔗</a> (JR 山手線，車程 8 分鐘)。",
    (3, "欣賞東京車站丸之內站舍建築"): f"丸之內站前廣場，與紅磚站舍建築合影。",
    (3, "🌇 KITTE頂樓花園眺望東京車站"): f"搭電梯直達 <a class=\"map-link-inline\" href=\"{MASTER_NAV_MAP.get('KITTE花園 (ＫＩＴＴＥガーデン)', '')}\" target=\"_blank\">KITTE 6F 屋頂花園 🔗</a>，免費俯瞰東京車站紅磚站舍與新幹線進出站，室內有空調。",
    (3, "午餐：天丼Tenya"): f"<strong>首選餐廳：</strong><a class=\"map-link-inline\" href=\"{MASTER_NAV_MAP.get('天丼てんや (天丼てんや 八重洲店)', '')}\" target=\"_blank\">🍤 天丼てんや 八重洲店 🔗</a> (八重洲地下街 B1F 南1號) 日式炸蝦天丼，人均 ¥560～¥850。<br><strong>備案 1：</strong><a class=\"map-link-inline\" href=\"{MASTER_NAV_MAP.get('だし茶漬け えん KITTE丸の内店', '')}\" target=\"_blank\">だし茶漬け えん KITTE丸の内店 🔗</a> (高湯茶泡飯，¥850-1,100)<br><strong>備案 2：</strong><a class=\"map-link-inline\" href=\"{MASTER_NAV_MAP.get('燕子烤肉漢堡排 (つばめグリル 大丸東京店)', '')}\" target=\"_blank\">燕子烤肉漢堡排 🔗</a> (大丸東京店 12F)",
    (3, "前往上野"): f"搭乘 JR 山手線 8 分鐘直達 <a class=\"map-link-inline\" href=\"{MASTER_NAV_MAP.get('上野站', '')}\" target=\"_blank\">上野站 🔗</a>（公園口出站設有電梯）。",
    (3, "參觀國立科學博物館"): f"🎫 <strong>需購票</strong>。參觀地球館 B1 恐龍化石骨骼、3F 野生動物標本展廳與 360 度球幕影院。",
    (3, "享用鴨 to 蔥拉麵｜OPTION"): f"<strong>首選名店：</strong><a class=\"map-link-inline\" href=\"{MASTER_NAV_MAP.get('鴨 to 蔥拉麵 (らーめん 鴨to葱 御徒町本店)', '')}\" target=\"_blank\">🍜 鴨 to 蔥拉麵 御徒町本店 🔗</a> 香濃鴨肉醬油拉麵（人均 ¥1,000～¥1,400）。<br><strong>🚨 排隊停損防雷規則：</strong>排隊 ≤ 3 組才吃，超過直接啟動阿美橫丁小吃備案。",
    (3, "阿美橫丁逛街採買"): f"<strong>必掃名店：</strong><br>• <a class=\"map-link-inline\" href=\"{MASTER_NAV_MAP.get('二木菓子 (二木の菓子 第一営業所)', '')}\" target=\"_blank\">二木菓子（第一営業所） 🔗</a>：掃日本零食名產。<br>• <a class=\"map-link-inline\" href=\"{MASTER_NAV_MAP.get('OS Drug 上野店', '')}\" target=\"_blank\">OS Drug 上野店 🔗</a>：藥妝免退稅價格之冠。<br>• 街邊小吃：<a class=\"map-link-inline\" href=\"{MASTER_NAV_MAP.get('肉之大山 (肉の大山 上野店)', '')}\" target=\"_blank\">肉之大山炸肉餅 🔗</a>、<a class=\"map-link-inline\" href=\"{MASTER_NAV_MAP.get('みなとや食品', '')}\" target=\"_blank\">みなとや章魚燒 🔗</a>。<br>• <a class=\"map-link-inline\" href=\"{MASTER_NAV_MAP.get('多慶屋 (多慶屋 TAKEYA 1)', '')}\" target=\"_blank\">多慶屋（TAKEYA） 🔗</a>：紫色商場一站式補貨備案。",
    (3, "回飯店放戰利品"): f"🧳 阿美橫丁買的零食、藥妝、伴手禮先放回房間，<strong>空手去吃晚餐</strong>。只多走約 50 公尺：西口回飯店 110 公尺，飯店走到吉野家 240 公尺。",
    (3, "🚆 前往御徒町站搭車"): f"步行至 JR <a class=\"map-link-inline\" href=\"{MASTER_NAV_MAP.get('御徒町站', '')}\" target=\"_blank\">御徒町站 🔗</a> 搭乘電車返回淺草橋。",
    (3, "晚餐：吉野家"): f"<strong>首選餐廳：</strong><a class=\"map-link-inline\" href=\"{MASTER_NAV_MAP.get('吉野家 (吉野家 浅草橋店)', '')}\" target=\"_blank\">吉野家 浅草橋店 🔗</a>。<br><strong>備案：</strong><a class=\"map-link-inline\" href=\"{MASTER_NAV_MAP.get('松屋 (松屋 浅草橋店)', '')}\" target=\"_blank\">松屋 浅草橋店 🔗</a>。",

    # Day 4
    (4, "前往三鷹"): f"🚪 <strong>西口進站</strong>。搭 🟡 JR 中央・總武線至御茶之水，同月台轉 🟠 中央線快速直達 <a class=\"map-link-inline\" href=\"{MASTER_NAV_MAP.get('三鷹站 (三鷹駅)', '')}\" target=\"_blank\">三鷹站 🔗</a>。",

    # Day 5
    (5, "前往淺草"): f"🚪 <strong>A3 出口進站</strong>（沒帶大行李走 A3 最近）。搭 🌹 都營淺草線前往淺草，目標 <a class=\"map-link-inline\" href=\"{MASTER_NAV_MAP.get('雷門 (雷門)', '')}\" target=\"_blank\">雷門 🔗</a>。",
    (5, "前往台場（日本科學未來館）"): f"🚪 <strong>A3 出口進站</strong>。搭 🌹 都營淺草線至新橋，轉 🟠 百合海鷗線前往台場的日本科學未來館。",
    (5, "觀賞都廳光雕投影秀"): f"看 <strong>19:00－19:15</strong> 這場，共 15 分鐘。<strong>要下樓到地面的都民廣場看</strong>，45 樓展望室看不到。免費、不需預約。8/24 為平日場，沒有哥吉拉與寶可夢。",

    # Day 6
    (6, "前往築地場外市場"): f"🚪 <strong>A3 出口進站</strong>（行李已寄放在飯店，走最近的 A3）。搭 🌹 都營淺草線至東銀座，步行前往 <a class=\"map-link-inline\" href=\"{MASTER_NAV_MAP.get('築地場外市場 (築地場外市場)', '')}\" target=\"_blank\">築地場外市場 🔗</a>。",
    (6, "領取行李並前往車站"): f"回飯店領取行李，做最後的隨身物品確認。🧳 <strong>帶大行李改走 A1 出口進站</strong>，那是唯一有直達地面電梯的出口，切勿走純樓梯。",
    (6, "🚆 前往羽田機場"): f"🧳 <strong>走 A1 出口（無障礙電梯）進站</strong>。搭 🌹 都營淺草線直通 🔴 京急機場線的機場特快，一車直達 <a class=\"map-link-inline\" href=\"{MASTER_NAV_MAP.get('羽田機場第3航廈', '')}\" target=\"_blank\">羽田機場第 3 航廈 🔗</a>，免換車。"
}

def parse_v10_markdown():
    filepath = '/home/owen/tokyo/README.md'
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    content = content.replace('\r\n', '\n')

    meta = {
        'member': "我 / 父親 / 母親 / 女兒（9歲，150cm） / 兒子（7歲，130cm）",
        'flight_go': "去程：CI220 松山(TSA) → 羽田(HND) 09:00－13:10",
        'flight_back': "回程：CI221 羽田(HND) → 松山(TSA) 14:30－16:55",
        'hotel_name': "海茵娜酒店东京浅草桥 (Henn na Hotel Tokyo Asakusabashi)",
        'hotel_addr': "1-10-5 Asakusabashi, Taito-ku, Tokyo 111-0053, JAPAN",
        'hotel_jp_addr': "東京都台東区浅草橋1-10-5"
    }

    # Day 1 標題之前的行前資訊（航班接送／住宿／新手交通提醒／行程與餐點總覽）。
    # 日程正則只切取 `## **📅 Day N` 之後的內容，這段以往在 PWA 完全看不到，
    # 現改由「📌 行前」頁籤呈現。
    pre_match = re.search(r'\n(## \*\*✈️ .*?)\n## \*\*📅 Day 1', content, re.DOTALL)
    meta['preamble'] = pre_match.group(1).strip() if pre_match else ''

    days_data = {
        1: {'common_before': [], 'plan_a': [], 'plan_b': [], 'common_after': []},
        2: {'parents': {'common_before': [], 'sunny': [], 'rainy': [], 'common_after': []}, 'kids': []},
        3: {'common_before': [], 'sunny': [], 'rainy': [], 'common_after': []},
        4: [],
        5: {'common_before': [], 'plan_a': [], 'plan_b': [], 'rainy': []},
        6: []
    }

    # Day 1
    d1_match = re.search(r'## \*\*📅 Day 1.*?\n(.*?)(?=\n## \*\*📅 Day 2|\Z)', content, re.DOTALL)
    if d1_match:
        d1_text = d1_match.group(1)
        slots = re.split(r'\n(?=#{3,4} \*\*)', d1_text)
        current_sub = 'common_before'
        for s in slots:
            s = s.strip()
            if not s:
                continue
            lines = s.split('\n')
            h = lines[0]
            b = '\n'.join(lines[1:])
            
            if '共同收尾' in h:
                current_sub = 'common_after'
                continue
            elif 'Plan A' in h:
                current_sub = 'plan_a'
                continue
            elif 'Plan B' in h:
                current_sub = 'plan_b'
                continue

            h_clean = h.replace('####', '').replace('###', '').replace('**', '').strip()
            time_m = re.match(r'^([\d:：]+－[\d:：]+|[\d:：]+)\s*(.*)', h_clean)
            slot_time = time_m.group(1) if time_m else ""
            slot_title_raw = time_m.group(2) if time_m else h_clean
            slot_title = clean_title(slot_title_raw)
            if not slot_title:
                continue

            cat, cat_zh, cat_icon = get_category_info(slot_title)
            maps_link = get_first_destination_map_link(1, slot_title_raw, b)
            
            summary = CUSTOM_SUMMARIES_V10.get((1, slot_title))
            if not summary:
                for (d, t), sm in CUSTOM_SUMMARIES_V10.items():
                    if d == 1 and (t in slot_title or slot_title in t):
                        summary = sm
                        break
            if not summary:
                summary = clean_markdown_for_summary(b)

            days_data[1][current_sub].append({
                'time': slot_time,
                'title': slot_title,
                'category': cat,
                'category_zh': cat_zh,
                'category_icon': cat_icon,
                'summary': summary,
                'maps_link': maps_link,
                'html_content': markdown_to_html(b.strip()),
                'has_modal': len(b.strip()) > 20
            })

    # Day 2 Parents
    d2p_match = re.search(r'## \*\*📅 Day 2.*?長輩組.*?\n(.*?)(?=\n## \*\*📅 Day 2.*?親子組|\n## \*\*📅 Day 3|\Z)', content, re.DOTALL)
    if d2p_match:
        slots = re.split(r'\n(?=#{3,4} \*\*)', d2p_match.group(1))
        current_sub = 'common_before'
        for s in slots:
            s = s.strip()
            if not s:
                continue
            s_lines = s.split('\n')
            h = s_lines[0]
            b = '\n'.join(s_lines[1:])
            
            if '共同收尾' in h:
                current_sub = 'common_after'
                continue
            elif '晴天' in h:
                current_sub = 'sunny'
                continue
            elif '雨天' in h:
                current_sub = 'rainy'
                continue
            
            h_clean = h.replace('####', '').replace('###', '').replace('**', '').strip()
            time_m = re.match(r'^([\d:：]+－[\d:：]+|[\d:：]+)\s*(.*)', h_clean)
            slot_time = time_m.group(1) if time_m else ""
            slot_title_raw = time_m.group(2) if time_m else h_clean
            slot_title = clean_title(slot_title_raw)
            if not slot_title:
                continue
            cat, cat_zh, cat_icon = get_category_info(slot_title)
            maps_link = get_first_destination_map_link(2, slot_title_raw, b)
            summary = CUSTOM_SUMMARIES_V10.get((2, slot_title))
            if not summary:
                for (d, t), sm in CUSTOM_SUMMARIES_V10.items():
                    if d == 2 and ("午餐窗口" not in t and "晚餐窗口" not in t and "迪士尼" not in t and "遊玩" not in t) and (t in slot_title or slot_title in t):
                        summary = sm
                        break
            if not summary:
                summary = clean_markdown_for_summary(b)
            days_data[2]['parents'][current_sub].append({
                'time': slot_time,
                'title': slot_title,
                'category': cat,
                'category_zh': cat_zh,
                'category_icon': cat_icon,
                'summary': summary,
                'maps_link': maps_link,
                'html_content': markdown_to_html(b.strip()),
                'has_modal': len(b.strip()) > 20
            })

    # Day 2 Kids
    d2k_match = re.search(r'## \*\*📅 Day 2.*?親子組.*?\n(.*?)(?=\n## \*\*📅 Day 3|\Z)', content, re.DOTALL)
    if d2k_match:
        slots = re.split(r'\n(?=#{3,4} \*\*)', d2k_match.group(1))
        for s in slots:
            s = s.strip()
            if not s or '🎟️ 建議購買' in s or '⏱️ 免費 Priority' in s or '🍿 今日必做' in s or '💰 迪士尼預估' in s:
                continue
            lines = s.split('\n')
            h = lines[0]
            b = '\n'.join(lines[1:])
            h_clean = h.replace('####', '').replace('###', '').replace('**', '').strip()
            time_m = re.match(r'^([\d:：]+－[\d:：]+|[\d:：]+)\s*(.*)', h_clean)
            slot_time = time_m.group(1) if time_m else ""
            slot_title_raw = time_m.group(2) if time_m else h_clean
            slot_title = clean_title(slot_title_raw)
            if not slot_title:
                continue
            cat, cat_zh, cat_icon = get_category_info(slot_title)
            maps_link = get_first_destination_map_link(2, slot_title_raw, b)
            summary = CUSTOM_SUMMARIES_V10.get((2, slot_title))
            if not summary:
                for (d, t), sm in CUSTOM_SUMMARIES_V10.items():
                    if d == 2 and ("吉野家" not in t and "宇奈とと" not in t and "上野" not in t and "長輩" not in t and "松坂屋" not in t and "兔屋" not in t) and (t in slot_title or slot_title in t):
                        summary = sm
                        break
            if not summary:
                summary = clean_markdown_for_summary(b)
            days_data[2]['kids'].append({
                'time': slot_time,
                'title': slot_title,
                'category': cat,
                'category_zh': cat_zh,
                'category_icon': cat_icon,
                'summary': summary,
                'maps_link': maps_link,
                'html_content': markdown_to_html(b.strip()),
                'has_modal': len(b.strip()) > 20
            })

    # Day 3（含 ☀️ 晴天方案／☔ 雨天方案 分流）
    # 分流標題是 `#### ☀️ **晴天方案**`，井號後面不是 `**`，所以這裡的切分正則
    # 不能沿用 `#{3,4} \*\*`，必須放寬成 `#{3,4} `，讓標記行自己成為一個區塊。
    d3_match = re.search(r'## \*\*📅 Day 3.*?\n(.*?)(?=\n## \*\*📅 Day 4|\Z)', content, re.DOTALL)
    if d3_match:
        slots = re.split(r'\n(?=#{3,4} )', d3_match.group(1))
        current_sub = 'common_before'
        for s in slots:
            s = s.strip()
            if not s:
                continue
            s_lines = s.split('\n')
            h = s_lines[0]
            b = '\n'.join(s_lines[1:])

            if '晴天方案' in h:
                current_sub = 'sunny'
                continue
            elif '雨天方案' in h:
                current_sub = 'rainy'
                continue

            h_clean = h.replace('####', '').replace('###', '').replace('**', '').strip()
            time_m = re.match(r'^([\d:：]+－[\d:：]+|[\d:：]+)\s*(.*)', h_clean)
            slot_time = time_m.group(1) if time_m else ""
            slot_title_raw = time_m.group(2) if time_m else h_clean
            slot_title = clean_title(slot_title_raw)
            if not slot_title:
                continue
            cat, cat_zh, cat_icon = get_category_info(slot_title)
            summary = CUSTOM_SUMMARIES_V10.get((3, slot_title))
            if not summary:
                for (d, t), sm in CUSTOM_SUMMARIES_V10.items():
                    if d == 3 and (t in slot_title or slot_title in t):
                        summary = sm
                        break
            if not summary:
                summary = clean_markdown_for_summary(b)
            days_data[3][current_sub].append({
                'time': slot_time,
                'title': slot_title,
                'category': cat,
                'category_zh': cat_zh,
                'category_icon': cat_icon,
                'summary': summary,
                'maps_link': get_first_destination_map_link(3, slot_title_raw, b),
                'html_content': markdown_to_html(b.strip()),
                'has_modal': len(b.strip()) > 20
            })
            # 雨天區塊以水平線收尾，之後的時段是晴雨共用的下半天
            if current_sub == 'rainy' and b.rstrip().endswith('---'):
                current_sub = 'common_after'

    # Day 4, 6
    for day in [4, 6]:
        d_match = re.search(rf'## \*\*📅 Day {day}.*?\n(.*?)(?=\n## \*\*📅 Day {day+1}|\Z)', content, re.DOTALL)
        if d_match:
            slots = re.split(r'\n(?=#{3,4} \*\*)', d_match.group(1))
            for s in slots:
                s = s.strip()
                if not s:
                    continue
                lines = s.split('\n')
                h = lines[0]
                b = '\n'.join(lines[1:])
                h_clean = h.replace('####', '').replace('###', '').replace('**', '').strip()
                time_m = re.match(r'^([\d:：]+－[\d:：]+|[\d:：]+)\s*(.*)', h_clean)
                slot_time = time_m.group(1) if time_m else ""
                slot_title_raw = time_m.group(2) if time_m else h_clean
                slot_title = clean_title(slot_title_raw)
                if not slot_title:
                    continue
                cat, cat_zh, cat_icon = get_category_info(slot_title)
                maps_link = get_first_destination_map_link(day, slot_title_raw, b)
                summary = CUSTOM_SUMMARIES_V10.get((day, slot_title))
                if not summary:
                    for (d, t), sm in CUSTOM_SUMMARIES_V10.items():
                        if d == day and (t in slot_title or slot_title in t):
                            summary = sm
                            break
                if not summary:
                    summary = clean_markdown_for_summary(b)
                days_data[day].append({
                    'time': slot_time,
                    'title': slot_title,
                    'category': cat,
                    'category_zh': cat_zh,
                    'category_icon': cat_icon,
                    'summary': summary,
                    'maps_link': maps_link,
                    'html_content': markdown_to_html(b.strip()),
                    'has_modal': len(b.strip()) > 20
                })

    # Day 5
    d5_match = re.search(r'## \*\*📅 Day 5.*?\n(.*?)(?=\n## \*\*📅 Day 6|\Z)', content, re.DOTALL)
    if d5_match:
        slots = re.split(r'\n(?=#{3,4} \*\*)', d5_match.group(1))
        current_sub = 'common_before'
        for s in slots:
            s = s.strip()
            if not s:
                continue
            s_lines = s.split('\n')
            h = s_lines[0]
            b = '\n'.join(s_lines[1:])
            
            if '雨天備案' in h or '台場科技' in h:
                current_sub = 'rainy'
                continue
            elif 'Plan A' in h:
                current_sub = 'plan_a'
                continue
            elif 'Plan B' in h:
                current_sub = 'plan_b'
                continue
            elif '動態決策' in h or '下午/傍晚' in h:
                continue

            h_clean = h.replace('####', '').replace('###', '').replace('**', '').strip()
            time_m = re.match(r'^([\d:：]+－[\d:：]+|[\d:：]+)\s*(.*)', h_clean)
            slot_time = time_m.group(1) if time_m else ""
            slot_title_raw = time_m.group(2) if time_m else h_clean
            slot_title = clean_title(slot_title_raw)
            if not slot_title:
                continue
            cat, cat_zh, cat_icon = get_category_info(slot_title)
            maps_link = get_first_destination_map_link(5, slot_title_raw, b)
            summary = CUSTOM_SUMMARIES_V10.get((5, slot_title))
            if not summary:
                for (d, t), sm in CUSTOM_SUMMARIES_V10.items():
                    if d == 5 and (t in slot_title or slot_title in t):
                        summary = sm
                        break
            if not summary:
                summary = clean_markdown_for_summary(b)
            days_data[5][current_sub].append({
                'time': slot_time,
                'title': slot_title,
                'category': cat,
                'category_zh': cat_zh,
                'category_icon': cat_icon,
                'summary': summary,
                'maps_link': maps_link,
                'html_content': markdown_to_html(b.strip()),
                'has_modal': len(b.strip()) > 20
            })

    return meta, days_data

ARTICLE_KEYWORDS = ('介紹文', '攻略', '文章', '教學', '懶人包', '菜單')

# 票務狀態標籤：在 README 時段內文寫「> 🎫 **票務狀態：已購票**」即可，
# 這樣 Docsify 版與 PWA 都看得到，且改標題時不會靜默失效。
TICKET_STATES = (
    ('已購票', 'ticket-done', '🎫 已購票'),
    ('已訂位', 'ticket-booked', '🍽️ 已訂位'),
    ('免費入場', 'ticket-free', '🆓 免費入場'),
    ('需購票', 'ticket-todo', '🎫 需購票'),
)


def detect_ticket_state(html_content):
    """回傳 (css_class, 標籤文字)，沒有標記則回傳 None。"""
    if not html_content:
        return None
    plain = re.sub(r'<[^>]+>', '', html_content)
    for keyword, css, label in TICKET_STATES:
        if f'票務狀態：{keyword}' in plain:
            return css, label
    return None


def count_articles(html_content):
    """數出該時段內文有幾篇可閱讀的外部文章（排除 Google Maps 導航連結）。"""
    if not html_content:
        return 0
    seen = set()
    for href, text in re.findall(r'<a\b[^>]*href="(https?://[^"]+)"[^>]*>(.*?)</a>',
                                 html_content, re.DOTALL):
        if 'google.com/maps' in href or 'maps.app.goo.gl' in href:
            continue
        plain = re.sub(r'<[^>]+>', '', text)
        if any(k in plain for k in ARTICLE_KEYWORDS):
            seen.add(href)
    return len(seen)


def render_prep_body(lines):
    """渲染行前段落的內文：連續的 `|` 開頭行合併成表格，其餘交給 markdown_to_html。"""
    parts = []
    buf = []
    table = []

    def flush_buf():
        if buf:
            parts.append(markdown_to_html('\n'.join(buf)))
            buf.clear()

    def flush_table():
        if not table:
            return
        rows = [[c.strip() for c in r.strip().strip('|').split('|')] for r in table]
        header, body = rows[0], [r for r in rows[1:] if set(''.join(r)) - set(': -')]
        html = '<div class="prep-table-wrap"><table class="prep-table"><thead><tr>'
        html += ''.join(f'<th>{format_inline_markdown(c)}</th>' for c in header)
        html += '</tr></thead><tbody>'
        for r in body:
            html += '<tr>' + ''.join(f'<td>{format_inline_markdown(c)}</td>' for c in r) + '</tr>'
        parts.append(html + '</tbody></table></div>')
        table.clear()

    for line in lines:
        stripped = line.strip()
        if stripped.startswith('|'):
            flush_buf()
            table.append(stripped)
        elif stripped.startswith(('<details', '</details', '<summary')):
            # 摺疊區塊是原生 HTML，包進 <p> 會被瀏覽器拆壞
            flush_table()
            flush_buf()
            parts.append(stripped)
        else:
            flush_table()
            # 略過分隔線與只有 `>` 的空引用行（後者會產生空 <p>）
            if stripped not in ('---', '>'):
                # 還原 Markdown 逸出字元（README 用 `1\.`、`\=` 避免被誤解析）
                buf.append(re.sub(r'\\([.\-=+#|*_`])', r'\1', line))
    flush_table()
    flush_buf()
    return '\n'.join(parts)


def render_prep_html(md_text, meta):
    """把 Day 1 之前的行前 Markdown 轉成「📌 行前」頁籤的 HTML。"""
    if not md_text:
        return ''
    html = ''
    for block in re.split(r'\n(?=## \*\*)', md_text):
        lines = block.strip().split('\n')
        if not lines or not lines[0].startswith('## '):
            continue
        heading = lines[0].lstrip('#').strip().strip('*').replace('\\', '')
        html += f'      <div class="prep-block">\n        <h3 class="prep-title">{heading}</h3>\n'
        html += render_prep_body(lines[1:])
        # README 的住宿地址是羅馬拼音，給計程車司機看的日文地址只有這裡有
        if '住宿資訊' in heading and meta.get('hotel_jp_addr'):
            jp_addr = meta['hotel_jp_addr']
            html += (f'\n        <div class="prep-copy-row">'
                     f'<span class="prep-copy-label">🚕 給司機看</span>'
                     f'<span class="prep-copy-val">{jp_addr}</span>'
                     f'<button class="copy-btn" onclick="copyText(\'{jp_addr}\', \'已複製日文地址！\')">複製</button>'
                     f'</div>')
        html += '\n      </div>\n'
    return html


def build_card_html(item_id, item):
    btn_html = ""
    if item['has_modal']:
        btn_html = f'<button class="view-original-btn" onclick="openOriginalModal(\'card-item-{item_id}\')">📖 完整說明與祕訣</button>'
        
    ticket = detect_ticket_state(item.get('html_content', ''))
    ticket_tag_html = ''
    if ticket:
        css, label = ticket
        ticket_tag_html = f'<span class="tag tag-{css}">{label}</span>'

    n_articles = count_articles(item.get('html_content', ''))
    article_tag_html = ""
    if n_articles:
        label = f'📄 攻略 {n_articles}' if n_articles > 1 else '📄 攻略'
        title = f'此時段有 {n_articles} 篇介紹文／攻略可閱讀，點我展開完整說明'
        article_tag_html = (
            f'<button class="tag tag-article" title="{title}" '
            f'onclick="openOriginalModal(\'card-item-{item_id}\')">{label}</button>'
        )

    action_btn_html = ""
    if item.get('maps_link'):
        action_btn_html = f"""<div class="card-actions">
              <a class="map-link-btn" href="{item['maps_link']}" target="_blank" title="開啟 Google Maps 導航（此時段第一個目的地）">📍 導航</a>
            </div>"""

    return f"""      <div class="timeline-item" data-category="{item['category']}">
        <div class="timeline-check">
          <label class="check-wrapper" title="標記已完成">
            <input type="checkbox" id="item-{item_id}" onchange="toggleCheck('item-{item_id}')">
            <span class="checkmark"></span>
          </label>
          <div class="timeline-line"></div>
        </div>
        <div class="timeline-card" id="card-item-{item_id}">
          <div class="card-header">
            <span class="card-time">{item['time']}</span>
            <div class="card-tags">
              {ticket_tag_html}{article_tag_html}<span class="tag tag-{item['category']}">{item['category_icon']} {item['category_zh']}</span>
            </div>
          </div>
          <h3 class="card-title">
            <span>{item['title']}</span>
            {action_btn_html}
          </h3>
          <div class="card-body">
            <p class="card-summary">{item['summary']}</p>
            {btn_html}
            <div class="original-content-holder" style="display: none;">
              {item['html_content']}
            </div>
          </div>
        </div>
      </div>\n"""

def render_full_pwa_html(meta, days_data):
    timeline_html = ""

    # 行前（Day 1 之前的段落）
    prep_body = render_prep_html(meta.get('preamble', ''), meta)
    if prep_body:
        timeline_html += """    <!-- 行前 Section -->
    <div class="prep-section" id="prep-section" style="display: none;">
      <div class="day-overview-header">
        <h2 class="day-overview-title">行前必讀：航班住宿 × 搭車提醒 × 全程總覽</h2>
      </div>
""" + prep_body + "    </div>\n\n"

    # Day 1
    timeline_html += """    <!-- Day 1 Section -->
    <div class="day-section" id="day1-section">
      <div class="day-overview-header">
        <h2 class="day-overview-title">抵達東京 × 秋葉原慢遊</h2>
      </div>
      <div class="sub-toggle-wrapper">
        <div class="sub-toggle-container">
          <button class="sub-toggle-btn active" onclick="switchDay1Plan('A')">🌟 Plan A：秋葉原漫遊（拍貼/扭蛋/壽司郎）</button>
          <button class="sub-toggle-btn" onclick="switchDay1Plan('B')">🌃 Plan B：新宿 3D 巨貓（Gusto家庭餐廳）</button>
        </div>
      </div>
"""
    for idx, it in enumerate(days_data[1]['common_before']):
        timeline_html += build_card_html(f"d1-cb{idx}", it)
    
    timeline_html += '      <div class="day1-plan-A">\n'
    for idx, it in enumerate(days_data[1]['plan_a']):
        timeline_html += build_card_html(f"d1-pa{idx}", it)
    timeline_html += '      </div>\n'
    
    timeline_html += '      <div class="day1-plan-B" style="display: none;">\n'
    for idx, it in enumerate(days_data[1]['plan_b']):
        timeline_html += build_card_html(f"d1-pb{idx}", it)
    timeline_html += '      </div>\n'
    
    for idx, it in enumerate(days_data[1]['common_after']):
        timeline_html += build_card_html(f"d1-ca{idx}", it)
    timeline_html += '    </div>\n\n'

    # Day 2
    timeline_html += """    <!-- Day 2 Section -->
    <div class="day-section" id="day2-section" style="display: none;">
      <div class="day-overview-header">
        <h2 class="day-overview-title">雙線交織：上野漫遊 (長輩組) ＆ 迪士尼樂園 (親子組)</h2>
      </div>
      <div class="sub-toggle-wrapper">
        <div class="sub-toggle-container">
          <button class="sub-toggle-btn active" id="day2-btn-parents" onclick="switchDay2Group('parents')">👵 長輩組：上野松坂屋 × 國立西洋美術館 × 鰻魚飯</button>
          <button class="sub-toggle-btn" id="day2-btn-kids" onclick="switchDay2Group('kids')">🏰 親子組：東京迪士尼樂園全日歡樂體驗</button>
        </div>
      </div>
      <div class="day2-parents-itinerary">
        <div class="sub-toggle-wrapper" style="margin-top: 10px; margin-bottom: 16px;">
          <div class="sub-toggle-container">
            <button class="sub-toggle-btn active" id="day2-parents-btn-sunny" onclick="switchDay2ParentsPlan('sunny')">☀️ 晴天方案：不忍池 × 戶外散步 × 西洋美術館</button>
            <button class="sub-toggle-btn" id="day2-parents-btn-rainy" onclick="switchDay2ParentsPlan('rainy')">☔ 雨天備案：東京國立博物館 × 松坂屋室內展</button>
          </div>
        </div>
        <div class="day2-parents-common-before">
"""
    for idx, it in enumerate(days_data[2]['parents']['common_before']):
        timeline_html += build_card_html(f"d2p-cb{idx}", it)
    timeline_html += """        </div>
        <div class="day2-parents-sunny">
"""
    for idx, it in enumerate(days_data[2]['parents']['sunny']):
        timeline_html += build_card_html(f"d2p-sunny{idx}", it)
    timeline_html += """        </div>
        <div class="day2-parents-rainy" style="display: none;">
"""
    for idx, it in enumerate(days_data[2]['parents']['rainy']):
        timeline_html += build_card_html(f"d2p-rainy{idx}", it)
    timeline_html += """        </div>
        <div class="day2-parents-common-after">
"""
    for idx, it in enumerate(days_data[2]['parents']['common_after']):
        timeline_html += build_card_html(f"d2p-ca{idx}", it)
    timeline_html += """        </div>
      </div>
      <div class="day2-kids-itinerary" style="display: none;">
"""
    for idx, it in enumerate(days_data[2]['kids']):
        timeline_html += build_card_html(f"d2k-{idx}", it)
    timeline_html += '      </div>\n    </div>\n\n'
    # Day 3
    timeline_html += """    <!-- Day 3 Section -->
    <div class="day-section" id="day3-section" style="display: none;">
      <div class="day-overview-header">
        <h2 class="day-overview-title">東京車站菓子樂園 × 科學博物館探險 × 阿美橫丁採買</h2>
      </div>
      <div class="sub-toggle-wrapper">
        <div class="sub-toggle-container">
          <button class="sub-toggle-btn active" id="day3-btn-sunny" onclick="switchDay3Plan('sunny')">☀️ 晴天方案：菓子樂園 × KITTE 頂樓花園</button>
          <button class="sub-toggle-btn" id="day3-btn-rainy" onclick="switchDay3Plan('rainy')">☔ 雨天方案：GRANSTA × Intermediatheque</button>
        </div>
      </div>
"""
    for idx, it in enumerate(days_data[3]['common_before']):
        timeline_html += build_card_html(f"d3-cb{idx}", it)

    timeline_html += '      <div class="day3-plan-sunny">\n'
    for idx, it in enumerate(days_data[3]['sunny']):
        timeline_html += build_card_html(f"d3-s{idx}", it)
    timeline_html += '      </div>\n'

    timeline_html += '      <div class="day3-plan-rainy" style="display: none;">\n'
    for idx, it in enumerate(days_data[3]['rainy']):
        timeline_html += build_card_html(f"d3-r{idx}", it)
    timeline_html += '      </div>\n'

    for idx, it in enumerate(days_data[3]['common_after']):
        timeline_html += build_card_html(f"d3-ca{idx}", it)
    timeline_html += '    </div>\n\n'

    # Day 4
    timeline_html += """    <!-- Day 4 Section -->
    <div class="day-section" id="day4-section" style="display: none;">
      <div class="day-overview-header">
        <h2 class="day-overview-title">吉卜力美術館 × 哈莫尼卡橫丁 × 吉祥寺商圈漫遊</h2>
      </div>
"""
    for idx, it in enumerate(days_data[4]):
        timeline_html += build_card_html(f"d4-{idx}", it)
    timeline_html += '    </div>\n\n'

    # Day 5
    timeline_html += """    <!-- Day 5 Section -->
    <div class="day-section" id="day5-section" style="display: none;">
      <div class="day-overview-header">
        <h2 class="day-overview-title">下町風情 × 晴空塔水族館 × 新宿都廳百萬夜景</h2>
      </div>
      <div class="sub-toggle-wrapper">
        <div class="sub-toggle-container">
          <button class="sub-toggle-btn active" id="day5-btn-planA" onclick="switchDay5Plan('A')">🌃 晴天 Plan A：新宿都廳夜景</button>
          <button class="sub-toggle-btn" id="day5-btn-planB" onclick="switchDay5Plan('B')">🛍️ 晴天 Plan B：晴空街道晚餐</button>
          <button class="sub-toggle-btn" id="day5-btn-rainy" onclick="switchDay5Plan('rainy')">☔ 雨天備案：台場 × 微縮世界</button>
        </div>
      </div>
      <div class="day5-sunny-common">
"""
    for idx, it in enumerate(days_data[5]['common_before']):
        timeline_html += build_card_html(f"d5-cb{idx}", it)
    timeline_html += """      </div>
      <div class="day5-plan-A">
"""
    for idx, it in enumerate(days_data[5]['plan_a']):
        timeline_html += build_card_html(f"d5-pa{idx}", it)
    timeline_html += """      </div>
      <div class="day5-plan-B" style="display: none;">
"""
    for idx, it in enumerate(days_data[5]['plan_b']):
        timeline_html += build_card_html(f"d5-pb{idx}", it)
    timeline_html += """      </div>
      <div class="day5-plan-rainy" style="display: none;">
"""
    for idx, it in enumerate(days_data[5]['rainy']):
        timeline_html += build_card_html(f"d5-rainy{idx}", it)
    timeline_html += '      </div>\n    </div>\n\n'

    # Day 6
    timeline_html += """    <!-- Day 6 Section -->
    <div class="day-section" id="day6-section" style="display: none;">
      <div class="day-overview-header">
        <h2 class="day-overview-title">築地晨間美食巡禮 × 回程前往機場</h2>
      </div>
"""
    for idx, it in enumerate(days_data[6]):
        timeline_html += build_card_html(f"d6-{idx}", it)
    timeline_html += '    </div>\n\n'

    full_page = f"""<!DOCTYPE html>
<html lang="zh-TW">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
  <meta name="theme-color" content="#12141c">
  <meta name="apple-mobile-web-app-capable" content="yes">
  <meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
  <meta name="apple-mobile-web-app-title" content="東京自由行2026">
  <title>2026 東京 6天5夜親子自由行 V10</title>
  
  <link rel="manifest" href="manifest.json">
  <link rel="apple-touch-icon" href="icon-192.png">
  
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700&family=Noto+Sans+TC:wght@300;400;500;700&display=swap" rel="stylesheet">
  
  <style>
    :root {{
      --bg-dark: #0f111a;
      --card-bg: rgba(23, 27, 40, 0.85);
      --card-border: rgba(255, 255, 255, 0.08);
      --accent-coral: #E45F56;
      --accent-blue: #38bdf8;
      --accent-green: #34d399;
      --accent-purple: #a78bfa;
      --accent-gold: #fbbf24;
      --text-main: #f3f4f6;
      --text-muted: #94a3b8;
      --shadow-premium: 0 10px 30px -10px rgba(0, 0, 0, 0.5);
      --blur-strength: 16px;
      --transition-smooth: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
    }}

    * {{
      box-sizing: border-box;
      margin: 0;
      padding: 0;
      -webkit-tap-highlight-color: transparent;
    }}

    body {{
      font-family: 'Outfit', 'Noto Sans TC', sans-serif;
      background-color: var(--bg-dark);
      color: var(--text-main);
      line-height: 1.5;
      padding-bottom: 90px;
      background-image: 
        radial-gradient(circle at 10% 20%, rgba(228, 95, 86, 0.08) 0%, transparent 40%),
        radial-gradient(circle at 90% 80%, rgba(56, 189, 248, 0.08) 0%, transparent 40%);
      background-attachment: fixed;
    }}

    .app-header {{
      background: rgba(15, 17, 26, 0.92);
      backdrop-filter: blur(var(--blur-strength));
      -webkit-backdrop-filter: blur(var(--blur-strength));
      border-bottom: 1px solid var(--card-border);
      position: sticky;
      top: 0;
      z-index: 100;
      padding: 12px 16px 8px;
    }}

    .header-top {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 8px;
    }}

    .app-title {{
      font-size: 1.15rem;
      font-weight: 700;
      color: #fff;
      display: flex;
      align-items: center;
      gap: 6px;
    }}

    .font-size-btn {{
      flex: 0 0 auto;
      min-height: 44px;
      padding: 6px 12px;
      margin-left: auto;
      border-radius: 12px;
      border: 1px solid var(--card-border);
      background: rgba(255, 255, 255, 0.06);
      color: var(--text-main);
      font-size: 0.78rem;
      font-weight: 600;
      cursor: pointer;
      white-space: nowrap;
      transition: var(--transition-smooth);
    }}
    .font-size-btn:active {{
      background: rgba(255, 255, 255, 0.16);
    }}

    .progress-bar-container {{
      height: 4px;
      background: rgba(255, 255, 255, 0.1);
      border-radius: 2px;
      overflow: hidden;
      margin-bottom: 10px;
    }}
    .progress-bar-fill {{
      height: 100%;
      background: linear-gradient(90deg, var(--accent-coral), var(--accent-blue));
      width: 0%;
      transition: width 0.3s ease;
    }}

    .day-tabs {{
      display: flex;
      gap: 6px;
      overflow-x: auto;
      padding-bottom: 4px;
      scrollbar-width: none;
    }}
    .day-tabs::-webkit-scrollbar {{
      display: none;
    }}

    .day-tab {{
      flex: 0 0 auto;
      padding: 6px 14px;
      border-radius: 20px;
      border: 1px solid var(--card-border);
      background: rgba(255, 255, 255, 0.05);
      color: var(--text-muted);
      font-size: 0.85rem;
      font-weight: 600;
      cursor: pointer;
      transition: var(--transition-smooth);
      white-space: nowrap;
    }}

    .day-tab.active {{
      background: var(--accent-coral);
      color: #fff;
      border-color: var(--accent-coral);
      box-shadow: 0 4px 12px rgba(228, 95, 86, 0.35);
    }}

    .prep-section {{
      padding: 0 16px 24px;
    }}
    .prep-block {{
      background: var(--card-bg);
      backdrop-filter: blur(var(--blur-strength));
      border: 1px solid var(--card-border);
      border-radius: 14px;
      padding: 14px 16px;
      margin-bottom: 14px;
    }}
    .prep-title {{
      font-size: 1.02rem;
      font-weight: 700;
      color: var(--accent-gold);
      margin-bottom: 10px;
      padding-bottom: 8px;
      border-bottom: 1px solid var(--card-border);
    }}
    .prep-block p {{
      font-size: 0.9rem;
      line-height: 1.7;
      margin-bottom: 8px;
    }}
    .prep-block .modal-list li {{
      font-size: 0.9rem;
      line-height: 1.7;
    }}
    .prep-table-wrap {{
      overflow-x: auto;
      -webkit-overflow-scrolling: touch;
      margin-bottom: 10px;
    }}
    .prep-table {{
      border-collapse: collapse;
      width: 100%;
      min-width: 520px;
      font-size: 0.82rem;
    }}
    .prep-table th, .prep-table td {{
      border: 1px solid var(--card-border);
      padding: 8px 10px;
      text-align: left;
      vertical-align: top;
      line-height: 1.6;
    }}
    .prep-table th {{
      background: rgba(255, 255, 255, 0.06);
      font-weight: 700;
      white-space: nowrap;
    }}
    .prep-table td:first-child {{
      text-align: center;
      /* 不用 nowrap：長店名會把第一欄撐到數百 px，把後面的欄位擠掉。
         改為限寬換行，短標籤（時間、樓層）照樣維持單行。 */
      max-width: 11em;
      word-break: break-word;
    }}
    .prep-table td:nth-child(2) {{
      min-width: 11em;
    }}

    .prep-copy-row {{
      display: flex;
      align-items: center;
      gap: 8px;
      flex-wrap: wrap;
      margin-top: 8px;
      padding: 8px 10px;
      background: rgba(255, 255, 255, 0.05);
      border-radius: 8px;
      font-size: 0.86rem;
    }}
    .prep-copy-label {{
      color: var(--text-muted);
      white-space: nowrap;
    }}
    .prep-copy-val {{
      font-weight: 600;
      color: #fff;
    }}

    .copy-btn {{
      background: rgba(255, 255, 255, 0.1);
      border: 1px solid rgba(255, 255, 255, 0.15);
      color: var(--accent-blue);
      border-radius: 6px;
      padding: 2px 8px;
      font-size: 0.75rem;
      cursor: pointer;
      margin-left: 6px;
      text-decoration: none;
    }}

    .day-overview-header {{
      margin: 8px 16px 12px;
      padding: 10px 14px;
      background: linear-gradient(135deg, rgba(255, 255, 255, 0.07) 0%, rgba(255, 255, 255, 0.02) 100%);
      border: 1px solid var(--card-border);
      border-radius: 12px;
      backdrop-filter: blur(var(--blur-strength));
      text-align: center;
    }}
    .day-overview-title {{
      font-size: 0.95rem;
      font-weight: 700;
      color: #fff;
      line-height: 1.4;
      margin: 0;
    }}

    .sub-toggle-wrapper {{
      margin: 8px 16px 16px;
    }}
    .sub-toggle-container {{
      display: flex;
      background: rgba(0, 0, 0, 0.3);
      padding: 4px;
      border-radius: 12px;
      border: 1px solid var(--card-border);
      gap: 4px;
    }}
    .sub-toggle-btn {{
      flex: 1;
      border: none;
      background: transparent;
      color: var(--text-muted);
      padding: 8px 6px;
      font-size: 0.8rem;
      font-weight: 600;
      border-radius: 8px;
      cursor: pointer;
      transition: var(--transition-smooth);
      text-align: center;
      line-height: 1.3;
    }}
    .sub-toggle-btn.active {{
      background: rgba(255, 255, 255, 0.12);
      color: #fff;
      box-shadow: 0 2px 8px rgba(0, 0, 0, 0.3);
    }}

    .timeline-container {{
      padding: 0 16px;
    }}

    .timeline-item {{
      display: flex;
      gap: 12px;
      margin-bottom: 14px;
      position: relative;
    }}

    .timeline-check {{
      display: flex;
      flex-direction: column;
      align-items: center;
      width: 28px;
      flex-shrink: 0;
      padding-top: 4px;
    }}

    .check-wrapper {{
      position: relative;
      cursor: pointer;
      width: 26px;
      height: 26px;
      display: inline-block;
    }}
    /* 把觸控範圍撐到 44x44（iOS/Android 人體工學下限），但不佔版面 */
    .check-wrapper::before {{
      content: "";
      position: absolute;
      top: -9px;
      left: -9px;
      right: -9px;
      bottom: -9px;
    }}
    .check-wrapper input {{
      opacity: 0;
      width: 0;
      height: 0;
    }}
    .checkmark {{
      position: absolute;
      top: 0;
      left: 0;
      height: 26px;
      width: 26px;
      background-color: rgba(255, 255, 255, 0.12);
      border: 2px solid rgba(255, 255, 255, 0.6);
      border-radius: 8px;
      box-shadow: inset 0 1px 2px rgba(0, 0, 0, 0.35);
      transition: var(--transition-smooth);
    }}
    .check-wrapper:hover input ~ .checkmark {{
      border-color: var(--accent-coral);
      background-color: rgba(255, 255, 255, 0.2);
    }}
    .check-wrapper input:focus-visible ~ .checkmark {{
      outline: 2px solid var(--accent-gold);
      outline-offset: 2px;
    }}
    .check-wrapper input:checked ~ .checkmark {{
      background-color: var(--accent-green);
      border-color: var(--accent-green);
      box-shadow: 0 0 0 3px rgba(52, 211, 153, 0.28);
    }}
    .checkmark:after {{
      content: "";
      position: absolute;
      display: none;
    }}
    .check-wrapper input:checked ~ .checkmark:after {{
      display: block;
      left: 8px;
      top: 3px;
      width: 6px;
      height: 12px;
      border: solid #0f172a;
      border-width: 0 3px 3px 0;
      transform: rotate(45deg);
    }}

    .timeline-line {{
      width: 2px;
      background: rgba(255, 255, 255, 0.08);
      flex: 1;
      margin-top: 6px;
      border-radius: 1px;
    }}

    .timeline-card {{
      flex: 1;
      background: var(--card-bg);
      backdrop-filter: blur(var(--blur-strength));
      -webkit-backdrop-filter: blur(var(--blur-strength));
      border: 1px solid var(--card-border);
      border-radius: 14px;
      padding: 12px 14px;
      box-shadow: var(--shadow-premium);
      transition: var(--transition-smooth);
    }}

    .timeline-item.completed .timeline-card {{
      opacity: 0.55;
      filter: grayscale(0.2);
    }}

    .card-header {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 6px;
    }}

    .card-time {{
      font-size: 0.8rem;
      font-weight: 700;
      color: var(--accent-gold);
      letter-spacing: 0.5px;
    }}

    .card-tags {{
      display: flex;
      gap: 4px;
    }}

    .tag {{
      font-size: 0.7rem;
      padding: 2px 6px;
      border-radius: 6px;
      font-weight: 600;
    }}
    .tag-food {{ background: rgba(228, 95, 86, 0.2); color: #ff7b72; border: 1px solid rgba(228, 95, 86, 0.3); }}
    .tag-transport {{ background: rgba(56, 189, 248, 0.2); color: #7dd3fc; border: 1px solid rgba(56, 189, 248, 0.3); }}
    .tag-attraction {{ background: rgba(167, 139, 250, 0.2); color: #c4b5fd; border: 1px solid rgba(167, 139, 250, 0.3); }}
    .tag-stay {{ background: rgba(52, 211, 153, 0.2); color: #6ee7b7; border: 1px solid rgba(52, 211, 153, 0.3); }}

    /* 有介紹文／攻略可讀：點擊直接開啟完整說明抽屜 */
    .tag-article {{
      background: rgba(245, 158, 11, 0.22);
      color: #fcd34d;
      border: 1px solid rgba(245, 158, 11, 0.45);
      font-family: inherit;
      cursor: pointer;
      -webkit-tap-highlight-color: transparent;
      transition: transform 0.15s ease, background 0.15s ease;
    }}
    .tag-article:hover, .tag-article:active {{
      background: rgba(245, 158, 11, 0.38);
      transform: translateY(-1px);
    }}

    /* 票務狀態：已購票／已訂位為綠色（安心），需購票為紅色（待辦） */
    .tag-ticket-done {{ background: rgba(34, 197, 94, 0.22); color: #86efac; border: 1px solid rgba(34, 197, 94, 0.45); }}
    .tag-ticket-booked {{ background: rgba(34, 197, 94, 0.22); color: #86efac; border: 1px solid rgba(34, 197, 94, 0.45); }}
    .tag-ticket-free {{ background: rgba(56, 189, 248, 0.2); color: #7dd3fc; border: 1px solid rgba(56, 189, 248, 0.4); }}
    .tag-ticket-todo {{
      background: rgba(239, 68, 68, 0.22);
      color: #fca5a5;
      border: 1px solid rgba(239, 68, 68, 0.5);
      animation: ticketPulse 2.4s ease-in-out infinite;
    }}
    @keyframes ticketPulse {{
      0%, 100% {{ box-shadow: 0 0 0 0 rgba(239, 68, 68, 0); }}
      50% {{ box-shadow: 0 0 0 3px rgba(239, 68, 68, 0.18); }}
    }}

    .card-title {{
      font-size: 0.98rem;
      font-weight: 700;
      color: #fff;
      margin-bottom: 6px;
      display: flex;
      justify-content: space-between;
      align-items: flex-start;
      gap: 8px;
    }}

    .card-actions {{
      display: flex;
      gap: 4px;
      flex-shrink: 0;
    }}

    .map-link-btn {{
      display: inline-flex;
      align-items: center;
      background: rgba(56, 189, 248, 0.15);
      color: var(--accent-blue);
      border: 1px solid rgba(56, 189, 248, 0.3);
      padding: 3px 8px;
      border-radius: 6px;
      font-size: 0.72rem;
      font-weight: 600;
      text-decoration: none;
      transition: var(--transition-smooth);
    }}
    .map-link-btn:hover {{
      background: var(--accent-blue);
      color: #000;
    }}

    .card-summary {{
      font-size: 0.85rem;
      color: #cbd5e1;
      line-height: 1.45;
      margin-bottom: 8px;
    }}

    .view-original-btn {{
      background: rgba(255, 255, 255, 0.06);
      border: 1px solid rgba(255, 255, 255, 0.12);
      color: #e2e8f0;
      width: 100%;
      padding: 6px 10px;
      border-radius: 8px;
      font-size: 0.78rem;
      font-weight: 600;
      cursor: pointer;
      transition: var(--transition-smooth);
      display: flex;
      justify-content: center;
      align-items: center;
      gap: 4px;
    }}
    .view-original-btn:hover {{
      background: rgba(255, 255, 255, 0.12);
      color: #fff;
    }}

    .modal-overlay {{
      position: fixed;
      top: 0;
      left: 0;
      right: 0;
      bottom: 0;
      background: rgba(0, 0, 0, 0.65);
      backdrop-filter: blur(6px);
      z-index: 999;
      opacity: 0;
      visibility: hidden;
      transition: all 0.3s ease;
    }}
    .modal-overlay.active {{
      opacity: 1;
      visibility: visible;
    }}

    .modal-sheet {{
      position: fixed;
      left: 0;
      right: 0;
      bottom: 0;
      max-height: 85vh;
      background: #171b28;
      border-top-left-radius: 20px;
      border-top-right-radius: 20px;
      border-top: 1px solid rgba(255, 255, 255, 0.15);
      z-index: 1000;
      transform: translateY(100%);
      transition: transform 0.3s cubic-bezier(0.32, 1, 0.23, 1);
      display: flex;
      flex-direction: column;
    }}
    .modal-sheet.active {{
      transform: translateY(0);
    }}

    .sheet-handle {{
      width: 38px;
      height: 4px;
      background: rgba(255, 255, 255, 0.3);
      border-radius: 2px;
      margin: 10px auto 4px;
    }}

    .sheet-header {{
      padding: 10px 18px 12px;
      border-bottom: 1px solid var(--card-border);
      display: flex;
      justify-content: space-between;
      align-items: center;
    }}
    .sheet-title {{
      font-size: 1.05rem;
      font-weight: 700;
      color: #fff;
    }}
    .sheet-close {{
      background: rgba(255, 255, 255, 0.1);
      border: none;
      color: #fff;
      width: 28px;
      height: 28px;
      border-radius: 50%;
      font-size: 1.1rem;
      cursor: pointer;
      display: flex;
      align-items: center;
      justify-content: center;
    }}

    .sheet-body {{
      padding: 16px 18px 30px;
      overflow-y: auto;
      font-size: 0.9rem;
      color: #cbd5e1;
      line-height: 1.6;
    }}

    .modal-quote {{
      background: rgba(255, 255, 255, 0.04);
      border-left: 3px solid var(--accent-coral);
      padding: 10px 12px;
      border-radius: 0 8px 8px 0;
      margin-bottom: 12px;
    }}
    .modal-list {{
      padding-left: 18px;
      margin-bottom: 10px;
    }}
    .modal-list li {{
      margin-bottom: 6px;
    }}
    .map-link-inline {{
      color: var(--accent-blue);
      text-decoration: none;
      font-weight: 600;
    }}
    .map-link-inline:hover {{
      text-decoration: underline;
    }}

    .emergency-card {{
      margin: 16px;
      background: rgba(228, 95, 86, 0.08);
      border: 1px solid rgba(228, 95, 86, 0.25);
      border-radius: 14px;
      padding: 12px 14px;
    }}
    .emergency-header {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      cursor: pointer;
    }}
    .emergency-title {{
      font-size: 0.9rem;
      font-weight: 700;
      color: #ff7b72;
      display: flex;
      align-items: center;
      gap: 6px;
    }}

    .toast {{
      position: fixed;
      bottom: 24px;
      left: 50%;
      transform: translateX(-50%) translateY(100px);
      background: rgba(30, 41, 59, 0.95);
      backdrop-filter: blur(8px);
      color: #fff;
      padding: 10px 20px;
      border-radius: 24px;
      border: 1px solid rgba(255, 255, 255, 0.15);
      box-shadow: 0 10px 25px rgba(0,0,0,0.5);
      font-size: 0.85rem;
      font-weight: 500;
      z-index: 2000;
      transition: transform 0.3s cubic-bezier(0.4, 0, 0.2, 1);
      display: flex;
      align-items: center;
      gap: 8px;
    }}
    .toast.show {{
      transform: translateX(-50%) translateY(0);
    }}
  </style>
  <script>
    // 在畫面繪製前先套用上次選的字級，避免載入瞬間字體大小跳動
    (function () {{
      var pct = [90, 100, 115, 130][parseInt(localStorage.getItem('fontScaleIdx'), 10)];
      if (pct) document.documentElement.style.fontSize = pct + '%';
    }})();
  </script>
</head>
<body>

  <header class="app-header">
    <div class="header-top">
      <div class="app-title">
        <span>🗼 東京親子自由行</span>
      </div>
      <button class="font-size-btn" id="fontSizeBtn" onclick="cycleFontSize()" aria-label="調整文字大小">🔠 標準</button>
    </div>
    
    <div class="progress-bar-container">
      <div class="progress-bar-fill" id="progressBar"></div>
    </div>

    <nav class="day-tabs" id="dayTabs">
      <button class="day-tab" onclick="switchDay(0)">📌 置頂</button>
      <button class="day-tab active" onclick="switchDay(1)">D1 (8/20四)</button>
      <button class="day-tab" onclick="switchDay(2)">D2 (8/21五)</button>
      <button class="day-tab" onclick="switchDay(3)">D3 (8/22六)</button>
      <button class="day-tab" onclick="switchDay(4)">D4 (8/23日)</button>
      <button class="day-tab" onclick="switchDay(5)">D5 (8/24一)</button>
      <button class="day-tab" onclick="switchDay(6)">D6 (8/25二)</button>
    </nav>
  </header>

  <main class="timeline-container">
{timeline_html}
  </main>

  <section class="emergency-card">
    <div class="emergency-header" onclick="toggleEmergency()">
      <div class="emergency-title">🚨 緊急求助與重要指引</div>
      <span style="font-size: 0.8rem; color: #ff7b72;">展開 / 收合</span>
    </div>
    <div id="emergencyBody" style="display: none; margin-top: 10px; font-size: 0.82rem; color: #cbd5e1; line-height: 1.6;">
      <p><strong>📞 報警：</strong>110 | <strong>救護車/消防：</strong>119</p>
      <p><strong>🇹🇼 駐日代表處緊急聯絡電話：</strong>03-3280-7917（急難救助專用）</p>
      <p><strong>💳 兒童 Suica 遺失處理：</strong>憑購買時登記之護照姓名至 JR 綠色窗口補發。</p>
      <p><strong>⚠️ 退稅提醒：</strong>購物結帳前主動出示護照，食品/藥妝未稅滿 ¥5,000 即可享有免稅。</p>
    </div>
  </section>

  <div class="modal-overlay" id="modalOverlay" onclick="closeModal()"></div>
  <div class="modal-sheet" id="modalSheet">
    <div class="sheet-handle"></div>
    <div class="sheet-header">
      <div class="sheet-title" id="modalTitle">行程詳細說明</div>
      <button class="sheet-close" onclick="closeModal()">×</button>
    </div>
    <div class="sheet-body" id="modalBody"></div>
  </div>

  <div class="toast" id="toastBox">通知訊息</div>

  <script>
    let currentDay = 1;
    const STORAGE_KEY = 'tokyo_2026_checklist_v10';
    let checkedItems = JSON.parse(localStorage.getItem(STORAGE_KEY) || '{{}}');

    document.addEventListener('DOMContentLoaded', () => {{
      restoreChecklist();
      updateProgressBar();
      registerServiceWorker();
      initSwipeNavigation();
      applyFontSize(fontSizeIdx, false);
      restoreBranches();
      restoreLastPosition();
    }});

    // 還原上次選的分流（Plan A/B、長輩組/親子組、晴天/雨天）。
    // 必須在 restoreLastPosition() 之前跑：切換分流會改變頁面高度，
    // 先還原完才捲得到正確位置。
    function restoreBranches() {{
      const saved = [
        ['branchDay1', switchDay1Plan],
        ['branchDay2Group', switchDay2Group],
        ['branchDay2Parents', switchDay2ParentsPlan],
        ['branchDay3', switchDay3Plan],
        ['branchDay5', switchDay5Plan]
      ];
      saved.forEach(([key, fn]) => {{
        const val = localStorage.getItem(key);
        if (val) fn(val);
      }});
    }}

    // 記住上次看到哪一天與捲動位置。PWA 被系統回收後重新開啟時，
    // 預設會回到 D1，對正在看 Day 3 的人很不方便。
    function restoreLastPosition() {{
      // 先把捲動位置讀出來，switchDay() 會把它歸零（手動換天要回到頂端）
      const y = parseInt(localStorage.getItem('lastScroll'), 10);
      const day = parseInt(localStorage.getItem('lastDay'), 10);
      // 傳 false：這裡要回到「上次離開的捲動位置」，
      // 不能被「捲到第一個未勾選」蓋掉
      if (day >= 0 && day <= 6 && day !== currentDay) switchDay(day, false);

      if (y > 0) {{
        // 等版面與圖片穩定後再捲，否則會被 switchDay 的置頂蓋掉
        requestAnimationFrame(() => setTimeout(() => window.scrollTo({{ top: y }}), 120));
      }}
      ['visibilitychange', 'pagehide'].forEach(evt =>
        document.addEventListener(evt, () => localStorage.setItem('lastScroll', Math.round(window.scrollY))));
    }}

    // 文字大小：整份 CSS 都用 rem，所以只要改根字級就能整頁等比縮放。
    // 選擇存在 localStorage，下次開啟（含安裝成 App 後）沿用。
    const FONT_LEVELS = [
      {{ label: '小', pct: 90 }},
      {{ label: '標準', pct: 100 }},
      {{ label: '大', pct: 115 }},
      {{ label: '特大', pct: 130 }}
    ];
    let fontSizeIdx = (function () {{
      const saved = parseInt(localStorage.getItem('fontScaleIdx'), 10);
      return (saved >= 0 && saved < FONT_LEVELS.length) ? saved : 1;
    }})();

    function applyFontSize(idx, notify) {{
      fontSizeIdx = idx;
      const level = FONT_LEVELS[idx];
      document.documentElement.style.fontSize = level.pct + '%';
      localStorage.setItem('fontScaleIdx', idx);
      const btn = document.getElementById('fontSizeBtn');
      if (btn) btn.textContent = '🔠 ' + level.label;
      if (notify) showToast('文字大小：' + level.label);
    }}

    function cycleFontSize() {{
      applyFontSize((fontSizeIdx + 1) % FONT_LEVELS.length, true);
    }}

    // 左右滑動切換天數。刻意避開會橫向捲動的區域（總覽表格、頁籤列、
    // 分流按鈕列）與開啟中的抽屜，否則會跟它們自己的橫向捲動打架。
    function initSwipeNavigation() {{
      const NO_SWIPE = '.prep-table-wrap, .day-tabs, .sub-toggle-container, .modal-sheet';
      const MIN_DIST = 60;      // 位移不足視為誤觸
      const RATIO = 1.8;        // 橫向要明顯大於縱向，才不會擋到上下捲動
      const MAX_TIME = 600;     // 太慢的拖曳不算滑動
      let x0 = null, y0 = 0, t0 = 0, blocked = false;

      document.addEventListener('touchstart', e => {{
        if (e.touches.length !== 1) {{ x0 = null; return; }}
        const sheet = document.getElementById('modalSheet');
        blocked = !!(e.target.closest && e.target.closest(NO_SWIPE)) ||
                  !!(sheet && sheet.classList.contains('active'));
        x0 = e.touches[0].clientX;
        y0 = e.touches[0].clientY;
        t0 = Date.now();
      }}, {{ passive: true }});

      document.addEventListener('touchend', e => {{
        if (x0 === null || blocked) return;
        const dx = e.changedTouches[0].clientX - x0;
        const dy = e.changedTouches[0].clientY - y0;
        const dt = Date.now() - t0;
        x0 = null;
        if (dt > MAX_TIME) return;
        if (Math.abs(dx) < MIN_DIST || Math.abs(dx) < Math.abs(dy) * RATIO) return;
        const next = currentDay + (dx < 0 ? 1 : -1);
        if (next < 0 || next > 6) return;
        switchDay(next);
      }}, {{ passive: true }});
    }}

    // 換天時捲到「第一個還沒打勾的時段」，現場翻到當天就直接看到下一步要做什麼。
    // 全部打勾或找不到時退回置頂，行為與改動前一致。
    function scrollToFirstUnchecked(day) {{
      const toTop = () => window.scrollTo({{ top: 0, behavior: 'smooth' }});
      const sec = document.querySelectorAll('.day-section')[day - 1];
      if (day === 0 || !sec) return toTop();
      // offsetParent 為 null 代表被隱藏（例如另一個分支的卡片），要排除
      const pending = [...sec.querySelectorAll('.check-wrapper input[type="checkbox"]')]
        .filter(cb => cb.offsetParent !== null).find(cb => !cb.checked);
      const item = pending && (pending.closest('.timeline-item') || pending.closest('.timeline-card'));
      if (!item) return toTop();
      const header = document.querySelector('.app-header');
      const offset = (header ? header.offsetHeight : 0) + 12;
      const top = window.scrollY + item.getBoundingClientRect().top - offset;
      window.scrollTo({{ top: Math.max(0, top), behavior: 'smooth' }});
    }}

    function switchDay(day, autoScroll = true) {{
      currentDay = day;
      localStorage.setItem('lastDay', day);
      localStorage.setItem('lastScroll', 0);
      // 第 0 個頁籤是「📌 置頂」（行前資訊），其後才是 D1～D6
      document.querySelectorAll('.day-tab').forEach((tab, i) => {{
        tab.classList.toggle('active', i === day);
      }});
      const prep = document.getElementById('prep-section');
      if (prep) prep.style.display = (day === 0) ? 'block' : 'none';
      document.querySelectorAll('.day-section').forEach((sec, i) => {{
        sec.style.display = (i + 1 === day) ? 'block' : 'none';
      }});
      // 滑動切換時把作用中的頁籤帶進視野。只捲動頁籤列本身，
      // 不用 scrollIntoView——它會連帶動到頁面的垂直捲動，跟下面的置頂打架。
      const tabs = document.getElementById('dayTabs');
      const activeTab = document.querySelectorAll('.day-tab')[day];
      if (tabs && activeTab) {{
        tabs.scrollTo({{ left: activeTab.offsetLeft - (tabs.clientWidth - activeTab.clientWidth) / 2, behavior: 'smooth' }});
      }}
      if (autoScroll) {{
        // 等 display 切換後的版面重排完成再量位置，否則量到的是舊高度
        requestAnimationFrame(() => scrollToFirstUnchecked(day));
      }} else {{
        window.scrollTo({{ top: 0, behavior: 'smooth' }});
      }}
    }}

    function switchDay1Plan(plan) {{
      localStorage.setItem('branchDay1', plan);
      const isPlanA = plan === 'A';
      document.querySelectorAll('#day1-section .sub-toggle-btn')[0].classList.toggle('active', isPlanA);
      document.querySelectorAll('#day1-section .sub-toggle-btn')[1].classList.toggle('active', !isPlanA);
      document.querySelector('.day1-plan-A').style.display = isPlanA ? 'block' : 'none';
      document.querySelector('.day1-plan-B').style.display = isPlanA ? 'none' : 'block';
    }}

    function switchDay3Plan(plan) {{
      localStorage.setItem('branchDay3', plan);
      const isSunny = plan === 'sunny';
      document.getElementById('day3-btn-sunny').classList.toggle('active', isSunny);
      document.getElementById('day3-btn-rainy').classList.toggle('active', !isSunny);
      document.querySelector('.day3-plan-sunny').style.display = isSunny ? 'block' : 'none';
      document.querySelector('.day3-plan-rainy').style.display = isSunny ? 'none' : 'block';
    }}

    function switchDay2Group(group) {{
      localStorage.setItem('branchDay2Group', group);
      const isParents = group === 'parents';
      document.getElementById('day2-btn-parents').classList.toggle('active', isParents);
      document.getElementById('day2-btn-kids').classList.toggle('active', !isParents);
      document.querySelector('.day2-parents-itinerary').style.display = isParents ? 'block' : 'none';
      document.querySelector('.day2-kids-itinerary').style.display = isParents ? 'none' : 'block';
    }}

    function switchDay2ParentsPlan(plan) {{
      localStorage.setItem('branchDay2Parents', plan);
      const isSunny = plan === 'sunny';
      document.getElementById('day2-parents-btn-sunny').classList.toggle('active', isSunny);
      document.getElementById('day2-parents-btn-rainy').classList.toggle('active', !isSunny);
      const sunnyElem = document.querySelector('.day2-parents-sunny');
      if (sunnyElem) {{
        sunnyElem.style.display = isSunny ? 'block' : 'none';
      }}
      const rainyElem = document.querySelector('.day2-parents-rainy');
      if (rainyElem) {{
        rainyElem.style.display = isSunny ? 'none' : 'block';
      }}
    }}

    function switchDay5Plan(plan) {{
      localStorage.setItem('branchDay5', plan);
      const isPlanA = plan === 'A';
      const isPlanB = plan === 'B';
      const isRainy = plan === 'rainy';
      
      document.getElementById('day5-btn-planA').classList.toggle('active', isPlanA);
      document.getElementById('day5-btn-planB').classList.toggle('active', isPlanB);
      document.getElementById('day5-btn-rainy').classList.toggle('active', isRainy);
      
      const commonElem = document.querySelector('.day5-sunny-common');
      if (commonElem) {{
        commonElem.style.display = isRainy ? 'none' : 'block';
      }}
      
      const planAElem = document.querySelector('.day5-plan-A');
      if (planAElem) {{
        planAElem.style.display = isPlanA ? 'block' : 'none';
      }}
      
      const planBElem = document.querySelector('.day5-plan-B');
      if (planBElem) {{
        planBElem.style.display = isPlanB ? 'block' : 'none';
      }}
      
      const rainyElem = document.querySelector('.day5-plan-rainy');
      if (rainyElem) {{
        rainyElem.style.display = isRainy ? 'block' : 'none';
      }}
    }}

    function toggleCheck(id) {{
      const cb = document.getElementById(id);
      if (cb) {{
        checkedItems[id] = cb.checked;
        localStorage.setItem(STORAGE_KEY, JSON.stringify(checkedItems));
        const itemElem = cb.closest('.timeline-item');
        if (itemElem) {{
          itemElem.classList.toggle('completed', cb.checked);
        }}
        updateProgressBar();
        if (cb.checked) {{
          showToast('🎉 已標記完成該行程！');
        }}
      }}
    }}

    function restoreChecklist() {{
      for (const [id, isChecked] of Object.entries(checkedItems)) {{
        const cb = document.getElementById(id);
        if (cb) {{
          cb.checked = isChecked;
          const itemElem = cb.closest('.timeline-item');
          if (itemElem) {{
            itemElem.classList.toggle('completed', isChecked);
          }}
        }}
      }}
    }}

    function updateProgressBar() {{
      const allCheckboxes = document.querySelectorAll('.check-wrapper input[type="checkbox"]');
      if (allCheckboxes.length === 0) return;
      let checkedCount = 0;
      allCheckboxes.forEach(cb => {{
        if (cb.checked) checkedCount++;
      }});
      const pct = Math.round((checkedCount / allCheckboxes.length) * 100);
      document.getElementById('progressBar').style.width = pct + '%';
    }}

    function openOriginalModal(cardId) {{
      const card = document.getElementById(cardId);
      if (!card) return;
      const titleElem = card.querySelector('.card-title span');
      const timeElem = card.querySelector('.card-time');
      const contentElem = card.querySelector('.original-content-holder');
      
      const title = titleElem ? titleElem.innerText : '行程詳情';
      const time = timeElem ? timeElem.innerText : '';
      const html = contentElem ? contentElem.innerHTML : '';
      
      document.getElementById('modalTitle').innerText = (time ? time + ' ' : '') + title;
      document.getElementById('modalBody').innerHTML = html;
      
      document.getElementById('modalOverlay').classList.add('active');
      document.getElementById('modalSheet').classList.add('active');
      document.body.style.overflow = 'hidden';
    }}

    function closeModal() {{
      const sheet = document.getElementById('modalSheet');
      const overlay = document.getElementById('modalOverlay');
      // 清掉下滑手勢留下的 inline 樣式，否則下次開啟會停在被拖走的位置
      sheet.style.transition = '';
      sheet.style.transform = '';
      overlay.style.opacity = '';
      overlay.classList.remove('active');
      sheet.classList.remove('active');
      document.body.style.overflow = '';
    }}

    // 下滑關閉抽屜。只有在內容已捲到最頂、或手指按在把手／標題列時才啟動，
    // 否則會搶走正常的內容捲動。
    (function initSheetSwipe() {{
      const sheet = document.getElementById('modalSheet');
      const overlay = document.getElementById('modalOverlay');
      const body = document.getElementById('modalBody');
      if (!sheet || !overlay || !body) return;

      const CLOSE_DISTANCE = 90;   // 下滑超過這個距離就關閉
      const DEAD_ZONE = 6;         // 小於這個位移不判定方向，避免誤觸
      let startY = 0, dy = 0, dragging = false, decided = false;

      function springBack() {{
        sheet.style.transition = '';
        sheet.style.transform = '';
        overlay.style.opacity = '';
      }}

      sheet.addEventListener('touchstart', function (e) {{
        if (e.touches.length !== 1) return;
        startY = e.touches[0].clientY;
        dy = 0;
        decided = false;
        dragging = body.scrollTop <= 0 ||
                   !!(e.target.closest && e.target.closest('.sheet-handle, .sheet-header'));
        if (dragging) sheet.style.transition = 'none';
      }}, {{ passive: true }});

      sheet.addEventListener('touchmove', function (e) {{
        if (!dragging) return;
        dy = e.touches[0].clientY - startY;
        if (!decided) {{
          if (Math.abs(dy) < DEAD_ZONE) return;
          decided = true;
          if (dy < 0) {{ dragging = false; sheet.style.transition = ''; return; }}
        }}
        if (dy <= 0) return;
        e.preventDefault();
        sheet.style.transform = 'translateY(' + dy + 'px)';
        overlay.style.opacity = String(Math.max(0, 1 - dy / 400));
      }}, {{ passive: false }});

      function finishDrag() {{
        if (!dragging) return;
        dragging = false;
        if (dy > CLOSE_DISTANCE) {{
          closeModal();
        }} else {{
          springBack();
        }}
        dy = 0;
      }}

      sheet.addEventListener('touchend', finishDrag);
      sheet.addEventListener('touchcancel', finishDrag);
    }})();

    function showToast(msg) {{
      const toast = document.getElementById('toastBox');
      toast.innerText = msg;
      toast.classList.add('show');
      setTimeout(() => {{
        toast.classList.remove('show');
      }}, 2200);
    }}

    function copyText(text, successMsg) {{
      navigator.clipboard.writeText(text).then(() => {{
        showToast(successMsg || '已複製到剪貼簿！');
      }}).catch(() => {{
        showToast('複製失敗，請手動複製');
      }});
    }}

    function toggleEmergency() {{
      const body = document.getElementById('emergencyBody');
      body.style.display = (body.style.display === 'none') ? 'block' : 'none';
    }}

    function registerServiceWorker() {{
      if ('serviceWorker' in navigator) {{
        navigator.serviceWorker.register('./sw.js').then(reg => {{
          reg.onupdatefound = () => {{
            const installingWorker = reg.installing;
            installingWorker.onstatechange = () => {{
              if (installingWorker.state === 'installed' && navigator.serviceWorker.controller) {{
                showToast('🚀 行程已更新，重新整理即可載入最新版本');
              }}
            }};
          }};
        }}).catch(err => console.log('SW registration failed: ', err));
      }}
    }}
  </script>
</body>
</html>
"""
    return full_page

def main():
    meta, days_data = parse_v10_markdown()
    html_output = render_full_pwa_html(meta, days_data)
    with open('/home/owen/tokyo/itinerary.html', 'w', encoding='utf-8') as f:
        f.write(html_output)
    print("✅ Successfully built and verified itinerary.html!")

if __name__ == '__main__':
    main()
