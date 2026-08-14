# Project Rules

- **行程表編輯、網頁轉換與 Git 推送規則**：
  - 預設專注修改與維護 Markdown 行程表（僅維護 `README.md`，**不需要同步修改 `2026東京親子自由行_V10_Henna.md`**）。
  - **嚴禁在每次微調修改 Markdown 後自動執行網頁版轉換（`build_pwa.py`）或自動 `git push`**。
  - 只有在使用者明確要求（例如：「轉成網頁版」、「更新 PWA」、「幫我 push」）時，才執行網頁建置與代碼推送。

- **導航連結唯一真相來源規則（2026-08 起，Claude Code 與 Antigravity 共同適用）**：
  - `places.json` 是**所有 Google Maps 導航連結的唯一真相來源**。
  - **嚴禁直接編輯以下四個衍生檔**，它們由 `python3 sync_places.py --generate` 自動生成，手動修改會在下次生成時被覆蓋：
    - `navigation_links_dict.json`
    - `first_destinations.json`
    - `text_entities.json`
    - `navigation_links.html`
  - 要新增或修正地點：**只改 `places.json`**，接著依序執行
    `python3 sync_places.py --generate` ➔ `python3 sync_places.py --fix`（同步 README 內文網址）➔ `python3 build_pwa.py`（僅在使用者要求更新 PWA 時）。
  - 若直接在 `README.md` 內文新增了地點連結，執行 **`python3 sync_places.py --adopt`** 把這些「孤兒連結」收編進 `places.json`。
    ⚠️ 孤兒連結是最危險的一類：它們不在任何字典檔中，稽核規則因找不到同伴而抓不到，`--check` 也會略過。2026-08 抽查 26 個孤兒連結，其中 11 個 Place ID 是無效或指向錯誤地點的。
  - `canonical_nav_map.json` 為歷史遺留檔，**已無任何程式讀取**，請勿再寫入或依賴它。

- **Place ID 品質規則（重要，過去曾大量出錯）**：
  - **嚴禁憑空編造 Place ID 或座標。** 曾發生以尾碼遞增（如 `…F88`、`…F90`、`…F91`）偽造 ID，以及把同一經度複製給多家店的情形，導致導航靜默失效。
  - Place ID **必須經實際查證**取得，可用 [Place ID Finder](https://developers.google.com/maps/documentation/javascript/examples/places-placeid-finder) 或具備 API key 的 Google Maps 工具（Antigravity 的 google-maps MCP 可直接使用）。
  - ⚠️ **HTTP 200 不代表 Place ID 有效**：Google 對任何 `query_place_id` 都回 200，然後靜默退回用座標定位。要驗證有效性請用 Places API 的 Place Details，或執行離線稽核 `python3 place_id_audit.py`。
  - 每次改動導航連結後，務必執行 `python3 place_id_audit.py`（或包含它的 `full_validation_pipeline.py`），確認 5 項偽造偵測規則全數通過。

- **查詢 Place ID 只能用 Places API，嚴禁用 Geocoding（2026-08 實際踩過的坑）**：
  - **正確工具**（google-maps MCP）：
    | 用途 | 工具 |
    | :-- | :-- |
    | 由名稱／店名找地點 | **`maps_search_places`**（Places Text Search） |
    | 由既有 place_id 取權威資料 | **`maps_place_details`**（Place Details） |
    | 由純地址找座標 | `maps_geocode`（**僅此情境**適用） |
  - ⚠️ **前置條件：Google Cloud Console 必須同時啟用「Places API（新版）」與「Places API (Legacy)」。**
    上述兩個 MCP 工具走的是 **Legacy** 端點；若只啟用新版，呼叫會失敗。
  - 🚨 **工具失敗時，嚴禁靜默改用 `maps_geocode` 頂替**——這正是 2026-08 出錯的真正原因：
    當時 Legacy Places API 未啟用，導致 fallback 到 Geocoding，而 **Geocoding 回傳的是「地址／行政區」
    不是「商家 POI」**，遇到店名與地名同名時會**靜默降級**，回傳一個真實存在、格式正確、座標也在日本的 ID
    —— 但那是**町名的 ID**。實例：查「変なホテル東京 浅草橋」得到町名「淺草橋」；查「雷門」得到台東區
    的町名「雷門」；查「台場駅」得到町名「台場」；查「井の頭池」降級成「井の頭恩賜公園」。
  - **若 Places 工具不可用，正確做法是停下來回報「工具不可用、需啟用 Legacy Places API」，
    而不是換一個語意不同的 API 繼續跑完並宣稱成功。**
  - **每筆結果都要自檢是否為 POI**，符合任一條即為降級、必須丟棄重查：
    `formattedAddress` 無番地門牌｜`types` 含 `political`／`sublocality`／`locality`／`administrative_area_*`｜
    回傳名稱比查詢字串更短更泛化｜查車站卻沒回「駅／Station」｜查店家卻回建物名或地名。
  - ⚠️ 東京有大量町名與地標同名（**雷門、淺草橋、台場、銀座、築地、押上、有明**），查這些務必用完整設施全名。
  - ⚠️ 小地物易被降級到父層（井の頭池⊂井の頭恩賜公園、南展望室⊂東京都庁、世界市集⊂迪士尼樂園），
    請確認回傳名稱就是目標層級，不是它的容器。
  - **座標與 place_id 必須同一次查詢取得**，不可只更新其中一個（同一 place_id 只有一個標準座標）。
  - 查不到就在報告中標「查無」，**嚴禁用地區級 ID 頂替**——指向町名的導航連結比沒有連結更危險。
  - ⚠️ **驗證管線 PASS 不等於 Place ID 正確**：HTTP 200 測試與 5 條離線規則都抓不到「降級到行政區」
    （那些 ID 真實存在、格式正確、座標也在日本），**不可拿管線通過當作查證正確的證據**。
