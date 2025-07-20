#!/bin/bash

echo "📦 安裝 Python 依賴包..."
echo "=========================="

# 檢查 Python 是否安裝
if ! command -v python &> /dev/null; then
    echo "❌ Python 未安裝，請先安裝 Python"
    exit 1
fi

echo "✅ Python 已安裝"

# 檢查 conda 是否可用
if command -v conda &> /dev/null; then
    # 激活 ollama 環境
    source $(conda info --base)/etc/profile.d/conda.sh
    conda activate ollama
    echo "✅ 已激活 ollama conda 環境"
else
    echo "⚠️ conda 不可用，使用系統 Python"
fi

# 升級 pip
echo "🔄 升級 pip..."
python -m pip install --upgrade pip

# 安裝 requirements.txt 中的所有依賴
echo "📦 安裝項目依賴..."
if [ -f "requirements.txt" ]; then
    python -m pip install -r requirements.txt
    if [ $? -eq 0 ]; then
        echo "✅ 所有依賴安裝成功"
    else
        echo "❌ 依賴安裝失敗，請檢查錯誤訊息"
        exit 1
    fi
else
    echo "❌ requirements.txt 文件不存在"
    exit 1
fi

echo ""
echo "🎉 安裝完成！"
echo "現在可以使用以下命令啟動服務："
echo "  ./start_server.sh    - 啟動服務器"
echo "  ./start_client.sh    - 啟動客戶端"
echo "  ./start_chat.sh      - 一鍵啟動（服務器+客戶端）" 