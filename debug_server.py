#!/usr/bin/env python3
"""
診斷服務器啟動問題
"""

import sys
import os

print("🔍 開始診斷服務器啟動問題...")

# 1. 檢查 Python 版本
print(f"Python 版本: {sys.version}")

# 2. 檢查當前目錄
print(f"當前目錄: {os.getcwd()}")

# 3. 檢查模組導入
try:
    print("📦 檢查 FastAPI 導入...")
    from fastapi import FastAPI
    print("✅ FastAPI 導入成功")
except Exception as e:
    print(f"❌ FastAPI 導入失敗: {e}")
    sys.exit(1)

try:
    print("📦 檢查 uvicorn 導入...")
    import uvicorn
    print("✅ uvicorn 導入成功")
except Exception as e:
    print(f"❌ uvicorn 導入失敗: {e}")
    sys.exit(1)

try:
    print("📦 檢查 server.router 導入...")
    from server.router import router
    print("✅ server.router 導入成功")
except Exception as e:
    print(f"❌ server.router 導入失敗: {e}")
    sys.exit(1)

try:
    print("📦 檢查 server.cli_router 導入...")
    from server.cli_router import router as cli_router
    print("✅ server.cli_router 導入成功")
except Exception as e:
    print(f"❌ server.cli_router 導入失敗: {e}")
    sys.exit(1)

try:
    print("📦 檢查 server.chat_interface 導入...")
    from server.chat_interface import ChatInterface
    print("✅ server.chat_interface 導入成功")
except Exception as e:
    print(f"❌ server.chat_interface 導入失敗: {e}")
    sys.exit(1)

try:
    print("📦 檢查 agents 模組導入...")
    import agents
    print("✅ agents 模組導入成功")
except Exception as e:
    print(f"❌ agents 模組導入失敗: {e}")
    sys.exit(1)

# 4. 檢查目錄結構
print("📁 檢查目錄結構...")
required_dirs = ["server", "agents", "utils", "static"]
for dir_name in required_dirs:
    if os.path.exists(dir_name):
        print(f"✅ {dir_name} 目錄存在")
    else:
        print(f"❌ {dir_name} 目錄不存在")

# 5. 嘗試創建應用
print("🔧 嘗試創建 FastAPI 應用...")
try:
    from fastapi.middleware.cors import CORSMiddleware
    from fastapi.staticfiles import StaticFiles
    
    app = FastAPI()
    
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    app.include_router(router)
    app.include_router(cli_router, prefix="/cli")
    
    # 檢查靜態目錄
    if os.path.exists("static"):
        app.mount("/static", StaticFiles(directory="static"), name="static")
        print("✅ 靜態文件掛載成功")
    else:
        print("⚠️ 靜態目錄不存在，跳過掛載")
    
    print("✅ FastAPI 應用創建成功")
    
except Exception as e:
    print(f"❌ 創建 FastAPI 應用失敗: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print("🎉 診斷完成，所有檢查都通過！") 