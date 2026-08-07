---
name: generate-travel-itinerary
description: 將旅遊行程資料轉換為適合手機瀏覽的「單一檔案（Single-file）、純 HTML+CSS+JS、Mobile-First」個人專屬旅遊行程網頁。
---

# Generate Travel Itinerary Skill

當使用者要求將旅遊行程、景點規劃或行程表轉換為網頁時，請遵循以下規範與程式碼設計指南，生成一個高階、精美且完全自適應手機的單一 HTML 檔案。

## 核心設計規範

1. **手機優先與現代美學（Mobile-First & UI/UX）**：
   - 採用無邊框、精緻卡片式設計（Card Design）、毛玻璃效果（Glassmorphism）與滑順的過渡動畫。
   - 所有點擊區域（如頁籤、連結、核取方塊）必須大於 44x44px。
   - 使用 CSS 變數（Variables）實作質感深色模式（Dark Mode），搭配日系和風點綴色（如緋紅 `#E45F56`、藍綠 `#2C3E50`）。

2. **雙層內容結構與 iOS 風格抽屜彈出視窗（Bottom Sheet Modal）**：
   - **精簡卡片畫面**：卡片預設只呈現精簡但實用的行程摘要（包含重要資訊如建議路線、推薦必點、選項備案等），保持滑動順暢。避免使用無意義的佔位文字。
   - **完整原始說明抽屜**：提供「📖 完整原始說明」按鈕，點選後以 iOS 底部抽屜（Bottom Sheet）滑出完整段落。此處必須 100% 完整保留原始行程表（如 `README.md`）的內容與段落結構（如 blockquotes、條列清單、重要警示）。
   - **智慧按鈕隱藏**：若時段內容本身已足夠簡短，且點擊前後顯示內容一致時，**必須自動隱藏**「📖 完整原始說明」按鈕，避免不必要的互動。

3. **無死角 Google Maps 導航連結**：
   - 所有的主景點、餐廳、車站、飯店名稱，乃至**內文段落、備案說明、隱藏美食清單中提及的所有可能造訪地點**，都必須包裝成 Google Maps 的導航連結（格式：`https://www.google.com/maps/search/?api=1&query=確切名稱`），且均設定 `target="_blank"`。
   - **精準地標定位**：導航連結必須使用**最精準、能直達該分店/確切位置**的搜尋字串（如 `鳥良商店+新宿西口店`），而非模糊的通用名稱，避免 Google Maps 僅跳轉至一般搜尋或多點地圖。
   - **地理普查與糾錯**：必須主動核對行程中所有地點的真實位置。若發現原行程表有誤（如淺草橋的 RusaRuka、吉祥寺的 Jyonetsu Bakery），應主動替換為當地**真實存在且評分優良**的替代名店（如 MIYABI CAFE、Antendo），並在網頁中加註修正說明。
   - **連結對照表維護（navigation_links.html）**：所有導航連結（含自訂短網址）必須記錄在 [navigation_links.html](file:///home/owen/tokyo/navigation_links.html) 中。後續更新 `itinerary.html` 時，應優先讀取並對照此表以取得精確連結；若行程有新增景點/餐廳，也必須同步將新地點及其精準地圖連結寫入此表。

4. **動態互動與狀態管理**：
   - **分天頁籤（Tabs）**：頂部置頂固定（`position: sticky`）的頁籤，切換不同天數的行程。
   - **分線切換（Sub-toggles）**：針對特定天數的「雙路線（例如長輩組 vs 親子組）」或「決策方案（Plan A vs Plan B）」，提供子切換按鈕，點擊後即時過濾當天時間軸。
   - **行程進度打勾（Checklist）**：每張卡片附有 checkbox，點擊可標記「已完成」，並透過 `localStorage` 儲存狀態，重新整理不消失，並連動更新頂部進度條。

5. **檔案維護與程式碼規格**：
   - 輸出單一 HTML 檔案，所有的 CSS 樣式與 JavaScript 程式碼皆包裝在 `<style>` 與 `<script>` 中以利離線存取。
   - **手動精雕細琢**：避免使用自動化轉換腳本（如 `generate.py`）進行粗暴提取，因為 regex 解析易遺漏連結或造成排版混亂。應以手動維護、精修 HTML 為主，以保證 100% 格式與連結精準度。
   - **字元集與亂碼防範**：所有原始碼讀寫與修改必須強制使用 `UTF-8` 編碼，避免因字元轉換不當導致網頁中出現任何中文亂碼（如 ``）。
   - 嚴禁使用 Bootstrap、TailwindCSS 等外部框架，確保極速載入且可離線使用。
   - 必須包含 `<meta name="viewport" content="width=device-width, initial-scale=1.0, user-scalable=no">`。
