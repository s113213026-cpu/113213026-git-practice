# FastAPI 與 PostgreSQL 範例專案

本專案已完成環境配置與修復，包含資料庫建立、測試資料匯入、相依套件安裝與代碼問題修正。

---

## 🛠️ 已完成的修復與設定

1. **環境變數與 PATH 設定**：
   - 已將 Python (`pythoncore-3.14-64`) 與 PostgreSQL `bin` 路徑加入系統環境變數，現在可直接在終端機使用 `python`、`pip`、`fastapi`、`uv`、`psql`。
   - 設定 `PYTHONIOENCODING=utf-8` 與 `PYTHONUTF8=1`，解決 Windows Traditional Chinese (CP950) 終端機遇到 emoji 編碼錯誤的問題。

2. **資料庫建立與資料匯入**：
   - 在本機 PostgreSQL 建立資料庫 `mydb`。
   - 使用密碼 `0000` 匯入 `students.sql`（共 71 筆學生測試資料）。

3. **缺少套件安裝**：
   - 安裝 `psycopg[binary,pool]`（PostgreSQL 連線池與非同步驅動）。
   - 安裝 `itsdangerous`（`SessionMiddleware` 必要套件）。

4. **程式碼修復**：
   - [db.py](file:///c:/Users/user/Downloads/DB-Basic%20Example/db.py)：
     - 設定 Windows 下 psycopg 所需的 `WindowsSelectorEventLoopPolicy`。
     - 資料庫密碼改為讀取環境變數 `PGPASSWORD`，預設為 `0000`。
     - 移除容易在繁體中文 Windows 終端機引起 CP950 編碼異常的 emoji 輸出。
   - [main.py](file:///c:/Users/user/Downloads/DB-Basic%20Example/main.py)：
     - 修復 `app.include_router` 傳入字串導致的語法錯誤，正確匯入 `from routes.r import router as myRoute` 並掛載。
     - 新增根路徑 `/` 自動轉址到 `/students/list/template`。

---

## 🚀 如何啟動服務

在終端機中執行下列指令即可啟動不同範例：

### 1. 學生資料庫 CRUD 範例 (main.py)
```bash
fastapi dev main.py
```
或
```bash
uv run fastapi dev main.py
```
- 首頁 / 學生列表頁面：[http://127.0.0.1:8000/](http://127.0.0.1:8000/) 或 [http://127.0.0.1:8000/students/list/template](http://127.0.0.1:8000/students/list/template)
- **新增學生 (Create)**：
  - 點擊列表上方的 `➕ 新增學生` 按鈕或前往 [http://127.0.0.1:8000/student/create](http://127.0.0.1:8000/student/create)。
  - 填寫學號、姓名、系所、身高、體重後送出，會自動新增至 PostgreSQL 並導回列表。
- **修改學生 (Update)**：
  - 點擊列表中的 `✏️ 修改`（例如 `/student/edit/112212015`），可修改姓名、系所與身高，儲存後即時生效。
- **刪除學生 (Delete)**：
  - 點擊列表中的 `🗑️ 刪除`（例如 `/student/delete/112212015`），跳出確認對話框確認後即從資料庫刪除該筆學生資料。
- API JSON 列表：[http://127.0.0.1:8000/students/list](http://127.0.0.1:8000/students/list)
- 路由測試：[http://127.0.0.1:8000/test](http://127.0.0.1:8000/test)

---

### 2. Session 登入範例 (sessionLogin.py)
```bash
fastapi dev sessionLogin.py
```
- 首頁：[http://127.0.0.1:8000/](http://127.0.0.1:8000/)（未登入會自動轉跳至登入頁面）
- 測試帳號：帳號 `user`，密碼 `pass`。
- 登入後可進行登出測試。

---

### 3. APIRouter 模組化路由範例 (routerUse.py)
```bash
fastapi dev routerUse.py
```
- 首頁：[http://127.0.0.1:8000/](http://127.0.0.1:8000/)
- 模組路由：[http://127.0.0.1:8000/rou/tes](http://127.0.0.1:8000/rou/tes) 或 [http://127.0.0.1:8000/rou/test](http://127.0.0.1:8000/rou/test)
