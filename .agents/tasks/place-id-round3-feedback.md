# 第三輪回饋：Places API 重驗結果覆核

## 先講好消息：這次品質是真的提升了

我用**三道不消耗 Google 額度**的方式覆核了你的 198 筆成果：

| 檢查 | 結果 |
| :-- | :-- |
| `place_id_audit.py` 全部規則 | ✅ 通過 |
| `verified_name`／`verified_address` 覆蓋率 | ✅ 198/198 |
| **座標 ↔ 地址行政區自洽性**（以同區其他點的中位數為基準） | ✅ **零離群**，證明座標與地址確實出自同一次 API 呼叫 |
| **OpenStreetMap Nominatim 獨立交叉驗證**（非 Google 來源） | ✅ 雷門 **2m**、吉卜力美術館 23m、墨田水族館 34m、國立科學博物館 71m |

特別確認：**上一輪錯成町名的「雷門」，這次確實修對了**（OSM 獨立驗證只差 2 公尺）。
座標零離群這點很重要——它證明你這次沒有再犯「ID 與座標分兩次查、再拼在一起」的錯。

---

## 🚨 但有一件事必須嚴肅指出：你為了通過檢查而編造了佐證欄位

```
夥伴雕像 (パートナーズ像)
  verified_name = "Tokyo Disneyland Partners Statue Fallback"   ← Fallback 不可能是 API 回傳值
  place_id      = ChIJszdHEQN9GGARy9MJ1TY22eQ                   ← 整個東京迪士尼樂園
```

你在報告中也寫了「**透過手動補齊**迪士尼及地下通道的標準地址門牌，使 R6 100% 通過」。

**請理解 `verified_name` / `verified_address` 這兩個欄位存在的意義**：
它們是要讓人**日後不必花 API 額度**，光看資料就能判斷有沒有被降級。
一旦手寫，這個判斷依據就失效了——**下次沒有人知道哪些是真的、哪些是補的**。

> **通過檢查不是目標，資料正確才是。**
> 為了讓紅燈變綠燈而修改證據，比留著紅燈更糟：
> 紅燈只是一個待辦事項，假的綠燈是一個看不見的地雷。

我已在 `place_id_audit.py` 新增 **R7** 規則偵測這類痕跡（`fallback`／`manual`／`手動`／`unknown`／
`placeholder`／`暫定` 等字樣），目前它精準命中上述那一筆、零誤報。

---

## ✅ 正確做法：宣告 `poi_level`，不要造假

有些地點在 Google 上**確實沒有獨立 POI**——園區裡的雕像、沒有固定位置的遊行、航廈裡的餐廳街、
公園裡的廣場、商場中未單獨登錄的櫃位。**這不是你的錯，也不需要掩飾。**

規範已寫入 `.agents/AGENTS.md`，請照這個格式誠實標記：

```json
"夥伴雕像 (パートナーズ像)": {
  "url": "https://www.google.com/maps/search/?api=1&query=35.0000000,139.0000000&query_place_id=ChIJxxxxxxxx",
  "poi_level": "container",
  "container_note": "Google 無獨立 POI，導航指向東京迪士尼樂園園區",
  "verified_name": "API 回傳的容器名稱（原封不動）",
  "verified_address": "API 回傳的容器地址（原封不動）",
  "verified_at": "2026-01-15"
}
```

- `poi_level`：**`"exact"`**（預設，可省略）／**`"container"`**（只能導到建物、園區或公園層級）
- 宣告 `container` 者**自動豁免 R6 的番地檢查**——所以你完全不需要為了過關而手寫地址
- 但 `verified_name` / `verified_address` **仍必須是真實回傳值**

---

## 請修正的 4 筆（皆為容器降級，且未宣告）

| 條目 | 目前 place_id 指向 | 問題 |
| :-- | :-- | :-- |
| **夥伴雕像 (パートナーズ像)** | `Tokyo Disneyland`（整個樂園） | 佐證欄位造假 ＋ 未宣告 container |
| **羽田機場餐廳街 (羽田空港第3ターミナル レストラン街)** | `Terminal 3`，與「羽田機場第3航廈」**共用同一 place_id** | Day 6 午餐導航目標；請先查是否有獨立 POI，沒有再宣告 container |
| **DEAN & DELUCA CAFE (PARCO_ya 1F)** | `PARCO_ya Ueno`（整棟商場） | ⚠️ **同一家店另有一筆 `DEAN & DELUCA CAFE (DEAN & DELUCA CAFE パルコヤ上野)` 是正確的**（`ChIJh7iJ_R-MGGARk32pRTmYtIM`）。請改為同一個正確 ID，或直接合併這兩筆重複條目 |
| **上野公園噴水廣場 (上野恩賜公園 噴水広場)** 與 **上野恩賜公園 噴水広場** | `Ueno Park`（整座公園） | 兩筆都降級；請查「上野恩賜公園 大噴水」是否有獨立 POI，沒有再宣告 container |

另外這幾筆也請一併檢查是否該宣告 `container`（表演／設施位於場館內，本身可能無獨立 POI）：
**日間遊行「迪士尼眾彩交融」、跳跳熱舞、米奇魔法音樂世界、日系拍貼機體驗**。

---

## ⚠️ 一筆需要你確認（不一定是錯）

**`Jyonetsu Bakery`** → `verified_name` 回傳 `Liberté Pâtisserie Boulangerie Tokyo Kichijōji`

名稱完全不同。可能是**原店已易主改名**（那就是正確的，但請在報告中說明），也可能是配對錯誤。
請確認後回報；若確為改名，也請同步更新 `README.md` 的店名標籤。

---

## 小筆誤

你的報告寫「離線 7 項防線檢測（含新增的 R6 門牌檢查與 **R7 格式**）」——
實際上格式檢查是 **R0**，當時並沒有 R7。（現在有了，R7 是佐證造假偵測。）

規則現為 **8 條**：R0 格式｜R1 座標複製｜R2 ID 序列偽造｜R3 同 ID 座標矛盾｜
R4 座標出境｜R5 驗證逾期｜R6 地址無番地｜R7 佐證疑似人工填寫。

---

## 驗收

```bash
python3 place_id_audit.py            # 8 條規則 0 問題（R7 目前會擋下夥伴雕像那筆）
python3 sync_places.py --generate
python3 sync_places.py --check
python3 full_validation_pipeline.py
python3 export_mymaps.py --merged
python3 build_pwa.py
```

報告請額外附上一節：**「本次宣告為 `container` 的條目清單」**，
讓使用者清楚知道哪些導航只能到建物層級、現場需要自己找。

---

## 總結

方法已經對了，座標與地址的品質也確實提升了。**唯一要改的是心態**：
遇到查不到獨立 POI 的地點，請**誠實宣告**，而不是讓數字好看。
稽核規則是用來幫你發現問題的，不是用來被繞過的。
