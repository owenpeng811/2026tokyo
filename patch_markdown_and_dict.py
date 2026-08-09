import json, re

with open('/home/owen/tokyo/navigation_links_dict.json', 'r', encoding='utf-8') as f:
    nav_dict = json.load(f)

# Update 2026東京親子自由行_V10_Henna.md & README.md
for fpath in ['/home/owen/tokyo/2026東京親子自由行_V10_Henna.md', '/home/owen/tokyo/README.md']:
    with open(fpath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Day 3 backup dinner explicit links
    content = content.replace(
        "首選餐廳：**吉野家 (吉野家 浅草橋店)**",
        f"首選餐廳：[**吉野家 (吉野家 浅草橋店)**]({nav_dict['吉野家 (吉野家 浅草橋店)']})"
    )
    content = content.replace(
        "備案餐廳：**松屋 (松屋 浅草橋店)**",
        f"備案餐廳：[**松屋 (松屋 浅草橋店)**]({nav_dict['松屋 (松屋 浅草橋店)']})"
    )
    content = content.replace(
        "備案餐廳：**拉麵 ろく月 (らーめん ろく月)**",
        f"備案餐廳：[**拉麵 ろく月 (らーめん ろく月)**]({nav_dict['拉麵 ろく月 (らーめん ろく月)']})"
    )
    content = content.replace(
        "外帶 **Cow Cow Kitchen (東京Milk Cheese Factory)**",
        f"外帶 [**Cow Cow Kitchen (東京Milk Cheese Factory)**]({nav_dict['Cow Cow Kitchen (東京Milk Cheese Factory)']})"
    )

    with open(fpath, 'w', encoding='utf-8') as f:
        f.write(content)

print("Patched markdown files with explicit links!")
