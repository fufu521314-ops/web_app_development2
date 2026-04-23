# 小說閱讀器系統 路由與頁面設計 (Routes)

本文件規劃了系統的所有 URL 路由、對應的處理邏輯以及 Jinja2 模板。

## 1. 路由總覽表格

| 功能 | HTTP 方法 | URL 路徑 | 對應模板 | 說明 |
|---|---|---|---|---|
| **首頁 (Main)** | | | | |
| 首頁 | GET | `/` | `index.html` | 顯示熱門推薦與最新小說 |
| 搜尋小說 | GET | `/search` | `search.html` | 關鍵字搜尋結果 |
| 排行榜 | GET | `/ranking` | `ranking.html` | 顯示各類別排行榜 |
| **身分驗證 (Auth)** | | | | |
| 登入頁面 | GET | `/auth/login` | `auth/login.html` | 顯示登入表單 |
| 處理登入 | POST | `/auth/login` | — | 驗證身分，建立 Session |
| 註冊頁面 | GET | `/auth/register` | `auth/register.html` | 顯示註冊表單 |
| 處理註冊 | POST | `/auth/register` | — | 建立新帳號並重導向至登入 |
| 登出 | POST | `/auth/logout` | — | 清除 Session |
| **閱讀器 (Reader)** | | | | |
| 小說詳情 | GET | `/novel/<id>` | `novel/detail.html` | 顯示簡介與章節列表 |
| 閱讀章節 | GET | `/novel/<id>/read/<num>` | `novel/reader.html` | 顯示章節內容，自動更新進度 |
| 收藏/取消收藏 | POST | `/novel/<id>/collect` | — | 切換使用者的收藏狀態 |
| 個人中心 (書架) | GET | `/profile` | `profile.html` | 顯示閱讀紀錄與收藏清單 |

## 2. 路由詳細說明

### Auth 模組 (`app/routes/auth.py`)

- **`GET /auth/login`**
  - 輸入：無
  - 邏輯：渲染登入頁面。
- **`POST /auth/login`**
  - 輸入：表單欄位 `username`, `password`
  - 邏輯：呼叫 `User.get_by_username`，驗證密碼雜湊。
  - 輸出：成功重導向至首頁，失敗重新渲染並顯示錯誤。
- **`POST /auth/logout`**
  - 邏輯：清除 Flask Session。
  - 輸出：重導向至首頁。

### Main 模組 (`app/routes/main.py`)

- **`GET /`**
  - 邏輯：取得前 10 筆熱門小說 (views 排序)。
  - 輸出：渲染 `index.html`。
- **`GET /search`**
  - 輸入：URL 參數 `q` (關鍵字)
  - 邏輯：根據關鍵字模糊查詢小說標題或作者。
  - 輸出：渲染 `search.html`。

### Reader 模組 (`app/routes/reader.py`)

- **`GET /novel/<id>`**
  - 邏輯：取得小說資訊與所有章節列表。
  - 輸出：渲染 `novel/detail.html`。
- **`GET /novel/<id>/read/<num>`**
  - 邏輯：取得特定序號的章節內容；若使用者已登入，則更新 `Record` 表。
  - 輸出：渲染 `novel/reader.html`。
- **`POST /novel/<id>/collect`**
  - 邏輯：檢查使用者是否已登入，切換 `Collection` 紀錄。
  - 輸出：JSON 回應或重導向。

## 3. Jinja2 模板清單

所有模板皆位於 `app/templates/` 且繼承自 `base.html`。

- `base.html`: 包含 Navbar (Logo, 搜尋框, 登入/個人中心連結) 與 Footer。
- `index.html`: 瀑布流或網格顯示小說封面。
- `search.html`: 顯示搜尋結果列表。
- `ranking.html`: 條列式顯示各分類排行。
- `profile.html`: 分為「最近閱讀」與「收藏書單」兩個區塊。
- `auth/login.html`: 登入表單。
- `auth/register.html`: 註冊表單。
- `novel/detail.html`: 頂部為封面與簡介，下方為章節連結。
- `novel/reader.html`: 純淨閱讀介面，包含「上一章」、「目錄」、「下一章」控制鈕。

## 4. 路由骨架程式碼

已在 `app/routes/` 建立以下檔案與骨架：
- `auth.py`
- `main.py`
- `reader.py`
