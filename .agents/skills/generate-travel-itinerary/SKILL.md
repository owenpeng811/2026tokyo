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
   - 所有的主景點、餐廳、車站、飯店名稱，乃至**內文段落、備案說明、隱藏美食清單中提及的所有可能造訪地點**，都必須包裝成 Google Maps 的導航連結（格式：`https://www.google.com/maps/search/?api=1&query=地點名稱`），且均設定 `target="_blank"`。

4. **動態互動與狀態管理**：
   - **分天頁籤（Tabs）**：頂部置頂固定（`position: sticky`）的頁籤，切換不同天數的行程。
   - **分線切換（Sub-toggles）**：針對特定天數的「雙路線（例如長輩組 vs 親子組）」或「決策方案（Plan A vs Plan B）」，提供子切換按鈕，點擊後即時過濾當天時間軸。
   - **行程進度打勾（Checklist）**：每張卡片附有 checkbox，點擊可標記「已完成」，並透過 `localStorage` 儲存狀態，重新整理不消失，並連動更新頂部進度條。

5. **自動化編譯與程式碼規格**：
   - 輸出單一 HTML 檔案，所有的 CSS 樣式與 JavaScript 程式碼皆包裝在 `<style>` 與 `<script>` 中以利離線存取。
   - 必須提供一個 Python 腳本（如 `generate.py`）作為自動化編譯工具，能夠讀取原始 Markdown 行程表（`README.md`）並自動解析、注入自訂摘要，重新生成 HTML，確保行程變更時可一鍵更新。
   - 嚴禁使用 Bootstrap、TailwindCSS 等外部框架，確保極速載入且可離線使用。
   - 必須包含 `<meta name="viewport" content="width=device-width, initial-scale=1.0, user-scalable=no">`。
