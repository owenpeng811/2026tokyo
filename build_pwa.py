#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
import os
import json
import urllib.parse

def clean_url(url):
    if not url:
        return ""
    # Strip any trailing markdown punctuation or parentheses
    u = url.strip()
    u = re.sub(r'[\)\>\*\]\,\.\s\"\']+$', '', u)
    return u

def clean_title(title_raw):
    t = re.sub(r'\[(.*?)\]\(.*?\)', r'\1', title_raw)
    t = re.sub(r'\([^\)]*maps[^\)]*\)', '', t)
    # Remove emojis and markdown artifacts
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

def format_inline_markdown(text):
    if not text:
        return ""
    text = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', text)
    
    def replace_md_link(match):
        lbl = match.group(1)
        raw_url = match.group(2)
        clean_u = clean_url(raw_url)
        return f'<a class="map-link-inline" href="{clean_u}" target="_blank">{lbl} 🔗</a>'
    text = re.sub(r'\[(.*?)\]\((https?://[^\)]+)\)', replace_md_link, text)
    
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
        return first
    return "<br>".join(summary_parts)

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
        
    return '\n'.join(html_lines)

# Master curated navigation links
MASTER_NAV_MAP = {
    "羽田機場": "https://maps.app.goo.gl/uX7kK5Wj9s6k1y8N7",
    "海茵娜酒店": "https://maps.app.goo.gl/87mm5h-MGGARngNQ8",
    "秋葉原站": "https://maps.app.goo.gl/B9Z2n8wYjGqH5V1r7",
    "GiGO 秋葉原3號館": "https://maps.app.goo.gl/B9Z2n8wYjGqH5V1r7",
    "日系拍貼機體驗": "https://maps.app.goo.gl/B9Z2n8wYjGqH5V1r7",
    "萬代扭蛋百貨店": "https://maps.app.goo.gl/2F8a4mK7eUvB3H6x9",
    "友都八喜": "https://maps.app.goo.gl/2kE5zC4Kk8J7bY8r9",
    "壽司郎": "https://maps.app.goo.gl/MfORxzyNGGARskRp8",
    "丸龜製麵": "https://share.google/oGaPfuaD4UqWdJCz9",
    "CoCo壹番屋": "https://maps.app.goo.gl/uX7kK5Wj9s6k1y8N7",
    "Cross Shinjuku 3D 巨貓": "https://maps.app.goo.gl/uLh3b6L88oT3b2B5A",
    "Gusto": "https://maps.app.goo.gl/FUOWQQCNGGARHkjP8",
    "LUMINE EST": "https://maps.app.goo.gl/Pz5pXj9s9S2K3D7g6",
    "肉之Hanamasa超市": "https://maps.app.goo.gl/LLEqzq7e73zUXbGU9",
    "松坂屋上野店": "https://maps.app.goo.gl/6RMcXZ6OGGARLLk8P",
    "PARCO_ya": "https://maps.app.goo.gl/uX7kK5Wj9s6k1y8N7",
    "DEAN & DELUCA": "https://maps.app.goo.gl/uX7kK5Wj9s6k1y8N7",
    "不忍池": "https://maps.app.goo.gl/6RMcXZ6OGGARLLk8P",
    "清水觀音堂": "https://maps.app.goo.gl/6RMcXZ6OGGARLLk8P",
    "兔屋": "https://maps.app.goo.gl/87mm5h-MGGARngNQ8",
    "すき家": "https://maps.app.goo.gl/87mm5h-MGGARngNQ8",
    "國立西洋美術館": "https://maps.app.goo.gl/J8q2bK6k8Y7u9N1P3",
    "名代 宇奈とと": "https://maps.app.goo.gl/uX7kK5Wj9s6k1y8N7",
    "松屋": "https://maps.app.goo.gl/uX7kK5Wj9s6k1y8N7",
    "東京迪士尼樂園": "https://maps.app.goo.gl/uX7kK5Wj9s6k1y8N7",
    "紅心皇后宴會大廳": "https://maps.app.goo.gl/uX7kK5Wj9s6k1y8N7",
    "廣場閣樓餐廳": "https://maps.app.goo.gl/uX7kK5Wj9s6k1y8N7",
    "明日樂園舞台餐廳": "https://maps.app.goo.gl/uX7kK5Wj9s6k1y8N7",
    "莎拉奶奶之家餐廳": "https://maps.app.goo.gl/uX7kK5Wj9s6k1y8N7",
    "紅連火箭筒餐廳": "https://maps.app.goo.gl/uX7kK5Wj9s6k1y8N7",
    "東京車站丸之內站舍": "https://maps.app.goo.gl/GgpXhyaLFhQmKBSe9",
    "東京車站一番街": "https://maps.app.goo.gl/82oR9GvFHCmhguiE8",
    "KITTE花園": "https://maps.app.goo.gl/bRVffwmYQMwP9qJ57",
    "天丼てんや": "https://maps.app.goo.gl/uX7kK5Wj9s6k1y8N7",
    "國立科學博物館": "https://maps.app.goo.gl/J8q2bK6k8Y7u9N1P3",
    "鴨 to 蔥拉麵": "https://maps.app.goo.gl/uX7kK5Wj9s6k1y8N7",
    "阿美橫丁": "https://maps.app.goo.gl/6RMcXZ6OGGARLLk8P",
    "二木菓子": "https://maps.app.goo.gl/6RMcXZ6OGGARLLk8P",
    "多慶屋": "https://maps.app.goo.gl/6RMcXZ6OGGARLLk8P",
    "三鷹之森吉卜力美術館": "https://maps.app.goo.gl/9t7mK4V8R3Q8v7sW6",
    "大戶屋": "https://maps.app.goo.gl/34k8Z1T3v7sW6",
    "SATOU": "https://maps.app.goo.gl/34k8Z1T3v7sW6",
    "串家物語": "https://maps.app.goo.gl/kX7m3Q8L9P2t4v8W9",
    "花丸烏龍麵": "https://maps.app.goo.gl/34k8Z1T3v7sW6",
    "一風堂": "https://maps.app.goo.gl/34k8Z1T3v7sW6",
    "淺草寺": "https://maps.app.goo.gl/j8aWGtGMGGARxgm47",
    "淺草文化觀光中心": "https://maps.app.goo.gl/j8aWGtGMGGARxgm47",
    "東京晴空塔": "https://maps.app.goo.gl/UaJR8NaOGGAR48j67",
    "達摩文字燒": "https://maps.app.goo.gl/UaJR8NaOGGAR48j67",
    "利久牛舌": "https://maps.app.goo.gl/UaJR8NaOGGAR48j67",
    "墨田水族館": "https://maps.app.goo.gl/UaJR8NaOGGAR48j67",
    "東京都廳": "https://maps.app.goo.gl/uLh3b6L88oT3b2B5A",
    "麥當勞": "https://maps.app.goo.gl/uLh3b6L88oT3b2B5A",
    "摩斯漢堡": "https://maps.app.goo.gl/uLh3b6L88oT3b2B5A",
    "築地場外市場": "https://maps.app.goo.gl/uX7kK5Wj9s6k1y8N7",
    "築地山長": "https://maps.app.goo.gl/uX7kK5Wj9s6k1y8N7"
}

CUSTOM_SUMMARIES_V10 = {
    # Day 1
    (1, "機場整備與購票"): "洗手間整備、ATM提款、整理行李。<strong>建議直接於機場辦理 2 張兒童 Welcome Suica</strong>（需出示護照，後續搭車最省事），每張建議先儲值 ¥2,000～3,000。",
    (1, "前往飯店 (Henn na Hotel)"): "<strong>搭乘首選（直達）：</strong>從羽田機場第3航廈站 搭乘「京急機場線 (直通都營淺草線)」直達 淺草橋站（A1 電梯出口）。車程約 40-45 分鐘，免提行李換車。",
    (1, "飯店 Check-in 與休息"): "步行抵達海茵娜酒店辦理 Check-in、置放行李、稍作休息，更換舒適鞋衣。",
    (1, "出發前往秋葉原"): "慢步 2 分鐘至 JR 淺草橋站，搭乘 JR 中央・總武線 (黃色列車) 1 站直達 秋葉原站 (車程僅 2 分鐘)。",
    (1, "GiGO 秋葉原3號館 (GiGO 秋葉原3号館)"): "體驗日本大型電玩中心、日式夾娃娃機（UFO Catcher），全家感受秋葉原熱鬧的次文化遊樂氛圍（預算約 ¥500～¥1,000）。",
    (1, "日系拍貼機體驗 (Purikura / GiGO 拍貼機專區)"): "<strong>全家合影紀念：</strong>走進日本最新「大眼美肌拍貼機」，全家 5 人拍下旅行初日開場全家福，觸控塗鴉並現場列印全彩貼紙（¥500/次）。",
    (1, "萬代扭蛋百貨店 秋葉原店 (ガシャポンのデパート 秋葉原店)"): "秋葉原規模最大官方扭蛋專門店，近千台最新動漫、寶可夢、迪士尼扭蛋機。每位小朋友選扭 1～2 顆開場禮物。<br><em>(Option: 友都八喜 6F 玩具模型展區)</em>",
    (1, "晚餐：壽司郎（90 分鐘寬裕大啖平價迴轉壽司）"): "<strong>首選餐廳：</strong><a class=\"map-link-inline\" href=\"https://maps.app.goo.gl/MfORxzyNGGARskRp8\" target=\"_blank\">🍣 壽司郎 秋葉原駅前店 🔗</a> 享用平價迴轉壽司（人均 ¥1,000～¥1,800）。<strong>已預約，客戶編號 7300</strong>。全中文觸控平板、現點現做軌道直送，90 分鐘寬裕用餐！<br><strong>備案 1：</strong>丸龜製麵 秋葉原店 (烏龍麵，¥500-900)<br><strong>備案 2：</strong>CoCo壹番屋 秋葉原站前店 (咖哩飯，¥800-1,200)",
    (1, "返回淺草橋"): "步行至 JR 秋葉原站，搭乘 JR 中央・總武線 1 站直達 淺草橋站 (車程 2 分鐘)。",
    (1, "Cross Shinjuku 3D 巨貓 (クロス新宿ビジョン)"): "新宿東口站前廣場抬頭欣賞生動逼真的超巨大 3D 三花貓演出，開闊廣場平坦安心觀賞。",
    (1, "晚餐：新宿東口家庭友善美食"): "<strong>首選餐廳：</strong><a class=\"map-link-inline\" href=\"https://maps.app.goo.gl/FUOWQQCNGGARHkjP8\" target=\"_blank\">🍽️ Gusto 新宿NOWAビル店 🔗</a> 享用平價日式家庭料理（漢堡排定食，人均 ¥800～¥1,200），全中文平板點餐、貓咪送餐機器人。<br><strong>備案：</strong>LUMINE EST 餐廳街 (7F/8F 蛋包飯/日式洋食)。",
    (1, "地方生鮮超市採買"): "前往飯店旁 <strong>肉之Hanamasa超市 (肉のハナマサ 浅草橋店)</strong> 採買：翌日早餐鮮乳、麵包、優格、礦泉水與當季水果。",
    (1, "回飯店休息整備"): "回到海茵娜酒店。整理明日迪士尼裝備（門票、Welcome Suica、行動電源）。全家輪流洗澡泡澡放鬆。",
    (1, "準時就寢"): "<strong>21:00－21:30 準時就寢</strong>，隔天 06:20 起床睡滿 9 小時，充足體力迎戰東京迪士尼！",

    # Day 2 Parents
    (2, "出發前往上野御徒町"): "從淺草橋搭 JR 總武線至秋葉原，轉山手線 1 站至<strong>御徒町站</strong>出站，車程僅 5 分鐘。",
    (2, "晨間清涼戶外散步（趁 10:00 前氣溫宜人）"): "松坂屋出發 ➔ 不忍池（賞荷花） ➔ 清水觀音堂（看月之松）。可順路步行至「兔屋 (うさぎや)」採買現做百年銅鑼燒。",
    (2, "進入室內基地營避暑（10:00 百貨開門）"): "<strong>首選基地營：</strong><a class=\"map-link-inline\" href=\"https://maps.app.goo.gl/uX7kK5Wj9s6k1y8N7\" target=\"_blank\">☕ DEAN & DELUCA CAFE (PARCO_ya 1F) 🔗</a>（人均 ¥500-800）。<br><strong>備案基地營：</strong>喫茶 トリコロール (松坂屋本館 2F)（人均 ¥800-1,200）。",
    (2, "午餐"): "<strong>首選餐廳：</strong><a class=\"map-link-inline\" href=\"https://maps.app.goo.gl/87mm5h-MGGARngNQ8\" target=\"_blank\">🍱 すき家 上野三丁目店 🔗</a> (松坂屋正對面) 享用牛鮭雙拼定食/牛肉丼（人均 ¥550～¥850）。全繁體中文平板點餐，自動收銀機結帳。<br><strong>備案：</strong>松坂屋地下美食街便當（冷氣座位區）。",
    (2, "正午酷暑亮點：國立西洋美術館（全室內強冷氣）"): "<strong>室內避暑亮點：</strong><a class=\"map-link-inline\" href=\"https://maps.app.goo.gl/J8q2bK6k8Y7u9N1P3\" target=\"_blank\">🏛️ 國立西洋美術館 🔗</a> 欣賞羅丹雕塑與莫內睡蓮（<strong>滿 65 歲長輩出示護照常設展免費入場</strong>，冷氣極強！）。",
    (2, "傍晚戶外悠閒漫步（陽光減弱）"): "前往上野公園中央噴水廣場林蔭散步，享受傍晚涼風。",
    (2, "晚餐"): "<strong>首選餐廳：</strong><a class=\"map-link-inline\" href=\"https://maps.app.goo.gl/uX7kK5Wj9s6k1y8N7\" target=\"_blank\">🐟 名代 宇奈とと 上野店 🔗</a> (JR高架橋旁) 炭火現烤鰻魚飯（推薦：雙倍鰻魚飯丼 ¥1,100，附大圖菜單手指比點）。<br><strong>備案：</strong>松屋 上野店 (繁體中文售票機，牛丼定食 ¥500-850)。",
    (2, "回程：前往JR 御徒町站"): "由御徒町搭乘山手線至秋葉原，轉總武線 1 站返抵淺草橋飯店，早點洗熱水澡放鬆休息。",

    # Day 2 Kids (Disney)
    (2, "迪士尼交通動線"): "淺草橋 ➔ 秋葉原 (總武線) ➔ 八丁堀 (地鐵日比谷線) ➔ 舞濱 (JR京葉線)。全程設有手扶梯與電梯，避開東京車站巨型轉乘。",
    (2, "抵達樂園門口"): "08:45 開園排隊。入園後立刻開啟 Disney App：<br>1. <strong>設施預約：</strong>購買「美女與野獸：魔法物語 (DPA)」或抽免費 Priority Pass。<br>2. <strong>防排隊關鍵：</strong>立即使用 <strong>Disney Mobile Order 手機點餐</strong> 預定今日 11:30 午餐與 18:00 晚餐時段！",
    (2, "必玩設施與行程建議"): "第一站：美女與野獸 (魔法物語 DPA) ➔ 第二站：小熊維尼獵蜜記 (Priority Pass) ➔ 第三站：巨雷山 (130cm)。",
    (2, "午後行程與遊行"): "<strong>日間遊行：</strong>提前 30-45 分鐘卡位欣賞。<br><strong>必玩推薦：</strong>幽靈公館、加勒比海盜、飛濺山（夏日清涼）。備選：怪獸電力公司、小小世界。",
    (2, "晚餐：主題餐廳時間"): "<strong>推薦餐廳：</strong>廣場閣樓餐廳（歐式套餐）或 莎拉奶奶之家餐廳（歐姆蛋包飯）。建議入園時即於 App Mobile Order 預訂 18:00 取餐時段。<br><strong>快速備案：</strong>紅連火箭筒餐廳（披薩/卡爾佐內烤餅，出餐極快）。",
    (2, "城堡點燈拍照、購買夜間點心與遊行卡位"): "灰姑娘城堡夜間點燈合影，買吉事果或米奇冰棒，19:30 前往圓環區域卡位休息。",
    (2, "東京迪士尼樂園電子大遊行「夢之光」"): "璀璨燈光花車與經典迪士尼音樂遊行（全長約 45 分鐘），全家坐著欣賞放鬆雙腿。",
    (2, "城堡高空投影秀「Reach for the Stars: Everlasting Dreams」"): "2026 夏季特別版（約 25 分鐘），結合漫威、大英雄天團與經典動畫的 3D 燈光投影與焰火震撼演出。",
    (2, "世界市集（World Bazaar）最後補貨與出園"): "於世界市集購買紀念品與伴手禮，約 21:50 離開樂園前往巴士總站/JR舞濱站。",
    (2, "親子組回程交通（首選巴士 / 備案電車）"): "<strong>首選（直達巴士）：</strong>出園至巴士總站搭乘直達 <strong>秋葉原站東口</strong> 的高速巴士（車程約 35-45 分鐘，上車有座位一路睡回秋葉原），轉總武線 1 站回淺草橋。<br><strong>備案：</strong>舞濱 ➔ 八丁堀 (京葉線) ➔ 秋葉原 (日比谷線) ➔ 淺草橋。",

    # Day 3
    (3, "搭乘 JR 前往東京車站"): "淺草橋 ➔ 秋葉原 ➔ 東京站 (JR 山手線，車程 8 分鐘)。",
    (3, "東京車站丸之內站舍 (東京駅丸の内駅舎)"): "漫步丸之內站前開闊廣場，在清晨涼風中與百年壯麗紅磚建築合影。",
    (3, "返回東京車站一番街入口等待開門"): "<strong>🚨 避坑防刷卡指南：</strong>從丸之內（西側）跨越到八重洲（東側）時，<strong>請走站外的「北地下自由通路」</strong>！千萬別刷 Suica 誤進站！",
    (3, "東京車站一番街 (東京駅一番街) (八重洲地下中央口)"): "10:00 一開門優先逛：寶可夢商店（站長皮卡丘）、TOMICA 專賣店、吉伊卡哇商店、橡子共和國（龍貓）。",
    (3, "KITTE花園 (ＫＩＴＴＥガーデン) (KITTE 6F)"): "搭電梯直達 KITTE 6F 屋頂花園，免費俯瞰東京車站紅磚站舍全景與新幹線進出站，室內空調充足。",
    (3, "午餐（東京車站周邊）"): "<strong>首選餐廳：</strong><a class=\"map-link-inline\" href=\"https://maps.app.goo.gl/uX7kK5Wj9s6k1y8N7\" target=\"_blank\">🍤 天丼てんや 八重洲店 🔗</a> (八重洲地下街 南1號) 享用日式炸蝦天丼（人均 ¥560～¥850）。出餐極快、平價美味！<br><strong>備案 1：</strong>だし茶漬け えん KITTE丸の内店 (高湯茶泡飯，¥850-1,100)<br><strong>備案 2：</strong>燕子烤肉漢堡排 (大丸東京店 12F)",
    (3, "前往上野"): "搭乘 JR 山手線 8 分鐘直達上野站（公園口出站設有電梯）。",
    (3, "國立科學博物館 (国立科学博物館)"): "正午避暑勝地！參觀地球館 B1 恐龍化石骨骼、3F 野生動物標本展廳及 360 度球幕影院，冷氣充足放鬆。",
    (3, "超人氣晚餐 ：鴨 to 蔥拉麵"): "<strong>首選名店：</strong>香濃鴨肉醬油拉麵（人均 ¥1,000～¥1,400）。<br><strong>🚨 排隊停損防雷規則：</strong>排隊 ≤ 3 組才吃，超過直接啟動阿美橫丁小吃備案，絕不在烈日下苦等！",
    (3, "阿美橫丁採買"): "<strong>必掃名店：</strong><br>• 二木菓子（二木の菓子 第一営業所）：掃日本零食名產（Calbee、干貝糖）。<br>• OS Drug 上野店：藥妝免退稅價格之冠。<br>• 街邊小吃：肉之大山炸肉餅、みなとや章魚燒。<br>• 多慶屋（TAKEYA）：紫色商場一站式補貨備案。",
    (3, "回程：前往JR 御徒町站"): "步行至 JR 御徒町站搭乘電車返回淺草橋。",
    (3, "晚餐（若下午沒吃鴨 to 蔥拉麵）"): "晚餐備案：吉野家 / 松屋 浅草橋店 / ろく月 雞白湯拉麵。",
    (3, "宵夜／點心（若下午已吃鴨 to 蔥拉麵）"): "外帶 Cow Cow Kitchen 牛奶起司派或便利商店點心。",

    # Day 4
    (4, "前往三鷹"): "淺草橋 ➔ 御茶之水 (總武線)。<strong>在御茶之水站「同月台正對面」無縫平行換乘</strong> JR 中央線快速直達三鷹站，省下 15 分鐘！",
    (4, "吉卜力接駁巴士"): "三鷹站南口 9 號公車站搭乘黃色龍貓彩繪接駁巴士（車程約 5 分鐘）。",
    (4, "三鷹之森吉卜力美術館 (三鷹の森ジブリ美術館)"): "參觀重點：龍貓售票亭 ➔ 貓巴士 ➔ 土星座短篇動畫 ➔ 屋頂天空之城巨神兵機械人。預約 10:00 第一梯次入場。",
    (4, "前往吉祥寺(吉祥寺)（Plan A 直達公車 / Plan B 林蔭散步）"): "<strong>首選 Plan A (防中暑公車)：</strong>美術館旁「萬助橋」站牌搭公車 5 分鐘直達吉祥寺站南口。<br><strong>備案 Plan B：</strong>走「井之頭恩賜公園」林蔭步道欣賞湖景。",
    (4, "午餐：大戶屋"): "<strong>首選餐廳：</strong><a class=\"map-link-inline\" href=\"https://maps.app.goo.gl/34k8Z1T3v7sW6\" target=\"_blank\">🍱 大戶屋 吉祥寺店 🔗</a> (ホワイトハウスビル 2F) 享用日式烤魚/雞肉定食（人均 ¥1,000～¥1,500，門口抽號入座）。<br><strong>備案：</strong>花丸烏龍麵 吉祥寺南口店 (讚岐烏龍麵，2 分鐘秒入座)。",
    (4, "吉祥寺商圈慢活 + 下午茶：SATOU 炸牛肉丸"): "逛 Sunroad 商店街（Loft 文具旗艦店、無印良品、大創）、探索哈莫尼卡橫丁昭和風情。排隊 10 人以下購買 <strong>SATOU 黑毛和牛炸牛肉丸</strong>。",
    (4, "晚餐：串家物語"): "<strong>首選餐廳：</strong><a class=\"map-link-inline\" href=\"https://maps.app.goo.gl/kX7m3Q8L9P2t4v8W9\" target=\"_blank\">🍢 串家物語 吉祥寺店 🔗</a> (ダイヤパレス吉祥寺 2F) 享用 DIY 炸串吃到飽（人均 ¥2,000～¥3,000）。<strong>建議 17:00 Hotpepper 線上預訂免排隊</strong>！<br><strong>備案：</strong>花丸烏龍麵 / 一風堂 吉祥寺店。",
    (4, "返回淺草橋"): "進站前外帶「Linde 德國麵包」或「Jyonetsu Bakery」人氣麵包當明日早餐。搭中央快速線至御茶之水同月台換總武線返回淺草橋。",
    (4, "回飯店休息"): "返抵海茵娜酒店休息。",

    # Day 5
    (5, "前往淺草"): "都營淺草線：淺草橋站 ➔ 淺草站 (直達僅 2 站 3 分鐘)。走 1 號或 3 號出口步行 1 分鐘即達雷門。",
    (5, "淺草寺"): "清晨人少漫步參拜：雷門大紅燈籠 ➔ 仲見世商店街 ➔ 寶藏門 ➔ 本堂祈福參拜。",
    (5, "展望台：淺草文化觀光中心 (浅草文化観光センター) (8F 展望台)"): "搭電梯直上 8 樓免費觀景台，俯瞰雷門、仲見世街紅色屋頂長廊與晴空塔全景，室內吹冷氣休憩。",
    (5, "前往東京晴空塔 (東京スカイツリー)"): "東武淺草站搭乘東武晴空塔線火車 3 分鐘直達「東京晴空塔站」，慢步搭電梯至 7 樓餐廳區。",
    (5, "午餐：東京晴空街道(東京ソラマチ) 餐廳街"): "<strong>首選餐廳：</strong><a class=\"map-link-inline\" href=\"https://maps.app.goo.gl/UaJR8NaOGGAR48j67\" target=\"_blank\">🥞 達摩文字燒 晴空塔店 🔗</a> (東京ソラマチ 7F) 享用東京下町文字燒與大阪燒（人均 ¥1,200～¥1,800）。店員桌邊代烤，11:00 開門免排隊！<br><strong>備案 1：</strong>利久牛舌 晴空塔店 (6F 碳烤牛舌定食)<br><strong>備案 2：</strong>宮武讚岐烏龍麵 / 一風堂 (3F 美食街)",
    (5, "墨田水族館 (すみだ水族館) (東京晴空塔城 5F/6F)"): "正午避暑！參觀超大開放式企鵝池、水母萬花筒隧道、金魚大展與東京大水槽。館內沙發座位多，長輩小孩悠閒吹冷氣放鬆。",
    (5, "【Option 選配行程】東京晴空街道 (東京ソラマチ) 散策與 30/31F 高空景觀"): "逛寶可夢中心、橡子共和國、晴空塔限定紀念品；搭電梯至 30F/31F 免費展望長廊俯瞰東京市景。",
    (5, "前往新宿西口（Plan A 交通）"): "押上站搭乘地鐵半藏門線至九段下站，同月台轉乘都營新宿線直達 新宿站 (車程約 25 分鐘)。",
    (5, "晚餐：新宿西口平價美食"): "<strong>首選餐廳：</strong><a class=\"map-link-inline\" href=\"https://maps.app.goo.gl/uX7kK5Wj9s6k1y8N7\" target=\"_blank\">🍔 麥當勞 新宿西口店 🔗</a> (繁體中文自動點餐機，出餐極快，人均 ¥600～¥1,000)。<br><strong>備案：</strong>摩斯漢堡 新宿西口店 (日式米漢堡，人均 ¥700～¥1,100)。",
    (5, "東京都廳第一本廳舍 (東京都庁舎) (南展望室 45F)"): "免費搭乘高速電梯直達 45 樓（202 公尺高空），欣賞 360 度百萬東京夜景（東京鐵塔、晴空塔與璀璨城市燈海）。",
    (5, "返回淺草橋"): "由新宿站搭乘 JR 中央快速線至御茶之水站，同月台轉乘總武線返回 淺草橋站。",
    (5, "晚餐：東京晴空街道 3F 美食街 (Plan B)"): "在 3 樓美食街享用宮武讚岐烏龍麵或一風堂拉麵（人均 ¥700～¥1,200）。隨後搭都營淺草線 4 站直達淺草橋。",

    # Day 6
    (6, "早餐與整理行李"): "享用早餐，整理行李辦理 Check-out，將全部大件行李免費寄放於海茵娜酒店櫃檯，輕裝出發。",
    (6, "退房"): "辦理退房手續，行李寄放櫃台。",
    (6, "前往築地場外市場"): "都營淺草線：淺草橋站 ➔ 東銀座站 (直達免轉車，僅 8 分鐘)。由 5 號或 6 號出口步行 3 分鐘即達築地。",
    (6, "築地場外市場（早餐）"): "享用現做熱騰騰美食：<strong>「築地山長」現做玉子燒</strong>（¥150-200/份）、現烤海鮮、新鮮草莓大福。隨後參訪波除稻荷神社。",
    (6, "前往東銀座站回飯店"): "步行至東銀座站搭乘都營淺草線返回淺草橋站。",
    (6, "領行李與車站移動"): "回海茵娜酒店櫃檯領取全部大行李，慢步前往淺草橋站 A1 無障礙電梯出口。",
    (6, "前往羽田機場 (超便利直達)"): "<strong>無障礙電梯進站：</strong>走淺草橋站 <strong>A1 出口無障礙電梯</strong> 直達月台，搭乘「機場快特 (直通京急線)」直達 羽田機場第3航廈站 (車程約 40-45 分鐘，免轉乘)。",
    (6, "辦理登機與安檢"): "起飛前 2.5 小時抵達第 3 航廈辦理登機與託運行李。逛江戶小路商場、觀景台看飛機起降。",
    (6, "輕食午餐與免稅店最後採買"): "管制區內享用平價定食/烏龍麵。於免稅店採買伴手禮（白色戀人、東京香蕉、Royce巧克力），14:00 前往登機門。",
    (6, "搭機返台 (CI221)"): "搭乘中華航空 CI221 班機（14:30 起飛），滿載戰利品與美好回憶平安返抵台北松山機場 (16:55)。"
}

def get_best_map_link(title, body):
    # 1. Search in body for explicit markdown link
    md_links = re.findall(r'\[.*?\]\((https?://[^\)]+)\)', title + " " + body)
    if md_links:
        return clean_url(md_links[0])
    
    # 2. Search in body for bare maps link
    bare_links = re.findall(r'https://www\.google\.com/maps/search/\?api=1&query=[^\s\)\"\']+|https://maps\.google\S+|https://maps\.app\S+|https://share\.google\S+', title + " " + body)
    if bare_links:
        return clean_url(bare_links[0])
        
    # 3. Search in MASTER_NAV_MAP
    for k, url in MASTER_NAV_MAP.items():
        if k in title:
            return clean_url(url)
            
    # 4. Fallback search URL
    clean_q = urllib.parse.quote(title)
    return f"https://www.google.com/maps/search/?api=1&query={clean_q}"

def parse_v10_markdown():
    filepath = '/home/owen/tokyo/2026東京親子自由行_V10_Henna.md'
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
        2: {'parents': [], 'kids': []},
        3: [],
        4: [],
        5: {'common_before': [], 'plan_a': [], 'plan_b': []},
        6: []
    }

    # Split Day 1
    d1_match = re.search(r'## \*\*📅 Day 1.*?\n(.*?)(?=\n## \*\*📅 Day 2|\Z)', content, re.DOTALL)
    if d1_match:
        d1_text = d1_match.group(1)
        # Split by ### or ####
        slots = re.split(r'\n(?=#{3,4} \*\*)', d1_text)
        current_sub = 'common_before'
        for s in slots:
            s = s.strip()
            if not s:
                continue
            lines = s.split('\n')
            h = lines[0]
            b = '\n'.join(lines[1:])
            
            if 'Plan A' in h:
                current_sub = 'plan_a'
                continue
            elif 'Plan B' in h:
                current_sub = 'plan_b'
                continue
            elif '共同收尾' in h:
                current_sub = 'common_after'
                continue

            h_clean = h.replace('####', '').replace('###', '').replace('**', '').strip()
            time_m = re.match(r'^([\d:：]+－[\d:：]+|[\d:：]+)\s*(.*)', h_clean)
            slot_time = time_m.group(1) if time_m else ""
            slot_title_raw = time_m.group(2) if time_m else h_clean
            slot_title = clean_title(slot_title_raw)
            if not slot_title:
                continue

            cat, cat_zh, cat_icon = get_category_info(slot_title)
            maps_link = get_best_map_link(slot_title_raw, b)
            
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
            maps_link = get_best_map_link(slot_title_raw, b)
            summary = CUSTOM_SUMMARIES_V10.get((2, slot_title))
            if not summary:
                for (d, t), sm in CUSTOM_SUMMARIES_V10.items():
                    if d == 2 and (t in slot_title or slot_title in t):
                        summary = sm
                        break
            if not summary:
                summary = clean_markdown_for_summary(b)
            days_data[2]['parents'].append({
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
            maps_link = get_best_map_link(slot_title_raw, b)
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
                maps_link = get_best_map_link(slot_title_raw, b)
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
            lines = s.split('\n')
            h = lines[0]
            b = '\n'.join(lines[1:])
            
            if 'Plan A' in h:
                current_sub = 'plan_a'
                # Check if this block contains text
                if '前往新宿西口' in b:
                    pass
            elif 'Plan B' in h:
                current_sub = 'plan_b'

            h_clean = h.replace('####', '').replace('###', '').replace('**', '').strip()
            time_m = re.match(r'^([\d:：]+－[\d:：]+|[\d:：]+)\s*(.*)', h_clean)
            slot_time = time_m.group(1) if time_m else ""
            slot_title_raw = time_m.group(2) if time_m else h_clean
            slot_title = clean_title(slot_title_raw)
            if not slot_title or 'Plan A' in slot_title or 'Plan B' in slot_title:
                if 'Plan A' in h and len(b.strip()) > 10:
                    slot_title = "新宿都廳百萬夜景 (Plan A 全覽)"
                elif 'Plan B' in h and len(b.strip()) > 10:
                    slot_title = "晴空街道商場與美食街 (Plan B 全覽)"
                else:
                    continue
            cat, cat_zh, cat_icon = get_category_info(slot_title)
            maps_link = get_best_map_link(slot_title_raw, b)
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
            <div class="card-actions">
              <a class="map-link-btn" href="{item['maps_link']}" target="_blank" title="開啟 Google Maps 導航">📍 導航</a>
            </div>
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
      <div class="sub-toggle-wrapper">
        <div class="sub-toggle-container">
          <button class="sub-toggle-btn active" id="day2-btn-parents" onclick="switchDay2Group('parents')">👵 長輩組：上野松坂屋 × 國立西洋美術館 × 鰻魚飯</button>
          <button class="sub-toggle-btn" id="day2-btn-kids" onclick="switchDay2Group('kids')">🏰 親子組：東京迪士尼樂園全日歡樂體驗</button>
        </div>
      </div>
      <div class="day2-parents-itinerary">
"""
    for idx, it in enumerate(days_data[2]['parents']):
        timeline_html += build_card_html(f"d2p-{idx}", it)
    timeline_html += """      </div>
      <div class="day2-kids-itinerary" style="display: none;">
"""
    for idx, it in enumerate(days_data[2]['kids']):
        timeline_html += build_card_html(f"d2k-{idx}", it)
    timeline_html += '      </div>\n    </div>\n\n'

    # Day 3
    timeline_html += """    <!-- Day 3 Section -->
    <div class="day-section" id="day3-section" style="display: none;">
"""
    for idx, it in enumerate(days_data[3]):
        timeline_html += build_card_html(f"d3-{idx}", it)
    timeline_html += '    </div>\n\n'

    # Day 4
    timeline_html += """    <!-- Day 4 Section -->
    <div class="day-section" id="day4-section" style="display: none;">
"""
    for idx, it in enumerate(days_data[4]):
        timeline_html += build_card_html(f"d4-{idx}", it)
    timeline_html += '    </div>\n\n'

    # Day 5
    timeline_html += """    <!-- Day 5 Section -->
    <div class="day-section" id="day5-section" style="display: none;">
      <div class="sub-toggle-wrapper">
        <div class="sub-toggle-container">
          <button class="sub-toggle-btn active" id="day5-btn-planA" onclick="switchDay5Plan('A')">🌃 Plan A：新宿西口平價速食 × 都廳百萬夜景</button>
          <button class="sub-toggle-btn" id="day5-btn-planB" onclick="switchDay5Plan('B')">🛍️ Plan B：晴空街道商場悠遊 × 3F美食街晚餐</button>
        </div>
      </div>
"""
    for idx, it in enumerate(days_data[5]['common_before']):
        timeline_html += build_card_html(f"d5-cb{idx}", it)
    timeline_html += '      <div class="day5-plan-A">\n'
    for idx, it in enumerate(days_data[5]['plan_a']):
        timeline_html += build_card_html(f"d5-pa{idx}", it)
    timeline_html += '      </div>\n'
    timeline_html += '      <div class="day5-plan-B" style="display: none;">\n'
    for idx, it in enumerate(days_data[5]['plan_b']):
        timeline_html += build_card_html(f"d5-pb{idx}", it)
    timeline_html += '      </div>\n    </div>\n\n'

    # Day 6
    timeline_html += """    <!-- Day 6 Section -->
    <div class="day-section" id="day6-section" style="display: none;">
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

    /* Modal Sheet */
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
      <button class="day-tab active" onclick="switchDay(1)">Day 1 (8/20)</button>
      <button class="day-tab" onclick="switchDay(2)">Day 2 (8/21)</button>
      <button class="day-tab" onclick="switchDay(3)">Day 3 (8/22)</button>
      <button class="day-tab" onclick="switchDay(4)">Day 4 (8/23)</button>
      <button class="day-tab" onclick="switchDay(5)">Day 5 (8/24)</button>
      <button class="day-tab" onclick="switchDay(6)">Day 6 (8/25)</button>
    </nav>
  </header>

  <section class="meta-card">
    <div class="meta-row">
      <span class="meta-label">🏨 住宿飯店</span>
      <span class="meta-val">
        {meta['hotel_name']}
        <a class="copy-btn" href="https://www.google.com/maps/search/?api=1&query={urllib.parse.quote(meta['hotel_name'])}" target="_blank">導航</a>
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

    function switchDay5Plan(plan) {{
      const isPlanA = plan === 'A';
      document.getElementById('day5-btn-planA').classList.toggle('active', isPlanA);
      document.getElementById('day5-btn-planB').classList.toggle('active', !isPlanA);
      document.querySelector('.day5-plan-A').style.display = isPlanA ? 'block' : 'none';
      document.querySelector('.day5-plan-B').style.display = isPlanA ? 'none' : 'block';
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
    print("✅ Successfully built and verified itinerary.html (PWA version V10)!")

if __name__ == '__main__':
    main()
