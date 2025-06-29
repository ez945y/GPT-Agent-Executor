import os
import csv
import json
import agents
import asyncio
from utils.timestamp import TimestampGenerator
from utils.logger import Logger
import websockets

class ChatInterface():
    active_websockets = {}
    agent_instances = []  # 保存 agent 實例的引用
    
    @classmethod
    async def handel_message(cls, websocket, uid, task, content):
        if task == "get_conversation":
            conversation_id = content.get('conversation_id')
            # 發送 chat_logs 和 think_logs
            chat_logs = await cls.read_logs_from_file("chat", conversation_id)
            think_logs = await cls.read_logs_from_file("think", conversation_id)
            await websocket.send_json({
                "type": "logs_update",
                "chat_logs": chat_logs,
                "think_logs": think_logs,
            })
        elif task == "start_conversation":
            await cls.start_conversation(uid)
        elif task == "stop_conversation":
            await cls.stop_conversation()
        
    @classmethod
    async def send_conversation(cls, conversation_id):
        print(f"📤 發送對話更新: {conversation_id}")
        
        if conversation_id in cls.active_websockets:
                try:
                    chat_logs = await cls.read_latest_logs("chat")
                    think_logs = await cls.read_latest_logs("think")
                    await cls.active_websockets[conversation_id].send_json({
                    "type": "logs_update",
                    "chat_logs": chat_logs,
                    "think_logs": think_logs,
                })
                    print(f"✅ 已向 WebSocket {conversation_id} 發送更新")
                except Exception as e:
                    print(f"❌ 向 WebSocket {conversation_id} 發送更新失敗: {e}")
                    # 移除斷開的 WebSocket
                    del cls.active_websockets[conversation_id]
        
        # 同時向 CLI WebSocket 發送更新（動態導入避免循環依賴）
        try:
            from server.cli_router import cli_websocket
            from starlette.websockets import WebSocketState
            if cli_websocket and getattr(cli_websocket, 'application_state', None) == WebSocketState.CONNECTED:
                try:
                    chat_logs = await cls.read_latest_logs("chat")
                    think_logs = await cls.read_latest_logs("think")
                    await cli_websocket.send_json({
                        "type": "logs_update",
                        "chat_logs": chat_logs,
                        "think_logs": think_logs,
                    })
                    print("✅ 已向 CLI WebSocket 發送更新")
                except Exception as e:
                    print(f"❌ 向 CLI WebSocket 發送更新失敗: {e}")
                    # 發送失敗時自動清理 cli_websocket
                    from server import cli_router
                    cli_router.cli_websocket = None
                    # 如果是 keepalive ping timeout 或 1011 internal error 也清理
                    if '1011' in str(e) or 'ping timeout' in str(e):
                        print("⚠️ 檢測到 keepalive ping timeout 或 1011 internal error，自動清理 cli_websocket")
                        cli_router.cli_websocket = None
            else:
                print("⚠️ CLI WebSocket 未連接或未 accept")
        except ImportError:
            # CLI router 可能還沒有加載
            pass
        except Exception as e:
            print(f"❌ 獲取 CLI WebSocket 失敗: {e}")
                
    @classmethod
    async def send_conversation_list(cls, uid):
        if uid in cls.active_websockets:
            conversation_list = cls.get_conversations()
            await cls.active_websockets[uid].send_json(json.dumps({
            "type": "log_list_update",
            "conversation_list": conversation_list
            }))

    @classmethod
    async def start_conversation(cls, uid):
        await Logger.set_conversation(cls, uid)
        await TimestampGenerator.generate_timestamp()

        think_agent = agents.ThinkAgent()
        tool_agent = agents.ToolAgent()
        target_agent = agents.TargetAgent()

        # 保存 agent 實例的引用
        cls.agent_instances = [think_agent, tool_agent, target_agent]

        # 創建 agent 任務
        cls.agent_tasks = [
            think_agent.start(),
            tool_agent.start(),
            target_agent.start(),
        ]

        # 在後台啟動 agents，不阻塞主線程
        async def run_agents():
            try:
                print("🚀 開始運行 agents...")
                await asyncio.gather(*cls.agent_tasks)
                print("✅ Agents 運行完成")
            except asyncio.CancelledError:
                print("🛑 Agents 任務被取消")
            except Exception as e:
                print(f"❌ Agent 運行錯誤: {e}")

        # 創建後台任務
        cls.agent_background_task = asyncio.create_task(run_agents())

        await cls.send_conversation_list(uid)  # 通知前端要刷新 list

    @classmethod
    async def stop_conversation(cls):
        """停止當前對話"""
        print("🛑 開始停止對話...")
        
        # 停止所有 agents
        for agent in cls.agent_instances:
            if hasattr(agent, 'stop'):
                try:
                    print(f"🛑 停止 agent: {type(agent).__name__}")
                    agent.stop()
                except Exception as e:
                    print(f"⚠️ 停止 agent {type(agent).__name__} 時發生錯誤: {e}")
        
        # 取消後台任務
        if hasattr(cls, 'agent_background_task') and cls.agent_background_task:
            try:
                print("🛑 取消後台 agent 任務...")
                cls.agent_background_task.cancel()
                # 等待任務取消完成
                try:
                    await cls.agent_background_task
                except asyncio.CancelledError:
                    print("✅ 後台 agent 任務已取消")
            except Exception as e:
                print(f"⚠️ 取消後台任務時發生錯誤: {e}")
        
        # 等待一下讓 agents 有時間停止
        await asyncio.sleep(1)
        
        # 清空 agent 實例列表
        cls.agent_instances = []
        
        # 清空任務引用
        if hasattr(cls, 'agent_tasks'):
            cls.agent_tasks = []
        if hasattr(cls, 'agent_background_task'):
            cls.agent_background_task = None
        
        print("✅ 對話已停止")
   
    @staticmethod
    async def get_conversations():
        log_dir = "log/chat"
        try:
            files = [f for f in os.listdir(log_dir) if f.endswith('.csv')]
            
            if not files:
                return []

            conversations = []
            for file in sorted(files, reverse=True):  # 按時間排序，最新的優先
                with open(os.path.join(log_dir, file), 'r', encoding='utf-8') as f:
                    reader = csv.DictReader(f)
                    messages = list(reader)
                    if messages:
                        conversations.append({
                            "id": file.replace(".csv", "").replace("chat_log_", ""),
                            "title": messages[0]["message"][:20] + "...",  # 用第一則訊息作為標題
                            "created_at": messages[0]["timestamp"]
                        })

            return conversations
        except Exception as e:
            print(e)
            return []

    @staticmethod
    async def read_logs_from_file(log_type: str, conversation_id: str):
        log_dir = f"log/{log_type}"
        try:
            files = [f for f in os.listdir(log_dir) if f.endswith('.csv')]
            
            if not files:
                return []

            logs = []
            for file in files:
                with open(os.path.join(log_dir, file), 'r', encoding='utf-8') as f:
                    reader = csv.DictReader(f)
                    for row in reader:
                        logs.append({
                            "timestamp": row["timestamp"],
                            "message": row["message"]
                        })

            return logs
        except Exception as e:
            print(e)
            return []

    @staticmethod
    async def read_latest_logs(log_type: str):
        log_dir = f"log/{log_type}"
        try:
            files = [f for f in os.listdir(log_dir) if f.endswith('.csv')]
            
            if not files:
                return []

            # 獲取最新的文件
            latest_file = sorted(files)[-1]
            
            logs = []
            with open(os.path.join(log_dir, latest_file), 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    logs.append({
                        "timestamp": row["timestamp"],
                        "message": row["message"]
                    })

            return logs
        except Exception as e:
            print(e)
            return []