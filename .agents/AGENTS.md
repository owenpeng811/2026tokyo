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
