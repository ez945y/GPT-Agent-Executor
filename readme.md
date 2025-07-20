# GPT Agent Executor：實現自主協作與持續運行

## 🚀 快速開始

1. **安裝依賴：** `./install_requirements.sh` (Linux/Mac) 或 `install_requirements.bat` (Windows)
2. **一鍵啟動：** `./start.sh` (Linux/Mac) 或 `start.bat` (Windows)



---

# 專案內容

[English version](README_EN.md)

本專案旨在構建一個基於 GPT 的自主智能體框架，實現智能體的持續運行和協作。

通過模組化的設計，我們將智能體分解為三大核心模塊：

* **Think Agent（思考智能體）：** 負責分析目標、規劃任務和生成行動方案。
* **Tool Agent（工具智能體）：** 根據思考智能體的決策，調用外部工具或 API 執行具體任務。
* **Target Agent（目標智能體）：** 負責觀察自己的念頭，決定自己要做什麼的tool，會回傳一個target。

此外，本專案提供友好的使用者交互介面，並支援 Ollama、Gemini API 和 OpenAI API 等多種語言模型後端，方便您根據需求選擇最適合的模型。

## 專案特色

* **自主運行：** 智能體能夠根據目標自主規劃和執行任務，無需人工干預。
* **模組化設計：** 三大核心模塊各司其職，方便擴展和維護。
* **多模型支援：** 支援 Ollama、Gemini API 和 OpenAI API 等多種語言模型後端，靈活選擇。
* **視覺語言模型（VLM）：** 支援圖像理解和分析，可處理圖片輸入。
* **智能工具集成：** 內建網路搜尋、內容摘要、自然表達等工具。
* **命令行界面：** 提供 CLI 客戶端和現代化命令行界面。
* **實時監控：** 實時顯示 AI 思考過程和對話狀態。
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
    * 支援工具：網路搜尋、內容摘要、自然表達等。
* **Target Agent：**
    * 負責觀察自己的念頭，決定自己要做什麼的tool，會回傳一個target。
    * 將目標回傳給think agent。
* **使用者交互：**
    * 提供命令列介面（CLI）。
    * 允許使用者設定目標、查看進度、與智能體互動。
    * 實時監控 AI 思考過程。
* **模型後端：**
    * 支援 Ollama、Gemini API 和 OpenAI API。
    * 支援視覺語言模型（VLM）功能。
    * 允許使用者根據需求選擇模型。

## 支援的模型

### Ollama 模型
- 本地部署，無需 API 金鑰
- 支援 VLM 模型（如 qwen2.5vl）
- 完全離線運行

### Gemini API
- Google 的 Gemini 模型
- 需要 API 金鑰
- 支援文字生成

### OpenAI API
- OpenAI 的 GPT 系列模型
- 支援自定義 API 端點（代理）
- 支援 VLM 功能
- 配置格式：`openai@https://your-proxy-url/v1`

## 內建工具

### 網路搜尋
- 使用 Google 搜尋 API
- 自動獲取網頁內容
- 返回標題、摘要和完整內容

### 內容摘要
- 智能摘要長文本內容
- 提取關鍵信息

### 自然表達
- 將 AI 思考轉化為自然語言表達
- 更人性化的回應

### 目標管理
- 觀察和設定目標清單
- 追蹤任務進度

## 使用場景

* **自動化任務執行：** 自動執行資料收集、報告生成、程式碼編寫等任務。
* **智能助手：** 提供個人助理、客戶服務、知識問答等服務。
* **圖像分析：** 使用 VLM 模型分析圖片內容。
* **研究與開發：** 用於探索智能體行為、測試語言模型能力。

## 安裝與啟動

### 第一步：安裝依賴（首次使用必須）

**macOS/Linux：**
```bash
./install_requirements.sh
```

**Windows：**
```cmd
install_requirements.bat
```

或者手動安裝：
```bash
pip install -r requirements.txt
```

### 第二步：配置環境變數（可選）

詳見下方的"配置說明"章節。

### 第三步：啟動服務

#### 方法一：一鍵啟動（推薦）

**macOS/Linux：**
```bash
./start.sh
```

**Windows：**
```cmd
start.bat
```

這些腳本會自動：
- 檢查依賴是否已安裝
- 檢查並啟動伺服器（開新視窗）
- 啟動聊天客戶端（當前視窗）
- 自動等待伺服器就緒



#### 方法二：手動啟動

1.  **啟動服務器：**
    ```bash
    python start_server.py
    ```

2.  **使用客戶端：**
    ```bash
    python cli_client.py
    ```

## 界面功能

### CLI 客戶端
- **統一界面：** 自動監控、實時狀態顯示
- **簡化命令：** 使用 `+` 符號發送消息
- **監控功能：** 實時顯示 AI 思考過程
- **完整功能：** 支持所有 API 端點

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

### 4. VLM 功能測試
```bash
# 測試視覺語言模型
python vlm_test.py "https://example.com/image.jpg" "描述這張圖片"
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
- 支持 CLI 客戶端



## 監控功能詳解

### 自動監控
- 啟動客戶端時自動開始後台監控
- 實時顯示 AI 的 think 輸出
- 不影響正常命令輸入

### 監控內容
- **普通模式**：只顯示 `{"思考": "內容"}` 的輸出
- **詳細模式**：顯示所有 cache pool 內容

監控命令詳見上方的"命令列表"章節。

## 配置說明

### 環境變數配置
創建 `.env` 文件：

```bash
# API 金鑰
SERP_API_KEY=your-serp-api-key
GEMINI_API_KEY=your-gemini-api-key
OPENAI_API_KEY=your-openai-api-key

# 模型配置
THINK_MODEL_NAME=gemini-flash-2.0
THINK_MODEL_TYPE=gemini
TARGET_MODEL_NAME=gemini-flash-2.0
TARGET_MODEL_TYPE=gemini
TOOL_MODEL_NAME=gemini-flash-2.0
TOOL_MODEL_TYPE=gemini

# 功能開關
SUPPORT_IMAGE=false

# 間隔設定（秒）
THINK_INTERVAL=6
TARGET_INTERVAL=60
TOOL_INTERVAL=15
```

### 模型配置示例
```bash
# Ollama 模型
THINK_MODEL_TYPE=ollama
THINK_MODEL_NAME=qwen2.5vl:3b

# Gemini 模型
THINK_MODEL_TYPE=gemini
THINK_MODEL_NAME=gemini-pro
GEMINI_API_KEY=your-api-key

# OpenAI 模型
THINK_MODEL_TYPE=openai@https://your-proxy-url/v1
THINK_MODEL_NAME=gpt-4o
OPENAI_API_KEY=your-api-key
```

## 注意事項

1. 確保服務器正在運行（`uvicorn main:app`）
2. CLI 客戶端會自動檢查服務器狀態
3. 監控功能在後台運行，不影響命令輸入
4. 使用 `Ctrl+C` 退出程序
5. 所有對話和思考都會記錄到日誌文件中
6. VLM 功能需要支援的模型（如 qwen2.5vl）
7. 網路搜尋功能需要 SerpAPI 金鑰
8. CLI 客戶端需要 Python 環境
9. 環境變數配置優先於代碼中的默認值

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
./install_requirements.sh

# 或手動安裝
pip install -r requirements.txt

# 或使用 conda
conda install requests fastapi uvicorn
```

### 權限問題
```bash
# 給啟動腳本執行權限
chmod +x start_chat.sh
```

### VLM 模型問題
```bash
# 檢查 Ollama 模型是否安裝
ollama list

# 安裝 VLM 模型
ollama pull qwen2.5vl:3b
```

### API 金鑰問題
- 確保在 `.env` 文件中正確配置 API 金鑰
- 檢查網路連接和 API 端點可用性
- 驗證 API 金鑰的有效性

### 環境變數問題
- 確保 `.env` 文件在項目根目錄
- 檢查變數名稱是否正確
- 重啟服務器以載入新的環境變數

## 未來展望

* 增加更多工具和 API 支援。
* 優化智能體的學習和推理能力。
* 開發更豐富的使用者交互介面。
* 探索多智能體協作。
* 增強 VLM 功能支援。

## 貢獻指南

* 歡迎貢獻程式碼、文件、測試用例等。
* 請參考貢獻指南，瞭解如何參與專案。

## 授權條款

* 本專案採用 [授權條款名稱] 授權。