#!/usr/bin/env python3
"""
CLI 客戶端腳本，使用 WebSocket 進行實時通信
"""

import asyncio
import websockets
import json
import argparse
import aioconsole
import sys
import signal
from typing import Optional

WS_URL = "ws://127.0.0.1:8000/cli/ws"

class WebSocketChatClient:
    def __init__(self, verbose: bool = False):
        self.websocket = None
        self.is_running = False
        self.conversation_id = None
        self.connected = False
        self.message_queue = asyncio.Queue()
        self.verbose = verbose
        self.last_chat_sequence = None  # 用 sequence 去重
        self.last_think_sequence = None
        self.ping_task = None
        self.connection_lock = asyncio.Lock()
        self.reconnect_attempts = 0
        self.max_reconnect_attempts = 3
        self.shutdown_event = asyncio.Event()
        
    def signal_handler(self, signum, frame):
        """信號處理器"""
        print(f"\n🛑 收到信號 {signum}，正在關閉...")
        self.shutdown_event.set()
        
    async def async_print(self, *args, **kwargs):
        """異步安全的打印函數"""
        try:
            message = " ".join(str(arg) for arg in args)
            await asyncio.get_event_loop().run_in_executor(
                None, lambda: print(message, **kwargs)
            )
        except Exception as e:
            # 如果異步打印失敗，回退到同步打印
            try:
                print(*args, **kwargs)
            except:
                pass
        
    async def keep_alive(self):
        while self.connected:
            try:
                pong_waiter = await self.websocket.ping()
                await pong_waiter
            except Exception as e:
                await self.async_print(f"⚠️ keep-alive ping 失敗: {e}")
                self.connected = False
                break
            await asyncio.sleep(10)

    async def ensure_connection(self):
        """確保連接狀態的原子性檢查"""
        async with self.connection_lock:
            if not self.connected:
                return await self.connect()
            return True
            
    async def safe_reconnect(self):
        """安全的重連機制"""
        if self.reconnect_attempts >= self.max_reconnect_attempts:
            return False
            
        self.reconnect_attempts += 1
        await asyncio.sleep(1)  # 延遲重連
        return await self.connect()
        
    async def connect(self):
        """連接到 WebSocket 服務器"""
        max_retries = 3
        retry_count = 0
        
        while retry_count < max_retries:
            try:
                self.websocket = await websockets.connect(WS_URL)
                self.connected = True
                self.reconnect_attempts = 0  # 重置重連計數
                await self.async_print("✅ 已連接到服務器")
                self.ping_task = asyncio.create_task(self.keep_alive())
                return True
            except Exception as e:
                retry_count += 1
                await self.async_print(f"❌ 連接失敗 (嘗試 {retry_count}/{max_retries}): {e}")
                if retry_count < max_retries:
                    await self.async_print("🔄 5秒後重試...")
                    await asyncio.sleep(5)
                else:
                    await self.async_print("❌ 連接失敗，已達最大重試次數")
                    return False

    async def disconnect(self):
        """斷開 WebSocket 連接"""
        if self.websocket:
            try:
                await self.websocket.close()
                await self.async_print("👋 已斷開連接")
            except Exception as e:
                await self.async_print(f"⚠️ 斷開連接時發生錯誤: {e}")
            finally:
                self.connected = False
                self.websocket = None
                if self.ping_task:
                    self.ping_task.cancel()
                    self.ping_task = None

    async def send_message(self, message_type: str, content: dict = None):
        """發送 WebSocket 消息"""
        if not self.connected:
            await self.async_print("❌ 未連接到服務器")
            return False
        
        max_retries = 2
        retry_count = 0
        
        while retry_count < max_retries:
            try:
                message = {
                    "type": message_type,
                    "content": content or {}
                }
                await self.websocket.send(json.dumps(message))
                return True
            except websockets.exceptions.ConnectionClosed:
                await self.async_print("❌ WebSocket 連接已關閉，無法發送訊息")
                self.connected = False
                return False
            except Exception as e:
                retry_count += 1
                await self.async_print(f"❌ 發送消息失敗 (嘗試 {retry_count}/{max_retries}): {e}")
                if retry_count < max_retries:
                    await asyncio.sleep(1)
                else:
                    self.connected = False
                    return False

    async def start_conversation(self, initial_task: str = None):
        """啟動對話"""
        if self.is_running:
            await self.async_print("💬 聊天已經在運行中...")
            return True
        
        await self.async_print("🚀 啟動對話...")
        if initial_task:
            await self.async_print(f"📋 初始任務: {initial_task}")
        
        # 發送測試訊息確認連接
        await self.async_print("🔍 發送測試訊息...")
        await self.send_message("test", {"message": "測試連接"})
        
        content = {"initial_task": initial_task} if initial_task else {}
        success = await self.send_message("start_conversation", content)
        if success:
            self.is_running = True
            return True
        return False

    async def stop_conversation(self):
        """停止對話"""
        if not self.is_running:
            await self.async_print("💬 聊天未在運行...")
            return True
        
        await self.async_print("🛑 停止對話...")
        success = await self.send_message("stop_conversation")
        if success:
            self.is_running = False
            self.conversation_id = None
            await self.async_print("✅ 已發送停止命令")
            return True
        else:
            await self.async_print("❌ 發送停止命令失敗")
            return False

    async def send_user_message(self, message: str):
        """發送用戶消息"""
        if not self.is_running:
            await self.async_print("❌ 請先使用 'start' 啟動聊天")
            return False
        
        if not message.strip():
            await self.async_print("❌ 消息不能為空")
            return False
        
        await self.async_print(f"📤 發送消息: {message}")
        success = await self.send_message("user_input", {"message": message})
        return success

    async def get_conversations(self):
        """獲取對話列表"""
        await self.async_print("📋 獲取對話列表...")
        await self.send_message("get_conversations")

    async def get_conversation(self, conversation_id: str):
        """獲取特定對話內容"""
        await self.async_print(f"📖 獲取對話內容: {conversation_id}")
        await self.send_message("get_conversation", {"conversation_id": conversation_id})

    async def get_cache_pool(self):
        """獲取 cache pool 內容"""
        await self.async_print("📦 獲取 Cache Pool 內容...")
        await self.send_message("get_cache_pool")

    async def get_status(self):
        """獲取系統狀態"""
        await self.async_print("📊 獲取系統狀態...")
        await self.send_message("get_status")

    async def listen_for_messages(self):
        """監聽 WebSocket 消息"""
        try:
            await self.async_print("🔍 開始監聽 WebSocket 訊息...")
            while self.connected:
                try:
                    message = await self.websocket.recv()
                    data = json.loads(message)
                    await self.handle_message(data)
                except websockets.exceptions.ConnectionClosed:
                    await self.async_print("🔌 WebSocket 連接已關閉")
                    self.connected = False
                    break
                except json.JSONDecodeError as e:
                    await self.async_print(f"❌ JSON 解析錯誤: {e}")
                    continue
                except Exception as e:
                    await self.async_print(f"❌ 接收消息錯誤: {e}")
                    if not self.connected:
                        break
                    continue
        except Exception as e:
            await self.async_print(f"❌ 監聽器錯誤: {e}")
        finally:
            await self.async_print("🔌 訊息監聽器已停止")
            self.connected = False

    async def handle_message(self, data: dict):
        """處理接收到的消息"""
        message_type = data.get("type")
        
        if message_type == "conversation_started":
            await self.async_print(f"✅ {data.get('message')}")
            self.conversation_id = data.get('conversation_id')
        
        elif message_type == "conversation_stopped":
            await self.async_print(f"✅ {data.get('message')}")
        
        elif message_type == "conversations_list":
            conversations = data.get('conversations', [])
            if conversations:
                await self.async_print("對話列表:")
                for conv in conversations:
                    await self.async_print(f"  ID: {conv.get('id')}")
                    await self.async_print(f"  標題: {conv.get('title')}")
                    await self.async_print(f"  創建時間: {conv.get('created_at')}")
                    await self.async_print("-" * 30)
            else:
                await self.async_print("📭 沒有對話記錄")
        
        elif message_type == "conversation_data":
            conversation_id = data.get('conversation_id')
            chat_logs = data.get('chat_logs', [])
            think_logs = data.get('think_logs', [])
            
            await self.async_print(f"📖 對話內容 (ID: {conversation_id}):")
            await self.async_print("聊天記錄:")
            for log in chat_logs[-5:]:  # 顯示最後5條
                await self.async_print(f"  {log.get('timestamp')}: {log.get('message')}")
            await self.async_print("思考記錄:")
            for log in think_logs[-5:]:  # 顯示最後5條
                await self.async_print(f"  {log.get('timestamp')}: {log.get('message')}")
        
        elif message_type == "cache_pool_data":
            cache_pool = data.get('cache_pool', [])
            length = data.get('length', 0)
            
            await self.async_print(f"📦 Cache Pool 內容 (長度: {length}):")
            for i, item in enumerate(cache_pool[-10:], 1):  # 顯示最後10條
                for key, value in item.items():
                    await self.async_print(f"  {i}. {key}: {value[:100]}{'...' if len(str(value)) > 100 else ''}")
        
        elif message_type == "status_data":
            status = data.get('system_status', 'unknown')
            cache_pool_length = data.get('cache_pool_length', 0)
            conversations_count = data.get('conversations_count', 0)
            
            await self.async_print("📊 系統狀態:")
            await self.async_print(f"  系統狀態: {status}")
            await self.async_print(f"  Cache Pool 長度: {cache_pool_length}")
            await self.async_print(f"  對話數量: {conversations_count}")
            await self.async_print(f"  🔄 聊天狀態: {'運行中' if self.is_running else '已停止'}")
        
        elif message_type == "logs_update":
            chat_logs = data.get('chat_logs', [])
            think_logs = data.get('think_logs', [])
            if self.verbose:
                if think_logs:
                    latest_think = think_logs[-1]
                    seq = latest_think.get('sequence') or latest_think.get('timestamp')
                    if seq != self.last_think_sequence:
                        await self.async_print(f"💭 {latest_think.get('timestamp')}: {latest_think.get('message')}")
                        self.last_think_sequence = seq
            else:
                if chat_logs:
                    latest_chat = chat_logs[-1]
                    seq = latest_chat.get('sequence') or latest_chat.get('timestamp')
                    if seq != self.last_chat_sequence:
                        await self.async_print(f"💬 {latest_chat.get('timestamp')}: {latest_chat.get('message')}")
                        self.last_chat_sequence = seq
        
        elif message_type == "error":
            await self.async_print(f"❌ 錯誤: {data.get('message')}")
        
        elif message_type == "test_response":
            await self.async_print(f"✅ 測試回應: {data.get('message')}")

    async def show_help(self):
        """異步顯示幫助信息"""
        help_lines = [
            "🎯 WebSocket CLI 聊天客戶端 - 指令說明",
            "=" * 50,
            "基本指令:",
            "  start                    - 啟動聊天（使用預設任務）",
            "  start --task <任務>      - 啟動聊天（指定初始任務）",
            "  start -t <任務>          - 啟動聊天（指定初始任務）",
            "  close/stop               - 關閉聊天",
            "  + <文字>                 - 發送消息（簡化模式）",
            "  send <文字>              - 發送消息（完整模式）",
            "  status                   - 顯示系統狀態",
            "  cache                    - 顯示 Cache Pool 內容",
            "",
            "高級指令:",
            "  list                     - 獲取對話列表",
            "  conv <id>                - 獲取對話內容",
            "  help                     - 顯示此幫助信息",
            "  quit/exit                - 退出程序",
            "",
            "顯示模式:",
            "  預設模式                 - 顯示 💬 chat 訊息",
            "  詳細模式 (--verbose/-v)  - 顯示 💭 think 訊息",
            "=" * 50,
            "💡 示例:",
            "  start",
            "  start --task 我想學習Python編程",
            "  start -t 今天天氣怎麼樣？",
            "  + 你好，我想和你聊天",
            "  send 今天天氣怎麼樣？",
            "  close",
            "",
            "💡 命令行模式:",
            "  python cli_client.py start --verbose",
            "  python cli_client.py start -v --task '我想學習Python'"
        ]
        
        for line in help_lines:
            await self.async_print(line)
            await asyncio.sleep(0.01)  # 避免阻塞

    async def run(self):
        """運行主程序"""
        # 註冊信號處理器
        signal.signal(signal.SIGINT, self.signal_handler)
        signal.signal(signal.SIGTERM, self.signal_handler)
        
        mode = "詳細模式 (💭 think)" if self.verbose else "預設模式 (💬 chat)"
        await self.async_print(f"🎯 WebSocket CLI 聊天客戶端 - {mode}")
        await self.async_print("輸入 'help' 查看所有指令")
        await self.async_print("-" * 30)
        
        # 連接到服務器
        if not await self.ensure_connection():
            return
        
        # 啟動消息監聽器
        await self.async_print("🔧 啟動訊息監聽器...")
        listener_task = asyncio.create_task(self.listen_for_messages())
        
        # 等待一下讓監聽器啟動
        await asyncio.sleep(0.1)
        
        try:
            while not self.shutdown_event.is_set():
                # 檢查連接狀態
                if not self.connected:
                    await self.async_print("❌ 連接已斷開，嘗試重新連接...")
                    if await self.safe_reconnect():
                        # 重新啟動消息監聽器
                        listener_task.cancel()
                        listener_task = asyncio.create_task(self.listen_for_messages())
                        await asyncio.sleep(0.1)
                    else:
                        await self.async_print("❌ 重新連接失敗，退出程序")
                        break
                
                # 使用非阻塞輸入，帶超時檢查
                try:
                    user_input = await asyncio.wait_for(
                        aioconsole.ainput(f""),
                        timeout=1.0
                    )
                    user_input = user_input.strip()
                except asyncio.TimeoutError:
                    # 超時時檢查是否需要關閉
                    if self.shutdown_event.is_set():
                        break
                    continue
                except (EOFError, KeyboardInterrupt):
                    await self.async_print("\n🛑 收到中斷信號")
                    break
                
                if not user_input:
                    continue
                
                # 處理指令
                if user_input.lower() in ['quit', 'exit']:
                    if self.is_running:
                        await self.stop_conversation()
                    break
                
                elif user_input.lower() in ['close', 'stop']:
                    await self.stop_conversation()
                
                elif user_input.lower() == 'start':
                    await self.start_conversation()
                
                elif user_input.lower().startswith('start '):
                    # 處理 start --task <任務> 或 start -t <任務>
                    parts = user_input.split()
                    if len(parts) >= 3 and (parts[1] == '--task' or parts[1] == '-t'):
                        task = ' '.join(parts[2:])
                        await self.start_conversation(initial_task=task)
                    else:
                        await self.async_print("❓ 用法: start --task <任務> 或 start -t <任務>")
                
                elif user_input.lower() == 'help':
                    await self.show_help()
                
                elif user_input.lower() == 'status':
                    await self.get_status()
                
                elif user_input.lower() == 'cache':
                    await self.get_cache_pool()
                
                elif user_input.startswith('+'):
                    message = user_input[1:].strip()
                    await self.send_user_message(message)
                
                elif user_input.lower().startswith('send '):
                    message = user_input[5:].strip()
                    await self.send_user_message(message)
                
                elif user_input.lower() == 'list':
                    await self.get_conversations()
                
                elif user_input.lower().startswith('conv '):
                    conv_id = user_input[5:].strip()
                    await self.get_conversation(conv_id)
                
                else:
                    await self.async_print("❓ 未知指令，輸入 'help' 查看所有指令")
        except KeyboardInterrupt:
            await self.async_print("\n🛑 收到中斷信號")
        except Exception as e:
            await self.async_print(f"❌ 運行時錯誤: {e}")
        finally:
            # 清理資源
            if self.is_running:
                await self.stop_conversation()
            await self.disconnect()
            listener_task.cancel()
            await self.async_print("👋 再見！")

async def main():
    """主函數"""
    parser = argparse.ArgumentParser(description="WebSocket CLI 聊天客戶端")
    parser.add_argument("command", nargs="?", help="命令")
    parser.add_argument("args", nargs="*", help="命令參數")
    parser.add_argument("--task", "-t", help="初始任務")
    parser.add_argument("--verbose", "-v", action="store_true", help="詳細模式，顯示 think 訊息")
    
    args = parser.parse_args()
    
    client = WebSocketChatClient(verbose=args.verbose)
    
    try:
        if args.command:
            # 命令行模式
            if not await client.connect():
                return
                
            command = args.command.lower()
            
            if command == "start":
                await client.start_conversation(initial_task=args.task)
            elif command == "send" and args.args:
                message = " ".join(args.args)
                await client.send_user_message(message)
            elif command == "list":
                await client.get_conversations()
            elif command == "conv" and args.args:
                await client.get_conversation(args.args[0])
            elif command == "cache":
                await client.get_cache_pool()
            elif command == "status":
                await client.get_status()
            elif command == "stop":
                await client.stop_conversation()
            else:
                print("用法: python cli_client.py <command> [args]")
                print("命令: start [--task <任務>], send <msg>, list, conv <id>, cache, status, stop")
                print("選項: --task, -t: 設置初始任務")
                print("選項: --verbose, -v: 詳細模式，顯示 think 訊息")
            
            await client.disconnect()
        else:
            # 互動模式
            await client.run()
    except KeyboardInterrupt:
        print("\n🛑 程序被中斷")
    except Exception as e:
        print(f"❌ 程序錯誤: {e}")
    finally:
        # 確保清理
        if client.connected:
            await client.disconnect()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n🛑 程序退出")
    except Exception as e:
        print(f"❌ 程序錯誤: {e}")
        sys.exit(1)