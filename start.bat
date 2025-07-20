@echo off
chcp 65001 >nul
setlocal enabledelayedexpansion

echo 🎯 CLI 聊天客戶端啟動器
echo ==========================

REM 檢查 Python 是否安裝
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python 未安裝，請先安裝 Python
    pause
    exit /b 1
)

echo ✅ Python 已安裝

REM 檢查必要的模組是否已安裝
echo 🔍 檢查依賴...
python -c "import fastapi, uvicorn, websockets, requests, ollama, google.generativeai, serpapi, pydantic, openai" >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ 缺少必要的依賴，請先運行 install_requirements.bat
    echo 或者手動安裝：pip install -r requirements.txt
    pause
    exit /b 1
)
echo ✅ 所有依賴已安裝

REM 檢查服務器是否運行
echo 🔍 檢查服務器狀態...
curl -s http://127.0.0.1:8000/cli/status >nul 2>&1
if %errorlevel% equ 0 (
    echo ✅ 服務器正在運行
    set SERVER_RUNNING=true
) else (
    echo ❌ 服務器未運行，將啟動服務器
    set SERVER_RUNNING=false
)

REM 如果服務器未運行，啟動服務器
if "%SERVER_RUNNING%"=="false" (
    echo 🚀 啟動伺服器...
    
    REM 啟動新視窗運行伺服器
    start "Ollama 伺服器" cmd /k "cd /d "%~dp0" && python start_server.py"
    
    REM 等待服務器啟動
    echo ⏳ 等待服務器啟動...
    for /l %%i in (1,1,30) do (
        curl -s http://127.0.0.1:8000/cli/status >nul 2>&1
        if !errorlevel! equ 0 (
            echo ✅ 服務器已啟動
            goto :server_ready
        )
        timeout /t 1 /nobreak >nul
        echo -n .
    )
    
    echo ❌ 服務器啟動失敗，請檢查錯誤訊息
    pause
    exit /b 1
)

:server_ready
echo.
echo 🎯 啟動 WebSocket CLI 聊天客戶端...
echo 功能特點：
echo • 實時 WebSocket 通信
echo • 自動監控 think 輸出
echo • 支持簡化命令（+ 發送消息）
echo • 支持完整命令（send、list、conv 等）
echo • 支持詳細模式（--verbose/-v 顯示 think 訊息）
echo • 支持初始化目標（--task/-t 設置初始任務）
echo • 實時狀態指示器
echo.
echo 使用 'help' 查看所有命令
echo 使用 Ctrl+C 退出
echo ==========================

REM 啟動客戶端
python cli_client.py

pause