# 待補導航連結（Pending Place IDs）

> 本檔記錄「已寫進 `README.md`，但尚未取得可信 Place ID」的地點。
> Claude Code 沒有 google-maps MCP，**依專案硬規定嚴禁憑空編造 Place ID 或座標**，
> 因此先在此登錄，由具備 google-maps MCP 的 Antigravity 補齊。
>
> 補齊流程：`maps_search_places` 查證 ➔ 寫入 `places.json` ➔
> `python3 sync_places.py --generate` ➔ `python3 sync_places.py --fix` ➔
> `python3 place_id_audit.py` ➔（使用者要求時）`python3 build_pwa.py`。

## 目前狀態

**無待補項目。**

---

## 已結案

### ✅ 薩莉亞 吉祥寺駅北口（サイゼリヤ 吉祥寺駅北口）

| 項目 | 內容 |
| :-- | :-- |
| 登錄日 | 2026-08-15 |
| 結案日 | 2026-08-15（同日） |
| 出現位置 | `README.md` Day 4 `### **12:50－14:20 🍽️ 午餐：薩莉亞**`（首選餐廳） |
| Place ID | `ChIJi3cb1kfuGGARiZitA8UrSEQ` |
| 座標 | `35.7043574,139.5789601` |
| `first_dest` | `4_午餐` |

#### 取得途徑（可完整重現，非憑空編造）

1. **使用者**在 Google Maps 上親自找到該店，提供短網址 `https://maps.app.goo.gl/S1mokzpwvf2wmVKAA`。
2. `curl -sIL` 解析 302 導向，取得完整網址，其中含 ftid
   `!1s0x6018ee47d61b778b:0x44482bc503ad9889`。
3. 依 Google 既定編碼把 ftid 轉為 place ID：
   protobuf `0x0A 0x12 0x09 + LE64(0x6018ee47d61b778b) + 0x11 + LE64(0x44482bc503ad9889)`
   ➔ base64url ➔ `ChIJi3cb1kfuGGARiZitA8UrSEQ`。
4. **反查驗證**：以 `https://www.google.com/maps/place/?q=place_id:ChIJi3cb1kfuGGARiZitA8UrSEQ`
   用瀏覽器實際開啟，Google 回到**同一個 POI**——ftid 相同、座標
   `!8m2!3d35.7043574!4d139.5789601`、名稱與地址一致。這一步是關鍵：
   它證明轉換沒錯，而不是只證明「Google 回了 200」。
5. `hl=ja` 顯示店名 **「サイゼリヤ 吉祥寺駅北口」**、地址
   **「東京都武蔵野市吉祥寺本町１丁目８−３ ｺｽﾓ吉祥寺 3F」**，
   與官方店舖頁 <https://shop.saizeriya.co.jp/sz_restaurant/spot/detail?code=0837>
   的店名與地址**逐字相符**。

#### POI 自檢結果（全數通過）

- ✅ 地址有番地門牌（1-8-3），不是町名層級
- ✅ 名稱含「サイゼリヤ」，不是行政區名
- ✅ 是商家 POI，非 `political`／`sublocality`／`locality`
- ✅ 座標在日本境內，且與其他吉祥寺地點的 S2 cell 前綴一致（`…fuGGAR`）

#### ⚠️ 先前一個誤判，已更正

初次登錄時我把「サイゼリヤ 吉祥寺駅北口コピス前店」列為**不同分店**，**那是錯的**。
Google 的中文顯示名為「薩莉亞 Saizeriya 吉祥寺站北口Coppice前店」，
日文顯示名為「サイゼリヤ 吉祥寺駅北口」，**同一個 place_id、同一個地址**，
就是官方店舖頁 code=0837 那家。**同店異名，不是兩家店。**

真正需要區分的是這兩家（地址不同）：

| 店名 | 說明 |
| :-- | :-- |
| **サイゼリヤ 吉祥寺駅北口**（＝コピス前店，1-8-3 コスモ吉祥寺 3F） | ✅ 行程採用 |
| サイゼリヤ 吉祥寺駅南口（code 1495） | ❌ 南口，需穿越車站 |

#### `verified_*` 欄位的來源說明

`verified_name` / `verified_address` 取自 **Google Maps 網頁介面 `hl=en` 的實際顯示值**，
**不是 Places API 回傳**（本機無 API key）。`places.json` 該筆的 `verified_source`
欄位已如實記載此事，未偽稱為 API 回傳值。
若日後 Antigravity 以 `maps_place_details` 重查，請直接以 API 回傳值覆寫這兩欄，
並可移除 `verified_source`。

---

## 附：短網址轉標準連結的通用做法

使用者日後若再提供 `maps.app.goo.gl` 短網址，可依同一流程處理，**不需要 API key**：

```bash
# 1. 解析短網址，取出 ftid（!1s0x????????????????:0x????????????????）
curl -sIL "https://maps.app.goo.gl/XXXXXXXX" | grep -i "^location:"

# 2. ftid ➔ place_id
python3 -c "
import base64, struct
a=0xAAAAAAAAAAAAAAAA; b=0xBBBBBBBBBBBBBBBB   # 換成實際的兩段 hex
blob=b'\x0a\x12\x09'+struct.pack('<Q',a)+b'\x11'+struct.pack('<Q',b)
print(base64.urlsafe_b64encode(blob).decode().rstrip('='))
"

# 3. 反查驗證（必做，不可略過）
#    用瀏覽器開 https://www.google.com/maps/place/?q=place_id:<算出來的ID>
#    確認回到同一個 POI，並記下網址中 !8m2!3d<lat>!4d<lng> 的權威座標
```

⚠️ **第 3 步不能省**。只有反查回到同一 POI，才算驗證過；
單純「HTTP 回 200」在 Google Maps 上完全不代表 Place ID 有效。

⚠️ 短網址本身**不可**直接寫進 `README.md`——專案禁止 `maps.app.goo.gl`
（會出現 `Dynamic Link Not Found`，驗證管線階段 3 會擋）。它只能當作查證的輸入。
