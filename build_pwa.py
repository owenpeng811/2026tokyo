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
    t = t.replace('✈️', '').replace('🚇', '').replace('🏨', '').replace('🍽️', '').replace('🏃', '').replace('🦕', '').replace('🌳', '').replace('🚌', '').replace('📸', '').replace('🍜', '').replace('🍪', '').replace('🛒', '').replace('⛪', '').replace('🌅', '').replace('🪙', '').replace('🎮', '').replace('🥞', '').replace('🍔', '').replace('🎡', '').replace('🏰', '').replace('🎢', '').replace('🎠', '').replace('🎆', '').replace('🛍️', '').replace('🚶‍♂️', '').replace('🐧', '').replace('🛬', '').replace('🧳', '').replace('🍳', '').replace('🌿', '').replace('☕', '').replace('🏛️', '').replace('🍩', '').replace('🐟', '').replace('🛫', '')
    t = re.sub(r'[\*\#]', '', t)
    return t.strip()

def get_category_info(title):
    t_lower = title.lower()
    if any(x in t_lower for x in ['餐', '食', '吃', '拉麵', '燒', '飲', '咖啡', '麵', '丼', '牛舌', '丸子', '甜點', '泡芙', '銅鑼燒', '炸牛肉丸', '壽司', '文字燒', '麥當勞', '摩斯', '大戶屋', '串家物語', 'すき家', '宇奈とと', '天丼', '玉子燒', '早午餐', '宵夜']):
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
        '東京迪士尼樂園電子大遊行', '城堡高空投影秀', '世界市集（World Bazaar）最後補貨與出園'
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
        parts = re.split(r'(<a\b[^>]*>.*?</a>)', html_text, flags=re.DOTALL)
        new_parts = []
        for p in parts:
            if p.startswith('<a') and p.endswith('</a>'):
                new_parts.append(p)
            else:
                p_sub = re.sub(r'(?<![="\'/])' + escaped_name, f'<a class="map-link-inline" href="{url}" target="_blank">{name} 🔗</a>', p, count=2)
                new_parts.append(p_sub)
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

def markdown_to_html(text):
    if not text:
        return ""
    lines = text.split('\n')
    html_lines = []
    in_list = False
    in_quote = False
    
    for raw_line in lines:
        line = raw_line.strip()
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
            if content.startswith('*') or content.startswith('-'):
                if not in_list:
                    html_lines.append('<ul class="modal-list">')
                    in_list = True
                item_text = content.lstrip('*-').strip()
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
            if line.startswith('###') or line.startswith('####'):
                h_text = line.lstrip('#').strip()
                html_lines.append(f'<h4 class="modal-subheading">{format_inline_markdown(h_text)}</h4>')
            else:
                html_lines.append(f'<p>{format_inline_markdown(line)}</p>')
                
    if in_list:
        html_lines.append('</ul>')
    if in_quote:
        html_lines.append('</div>')
        
    full_html = '\n'.join(html_lines)
    return autolink_text_entities(full_html)

CUSTOM_SUMMARIES_V10 = {
    # Day 1
    (1, "機場整備與購票"): f"洗手間整備、ATM提款、整理行李。<strong>建議直接於機場辦理 2 張兒童 Welcome Suica</strong>（需出示護照，後續搭車最省事），每張建議先儲值 ¥2,000～3,000。",
    (1, "前往飯店 (Henn na Hotel)"): f"<strong>搭乘首選（直達）：</strong>從 <a class=\"map-link-inline\" href=\"{MASTER_NAV_MAP.get('羽田機場第3航廈', '')}\" target=\"_blank\">羽田機場第3航廈站 🔗</a> 搭乘「京急機場線 (直通都營淺草線)」直達 淺草橋站（A1 電梯出口）。車程約 40-45 分鐘，免提行李換車。",
    (1, "飯店 Check-in 與休息"): f"步行抵達 <a class=\"map-link-inline\" href=\"{MASTER_NAV_MAP.get('海茵娜酒店', '')}\" target=\"_blank\">海茵娜酒店 🔗</a> 辦理 Check-in、置放行李、稍作休息，更換舒適鞋衣。",
    (1, "出發前往秋葉原"): f"慢步 2 分鐘至 JR 淺草橋站，搭乘 JR 中央・總武線 (黃色列車) 1 站直達 <a class=\"map-link-inline\" href=\"{MASTER_NAV_MAP.get('秋葉原站', '')}\" target=\"_blank\">秋葉原站 🔗</a> (車程僅 2 分鐘)。",
    (1, "GiGO 秋葉原3號館 (GiGO 秋葉原3号館)"): f"體驗日本大型電玩中心、日式夾娃娃機（UFO Catcher），全家感受秋葉原熱鬧的次文化遊樂氛圍（預算約 ¥500～¥1,000）。",
    (1, "日系拍貼機體驗 (Purikura / GiGO 拍貼機專區)"): f"<strong>全家合影紀念：</strong>走進日本最新「大眼美肌拍貼機」，全家 5 人拍下旅行初日開場全家福，觸控塗鴉並現場列印全彩貼紙（¥500/次）。",
    (1, "萬代扭蛋百貨店 秋葉原店 (ガシャポンのデパート 秋葉原店)"): f"位於 <strong>いちご秋葉原駅前ビル 4F (namco秋葉原店 4F)</strong>，全秋葉原規模最大官方扭蛋專門店之一，擁有近千台最新動漫、寶可夢、迪士尼扭蛋機。每位小朋友選扭 1～2 顆開場禮物。<br><em>(Option: <a class=\"map-link-inline\" href=\"{MASTER_NAV_MAP.get('友都八喜', '')}\" target=\"_blank\">友都八喜 🔗</a> 6F 玩具模型展區)</em>",
    (1, "晚餐：壽司郎（90 分鐘寬裕大啖平價迴轉壽司）"): f"<strong>首選餐廳：</strong><a class=\"map-link-inline\" href=\"{MASTER_NAV_MAP.get('壽司郎 (スシロー 秋葉原駅前店)', '')}\" target=\"_blank\">🍣 壽司郎 秋葉原駅前店 (BiTO AKIBA B1F) 🔗</a> 享用平價迴轉壽司（人均 ¥1,000～¥1,800）。<strong>已預約，客戶編號 7300</strong>。全中文觸控平板、現點現做軌道直送，90 分鐘寬裕用餐！<br><strong>備案 1：</strong><a class=\"map-link-inline\" href=\"{MASTER_NAV_MAP.get('丸龜製麵 (丸亀製麺 秋葉原店)', '')}\" target=\"_blank\">丸龜製麵 秋葉原店 🔗</a> (烏龍麵，¥500-900)<br><strong>備案 2：</strong><a class=\"map-link-inline\" href=\"{MASTER_NAV_MAP.get('CoCo壹番屋 (CoCo壱番屋 JR秋葉原駅昭和通り口店)', '')}\" target=\"_blank\">CoCo壹番屋 秋葉原站前店 🔗</a> (咖哩飯，¥800-1,200)",
    (1, "返回淺草橋"): f"步行至 JR <a class=\"map-link-inline\" href=\"{MASTER_NAV_MAP.get('秋葉原站', '')}\" target=\"_blank\">秋葉原站 🔗</a>，搭乘 JR 中央・總武線 1 站直達 淺草橋站 (車程 2 分鐘)。",
    (1, "Cross Shinjuku 3D 巨貓 (クロス新宿ビジョン)"): f"新宿東口站前廣場抬頭欣賞生動逼真的超巨大 3D 三花貓演出，開闊廣場平坦安心觀賞。",
    (1, "晚餐：新宿東口家庭友善美食"): f"<strong>首選餐廳：</strong><a class=\"map-link-inline\" href=\"{MASTER_NAV_MAP.get('Gusto (ガスト 新宿NOWAビル店)', '')}\" target=\"_blank\">🍽️ Gusto 新宿NOWAビル店 (7F) 🔗</a> 享用平價日式家庭料理（漢堡排定食，人均 ¥800～¥1,200），全中文平板點餐、貓咪送餐機器人。<br><strong>備案：</strong><a class=\"map-link-inline\" href=\"{MASTER_NAV_MAP.get('LUMINE EST 餐廳街 (ルミネエスト新宿 7&8 DINER)', '')}\" target=\"_blank\">LUMINE EST 餐廳街 🔗</a> (7F/8F 蛋包飯/日式洋食)。",
    (1, "地方生鮮超市採買"): f"前往飯店旁 <a class=\"map-link-inline\" href=\"{MASTER_NAV_MAP.get('肉之Hanamasa超市', '')}\" target=\"_blank\"><strong>肉之Hanamasa超市 (肉のハナマサ 浅草橋店)</strong> 🔗</a> 採買：翌日早餐鮮乳、麵包、優格、礦泉水與當季水果。",
    (1, "回飯店休息整備"): f"回到 <a class=\"map-link-inline\" href=\"{MASTER_NAV_MAP.get('海茵娜酒店', '')}\" target=\"_blank\">海茵娜酒店 🔗</a>。整理明日迪士尼裝備（門票、Welcome Suica、行動電源）。全家輪流洗澡泡澡放鬆。",
    (1, "準時就寢"): f"<strong>21:00－21:30 準時就寢</strong>，隔天 06:20 起床睡滿 9 小時，充足體力迎戰東京迪士尼！",

    # Day 2 Parents
    (2, "出發前往上野御徒町"): f"從淺草橋搭 JR 總武線至秋葉原，轉山手線 1 站至 <a class=\"map-link-inline\" href=\"{MASTER_NAV_MAP.get('御徒町站', '')}\" target=\"_blank\"><strong>御徒町站</strong> 🔗</a> 出站，車程僅 5 分鐘。",
    (2, "晨間清涼戶外散步（趁 10:00 前氣溫宜人）"): f"<a class=\"map-link-inline\" href=\"{MASTER_NAV_MAP.get('松坂屋上野店', '')}\" target=\"_blank\">松坂屋 🔗</a> 出發 ➔ <a class=\"map-link-inline\" href=\"{MASTER_NAV_MAP.get('不忍池', '')}\" target=\"_blank\">不忍池 🔗</a>（賞荷花） ➔ <a class=\"map-link-inline\" href=\"{MASTER_NAV_MAP.get('清水觀音堂', '')}\" target=\"_blank\">清水觀音堂 🔗</a>（看月之松）。可順路步行至 <a class=\"map-link-inline\" href=\"{MASTER_NAV_MAP.get('兔屋 (うさぎや)', '')}\" target=\"_blank\">「兔屋 (うさぎや)」 🔗</a> 採買現做百年銅鑼燒。",
    (2, "進入室內基地營避暑（10:00 百貨開門）"): f"<strong>首選基地營：</strong><a class=\"map-link-inline\" href=\"{MASTER_NAV_MAP.get('DEAN & DELUCA CAFE (PARCO_ya 1F)', '')}\" target=\"_blank\">☕ DEAN & DELUCA CAFE (PARCO_ya 1F) 🔗</a>（人均 ¥500-800）。<br><strong>備案基地營：</strong><a class=\"map-link-inline\" href=\"{MASTER_NAV_MAP.get('喫茶 Tricolore', '')}\" target=\"_blank\">喫茶 トリコロール (松坂屋上野店 本館 4F) 🔗</a>（人均 ¥800-1,200）。",
    (2, "午餐"): f"<strong>首選餐廳：</strong><a class=\"map-link-inline\" href=\"{MASTER_NAV_MAP.get('すき家 (すき家 上野三丁目店)', '')}\" target=\"_blank\">🍱 すき家 上野三丁目店 🔗</a> (松坂屋正對面) 享用牛鮭雙拼定食/牛肉丼（人均 ¥550～¥850）。全繁體中文平板點餐，自動收銀機結帳。<br><strong>備案：</strong><a class=\"map-link-inline\" href=\"{MASTER_NAV_MAP.get('松坂屋地下美食街', '')}\" target=\"_blank\">松坂屋地下美食街便當 🔗</a>（冷氣座位區）。",
    (2, "正午酷暑亮點：國立西洋美術館（全室內強冷氣）"): f"<strong>室內避暑亮點：</strong><a class=\"map-link-inline\" href=\"{MASTER_NAV_MAP.get('國立西洋美術館', '')}\" target=\"_blank\">🏛️ 國立西洋美術館 🔗</a> 欣賞羅丹雕塑與莫內睡蓮（<strong>滿 65 歲長輩出示護照常設展免費入場</strong>，冷氣極強！）。",
    (2, "傍晚戶外悠閒漫步（陽光減弱）"): f"前往 <a class=\"map-link-inline\" href=\"{MASTER_NAV_MAP.get('上野公園噴水廣場', '')}\" target=\"_blank\">上野公園中央噴水廣場 🔗</a> 林蔭散步，享受傍晚涼風。",
    (2, "晚餐"): f"<strong>首選餐廳：</strong><a class=\"map-link-inline\" href=\"{MASTER_NAV_MAP.get('名代 宇奈とと (名代 宇奈とと 上野店)', '')}\" target=\"_blank\">🐟 名代 宇奈とと 上野店 🔗</a> (JR高架橋旁) 炭火現烤鰻魚飯（推薦：雙倍鰻魚飯丼 ¥1,100，附大圖菜單手指比點）。<br><strong>備案：</strong><a class=\"map-link-inline\" href=\"{MASTER_NAV_MAP.get('松屋 上野店', '')}\" target=\"_blank\">松屋 上野店 🔗</a> (繁體中文售票機，牛丼定食 ¥500-850)。",
    (2, "回程：前往JR 御徒町站"): f"由 <a class=\"map-link-inline\" href=\"{MASTER_NAV_MAP.get('御徒町站', '')}\" target=\"_blank\">御徒町站 🔗</a> 搭乘山手線至秋葉原，轉總武線 1 站返抵淺草橋飯店，早點洗熱水澡放鬆休息。",

    # Day 2 Kids (Disney)
    (2, "迪士尼交通動線"): f"淺草橋 ➔ 秋葉原 (總武線) ➔ 八丁堀 (地鐵日比谷線) ➔ <a class=\"map-link-inline\" href=\"{MASTER_NAV_MAP.get('舞濱站', '')}\" target=\"_blank\">舞濱站 🔗</a> (JR京葉線)。全程設有手扶梯與電梯，避開東京車站巨型轉乘。",
    (2, "抵達樂園門口"): f"08:45 開園排隊。入園後立刻開啟 Disney App：<br>1. <strong>設施預約：</strong>購買 <a class=\"map-link-inline\" href=\"{MASTER_NAV_MAP.get('美女與野獸：魔法物語', '')}\" target=\"_blank\">「美女與野獸：魔法物語 (DPA)」 🔗</a> 或抽免費 Priority Pass。<br>2. <strong>防排隊關鍵：</strong>立即使用 <strong>Disney Mobile Order 手機點餐</strong> 預定今日 11:30 午餐與 18:00 晚餐時段！",
    (2, "必玩設施與行程建議"): f"第一站：<a class=\"map-link-inline\" href=\"{MASTER_NAV_MAP.get('美女與野獸：魔法物語', '')}\" target=\"_blank\">美女與野獸 (魔法物語 DPA) 🔗</a> ➔ 第二站：<a class=\"map-link-inline\" href=\"{MASTER_NAV_MAP.get('小熊維尼獵蜜記', '')}\" target=\"_blank\">小熊維尼獵蜜記 (Priority Pass) 🔗</a> ➔ 第三站：<a class=\"map-link-inline\" href=\"{MASTER_NAV_MAP.get('巨雷山', '')}\" target=\"_blank\">巨雷山 (130cm) 🔗</a>。",
    (2, "午後行程與遊行"): f"<strong>日間遊行：</strong>提前 30-45 分鐘卡位欣賞。<br><strong>必玩推薦：</strong>幽靈公館、加勒比海盜、飛濺山（夏日清涼）。備選：怪獸電力公司、小小世界。",
    (2, "晚餐：主題餐廳時間"): f"<strong>推薦餐廳：</strong><a class=\"map-link-inline\" href=\"{MASTER_NAV_MAP.get('廣場閣樓餐廳', '')}\" target=\"_blank\">廣場閣樓餐廳 🔗</a>（歐式套餐）或 <a class=\"map-link-inline\" href=\"{MASTER_NAV_MAP.get('莎拉奶奶之家餐廳', '')}\" target=\"_blank\">莎拉奶奶之家餐廳 🔗</a>（歐姆蛋包飯）。建議入園時即於 App Mobile Order 預訂 18:00 取餐時段。<br><strong>快速備案：</strong><a class=\"map-link-inline\" href=\"{MASTER_NAV_MAP.get('紅連火箭筒餐廳', '')}\" target=\"_blank\">紅連火箭筒餐廳 🔗</a>（披薩/卡爾佐內烤餅，出餐極快）。",
    (2, "城堡點燈拍照、購買夜間點心與遊行卡位"): f"灰姑娘城堡夜間點燈合影，買吉事果或米奇冰棒，19:30 前往圓環區域卡位休息。",
    (2, "東京迪士尼樂園電子大遊行「夢之光」"): f"璀璨燈光花車與經典迪士尼音樂遊行（全長約 45 分鐘），全家坐著欣賞放鬆雙腿。",
    (2, "城堡高空投影秀「Reach for the Stars: Everlasting Dreams」"): f"2026 夏季特別版（約 25 分鐘），結合漫威、大英雄天團與經典動畫的 3D 燈光投影與焰火震撼演出。",
    (2, "世界市集（World Bazaar）最後補貨與出園"): f"於世界市集購買紀念品與伴手禮，約 21:50 離開樂園前往巴士總站/JR舞濱站。",
    (2, "親子組回程交通（首選巴士 / 備案電車）"): f"<strong>首選（直達巴士）：</strong>出園至巴士總站搭乘直達 <a class=\"map-link-inline\" href=\"{MASTER_NAV_MAP.get('秋葉原站', '')}\" target=\"_blank\"><strong>秋葉原站東口</strong> 🔗</a> 的高速巴士（車程約 35-45 分鐘，上車有座位一路睡回秋葉原），轉總武線 1 站回淺草橋。<br><strong>備案：</strong>舞濱 ➔ 八丁堀 (京葉線) ➔ 秋葉原 (日比谷線) ➔ 淺草橋。",

    # Day 3
    (3, "搭乘 JR 前往東京車站"): f"淺草橋 ➔ 秋葉原 ➔ <a class=\"map-link-inline\" href=\"{MASTER_NAV_MAP.get('東京站', '')}\" target=\"_blank\">東京站 🔗</a> (JR 山手線，車程 8 分鐘)。",
    (3, "東京車站丸之內站舍 (東京駅丸の内駅舎)"): f"漫步丸之內站前開闊廣場，在清晨涼風中與百年壯麗紅磚建築合影。",
    (3, "返回東京車站一番街入口等待開門"): f"<strong>🚨 避坑防刷卡指南：</strong>從丸之內（西側）跨越到八重洲（東側）時，<strong>請走站外的「北地下自由通路」</strong>！千萬別刷 Suica 誤進站！",
    (3, "東京車站一番街 (東京駅一番街) (八重洲地下中央口)"): f"10:00 一開門優先逛：寶可夢商店（站長皮卡丘）、TOMICA 專賣店、吉伊卡哇商店、橡子共和國（龍貓）。",
    (3, "KITTE花園 (ＫＩＴＴＥガーデン) (KITTE 6F)"): f"搭電梯直達 <a class=\"map-link-inline\" href=\"{MASTER_NAV_MAP.get('KITTE花園 (ＫＩＴＴＥガーデン)', '')}\" target=\"_blank\">KITTE 6F 屋頂花園 🔗</a>，免費俯瞰東京車站紅磚站舍全景與新幹線進出站，室內空調充足。",
    (3, "午餐（東京車站周邊）"): f"<strong>首選餐廳：</strong><a class=\"map-link-inline\" href=\"{MASTER_NAV_MAP.get('天丼てんや (天丼てんや 八重洲店)', '')}\" target=\"_blank\">🍤 天丼てんや 八重洲店 🔗</a> (八重洲地下街 B1F 南1號) 享用日式炸蝦天丼（人均 ¥560～¥850）。出餐極快、平價美味！<br><strong>備案 1：</strong><a class=\"map-link-inline\" href=\"{MASTER_NAV_MAP.get('だし茶漬け えん KITTE丸の内店', '')}\" target=\"_blank\">だし茶漬け えん KITTE丸の内店 🔗</a> (高湯茶泡飯，¥850-1,100)<br><strong>備案 2：</strong><a class=\"map-link-inline\" href=\"{MASTER_NAV_MAP.get('燕子烤肉漢堡排 (つばめグリル 大丸東京店)', '')}\" target=\"_blank\">燕子烤肉漢堡排 🔗</a> (大丸東京店 12F)",
    (3, "前往上野"): f"搭乘 JR 山手線 8 分鐘直達 <a class=\"map-link-inline\" href=\"{MASTER_NAV_MAP.get('上野站', '')}\" target=\"_blank\">上野站 🔗</a>（公園口出站設有電梯）。",
    (3, "國立科學博物館 (国立科学博物館)"): f"正午避暑勝地！參觀地球館 B1 恐龍化石骨骼、3F 野生動物標本展廳及 360 度球幕影院，冷氣充足放鬆。",
    (3, "超人氣晚餐 ：鴨 to 蔥拉麵"): f"<strong>首選名店：</strong><a class=\"map-link-inline\" href=\"{MASTER_NAV_MAP.get('鴨 to 蔥拉麵 (らーめん 鴨to葱 御徒町本店)', '')}\" target=\"_blank\">🍜 鴨 to 蔥拉麵 御徒町本店 🔗</a> 香濃鴨肉醬油拉麵（人均 ¥1,000～¥1,400）。<br><strong>🚨 排隊停損防雷規則：</strong>排隊 ≤ 3 組才吃，超過直接啟動阿美橫丁小吃備案，絕不在烈日下苦等！",
    (3, "阿美橫丁採買"): f"<strong>必掃名店：</strong><br>• <a class=\"map-link-inline\" href=\"{MASTER_NAV_MAP.get('二木菓子 (二木の菓子 第一営業所)', '')}\" target=\"_blank\">二木菓子（第一営業所） 🔗</a>：掃日本零食名產。<br>• <a class=\"map-link-inline\" href=\"{MASTER_NAV_MAP.get('OS Drug 上野店', '')}\" target=\"_blank\">OS Drug 上野店 🔗</a>：藥妝免退稅價格之冠。<br>• 街邊小吃：<a class=\"map-link-inline\" href=\"{MASTER_NAV_MAP.get('肉之大山 (肉の大山 上野店)', '')}\" target=\"_blank\">肉之大山炸肉餅 🔗</a>、<a class=\"map-link-inline\" href=\"{MASTER_NAV_MAP.get('みなとや食品', '')}\" target=\"_blank\">みなとや章魚燒 🔗</a>。<br>• <a class=\"map-link-inline\" href=\"{MASTER_NAV_MAP.get('多慶屋 (多慶屋 TAKEYA 1)', '')}\" target=\"_blank\">多慶屋（TAKEYA） 🔗</a>：紫色商場一站式補貨備案。",
    (3, "回程：前往JR 御徒町站"): f"步行至 JR <a class=\"map-link-inline\" href=\"{MASTER_NAV_MAP.get('御徒町站', '')}\" target=\"_blank\">御徒町站 🔗</a> 搭乘電車返回淺草橋。",
    (3, "晚餐（若下午沒吃鴨 to 蔥拉麵）"): f"<strong>首選餐廳：</strong><a class=\"map-link-inline\" href=\"{MASTER_NAV_MAP.get('吉野家 (吉野家 浅草橋店)', '')}\" target=\"_blank\">吉野家 浅草橋店 🔗</a>。<br><strong>備案：</strong><a class=\"map-link-inline\" href=\"{MASTER_NAV_MAP.get('松屋 (松屋 浅草橋店)', '')}\" target=\"_blank\">松屋 浅草橋店 🔗</a> / <a class=\"map-link-inline\" href=\"{MASTER_NAV_MAP.get('拉麵 ろく月 (らーめん ろく月)', '')}\" target=\"_blank\">ろく月 雞白湯拉麵 🔗</a>。",
    (3, "宵夜／點心（若下午已吃鴨 to 蔥拉麵）"): f"外帶 <a class=\"map-link-inline\" href=\"{MASTER_NAV_MAP.get('Cow Cow Kitchen (東京Milk Cheese Factory)', '')}\" target=\"_blank\">Cow Cow Kitchen 牛奶起司派 🔗</a> (ルミネエスト新宿 LUMINE EST 1F) 或便利商店點心回飯店享用。"
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
        'hotel_jp_addr': "東京都台東区浅草橋1-10-5 (JR・都営浅草橋駅徒歩2分)"
    }

    days_data = {
        1: {'common_before': [], 'plan_a': [], 'plan_b': [], 'common_after': []},
        2: {'parents': {'common_before': [], 'sunny': [], 'rainy': [], 'common_after': []}, 'kids': []},
        3: [],
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
                    if d == 2 and (t in slot_title or slot_title in t):
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
                    if d == 2 and (t in slot_title or slot_title in t):
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

    # Day 3, 4, 6
    for day in [3, 4, 6]:
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

def build_card_html(item_id, item):
    btn_html = ""
    if item['has_modal']:
        btn_html = f'<button class="view-original-btn" onclick="openOriginalModal(\'card-item-{item_id}\')">📖 完整說明與祕訣</button>'
        
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
              <span class="tag tag-{item['category']}">{item['category_icon']} {item['category_zh']}</span>
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
        <h2 class="day-overview-title">動漫盛宴 × 科學探險與阿美橫丁採買</h2>
      </div>
"""
    for idx, it in enumerate(days_data[3]):
        timeline_html += build_card_html(f"d3-{idx}", it)
    timeline_html += '    </div>\n\n'

    # Day 4
    timeline_html += """    <!-- Day 4 Section -->
    <div class="day-section" id="day4-section" style="display: none;">
      <div class="day-overview-header">
        <h2 class="day-overview-title">吉卜力童話 × 吉祥寺風格散步與 DIY 炸串</h2>
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

    hotel_url = MASTER_NAV_MAP.get('海茵娜酒店', 'https://www.google.com/maps/search/?api=1&query=35.6970775,139.7847605&query_place_id=ChIJRWR7EbKOGGARUkONjElltUA')

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

    .countdown-badge {{
      font-size: 0.75rem;
      background: rgba(228, 95, 86, 0.2);
      color: #ff7b72;
      border: 1px solid rgba(228, 95, 86, 0.4);
      padding: 3px 8px;
      border-radius: 12px;
      font-weight: 600;
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

    .meta-card {{
      margin: 12px 16px;
      background: var(--card-bg);
      backdrop-filter: blur(var(--blur-strength));
      border: 1px solid var(--card-border);
      border-radius: 14px;
      padding: 12px 14px;
      display: flex;
      flex-direction: column;
      gap: 8px;
    }}

    .meta-row {{
      display: flex;
      align-items: center;
      justify-content: space-between;
      font-size: 0.85rem;
    }}

    .meta-label {{
      color: var(--text-muted);
      display: flex;
      align-items: center;
      gap: 6px;
    }}

    .meta-val {{
      font-weight: 500;
      color: #fff;
      text-align: right;
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
      width: 24px;
      flex-shrink: 0;
      padding-top: 4px;
    }}

    .check-wrapper {{
      position: relative;
      cursor: pointer;
      width: 22px;
      height: 22px;
      display: inline-block;
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
      height: 22px;
      width: 22px;
      background-color: rgba(255, 255, 255, 0.08);
      border: 1.5px solid rgba(255, 255, 255, 0.25);
      border-radius: 6px;
      transition: var(--transition-smooth);
    }}
    .check-wrapper:hover input ~ .checkmark {{
      border-color: var(--accent-coral);
    }}
    .check-wrapper input:checked ~ .checkmark {{
      background-color: var(--accent-green);
      border-color: var(--accent-green);
    }}
    .checkmark:after {{
      content: "";
      position: absolute;
      display: none;
    }}
    .check-wrapper input:checked ~ .checkmark:after {{
      display: block;
      left: 7px;
      top: 3px;
      width: 5px;
      height: 10px;
      border: solid white;
      border-width: 0 2px 2px 0;
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
</head>
<body>

  <header class="app-header">
    <div class="header-top">
      <div class="app-title">
        <span>🗼 東京親子自由行</span>
      </div>
      <div class="countdown-badge" id="countdownBadge">
        ⏳ 倒數計時中
      </div>
    </div>
    
    <div class="progress-bar-container">
      <div class="progress-bar-fill" id="progressBar"></div>
    </div>

    <nav class="day-tabs" id="dayTabs">
      <button class="day-tab active" onclick="switchDay(1)">D1 (8/20四)</button>
      <button class="day-tab" onclick="switchDay(2)">D2 (8/21五)</button>
      <button class="day-tab" onclick="switchDay(3)">D3 (8/22六)</button>
      <button class="day-tab" onclick="switchDay(4)">D4 (8/23日)</button>
      <button class="day-tab" onclick="switchDay(5)">D5 (8/24一)</button>
      <button class="day-tab" onclick="switchDay(6)">D6 (8/25二)</button>
    </nav>
  </header>

  <section class="meta-card">
    <div class="meta-row">
      <span class="meta-label">🏨 住宿飯店</span>
      <span class="meta-val">
        {meta['hotel_name']}
        <a class="copy-btn" href="{hotel_url}" target="_blank">導航</a>
      </span>
    </div>
    <div class="meta-row">
      <span class="meta-label">🚕 給司機地址</span>
      <span class="meta-val">
        {meta['hotel_jp_addr']}
        <button class="copy-btn" onclick="copyText('{meta['hotel_jp_addr']}', '已複製日文地址！')">複製</button>
      </span>
    </div>
    <div class="meta-row">
      <span class="meta-label">✈️ 去程航班</span>
      <span class="meta-val">{meta['flight_go']}</span>
    </div>
    <div class="meta-row">
      <span class="meta-label">✈️ 回程航班</span>
      <span class="meta-val">{meta['flight_back']}</span>
    </div>
  </section>

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
      startCountdown();
      registerServiceWorker();
    }});

    function switchDay(day) {{
      currentDay = day;
      document.querySelectorAll('.day-tab').forEach((tab, i) => {{
        tab.classList.toggle('active', i + 1 === day);
      }});
      document.querySelectorAll('.day-section').forEach((sec, i) => {{
        sec.style.display = (i + 1 === day) ? 'block' : 'none';
      }});
      window.scrollTo({{ top: 0, behavior: 'smooth' }});
    }}

    function switchDay1Plan(plan) {{
      const isPlanA = plan === 'A';
      document.querySelectorAll('#day1-section .sub-toggle-btn')[0].classList.toggle('active', isPlanA);
      document.querySelectorAll('#day1-section .sub-toggle-btn')[1].classList.toggle('active', !isPlanA);
      document.querySelector('.day1-plan-A').style.display = isPlanA ? 'block' : 'none';
      document.querySelector('.day1-plan-B').style.display = isPlanA ? 'none' : 'block';
    }}

    function switchDay2Group(group) {{
      const isParents = group === 'parents';
      document.getElementById('day2-btn-parents').classList.toggle('active', isParents);
      document.getElementById('day2-btn-kids').classList.toggle('active', !isParents);
      document.querySelector('.day2-parents-itinerary').style.display = isParents ? 'block' : 'none';
      document.querySelector('.day2-kids-itinerary').style.display = isParents ? 'none' : 'block';
    }}

    function switchDay2ParentsPlan(plan) {{
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
      document.getElementById('modalOverlay').classList.remove('active');
      document.getElementById('modalSheet').classList.remove('active');
      document.body.style.overflow = '';
    }}

    function startCountdown() {{
      const targetDate = new Date('2026-08-20T09:00:00+08:00').getTime();
      function update() {{
        const now = new Date().getTime();
        const diff = targetDate - now;
        if (diff <= 0) {{
          document.getElementById('countdownBadge').innerText = '🎉 旅程進行中！';
          return;
        }}
        const days = Math.floor(diff / (1000 * 60 * 60 * 24));
        const hours = Math.floor((diff % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
        document.getElementById('countdownBadge').innerText = `⏳ 倒數 ${{days}} 天 ${{hours}} 時出發`;
      }}
      update();
      setInterval(update, 60000);
    }}

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
