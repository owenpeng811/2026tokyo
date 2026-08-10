for fname in ['README.md', '2026東京親子自由行_V10_Henna.md']:
    fpath = f'/home/owen/tokyo/{fname}'
    with open(fpath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Fix Tokyo station photo emoji
    content = content.replace('### **09:25－09:45 \ufffd\ufffd 欣賞東京車站丸之內站舍建築**', '### **09:25－09:45 📸 欣賞東京車站丸之內站舍建築**')
    content = content.replace('### **09:25－09:45  欣賞東京車站丸之內站舍建築**', '### **09:25－09:45 📸 欣賞東京車站丸之內站舍建築**')
    content = content.replace('### **09:25－09:45  欣賞東京車站丸之內站舍建築**', '### **09:25－09:45 📸 欣賞東京車站丸之內站舍建築**')

    # Fix Ghibli bus emoji
    content = content.replace('> * \ufffd\ufffd **接駁巴士外觀特徵**：', '> * 🚌 **接駁巴士外觀特徵**：')
    content = content.replace('> *  **接駁巴士外觀特徵**：', '> * 🚌 **接駁巴士外觀特徵**：')
    content = content.replace('> *  **接駁巴士外觀特徵**：', '> * �� **接駁巴士外觀特徵**：')

    with open(fpath, 'w', encoding='utf-8') as f:
        f.write(content)

print("Fixed corrupt emojis in both Markdown files!")
