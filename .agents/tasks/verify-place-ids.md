# 任務：以 google-maps MCP 全量查證並修正所有導航連結

## 你的角色與目標

你是本 repo（2026 東京親子自由行行程表）的導航資料稽核者。
請使用 **google-maps MCP**（你有自己的 API key，不受共用配額限制）逐筆查證 `places.json` 中**所有**地點，
讓以下三個出口全部正確：

1. **PWA 版**（`itinerary.html`）卡片右上角的「📍 導航」按鈕
2. **Docsify 版**（`README.md`）內文點擊景點名稱的超連結
3. **Google My Maps CSV 匯出**（`exports/*.csv`）的經緯度定位

---

## 背景：這份資料過去出過什麼錯

2026-08 稽核發現大量**憑空捏造**的 Place ID 與座標，已修正 21 筆，但**仍有 85 個 Place ID 從未經 API 查證**。
已知的偽造手法有這幾種，查證時請特別留意：

| 手法 | 實例 |
| :-- | :-- |
| Place ID 尾碼遞增 | `…gq0F88`、`…gq0F90`、`…gq0F91`、`…gq0F92` 一整串 |
| 座標複製貼上 | 吉祥寺四家店共用同一經度 `139.5786162` |
| 張冠李戴 | JR 舞濱站與百合海鷗線台場站共用同一個 ID |
| 指向錯誤層級 | 萬代扭蛋百貨店指向「秋葉原電気街」整個區域 |
| 指向錯誤國家 | 巨雷山指向美國奧蘭多迪士尼（28.42, -81.58） |
| 店名根本不存在 | 「マツモトキヨシ 上野アメ横店」查無此店（實際有 Part1／Part2／Beauty館） |
| 店家已更名 | 「ガシャポンのデパート 秋葉原店」已改名為「ガシャポンバンダイオフィシャルショップ秋葉原店」 |

> 🚨 **最重要的一條**：連結能開、HTTP 回 200，**完全不代表 Place ID 有效**。
> Google 對任何 `query_place_id` 都回 200，然後**靜默退回用 `query` 的座標定位**。
> 若座標也是錯的，使用者會被導到錯誤地點而毫無警訊。
> **請一律用 Places API 實際查證，不要用「連結打得開」來判斷。**

---

## 唯一真相來源與檔案角色

| 檔案 | 角色 |
| :-- | :-- |
| **`places.json`** | **唯一真相來源，只准改這個** |
| `navigation_links_dict.json` | 🤖 生成物，`build_pwa.py` 讀取 |
| `first_destinations.json` | 🤖 生成物，卡片「📍 導航」第一目的地 |
| `text_entities.json` | 🤖 生成物，內文自動加連結 |
| `navigation_links.html` | 🤖 生成物，人工校對用對照表 |
| `README.md` | 內文網址可用 `sync_places.py --fix` 同步；**標籤文字需人工改** |
| `canonical_nav_map.json` | ⚰️ 歷史遺留，無程式讀取，**不要動它** |

**嚴禁直接編輯四個生成物**，任何修改都會在下次 `--generate` 時被覆蓋。

---

## 執行步驟

### 步驟 1：逐筆查證

讀取 `places.json` 的 `places` 物件，對**每一個**地點：

1. 從 `url` 取出現有的 `query_place_id` 與 `query=lat,lng`
2. 用 google-maps MCP 以 **key 括號內的官方日文名**查詢
   （例如 `大戶屋 (大戸屋ごはん処 吉祥寺店)` → 查 `大戸屋ごはん処 吉祥寺店`），取得權威資料：
   - `place_id`
   - 官方顯示名稱（`displayName`）
   - 完整地址（`formattedAddress`）
   - 經緯度（**保留 7 位小數**）
3. 交叉比對，判斷屬於哪一種情況：
   - ✅ **一致** → 只更新 `verified_at`
   - ⚠️ **Place ID 不同但確實是同一家店** → 以 API 回傳值為準覆寫
   - ❌ **Place ID 無效**（`NOT_FOUND` / `INVALID_ARGUMENT`）→ 以查詢結果覆寫
   - ❌ **指向錯誤地點或錯誤層級**（指到整條商店街、整棟大樓、別家分店）→ 改為指向**確切店家**
   - ❌ **已歇業／更名／搬遷** → 寫入現存的正確資料，並在報告中列出

### 步驟 2：處理特殊條目

**(a) 9 個沒有 `query_place_id` 的地點**（目前是純店名查詢連結）
它們在 My Maps CSV 匯出時**沒有座標**，請一律補上真實 Place ID 與經緯度：
天音、小ざさ、gashacoco、Dream Market、THANK YOU MART、哈莫尼卡橫丁等（以實際檔案為準）。

**(b) 2 個 key 是網址的異常條目**
`places.json` 中有兩筆的 key 直接是 `https://www.google.com/maps/search/?api=…`，
成因是初次彙整時它們只存在於 `first_destinations.json`、沒有任何標籤可用。
實際指向 **國立西洋美術館** 與 **鴨to蔥拉麵**，請正名為標準格式 `中文名 (官方日文全名)`。

**(c) 官方名稱與行程表不符時**
若查出的官方日文名與 `README.md` 內文標籤不同（如上述萬代扭蛋、松本清的例子），
請**一併修正 README 的標籤文字**，並維持專案的命名規範：

```markdown
[**中文名 (官方日文全名)**](https://www.google.com/maps/search/?api=1&query=<lat>,<lng>&query_place_id=<place_id>)（大樓／樓層備註）
```

⚠️ `sync_places.py --fix` **只同步網址、不會改標籤文字**，標籤要自己改。

### 步驟 3：寫回與傳播

```bash
# 只改 places.json，然後依序執行：
python3 sync_places.py --adopt      # 若 README 有未登錄的孤兒連結，先收編
python3 sync_places.py --generate   # 生成四個衍生檔
python3 sync_places.py --fix        # 同步 README 內文網址
python3 place_id_audit.py           # 離線偽造偵測，須 0 問題
python3 full_validation_pipeline.py # 階段 0-3 全量驗證
python3 export_mymaps.py --merged   # 重新匯出 My Maps CSV
python3 build_pwa.py                # 重新編譯 PWA
```

### 步驟 4：資料格式要求

`places.json` 每筆的 `url` 一律使用此格式，**經緯度保留 7 位小數**：

```
https://www.google.com/maps/search/?api=1&query=35.7032718,139.5784738&query_place_id=ChIJ-34cDUjuGGARIZkFocT8a5o
```

- ❌ **嚴禁**使用 `maps.app.goo.gl` 短網址（會出現 `Dynamic Link Not Found`，驗證管線會擋）
- ❌ **嚴禁**憑空編造 Place ID 或座標；查不到就在報告中標明「查無」，不要猜
- ✅ 每筆查證完成後把 `verified_at` 更新為當天日期（格式 `YYYY-MM-DD`）

---

## 驗收標準（全部都要通過）

- [ ] `python3 place_id_audit.py` → 7 條規則 0 問題
- [ ] `python3 sync_places.py --check` → README 與 places.json 完全一致
- [ ] `python3 full_validation_pipeline.py` → 階段 0～3 全數通過
- [ ] `python3 export_mymaps.py --merged` → **0 筆缺少座標**（目前有 6 筆）
- [ ] `places.json` 中**每一筆**都有真實 `query_place_id` 與 7 位小數經緯度
- [ ] `places.json` 中**每一筆**的 `verified_at` 都是本次查證日期
- [ ] 沒有任何 key 是網址的條目

---

## 請一併產出稽核報告

完成後輸出一份報告，分成四類：

1. **✅ 原本就正確**（給筆數即可，不用逐筆列出）
2. **🔧 已修正**：逐筆列出「地點名稱｜舊 Place ID｜新 Place ID｜錯誤原因」
3. **⚠️ 需人工判斷**：同名多家分店、疑似歇業、官方名稱與行程表落差大者
4. **❌ 查無資料**：完全查不到的地點，並說明你嘗試過的查詢字串

---

## 注意事項

- 依 `.agents/AGENTS.md`：**未經使用者明確要求不要 `git push`**。
  本任務允許執行 `build_pwa.py` 重新編譯（因為目標包含 PWA 導航正確），但**推送前請先詢問**。
- `README.md` 由 Docsify 直接渲染，**必須保持完成品、不能用佔位符**，因此只能被檢查與修正、不能被生成。
- 修改 README 標籤時請注意驗證管線的兩條規則：
  **粗體裸字零容忍**（實體地標一律要包超連結）、**命名規範**（連結標籤須含官方日文／英文名）。
