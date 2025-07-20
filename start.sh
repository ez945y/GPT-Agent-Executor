#!/bin/bash

# 檢查 conda 是否可用
if command -v conda &> /dev/null; then
    # 激活 ollama 環境
    source $(conda info --base)/etc/profile.d/conda.sh
    conda activate ollama
    echo "✅ 已激活 ollama conda 環境"
else
    echo "⚠️ conda 不可用，使用系統 Python"
fi

# 檢查 Python 是否安裝
if ! command -v python &> /dev/null; then
    echo "❌ Python 未安裝，請先安裝 Python"
    exit 1
fi

# 檢查必要的模組是否已安裝
echo "🔍 檢查依賴..."
python -c "import fastapi, uvicorn, websockets, requests, ollama, google.generativeai, serpapi, pydantic, openai" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "❌ 缺少必要的依賴，請先運行 ./install_requirements.sh"
    echo "或者手動安裝：pip install -r requirements.txt"
    exit 1
fi
echo "✅ 所有依賴已安裝"

# 檢查 8000 端口是否被佔用，若有則殺掉對應進程
PID=$(lsof -ti:8000)
if [ -n "$PID" ]; then
    echo "⚠️ 8000 端口被佔用，正在終止進程 $PID ..."
    kill -9 $PID
    sleep 1
fi

# 檢查服務器是否運行
echo "🔍 檢查服務器狀態..."
if curl -s --max-time 3 http://127.0.0.1:8000/cli/status > /dev/null 2>&1; then
    echo "✅ 服務器正在運行"
    SERVER_RUNNING=true
else
    echo "❌ 服務器未運行，將啟動服務器"
    SERVER_RUNNING=false
fi

# 捕捉 Ctrl+C 信號，結束後台伺服器進程
cleanup() {
    echo "🛑 收到中斷訊號，停止伺服器..."
    if [ -n "$SERVER_PID" ]; then
        kill $SERVER_PID
    fi
    exit 1
}
trap cleanup SIGINT SIGTERM

# 如果服務器未運行，啟動伺服器
if [ "$SERVER_RUNNING" = false ]; then
    echo "🚀 啟動伺服器..."
    # 在當前 shell 以後台模式啟動伺服器，並保存 PID
    python start_server.py &
    SERVER_PID=$!

    # 等待服務器啟動
    echo "⏳ 等待服務器啟動..."
    for i in {1..30}; do
        if curl -s --max-time 3 http://127.0.0.1:8000/cli/status > /dev/null 2>&1; then
            echo "✅ 服務器已啟動"
            break
        fi
        sleep 1
        echo -n "."
    done

    if ! curl -s --max-time 3 http://127.0.0.1:8000/cli/status > /dev/null 2>&1; then
        echo "❌ 服務器啟動失敗，請檢查錯誤訊息"
        exit 1
    fi
fi

echo ""
echo 🎯 啟動 WebSocket CLI 聊天客戶端...
echo 功能特點：
echo • 實時 WebSocket 通信
echo • 自動監控 think 輸出
echo • 支持簡化命令（+ 發送消息）
echo • 支持完整命令（send、list、conv 等）
echo • 支持詳細模式（--verbose/-v 顯示 think 訊息）
echo • 支持初始化目標（--task/-t 設置初始任務）
echo • 實時狀態指示器
echo ""
echo 使用 'help' 查看所有命令
echo 使用 Ctrl+C 退出
echo ==========================

# 啟動客戶端
python cli_client.py

# 客戶端退出後停止伺服器
if [ -n "$SERVER_PID" ]; then
    echo "🛑 停止伺服器..."
    kill $SERVER_PID
fi