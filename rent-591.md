
## Options

Write `query` section in `settings.toml`

All values in this map must be string.

- `kind`: single digit string 房屋類型
  - `1` 整層住家
  - `2` 獨立套房
- `shape`: comma separated digit string 房屋型態
  - `1,2` 公寓或電梯大樓
- `regionid`: single digit string 縣市 ID
  - `3` 新北市
- `section`: 鄉鎮市 ID
  - `26` 板橋區
- `rentprice`: 租金
  - single digit string 區間類別
    - `3` 一萬至兩萬
  - two digit string separated by comma 區間
    - `3000,15000` 三千至一萬五
- `option`: comma separated string 提供設備
  - `cold,wardrobe,bed`: 冷氣 床 衣櫃
- `other`: comma separated string 其他條件
  - `pet,cook`: 可養寵 可開伙
- `hasimg`: boolean string `1` 有圖
- `not_cover`: boolean string `1` 非頂加

Check 591 web site to discover other usages
