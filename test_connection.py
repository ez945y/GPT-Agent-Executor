#!/usr/bin/env python3
"""
測試 WebSocket 連接和斷開功能
"""

import asyncio
import websockets
import json
import time

WS_URL = "ws://127.0.0.1:8000/cli/ws"

async def test_connection():
    """測試連接和斷開"""
    print("🧪 開始測試 WebSocket 連接...")
    
    try:
        # 連接
        websocket = await websockets.connect(WS_URL)
        print("✅ 連接成功")
        
        # 發送測試消息
        test_message = {
            "type": "test",
            "content": {"message": "測試連接"}
        }
        await websocket.send(json.dumps(test_message))
        print("📤 已發送測試消息")
        
        # 接收回應
        response = await websocket.recv()
        data = json.loads(response)
        print(f"📥 收到回應: {data}")
        
        # 等待一下
        await asyncio.sleep(2)
        
        # 斷開連接
        await websocket.close()
        print("🔌 已斷開連接")
        
    except Exception as e:
        print(f"❌ 測試失敗: {e}")

if __name__ == "__main__":
    asyncio.run(test_connection()) 