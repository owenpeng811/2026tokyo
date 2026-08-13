# 手動更新 PWA 行程表 SOP

當你手動編輯完 `README.md` 之後，網頁版行程表（`itinerary.html`）**不會自動更新**，必須手動執行本文件的步驟重新編譯。

> `README.md` 是唯一的內容來源，`itinerary.html` 是編譯產物。
> **永遠不要手動編輯 `itinerary.html`** — 下次編譯會整份覆寫，改動會全部消失。

---

## 前置需求

只需要 Python 3，**不需要安裝任何套件**（全部使用標準函式庫）。

```bash
python3 --version    # 確認有 Python 3
cd /home/owen/tokyo  # 所有指令都在專案根目錄執行
```

---

## 操作流程

### 步驟 1：編譯 PWA

```bash
python3 build_pwa.py
```

**預期輸出：**

```
✅ Successfully built and verified itinerary.html!
```

這一步會讀取 `README.md`，重新產生整份 `itinerary.html`（單一檔案，內含全部 CSS/JS，可離線使用）。

### 步驟 2：跑驗證管線

```bash
python3 full_validation_pipeline.py
```

會實際連網逐一測試每個 Google Maps 連結，約需數十秒。**預期輸出：**

```
--- [階段 1] 掃描正文中是否有未加超連結的『粗體裸字實體』 ---
✅ 粗體裸字實體掃描 100% 通過！

--- [階段 2] 審查所有已標註超連結的命名格式 ---
✅ ...

--- [階段 3] 逐一測試所有 Google Maps 導航連結有效性 ---
  ✅ 正確有效數：127
  ❌ 異常失效數：0

🎉 驗證完全通過！
```

有問題請看下方「疑難排解」。

### 步驟 3：本機預覽（選用，但建議）

```bash
python3 -m http.server 8000
```

瀏覽器開 <http://localhost:8000/itinerary.html>，檢查新改的時段卡片有正確出現。按 `Ctrl+C` 結束。

> 一定要用這個方式預覽，不要直接用檔案總管雙擊開啟。Service Worker 只在 `http://` 或 `https://` 下才會註冊，用 `file://` 開啟看不到 PWA 的離線與安裝行為。

### 步驟 4：發布

```bash
git add README.md itinerary.html
git commit -m "docs: <這次改了什麼>，同步編譯 PWA"
git push
```

推上去後 GitHub Pages 會自動更新，手機端重新開啟即可看到新版。

---

## 編輯 `README.md` 的格式規則（重要）

`build_pwa.py` 是用**正規表達式**去切 Markdown 的，所以標題的寫法就等於程式的介面規格。以下格式寫錯，程式**不會報錯**，只會靜默漏掉整個時段：

### 每日大標題

```markdown
## **📅 Day 3（8/22 星期六）：東京車站 × 三鷹吉卜力**
```

### 時段卡片標題

```markdown
### **10:00－10:50 🍬 逛東京菓子樂園**
```

必須符合：

| 項目 | 規則 |
| :-- | :-- |
| 層級 | `###` 或 `####`（三或四個井號） |
| 粗體 | 標題整段要用 `**` 包起來 |
| 時間 | `HH:MM－HH:MM`，中間是**全形破折號 `－`**，不是半形 `-` |
| Emoji | 時間後面接一個 emoji |
| 名稱 | 寫「做什麼」而不是店名，例如 `逛東京菓子樂園` 而非 `東京おかしランド` |

### 分支切換的關鍵字

網頁版的二級切換頁籤（晴天／雨天、Plan A／Plan B、長輩組／親子組）是靠**標題關鍵字**判斷的，這些字不能改：

`Plan A` ／ `Plan B` ／ `共同收尾` ／ `長輩組` ／ `親子組` ／ `☀️ 晴天` ／ `☔ 雨天`

---

## 新增景點或餐廳時的額外步驟

> ⚠️ **2026-08 流程已變更**：導航連結改以 `places.json` 為唯一真相來源，
> `navigation_links.html` 與三個 JSON 都變成自動生成的產物，**不要再手動編輯它們**。

新增地點的正確流程：

```bash
# 1. 用 Place ID Finder 查到真實的 Place ID 與經緯度（嚴禁自己編）
#    https://developers.google.com/maps/documentation/javascript/examples/places-placeid-finder

# 2. 編輯 places.json 新增一筆（只改這個檔案）

# 3. 生成四個衍生檔
python3 sync_places.py --generate

# 4. 讓 README 內文網址與 places.json 一致
python3 sync_places.py --check     # 先看有哪些不一致
python3 sync_places.py --fix       # 自動修正

# 5. 稽核有無偽造特徵
python3 place_id_audit.py
```

<details>
<summary>📌 舊流程（已停用，僅供理解歷史）</summary>

若這次編輯**新增了一個地點**，光改 `README.md` 還不夠，導航連結要一併登錄：

1. 到 Google Maps 找到該店家，取得永久標準網址：

   ```
   https://www.google.com/maps/search/?api=1&query=緯度,經度&query_place_id=ChIJxxxxxxxxxxxx
   ```

   > ⚠️ **不要用 `maps.app.goo.gl` 短網址**，那種連結會失效（`Dynamic Link Not Found`），驗證管線的階段 3 會直接擋下來。

2. 在 `navigation_links.html`（人工校對用的基準對照表）登錄一筆。

3. 視用途同步到對應的 JSON：

   | 檔案 | 什麼時候要加 |
   | :-- | :-- |
   | `navigation_links_dict.json` | 一律都要加（主字典） |
   | `first_destinations.json` | 這個地點是某時段的**第一個目的地**時。key 格式為 `"天數_標題關鍵字"`，例如 `"3_逛東京菓子樂園"` |
   | `text_entities.json` | 希望這個店名在內文中被**自動加上連結**時（格式為 `["店名", "網址"]`） |

4. `README.md` 正文提到這個地點時，一律要包成超連結：

   ```markdown
   [**東京菓子樂園 (東京おかしランド)**](https://www.google.com/maps/search/?api=1&query=...)（八重洲地下中央口 B1F）
   ```

   只寫 `**東京菓子樂園 (東京おかしランド)**` 而沒有連結，驗證管線階段 1 會報錯。

</details>

---

## 匯出到 Google My Maps（每天一個圖層）

```bash
python3 export_mymaps.py --merged
```

會在 `exports/` 產生 `Day1.csv`、`Day2_長輩組.csv`、`Day2_親子組.csv`、`Day3.csv`…`Day6.csv`，外加合併的 `All.csv`。

### 匯入步驟

1. 開 <https://www.google.com/mymaps> ➔ **建立新地圖**
2. 點 **「匯入」** ➔ 上傳 `Day1.csv`
3. 「**選擇要放置地標的欄位**」：勾選 **`緯度`** 和 **`經度`** 兩欄
4. 「**選擇要做為地標標題的欄位**」：選 **`名稱`**
5. 圖層名稱改成「Day 1」
6. 點該圖層的 **「個別樣式」** ➔ 改為 **「依資料欄分類：`類別`」**，即可讓景點／餐廳／交通／購物／住宿各自一種顏色與圖示
7. 重複步驟 2–6 匯入其餘天數，每個 CSV 各自成為一個圖層

### 兩個限制要注意

- **My Maps 一張地圖最多 10 個圖層**。本行程共 7 個 CSV（Day 2 分長輩組／親子組），還有 3 層的餘裕。
- ⚠️ **My Maps 完全不吃 Place ID**，只認經緯度或地理編碼。因此 CSV 的定位依據是 `緯度`／`經度` 欄，與行程表導航連結用的 `query_place_id` 是兩套機制。

### 沒有座標的地點

有少數地點只有店名查詢連結、沒有座標（執行時會列出）。這些請**單獨匯入一次**，在步驟 3 改選 **`定位用名稱`** 欄，讓 My Maps 用日文店名地理編碼。

---

## 疑難排解

| 症狀 | 原因與處理 |
| :-- | :-- |
| 網頁上**整個時段消失** | 標題格式不合。檢查是否為 `### **` 開頭、時間是否用**全形 `－`**。 |
| 卡片**摘要沒跟著更新** | 該時段的摘要被 `build_pwa.py` 裡的 `CUSTOM_SUMMARIES_V10` 手寫覆蓋了，它以「(天數, 標題)」為索引。**改了標題文字就要同步改那裡**，否則舊摘要會繼續顯示。 |
| 卡片**沒有「📍 導航」按鈕** | 到 `places.json` 該地點的 `first_dest` 欄位加一筆 `"天數_標題關鍵字"`，再跑 `sync_places.py --generate`。（**不要直接改 `first_destinations.json`，會被覆蓋**） |
| 導航**導到錯誤的地點** | Place ID 可能是偽造或已失效。跑 `python3 place_id_audit.py` 稽核，再用 Place ID Finder 查真值後改 `places.json`。⚠️ 連結能開、回 HTTP 200 **不代表 Place ID 有效**。 |
| 改了字典檔卻**沒生效／又變回去** | 四個字典檔都是 `sync_places.py --generate` 的產物，手改會被覆蓋。**唯一該改的是 `places.json`**。 |
| **不該有導航卻出現**（如「退房」「就寢」） | 到 `build_pwa.py` 的 `is_non_nav_slot()` 函式，把這個時段標題加進靜態清單。 |
| 導航按鈕**指到錯的地方** | `first_destinations.json` 的 key 是用「包含」比對的，可能誤中別的時段。把 key 寫得更精確一點。 |
| 驗證**階段 1** 報錯（粗體裸字） | 正文有 `**中文 (日文)**` 卻沒包超連結。照上面「新增景點」第 4 點補上連結。 |
| 驗證**階段 2** 報錯（命名規範） | 連結標籤要寫成 `中文名 (官方日文名)`。**例外**：如果那是部落格攻略、官網之類的參考連結而非實體地標，這是誤判，可以忽略。 |
| 驗證**階段 3** 報錯（連結失效） | 多半是用了 `maps.app.goo.gl` 短網址，換成含 Place ID 的標準網址。 |
| 手機上的 PWA **看不到新版** | 先確認 `git push` 成功。若仍是舊的，編輯 `sw.js` 把 `CACHE_NAME` 的版本號往上加（例如 `travel-itinerary-v10` → `v11`），重新編譯並推送，可強制所有裝置更新快取。 |

---

## 兩個網頁版的差別

同一份 `README.md` 會產生兩個不同的網頁，別搞混：

| | 檔案 | 由誰產生 | 特性 |
| :-- | :-- | :-- | :-- |
| **Docsify 版** | `index.html` | 瀏覽器直接讀 `README.md` | 長文瀏覽，`git push` 後立即生效，**不需要編譯** |
| **PWA 版** | `itinerary.html` | `build_pwa.py` 編譯 | 卡片式時間軸、可安裝到手機桌面、可離線、有打勾進度 |

也就是說：**只改文字內容的話，Docsify 版 push 完就更新了；但 PWA 版一定要跑過 `python3 build_pwa.py` 才會更新。**
