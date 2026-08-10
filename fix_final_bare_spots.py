with open('/home/owen/tokyo/navigation_links_dict.json', 'r', encoding='utf-8') as f:
    import json
    nav_dict = json.load(f)

for fname in ['README.md', '2026東京親子自由行_V10_Henna.md']:
    fpath = f'/home/owen/tokyo/{fname}'
    with open(fpath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Fix hotel heading
    content = content.replace(
        '**海茵娜酒店东京浅草桥 (Henn na Hotel Tokyo Asakusabashi)** (住宿 5 晚)',
        f"[**海茵娜酒店东京浅草桥 (変なホテル東京 浅草橋)**]({nav_dict['海茵娜酒店东京浅草桥']}) (住宿 5 晚)"
    )

    # Fix 淺草橋站(浅草橋駅)
    content = content.replace(
        '**淺草橋站(浅草橋駅)**',
        f"[**淺草橋站 (浅草橋駅)**]({nav_dict['淺草橋站']})"
    )

    with open(fpath, 'w', encoding='utf-8') as f:
        f.write(content)

print("Fixed top hotel header and Asakusabashi station!")
