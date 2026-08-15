# 待補導航連結（Pending Place IDs）

> 本檔記錄「已寫進 `README.md`，但尚未取得經 Places API 查證的 Place ID」的地點。
> Claude Code 沒有 google-maps MCP，**依專案硬規定嚴禁憑空編造 Place ID 或座標**，
> 因此先在此登錄，由具備 google-maps MCP 的 Antigravity 補齊。
>
> 補齊流程：`maps_search_places` 查證 ➔ 寫入 `places.json` ➔
> `python3 sync_places.py --generate` ➔ `python3 sync_places.py --fix` ➔
> `python3 place_id_audit.py` ➔（使用者要求時）`python3 build_pwa.py`。

---

## 1. 薩莉亞 吉祥寺駅北口（サイゼリヤ 吉祥寺駅北口）

| 項目 | 內容 |
| :-- | :-- |
| 登錄日 | 2026-08-15 |
| 出現位置 | `README.md` Day 4 `### **12:50－14:20 🍽️ 午餐：薩莉亞**`（**首選餐廳**） |
| 官方店名 | `サイゼリヤ 吉祥寺駅北口`（官方店舖頁標示，**無「店」字尾**） |
| 官方地址 | `〒180-0004 東京都武蔵野市吉祥寺本町1-8-3ｺｽﾓ吉祥寺3F` |
| 官方電話 | `0422-29-7961` |
| 官方營業時間 | `10:00～23:30` |
| 官方付款方式 | 電子マネー(交通系)、クレジット(VISA等) |
| 官方店舖頁 | <https://shop.saizeriya.co.jp/sz_restaurant/spot/detail?code=0837> |

### ⚠️ 查證時的地雷

吉祥寺一帶有**多家**サイゼリヤ，查詢時務必用完整店名比對地址，不要選錯：

| 店名 | 是否為目標 |
| :-- | :-- |
| **サイゼリヤ 吉祥寺駅北口**（code 0837，吉祥寺本町 1-8-3 コスモ吉祥寺 3F） | ✅ **就是這家** |
| サイゼリヤ 吉祥寺駅南口（code 1495） | ❌ 南口，需穿越車站 |
| サイゼリヤ 吉祥寺駅北口コピス前店 | ❌ 不同分店 |
| サイゼリヤ 吉祥寺伊勢丹前店 | ❌ 不同分店 |

- 🚨 **嚴禁用 `maps_geocode`**：「吉祥寺本町」是町名，Geocoding 會靜默降級成行政區。
- ✅ POI 自檢：`formatted_address` 須有番地門牌（1-8-3）；`types` 不可含
  `political`／`sublocality`／`locality`／`administrative_area_*`；回傳名稱須含「サイゼリヤ」。
- 若只能定位到建物「コスモ吉祥寺」而非店家本身，請誠實宣告 `poi_level: "container"`
  並填 `container_note`，**不要手寫 `verified_*` 讓 R6 通過**。

### 補齊後必須連帶處理

1. `places.json` 新增本筆，`first_dest` 填 `["4_午餐"]`。
2. **把大戶屋那筆的 `first_dest` 中的 `"4_午餐"` 移除**——目前它是暫時代打，
   否則兩家會同時命中同一個 key。
3. `README.md` 該段的 **🚧 導航連結待補（重要）** 整條刪除，
   並把首選餐廳那行改回標準格式：
   `[**薩莉亞 (サイゼリヤ 吉祥寺駅北口)**](導航連結)（コスモ吉祥寺 3F，北口步行約 1 分鐘）…`
4. 重跑 `python3 full_validation_pipeline.py` 確認階段 0～3 全過。

### 現況（暫時代打）

- `README.md` 內文**沒有**薩莉亞的導航超連結，僅以純文字加註官方地址與電話。
- PWA 卡片「📍 導航」按鈕經 `first_dest: "4_午餐"` **暫時指向備案的大戶屋**
  （ホワイトハウスビル 2F，與薩莉亞同在北口側、相距約 150 公尺）。
  這是刻意的權衡，不是遺漏——寧可指到 150 公尺外的正確方向，也不編一個假的 Place ID。
