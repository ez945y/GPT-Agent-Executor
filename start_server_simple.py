#!/usr/bin/env python3
"""
簡化的服務器啟動腳本
"""

import os
import uvicorn
from fastapi import FastAPI
from server.router import router
from server.cli_router import router as cli_router
from fastapi.middleware.cors import CORSMiddleware

def ensure_log_directories():
    """確保所有必要的日誌目錄都存在"""
    log_dirs = ["log", "log/chat", "log/think", "log/tool"]
    for log_dir in log_dirs:
        os.makedirs(log_dir, exist_ok=True)
    print("✅ 日誌目錄初始化完成")

def create_app():
    """創建 FastAPI 應用"""
    # 初始化日誌目錄
    ensure_log_directories()
    
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
    
    return app

def main():
    """主函數"""
    try:
        print("🔧 正在創建 FastAPI 應用...")
        app = create_app()
        print("✅ FastAPI 應用創建成功")
        
        print("🎯 啟動 Ollama 聊天服務器")
        print("=" * 40)
        print("服務器地址: http://127.0.0.1:8000")
        print("CLI WebSocket: ws://127.0.0.1:8000/cli/ws")
        print("使用 Ctrl+C 關閉服務器")
        print("=" * 40)
        
        uvicorn.run(
            app,
            host="127.0.0.1",
            port=8000,
            log_level="info"
        )
        
    except KeyboardInterrupt:
        print("\n🛑 收到 Ctrl+C，正在關閉服務器...")
    except Exception as e:
        print(f"❌ 服務器錯誤: {e}")
        import traceback
        traceback.print_exc()
    finally:
        print("👋 服務器已關閉")

if __name__ == "__main__":
    main() 