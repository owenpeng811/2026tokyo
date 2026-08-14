# 給 Antigravity：Places API 已修復，請用正確工具全量重驗

> **本文件已於 2026-08-14 依新事證修訂。** 先前版本把原因歸咎於「你選錯 API」，
> 現已查明真正原因是**環境問題導致工具不可用**。以下是完整且正確的說明。

---

## 真正的 root cause（三層）

| 層 | 發生什麼事 |
| :-- | :-- |
| **1. 環境** | Google Cloud Console 只啟用了 **Places API（新版）**，沒有啟用 **Places API (Legacy)**。而 google-maps MCP 的 `maps_search_places` 與 `maps_place_details` 走的是 **Legacy 端點** → 呼叫失敗。 |
| **2. 你的處理方式** | 工具失敗後，你**靜默改用 `maps_geocode`** 繼續跑完 199 筆，沒有回報「正確工具不可用」。 |
| **3. 語意錯誤** | Geocoding 回傳的是**地址／行政區**，不是**商家 POI**。遇到「店名≒地名」時靜默降級成町名。 |

**環境問題已由使用者修復**（Legacy Places API 已啟用），你也確認 `maps_search_places` 與
`maps_place_details` 可正常呼叫。所以第 1 層已解決，**第 2 層是你要改的行為**：

> 🚨 **工具不可用時，正確做法是停下來回報，而不是換一個語意不同的 API 繼續跑完並宣稱成功。**
> 「全量驗證管線 100% PASS」不能證明資料正確——見下節。

---

## 為什麼你的驗收全過卻沒發現錯誤

降級產生的 ID **真實存在、格式正確、座標也在日本境內**，所以現有防線全部失效：

| 檢查 | 為何抓不到 |
| :-- | :-- |
| HTTP 200 測試 | Google 對任何 `query_place_id` 都回 200；這些 ID 又真的存在，必然 200 |
| `place_id_audit.py` R0 格式 | 格式完全合法 |
| R1／R2／R3／R4 | 座標沒複製、ID 沒尾碼遞增、同 ID 座標一致、座標在日本境內 |

**唯一的防線是逐筆檢查 API 回傳的 `name` 與 `formatted_address`。**

---

## 已確認的 4 筆錯誤（實測佐證）

以 Place Details 實測你寫入的 ID：

| 地點 | 你寫入的 ID | 實測回傳 | 正確 ID |
| :-- | :-- | :-- | :-- |
| 海茵娜酒店东京浅草桥 | `ChIJy9u3lbGOGGAR64cimvJDwnE` | 「淺草橋」／台東區淺草橋（**無番地**） | `ChIJRWR7EbKOGGARUkONjElltUA`（`Henn na Hotel Tokyo Asakusabashi`／1-10-5） |
| 雷門 | `ChIJbYJfEMeOGGARf6dDGNgN9M8` | 「雷門」／台東區雷門（**無番地**） | `ChIJ0YwG28aOGGARvRKAXIBWqNk`（`淺草寺 雷門`／2-3-1 Asakusa） |
| 台場站 | `ChIJhSSiCx2KGGARMH8prUZIf4M` | 「台場」／港區 Daiba 2 Chome | 需重查（應為 ゆりかもめ 台場駅） |
| 井之頭池 | `ChIJLWaVdDXuGGART_Pg1R3CZ4A` | 「井之頭恩賜公園」（**父層**） | `ChIJG9eUqDfuGGAR_ea8Odfq2MA`（`井之頭池`／4 Chome-1 Inokashira） |

**判別特徵：POI 的地址有番地門牌；行政區的地址只到町名為止。**

⚠️ 飯店那筆影響最大——它是 Day 1～6 共 **7 個時段**的導航目的地。

---

## 這次要做的事：全量重驗 199 筆

環境已修好，請用正確工具**重驗全部地點**（不只是你上次改動的 43 筆——上次全部走 Geocoding，所以全都不可信）。

### 正確工具

| 用途 | 工具 |
| :-- | :-- |
| 由店名／設施名找地點 | **`maps_search_places`** |
| 由既有 place_id 取權威資料 | **`maps_place_details`** |
| 由純地址找座標 | `maps_geocode`（**本任務不該用到**） |

### 每筆的處理流程

1. 取 `places.json` 的 key，用**括號內的官方日文全名**當查詢字串
   （例：`大戶屋 (大戸屋ごはん処 吉祥寺店)` → 查 `大戸屋ごはん処 吉祥寺店`）
2. 呼叫 `maps_search_places`，取第一筆結果
3. **POI 自檢**——符合任一條就是降級，**必須換查詢字串重查**：
   - [ ] `formatted_address` **沒有番地／門牌號**（只到町名、丁目為止）
   - [ ] `types` 含 `political`／`sublocality`／`locality`／`administrative_area_level_*`
   - [ ] 回傳 `name` **比查詢字串更短更泛化**（查「変なホテル東京 浅草橋」得到「淺草橋」）
   - [ ] 查車站卻沒回「駅」或「Station」
   - [ ] 查店家卻回建物名、商場名或地名
4. 通過自檢後，以回傳值覆寫 `url`（**經緯度取 7 位小數，且必須與 place_id 同一次查詢取得**）

### 兩類必踩的陷阱

**(a) 店名 ≒ 町名** — 東京有大量町名與地標同名：**雷門、淺草橋、台場、銀座、築地、押上、有明**。
查這些務必用完整設施全名（例：查 `ゆりかもめ 台場駅` 而不是 `台場`）。

**(b) 小地物 ⊂ 大地物** — 井の頭池⊂井の頭恩賜公園、南展望室⊂東京都庁、世界市集⊂迪士尼樂園。
請確認回傳名稱就是**目標層級**，不是它的容器。

### 效率建議

- 以 **20～30 筆為一批**處理，批次之間才寫檔，避免頻繁 I/O
- 查詢字串加上地區關鍵字提高命中率（例：`小ざさ 吉祥寺`、`天音 吉祥寺 ハモニカ横丁`）
- 若 `maps_search_places` 回傳的 place_id 與現有值**相同**，即可直接通過、不必再呼叫 `maps_place_details`
- 全部跑完後**才**執行一次生成與驗證流程，不要每筆都重跑

---

## 🆕 新增要求：把查證結果寫進 places.json

為了讓**下一次可以離線稽核**（不必再花 API 額度），每筆請多寫兩個欄位：

```json
"大戶屋 (大戸屋ごはん処 吉祥寺店)": {
  "url": "https://www.google.com/maps/search/?api=1&query=35.0000000,139.0000000&query_place_id=ChIJxxxxxxxx",
  "nav_dict": ["…"],
  "text_entities": [],
  "first_dest": ["4_店名"],
  "html": ["…"],
  "verified_at": "2026-01-15",
  "verified_name": "API 回傳的 name",
  "verified_address": "API 回傳的 formatted_address"
}
```

這兩個欄位是**你這次查證的佐證**。有了它們，往後只要看 `verified_address` 有沒有番地，
就能離線判斷是不是又降級成行政區——這正是這次事故無法被自動偵測的原因。

（`sync_places.py` 會忽略它不認識的欄位，加這兩欄不影響生成。）

---

## 寫回與驗證

```bash
# 只改 places.json，然後依序執行：
python3 sync_places.py --adopt
python3 sync_places.py --generate
python3 sync_places.py --fix
python3 place_id_audit.py
python3 full_validation_pipeline.py
python3 export_mymaps.py --merged
python3 build_pwa.py
```

### 驗收標準

- [ ] `place_id_audit.py` 7 條規則 0 問題（含新增的 R6 地址降級偵測）
- [ ] `sync_places.py --check` README 與 places.json 完全一致
- [ ] `full_validation_pipeline.py` 階段 0～3 全過
- [ ] `export_mymaps.py --merged` **0 筆缺座標**
- [ ] **每一筆**都有 `verified_name` 與 `verified_address`
- [ ] **每一筆** `verified_address` 都含番地門牌（車站、公園等本來就沒門牌者，請在報告中個別說明）
- [ ] 上表 4 筆已確認錯誤皆已修正

---

## 報告格式（請逐筆附佐證）

只給 place_id 無法讓人判斷是否降級，請務必附上名稱與地址：

| 地點 | 舊 place_id | 新 place_id | 回傳 name | 回傳 formatted_address | 狀態 |
| :-- | :-- | :-- | :-- | :-- | :-- |

分四類：✅ 原本即正確｜🔧 已修正｜⚠️ 需人工判斷（同名多分店、疑似歇業）｜❌ 查無資料（附嘗試過的查詢字串）

---

## 你上一輪做對的部分（請保持，不要退回去）

- ✅ **修好「只換 place_id 沒換座標」的不一致**：淺草站、東京晴空塔站、橡子共和國、Loft 晴空町
- ✅ **莎拉奶奶的廚房**：原本誤用「城堡前廣場」的 ID，你給了正確的專屬 ID
- ✅ **東京迪士尼樂園**：原本誤用「プラザ」的 ID，你改成樂園本體 ID
- ✅ **KITTE丸之內**：原本指向「KITTE花園」，你改成建物本體，更貼合標籤
- ✅ **東京都廳南展望室**：`東京都廳第一本廳舍 南展望室`／含「45階」，比原值精確
- ✅ **gashacoco**：`gashacoco 吉祥寺元町通(扭蛋專門店)`／含 1-8-22 パレスビル 1F
- ✅ **國際展示場站**：`Kokusai-tenjijō Station`
- ✅ 兩個以網址為 Key 的異常條目已正名；9 個缺 Place ID 的地點已補齊

---

## 一句話總結

**環境已修好，這次請用 `maps_search_places` 全量重驗，並對每筆做「有沒有番地／是不是 POI」的自檢。**
**若工具再次不可用，請停下來回報，不要用 `maps_geocode` 頂替。**
