@echo off
chcp 65001 >nul
setlocal enabledelayedexpansion

echo 📦 安裝 Python 依賴包...
echo ==========================

REM 檢查 Python 是否安裝
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python 未安裝，請先安裝 Python
    pause
    exit /b 1
)

echo ✅ Python 已安裝

REM 升級 pip
echo 🔄 升級 pip...
python -m pip install --upgrade pip

REM 安裝 requirements.txt 中的所有依賴
echo 📦 安裝項目依賴...
if exist "requirements.txt" (
    python -m pip install -r requirements.txt
    if %errorlevel% equ 0 (
        echo ✅ 所有依賴安裝成功
    ) else (
        echo ❌ 依賴安裝失敗，請檢查錯誤訊息
        pause
        exit /b 1
    )
) else (
    echo ❌ requirements.txt 文件不存在
    pause
    exit /b 1
)

echo.
echo 🎉 安裝完成！
echo 現在可以使用以下命令啟動服務：
echo   start_server.bat    - 啟動服務器
echo   start_client.bat    - 啟動客戶端
echo   start_chat.bat      - 一鍵啟動（服務器+客戶端）

pause 