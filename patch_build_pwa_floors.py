import re

with open('/home/owen/tokyo/build_pwa.py', 'r', encoding='utf-8') as f:
    code = f.read()

# Update CUSTOM_SUMMARIES_V10 in build_pwa.py with exact building and floor numbers
code = code.replace(
    '萬代扭蛋百貨店 秋葉原店 (ガシャポンのデパート 秋葉原店)',
    '萬代扭蛋百貨店 秋葉原店 (ガシャポンのデパート 秋葉原店)'
)
code = code.replace(
    '秋葉原規模最大官方扭蛋專門店，近千台最新動漫',
    '位於 <strong>いちご秋葉原駅前ビル 4F (namco秋葉原店 4F)</strong>，全秋葉原規模最大官方扭蛋專門店之一，擁有近千台最新動漫'
)
code = code.replace(
    '壽司郎 秋葉原駅前店',
    '壽司郎 秋葉原駅前店 (BiTO AKIBA B1F)'
)
code = code.replace(
    'Gusto 新宿NOWAビル店',
    'Gusto 新宿NOWAビル店 (7F)'
)
code = code.replace(
    '喫茶 トリコロール (松坂屋本館 2F)',
    '喫茶 トリコロール (松坂屋上野店 本館 4F)'
)
code = code.replace(
    '天丼てんや 八重洲店 🔗</a> (八重洲地下街 南1號)',
    '天丼てんや 八重洲店 🔗</a> (八重洲地下街 B1F 南1號)'
)
code = code.replace(
    '大戶屋 (大戸屋ごはん処 吉祥寺店)',
    '大戶屋 (大戸屋ごはん処 吉祥寺店) (ホワイトハウスビル 2F)'
)
code = code.replace(
    '串家物語 (神楽食堂 串家物語 吉祥寺店)',
    '串家物語 (神楽食堂 串家物語 吉祥寺店) (ダイヤパレス吉祥寺 2F)'
)
code = code.replace(
    'Cow Cow Kitchen 牛奶起司派 🔗</a>',
    'Cow Cow Kitchen 牛奶起司派 🔗</a> (ルミネエスト新宿 LUMINE EST 1F)'
)
code = code.replace(
    '達摩文字燒 (月島名物もんじゃ だるま 東京スカイツリータウン・ソラマチ店)',
    '達摩文字燒 (月島名物もんじゃ だるま 東京スカイツリータウン・ソラマチ店) (東京ソラマチ 東館 7F 餐廳街)'
)

with open('/home/owen/tokyo/build_pwa.py', 'w', encoding='utf-8') as f:
    f.write(code)

print("Patched build_pwa.py with floor info!")
