#!/usr/bin/env python3
"""
服務器啟動腳本，包含優雅關閉機制
"""

import os
import signal
import asyncio
import uvicorn
from contextlib import asynccontextmanager
from fastapi import FastAPI
from server.router import router
from server.cli_router import router as cli_router
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from server.chat_interface import ChatInterface

# 全局變量
shutdown_event = asyncio.Event()
app = None

def signal_handler(signum, frame):
    """信號處理器"""
    print(f"\n🛑 收到信號 {signum}，開始優雅關閉...")
    shutdown_event.set()

@asynccontextmanager
async def lifespan(app: FastAPI):
    """應用生命週期管理"""
    # 啟動時
    print("🚀 服務器正在啟動...")
    
    # 註冊信號處理器
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    yield
    
    # 關閉時
    print("🛑 服務器正在關閉，清理資源...")
    
    # 停止所有對話
    try:
        await ChatInterface.stop_conversation()
        print("✅ 已停止所有對話")
    except Exception as e:
        print(f"⚠️ 停止對話時發生錯誤: {e}")
    
    # 清理 WebSocket 連接
    try:
        from server.cli_router import cli_websocket, cli_connection_active
        if cli_websocket:
            cli_connection_active = False
            await cli_websocket.close()
            print("✅ 已關閉 CLI WebSocket 連接")
    except Exception as e:
        print(f"⚠️ 關閉 WebSocket 時發生錯誤: {e}")
    
    print("✅ 資源清理完成")

def ensure_log_directories():
    """確保所有必要的日誌目錄都存在"""
    log_dirs = ["log", "log/chat", "log/think", "log/tool"]
    for log_dir in log_dirs:
        os.makedirs(log_dir, exist_ok=True)
    print("✅ 日誌目錄初始化完成")

def create_app():
    """創建 FastAPI 應用"""
    global app
    
    # 初始化日誌目錄
    ensure_log_directories()
    
    app = FastAPI(lifespan=lifespan)
    
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    app.include_router(router)
    app.include_router(cli_router, prefix="/cli")
    app.mount("/static", StaticFiles(directory="static"), name="static")
    
    return app

def main():
    """主函數"""
    try:
        app = create_app()
        
        print("🎯 啟動 Ollama 聊天服務器")
        print("=" * 40)
        print("服務器地址: http://127.0.0.1:8000")
        print("CLI WebSocket: ws://127.0.0.1:8000/cli/ws")
        print("使用 Ctrl+C 優雅關閉服務器")
        print("=" * 40)
        
        uvicorn.run(
            app,
            host="127.0.0.1",
            port=8000,
            log_level="info",
            loop="asyncio"
        )
        
    except KeyboardInterrupt:
        print("\n🛑 收到 Ctrl+C，正在關閉服務器...")
    except Exception as e:
        print(f"❌ 服務器錯誤: {e}")
    finally:
        print("👋 服務器已關閉")

if __name__ == "__main__":
    main()