# GPT Agent Executor：實現自主協作與持續運行

# 專案內容

[English version](README_EN.md)

本專案旨在構建一個基於 GPT 的自主智能體框架，實現智能體的持續運行和協作。

通過模組化的設計，我們將智能體分解為三大核心模塊：

* **Think Agent（思考智能體）：** 負責分析目標、規劃任務和生成行動方案。
* **Tool Agent（工具智能體）：** 根據思考智能體的決策，調用外部工具或 API 執行具體任務。
* **Target Agent（目標智能體）：** 負責觀察自己的念頭，決定自己要做什麼的tool，會回傳一個target。

此外，本專案提供友好的使用者交互介面，並支援 Ollama 和 Gemini API 等多種語言模型後端，方便您根據需求選擇最適合的模型。

## 專案特色

* **自主運行：** 智能體能夠根據目標自主規劃和執行任務，無需人工干預。
* **模組化設計：** 三大核心模塊各司其職，方便擴展和維護。
* **多模型支援：** 支援 Ollama 和 Gemini API 等多種語言模型後端，靈活選擇。
* **使用者交互：** 提供友好的使用者交互介面，方便使用者與智能體互動。
* **持續學習：** 智能體能夠通過與環境互動不斷學習和進化。
* **一鍵啟動：** 提供便捷的啟動腳本，自動開啟伺服器和客戶端。

## 專案架構

* **Think Agent：**
    * 負責目標分析、任務規劃、行動決策。
    * 利用語言模型生成思考過程和行動方案。
* **Tool Agent：**
    * 根據 Think Agent 的決策，調用外部工具或 API。
    * 負責執行具體任務，並將結果返回給 Think Agent。
* **Target Agent：**
    * 負責觀察自己的念頭，決定自己要做什麼的tool，會回傳一個target。
    * 將目標回傳給think agent。
* **使用者交互：**
    * 提供命令列介面或 Web 介面。
    * 允許使用者設定目標、查看進度、與智能體互動。
* **模型後端：**
    * 支援 Ollama 和 Gemini API。
    * 允許使用者根據需求選擇模型。

## 使用場景

* **自動化任務執行：** 自動執行資料收集、報告生成、程式碼編寫等任務。
* **智能助手：** 提供個人助理、客戶服務、知識問答等服務。
* **研究與開發：** 用於探索智能體行為、測試語言模型能力。

## 安裝與啟動

### 方法一：一鍵啟動（推薦）

**macOS/Linux：**
```bash
./start_chat.sh
```

**Windows：**
```cmd
start_chat.bat
```

這些腳本會自動：
- 檢查並啟動伺服器（開新視窗）
- 啟動聊天客戶端（當前視窗）
- 自動等待伺服器就緒

### 方法二：手動啟動

1.  **安裝 Conda：**
    * 如果您的電腦上還沒有安裝 Conda，請從 Anaconda 官方網站下載並安裝 Anaconda 或 Miniconda。
2.  **建立 Conda 環境：**
    * 使用以下命令建立 Conda 環境：
        * `conda create --name continuous-gpt-ai-agent --file requirements.txt`
    * 或者，您也可以使用以下命令從 `requirements.txt` 檔案建立環境：
        * `conda env create -f environment.yml`
3.  **啟用 Conda 環境：**
    * 使用以下命令啟用 Conda 環境：
        * `conda activate continuous-gpt-ai-agent`
4.  **啟動服務器：**
    * `python start_server.py`
5.  **啟動客戶端：**
    * `python cli_client.py`

## 未來展望

* 增加更多工具和 API 支援。
* 優化智能體的學習和推理能力。
* 開發更豐富的使用者交互介面。
* 探索多智能體協作。

## 貢獻指南

* 歡迎貢獻程式碼、文件、測試用例等。
* 請參考貢獻指南，瞭解如何參與專案。

## 授權條款

* 本專案採用 [授權條款名稱] 授權。

# AI 聊天應用

這是一個基於 FastAPI 和 React 的 AI 聊天應用，支持多種交互方式。

## 功能特點

- 🤖 多代理系統：ThinkAgent、ToolAgent、TargetAgent
- 💬 多種客戶端：Web 界面、CLI 客戶端
- 🔄 實時監控：自動監控 AI 思考過程
- 🛠️ 工具集成：支持網絡搜索等功能
- 📊 日誌記錄：完整的聊天和思考日誌
- 🚀 一鍵啟動：自動開啟伺服器和客戶端

## 快速開始

### 方法一：一鍵啟動（推薦）

**macOS/Linux：**
```bash
./start_chat.sh
```

**Windows：**
```cmd
start_chat.bat
```

這會自動開啟兩個視窗：
- **伺服器視窗**：運行 FastAPI 服務器
- **客戶端視窗**：運行 CLI 聊天客戶端

### 方法二：手動啟動

#### 1. 啟動服務器

```bash
# 安裝依賴
pip install -r requirements.txt

# 啟動服務器
python start_server.py
```

#### 2. 使用客戶端

#### Web 界面
訪問 http://localhost:3000 使用 React 前端界面

#### CLI 客戶端（推薦）
```bash
# 互動模式（默認自動監控）
python cli_client.py

# 詳細模式（顯示所有監控內容）
python cli_client.py -v

# 命令行模式
python cli_client.py start
python cli_client.py send "你好"
python cli_client.py monitor
```

## CLI 客戶端功能

### 統一界面
- **自動監控**：啟動後自動開始監控 think 輸出
- **實時狀態**：顯示聊天狀態（🟢/🔴）和監控狀態（👀）
- **簡化命令**：使用 `+` 符號發送消息
- **完整功能**：支持所有 API 端點

### 監控功能
- **自動監控**：啟動時自動開始後台監控
- **think 輸出**：實時顯示 AI 的思考過程
- **詳細模式**：使用 `-v` 或 `monitor-verbose` 顯示所有內容
- **手動控制**：可隨時啟動/停止監控

### 命令列表
```bash
# 基本命令
start          - 啟動對話
close/stop     - 關閉對話
+ <文字>       - 發送消息（簡化模式）
send <文字>    - 發送消息（完整模式）
status         - 查看狀態
cache          - 查看 cache pool

# 監控命令
monitor        - 啟動實時監控
monitor-verbose - 啟動詳細監控（顯示所有內容）
stop-monitor   - 停止監控

# 高級命令
list           - 對話列表
conv <id>      - 查看對話內容
help           - 顯示幫助信息
quit/exit      - 退出程序
```

## 使用示例

### 1. 基本使用
```bash
# 啟動客戶端
python cli_client.py

# 在客戶端中：
🟢👀 > start
🟢👀 > + 你好，我想了解今天的天氣
🟢👀 > status
🟢👀 > close
```

### 2. 詳細監控
```bash
# 啟動詳細模式
python cli_client.py -v

# 或手動切換到詳細監控
🟢👀 > stop-monitor
🟢 > monitor-verbose
🟢👀 > + 你好
```

### 3. 命令行模式
```bash
# 直接執行命令
python cli_client.py start
python cli_client.py send "你好"
python cli_client.py monitor
python cli_client.py status
```

## API 端點

### CLI API (`/cli`)
- `POST /cli/start_conversation` - 啟動對話
- `POST /cli/send_message` - 發送消息
- `GET /cli/conversations` - 獲取對話列表
- `GET /cli/conversation/{id}` - 獲取對話內容
- `GET /cli/cache_pool` - 獲取 cache pool
- `GET /cli/status` - 獲取系統狀態
- `POST /cli/stop_conversation` - 停止對話

### WebSocket API (`/ws`)
- 實時雙向通信
- 支持 Web 界面

## 項目結構

```
ollama/
├── agents/              # AI 代理
│   ├── base_agent.py
│   ├── think_agent.py
│   ├── tool_agent.py
│   └── target_agent.py
├── server/              # 後端服務
│   ├── chat_interface.py
│   ├── cli_router.py
│   └── router.py
├── utils/               # 工具類
│   ├── logger.py
│   ├── public_cache.py
│   └── ...
├── cli_client.py        # CLI 客戶端（統一版）
├── start_chat.sh        # Linux/Mac 啟動腳本
├── start_chat.bat       # Windows 啟動腳本
└── README.md
```

## 監控功能詳解

### 自動監控
- 啟動客戶端時自動開始後台監控
- 實時顯示 AI 的 think 輸出
- 不影響正常命令輸入

### 監控內容
- **普通模式**：只顯示 `{"思考": "內容"}` 的輸出
- **詳細模式**：顯示所有 cache pool 內容

### 監控控制
- `monitor` - 啟動普通監控
- `monitor-verbose` - 啟動詳細監控
- `stop-monitor` - 停止監控

## 注意事項

1. 確保服務器正在運行（`uvicorn main:app`）
2. CLI 客戶端會自動檢查服務器狀態
3. 監控功能在後台運行，不影響命令輸入
4. 使用 `Ctrl+C` 退出程序
5. 所有對話和思考都會記錄到日誌文件中

## 故障排除

### 服務器連接失敗
```bash
# 檢查服務器是否運行
curl http://127.0.0.1:8000/cli/status

# 啟動服務器
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Python 環境問題
```bash
# 安裝依賴
pip install -r requirements.txt

# 或使用 conda
conda install requests fastapi uvicorn
```

### 權限問題
```bash
# 給啟動腳本執行權限
chmod +x start_chat.sh
```