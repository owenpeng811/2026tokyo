for fname in ['2026東京親子自由行_V10_Henna.md', 'README.md']:
    fpath = f'/home/owen/tokyo/{fname}'
    with open(fpath, 'r', encoding='utf-8') as f:
        text = f.read()

    text = text.replace('16:50－17:10 \ufffd\ufffd 日系拍貼機', '16:50－17:10 📸 日系拍貼機')
    text = text.replace('16:50－17:10  日系拍貼機', '16:50－17:10 📸 日系拍貼機')
    text = text.replace('16:50－17:10  日系拍貼機', '16:50－17:10 📸 日系拍貼機')

    text = text.replace('09:20－10:20 \ufffd\ufffd 晨間不忍池', '09:20－10:20 🌿 晨間不忍池')
    text = text.replace('09:20－10:20  晨間不忍池', '09:20－10:20 🌿 晨間不忍池')
    text = text.replace('09:20－10:20  晨間不忍池', '09:20－10:20 🌿 晨間不忍池')

    text = text.replace('19:00 \ufffd\ufffd 前往御徒町站搭車', '19:00 🚆 前往御徒町站搭車')
    text = text.replace('19:00  前往御徒町站搭車', '19:00 🚆 前往御徒町站搭車')
    text = text.replace('19:00  前往御徒町站搭車', '19:00 🚆 前往御徒町站搭車')

    # Remove any remaining \ufffd
    text = text.replace('\ufffd', '')

    with open(fpath, 'w', encoding='utf-8') as f:
        f.write(text)

print("Fixed all corrupted emojis in Markdown files!")
