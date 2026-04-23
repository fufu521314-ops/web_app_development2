# 小說閱讀器系統 流程圖設計 (Flowchart)

本文件描述了使用者的操作流程以及系統內部的資料流向，幫助開發團隊理解功能邏輯。

## 1. 使用者流程圖 (User Flow)

描述讀者從進入網站到完成閱讀或管理書單的操作路徑。

```mermaid
flowchart LR
    Start([使用者開啟網頁]) --> Home[首頁 - 熱門與分類]
    
    Home --> Search{搜尋或瀏覽？}
    Search -->|搜尋| SearchPage[搜尋結果頁]
    Search -->|瀏覽排行榜| RankingPage[排行榜頁]
    Search -->|直接點擊| NovelDetail[小說詳情頁]

    SearchPage --> NovelDetail
    RankingPage --> NovelDetail

    NovelDetail --> Read{開始閱讀？}
    Read -->|是| Reader[閱讀介面]
    Read -->|否| Home

    Reader --> Record[自動儲存閱讀進度]
    Record --> Reader

    Home --> Auth{是否登入？}
    Auth -->|未登入| Login[登入/註冊頁]
    Auth -->|已登入| Profile[個人中心/收藏書單]

    Login --> Profile
    Profile --> NovelDetail
```

## 2. 系統序列圖 (Sequence Diagram)

描述「使用者點擊閱讀小說」到「系統讀取內容並紀錄進度」的完整流程。

```mermaid
sequenceDiagram
    actor User as 使用者
    participant Browser as 瀏覽器
    participant Flask as Flask Route (reader.py)
    participant Model as Novel/Record Model
    participant DB as SQLite

    User->>Browser: 點擊「繼續閱讀」
    Browser->>Flask: GET /novel/1/read/10
    
    activate Flask
    Flask->>Model: 取得小說章節內容
    Model->>DB: SELECT content FROM chapters WHERE novel_id=1 AND chapter=10
    DB-->>Model: 回傳章節文字
    
    Flask->>Model: 更新閱讀進度
    Model->>DB: UPDATE records SET last_chapter=10 WHERE user_id=1 AND novel_id=1
    DB-->>Model: 成功
    
    Flask->>Browser: render_template(reader.html, content)
    deactivate Flask
    
    Browser-->>User: 顯示小說內容
```

## 3. 功能清單對照表

以下為系統主要功能的 URL 路徑與對應的 HTTP 方法。

| 功能名稱 | URL 路徑 | HTTP 方法 | 說明 |
|---|---|---|---|
| 首頁 | `/` | GET | 顯示熱門小說與分類入口 |
| 登入 | `/auth/login` | GET/POST | 顯示登入頁面與處理登入邏輯 |
| 註冊 | `/auth/register` | GET/POST | 顯示註冊頁面與處理註冊邏輯 |
| 搜尋 | `/search` | GET | 根據關鍵字搜尋小說 |
| 排行榜 | `/ranking` | GET | 顯示各分類的小說排行 |
| 小說詳情 | `/novel/<id>` | GET | 顯示小說簡介、章節列表 |
| 閱讀介面 | `/novel/<id>/read/<chapter>` | GET | 閱讀特定章節內容 |
| 收藏小說 | `/novel/<id>/collect` | POST | 將小說加入使用者的收藏清單 |
| 個人紀錄 | `/profile` | GET | 顯示使用者的閱讀紀錄與收藏書單 |
