# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Agent & Skill Rules

請遵守以下 Agent 與 Skill 的規範（內容為本專案的硬性規格，優先於一般慣例）：

@.agents/AGENTS.md
@.agents/skills/generate-travel-itinerary/SKILL.md
@.agents/skills/travel-itinerary-auditor/SKILL.md

## 專案性質

這不是一般軟體專案，而是一份 **2026 東京 6 天 5 夜親子自由行行程表**，以及把它編譯成離線 PWA 的工具鏈。真正的「原始碼」是 `README.md`（約 12 萬字的 Markdown 行程表）；Python 腳本是編譯器與 linter。

沒有測試框架、沒有套件管理檔、沒有 lint 設定。驗證靠 `full_validation_pipeline.py`，僅使用 Python 3 標準函式庫（`re`, `json`, `urllib`, `os`, `concurrent.futures`），無第三方依賴。

## 常用指令

```bash
# 編譯 PWA：README.md → itinerary.html（唯一的建置指令）
python3 build_pwa.py

# 全量驗證管線：階段 0 偽造偵測 + 粗體裸字 linter + 命名規範 + 全部連結 HTTP 檢測
# 失敗時 exit(1)。含網路請求（8 執行緒），約需數十秒
python3 full_validation_pipeline.py

# 導航連結：places.json 是唯一真相來源，四個字典檔皆由它生成
python3 sync_places.py --adopt      # 收編只存在於 README 的「孤兒連結」
python3 sync_places.py --generate   # 生成 navigation_links.html 與三個 JSON
python3 sync_places.py --check      # 檢查 README 內文網址是否與 places.json 一致
python3 sync_places.py --fix        # 自動修正 README 不一致的網址

# Place ID 離線偽造偵測（免 API key、免網路，已被驗證管線納為階段 0）
python3 place_id_audit.py
```

⚠️ 依 `.agents/AGENTS.md`：**微調 Markdown 後嚴禁自動執行 `build_pwa.py` 或 `git push`**，只有使用者明確要求（「轉成網頁版」／「更新 PWA」／「幫我 push」）時才執行。

驗證管線沒有「單一測試」的概念；若只想跑某一階段，直接在該檔案內以 `exit()` 提早中斷，或另寫暫存腳本置於 scratchpad（根目錄曾為此累積 42 個一次性腳本而被清理，見 commit `f2cbfa7`——不要再把暫存腳本留在 repo 根目錄）。

## 資料流架構

```
README.md  ──(build_pwa.py: parse → render)──▶  itinerary.html  ──▶  PWA (sw.js + manifest.json)
    │                    ▲
    │                    │ 注入導航連結
    │        navigation_links_dict.json / first_destinations.json
    │        canonical_nav_map.json / text_entities.json
    │                    ▲
    │        navigation_links.html（人工校對的唯一基準表，168 筆）
    │
    └──(index.html: Docsify SPA)──▶  GitHub Pages 直接渲染 README.md
```

同一份 `README.md` 有 **兩條獨立的呈現路徑**，改動時兩邊都要成立：

1. **Docsify** (`index.html`) 直接在瀏覽器渲染 `README.md`——所以 Markdown 內可以（且必須）使用 `<details><summary>`、行內 HTML 與錨點膠囊。
2. **PWA** (`build_pwa.py` → `itinerary.html`) 把 Markdown 重新解析成卡片式時間軸。

`2026東京親子自由行_V10_Henna.md` 是舊版快照，**不需維護**（見 AGENTS.md）。

## build_pwa.py 的解析契約（最脆弱的部分）

`parse_v10_markdown()` 用**正則表達式**切 `README.md`，因此 Markdown 的標題格式即為 API 契約。改動標題結構前務必確認對應的正則：

- 每日區塊：`## **📅 Day N（...）：...**`，以下一個 `## **📅 Day` 為界。
- 時段卡片：以 `### **` 或 `#### **` 切分（`re.split(r'\n(?=#{3,4} \*\*)')`），標題須為 `HH:MM－HH:MM <emoji> <活動名稱>`（全形破折號 `－`）。
- **分支切換靠標題關鍵字**，硬編在解析器內：`Plan A` / `Plan B` / `共同收尾` / `長輩組` / `親子組` / `☀️ 晴天` / `☔ 雨天`。`days_data` 的形狀因日而異：
  - Day 1、Day 5：`common_before / plan_a / plan_b`（Day 1 另有 `common_after`，Day 5 另有 `rainy`）
  - Day 2：`parents{common_before/sunny/rainy/common_after}` + `kids`
  - Day 3、4、6：單純列表
- 新增一天或新增分支形式，必須同時改 `parse_v10_markdown()` 與 `render_full_pwa_html()` 的頁籤邏輯。

其他關鍵函式：

- `get_category_info(title)` — 用中文關鍵字把時段分類為 food / transport / stay / attraction，決定卡片顏色與 emoji。新增料理或交通用語時要補關鍵字。
- `is_non_nav_slot(day, title, body)` — **白名單式**判斷哪些時段不該顯示「📍 導航」按鈕（飯店內早餐、退房、就寢、迪士尼園內表演等）。硬編中文字串清單；新增靜態時段須在此登錄，否則會產生無意義的關鍵字導航。
- `get_first_destination_map_link()` — 三段 fallback：`first_destinations.json`（key 格式 `"{day}_{標題關鍵字}"`）→ 內文第一個 Markdown 連結 → `navigation_links_dict.json` 最長字串匹配。
- `autolink_text_entities()` — 把 `text_entities.json`（list of `[名稱, URL]`）中的地名在已渲染 HTML 中自動加上連結，會跳過既有 `<a>` 區段，每個名稱最多取代 2 次。
- `CUSTOM_SUMMARIES_V10` — 以 `(day, title)` 為 key 的手寫卡片摘要，覆蓋自動生成的摘要。改標題時這裡也要跟著改，否則摘要會靜默失效（見 commit `f5d8b9b`、`a9b6bb8`）。

## 導航連結：places.json 為唯一真相來源

⚠️ **2026-08 流程變更**：原本同一網址散落 5 個檔案且無同步機制，導致大量偽造 Place ID 與座標漂移。現改為單一真相來源＋自動生成。

| 檔案 | 角色 |
| :-- | :-- |
| **`places.json`** | **唯一真相來源，只改這裡**。每筆記錄 `url`／`nav_dict`／`text_entities`／`first_dest`／`html`／`verified_at` |
| `navigation_links_dict.json` | 🤖 生成物，`build_pwa.py:36` 讀取，通用 fallback |
| `first_destinations.json` | 🤖 生成物，`build_pwa.py:43` 讀取，卡片「📍 導航」第一目的地 |
| `text_entities.json` | 🤖 生成物，`build_pwa.py:50` 讀取，內文自動加連結 |
| `navigation_links.html` | 🤖 生成物，供人開瀏覽器逐筆點開驗證，**無程式讀取** |
| `canonical_nav_map.json` | ⚰️ 歷史遺留，**無程式讀取**，勿再依賴 |

**維護流程**：改 `places.json` → `sync_places.py --generate` → `sync_places.py --fix`（同步 README）→（使用者要求時）`build_pwa.py`。

`README.md` 由 Docsify 直接渲染，必須是完成品、不能用佔位符，因此**只能被檢查與修正，不能被生成**。

⚠️ **HTTP 200 不代表 Place ID 有效** —— Google 對任何 `query_place_id` 都回 200 後靜默退回座標定位。驗證用 `place_id_audit.py`（6 條離線規則：格式、座標複製、ID 尾碼遞增、張冠李戴、座標出境、驗證逾期），或用具 API key 的 Places API。**嚴禁憑空編造 Place ID 或座標。**

URL 一律使用永久標準格式 `https://www.google.com/maps/search/?api=1&query=LAT,LNG&query_place_id=PLACE_ID`；**禁止** `maps.app.goo.gl` 短網址（會出現 `Dynamic Link Not Found`，驗證管線會擋）。

## 驗證管線的三個階段

`full_validation_pipeline.py` 只驗 `README.md`：

1. **粗體裸字零容忍 linter** — 先把所有 `[...](...)` 換成 placeholder，再抓剩下的 `**中文 (日文)**`。命中即違規（有白名單放行 Day 標題、預算、航班號、路線代號等非實體 metadata）。
2. **命名規範檢查** — 所有 Markdown 連結標籤須含 `(官方日文/英文名)`，或屬於標準地名白名單。
3. **HTTP 有效性** — 8 執行緒併發實際請求每個不重複外部連結，偵測 `Dynamic Link Not Found`；403/429 視為有效（Google 反爬），語法殘留 `)` `>` `*` 視為錯誤。

## PWA 與部署

- `sw.js`：HTML 走 Network-First（確保行前更新拿得到最新版），靜態資源走 Cache-First。改版時記得升 `CACHE_NAME`（目前 `travel-itinerary-v10`）。
- 部署為 GitHub Pages，remote 為 `git@github.com:owenpeng811/2026tokyo.git`；`index.html`（Docsify）是首頁，`itinerary.html` 是可安裝的 PWA。
- Commit 訊息慣用中文 conventional commits，且通常註明「同步編譯 PWA」與否。
