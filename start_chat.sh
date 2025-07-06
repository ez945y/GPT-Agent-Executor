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

# 檢查 websockets 模組
if ! python -c "import websockets" 2>/dev/null; then
    echo "📦 安裝 websockets 模組..."
    python -m pip install websockets
    if [ $? -ne 0 ]; then
        echo "❌ 安裝 websockets 失敗"
        exit 1
    fi
fi

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

# 如果服務器未運行，啟動服務器
if [ "$SERVER_RUNNING" = false ]; then
    echo "🚀 啟動伺服器..."
    
    # 檢測作業系統類型
    if [[ "$OSTYPE" == "darwin"* ]]; then
        # macOS
        osascript -e 'tell application "Terminal" to do script "cd \"'$(pwd)'\" && conda activate ollama && python start_server.py"'
    elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
        # Linux
        if command -v gnome-terminal &> /dev/null; then
            gnome-terminal -- bash -c "cd '$(pwd)' && conda activate ollama && python start_server.py; exec bash"
        elif command -v konsole &> /dev/null; then
            konsole -e bash -c "cd '$(pwd)' && conda activate ollama && python start_server.py; exec bash"
        elif command -v xterm &> /dev/null; then
            xterm -e bash -c "cd '$(pwd)' && conda activate ollama && python start_server.py; exec bash" &
        else
            echo "⚠️ 無法找到合適的終端模擬器，請手動啟動服務器"
            echo "   命令：conda activate ollama && python start_server.py"
        fi
    else
        echo "⚠️ 不支援的作業系統，請手動啟動服務器"
        echo "   命令：conda activate ollama && python start_server.py"
    fi
    
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