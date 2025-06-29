from fastapi import APIRouter, HTTPException, WebSocket, WebSocketDisconnect
from pydantic import BaseModel
import asyncio
import json
import uuid
from server.chat_interface import ChatInterface
from utils.logger import Logger
from utils.public_cache import CachePool
from utils.timestamp import TimestampGenerator
import agents

router = APIRouter(tags=["CLI Interface"])

class UserInputRequest(BaseModel):
    message: str

class ConversationRequest(BaseModel):
    conversation_id: str = None

# 保存 CLI WebSocket 連接
cli_websocket = None
cli_connection_active = False  # 添加連接狀態標誌

@router.websocket("/ws")
async def cli_websocket_endpoint(websocket: WebSocket):
    """
    CLI WebSocket 端點，用於實時通信
    """
    global cli_websocket, cli_connection_active
    cli_uid = "cli_interface"
    
    try:
        await websocket.accept()
        cli_websocket = websocket
        cli_connection_active = True
        print(f"✅ CLI WebSocket 已連接: {cli_uid}")
        
        while cli_connection_active:
            try:
                # 檢查連接狀態
                if websocket.client_state.value != 1:  # 1 = CONNECTED
                    print(f"🔌 WebSocket 連接狀態異常: {websocket.client_state.value}")
                    break
                
                data = await websocket.receive_text()
                message = json.loads(data)
                task = message.get("type")
                content = message.get("content")

                if task == "user_input":
                    received_text = message.get("content", {}).get("message")
                    if received_text:
                        await CachePool.add({"有人對你說話": received_text})
                        await Logger.log("chat", await CachePool.get_len(), {"有人對你說話": received_text})

                await handle_cli_message(websocket, cli_uid, task, content)
                
            except WebSocketDisconnect:
                print(f"🔌 CLI WebSocket 連接已斷開: {cli_uid}")
                break
            except json.JSONDecodeError as e:
                print(f"❌ JSON 解析錯誤: {e}")
                continue
            except Exception as e:
                print(f"❌ CLI WebSocket 處理錯誤: {e}")
                if websocket.client_state.value != 1:  # 如果連接已斷開，退出循環
                    break
                continue
                
    except Exception as e:
        print(f"❌ CLI WebSocket 連接錯誤: {e}")
    finally:
        # 確保清理連接狀態
        try:
            await ChatInterface.stop_conversation()
        except Exception as e:
            print(f"⚠️ 停止對話時發生錯誤: {e}")
        
        cli_websocket = None
        cli_connection_active = False
        print(f"🔌 CLI WebSocket 已清理: {cli_uid}")

def is_cli_websocket_connected():
    """檢查 CLI WebSocket 是否連接"""
    global cli_websocket, cli_connection_active
    return cli_websocket is not None and cli_connection_active and cli_websocket.client_state.value == 1

async def handle_cli_message(websocket, uid, task, content):
    """
    處理 CLI WebSocket 消息
    """
    if task == "start_conversation":
        initial_task = content.get('initial_task') if content else None
        await start_cli_conversation(websocket, uid, initial_task)
    elif task == "stop_conversation":
        await stop_cli_conversation(websocket)
    elif task == "get_conversations":
        await send_conversations(websocket)
    elif task == "get_conversation":
        conversation_id = content.get('conversation_id')
        await send_conversation(websocket, conversation_id)
    elif task == "get_cache_pool":
        await send_cache_pool(websocket)
    elif task == "get_status":
        await send_status(websocket)
    elif task == "test":
        # 測試訊息
        print("🔍 收到 CLI 測試訊息")
        await websocket.send_json({
            "type": "test_response",
            "message": "測試成功，WebSocket 連接正常"
        })

async def start_cli_conversation(websocket, uid, initial_task: str = None):
    """
    啟動 CLI 對話
    """
    try:
        print(f"🔧 開始啟動 CLI 對話: {uid}")
        if initial_task:
            print(f"📋 初始任務: {initial_task}")
        
        # 設置對話
        await Logger.set_conversation(ChatInterface, uid)
        await TimestampGenerator.generate_timestamp()
        print("✅ 對話設置完成")

        # 創建並啟動 agents
        think_agent = agents.ThinkAgent()
        tool_agent = agents.ToolAgent()
        target_agent = agents.TargetAgent()
        print("✅ Agents 創建完成")

        # 保存 agent 實例的引用
        ChatInterface.agent_instances = [think_agent, tool_agent, target_agent]

        # 創建 agent 任務
        agent_tasks = [
            think_agent.start(initial_task=initial_task),
            tool_agent.start(),
            target_agent.start(),
        ]

        # 在後台啟動 agents，不阻塞 WebSocket 響應
        async def run_agents():
            try:
                print("🚀 開始運行 agents...")
                await asyncio.gather(*agent_tasks)
                print("✅ Agents 運行完成")
            except Exception as e:
                print(f"❌ Agent 運行錯誤: {e}")

        # 創建後台任務
        asyncio.create_task(run_agents())

        # 發送成功消息
        await websocket.send_json({
            "type": "conversation_started",
            "message": "對話已啟動，agents 正在運行",
            "conversation_id": uid,
            "initial_task": initial_task
        })
        print("✅ 已發送啟動成功消息")

        # 等待一下讓 agents 開始運行
        await asyncio.sleep(1)

        # 發送初始狀態
        await send_status(websocket)
        print("✅ 已發送初始狀態")

    except Exception as e:
        print(f"❌ 啟動對話失敗: {e}")
        await websocket.send_json({
            "type": "error",
            "message": f"啟動對話失敗: {str(e)}"
        })

async def stop_cli_conversation(websocket):
    """
    停止 CLI 對話
    """
    try:
        print("🛑 停止 CLI 對話...")
        await ChatInterface.stop_conversation()
        await websocket.send_json({
            "type": "conversation_stopped",
            "message": "對話已停止"
        })
        print("✅ CLI 對話已停止")
    except Exception as e:
        print(f"❌ 停止 CLI 對話失敗: {e}")
        await websocket.send_json({
            "type": "error",
            "message": f"停止對話失敗: {str(e)}"
        })

async def send_conversations(websocket):
    """
    發送對話列表
    """
    try:
        conversations = await ChatInterface.get_conversations()
        await websocket.send_json({
            "type": "conversations_list",
            "conversations": conversations
        })
    except Exception as e:
        await websocket.send_json({
            "type": "error",
            "message": f"獲取對話列表失敗: {str(e)}"
        })

async def send_conversation(websocket, conversation_id):
    """
    發送特定對話內容
    """
    try:
        chat_logs = await ChatInterface.read_logs_from_file("chat", conversation_id)
        think_logs = await ChatInterface.read_logs_from_file("think", conversation_id)
        
        await websocket.send_json({
            "type": "conversation_data",
            "conversation_id": conversation_id,
            "chat_logs": chat_logs,
            "think_logs": think_logs
        })
    except Exception as e:
        await websocket.send_json({
            "type": "error",
            "message": f"獲取對話內容失敗: {str(e)}"
        })

async def send_cache_pool(websocket):
    """
    發送 cache pool 內容
    """
    try:
        cache_content = await CachePool.get_all()
        await websocket.send_json({
            "type": "cache_pool_data",
            "cache_pool": cache_content,
            "length": await CachePool.get_len()
        })
    except Exception as e:
        await websocket.send_json({
            "type": "error",
            "message": f"獲取 cache pool 失敗: {str(e)}"
        })

async def send_status(websocket):
    """
    發送系統狀態
    """
    try:
        cache_length = await CachePool.get_len()
        conversations = await ChatInterface.get_conversations()
        
        await websocket.send_json({
            "type": "status_data",
            "cache_pool_length": cache_length,
            "conversations_count": len(conversations),
            "system_status": "running"
        })
    except Exception as e:
        await websocket.send_json({
            "type": "error",
            "message": f"獲取狀態失敗: {str(e)}"
        })

# 保留原有的 HTTP 端點作為備用
@router.post("/start_conversation")
async def start_conversation():
    """
    啟動一個新的對話 (HTTP 備用)
    """
    try:
        # 生成一個虛擬的 uid 用於 CLI 介面
        cli_uid = "cli_interface"
        
        # 設置對話
        await Logger.set_conversation(ChatInterface, cli_uid)
        await TimestampGenerator.generate_timestamp()

        # 創建並啟動 agents
        think_agent = agents.ThinkAgent()
        tool_agent = agents.ToolAgent()
        target_agent = agents.TargetAgent()

        # 保存 agent 實例的引用
        ChatInterface.agent_instances = [think_agent, tool_agent, target_agent]

        # 創建 agent 任務
        agent_tasks = [
            think_agent.start(),
            tool_agent.start(),
            target_agent.start(),
        ]

        # 在後台啟動 agents，不阻塞 API 響應
        async def run_agents():
            try:
                await asyncio.gather(*agent_tasks)
            except Exception as e:
                print(f"Agent 運行錯誤: {e}")

        # 創建後台任務
        asyncio.create_task(run_agents())

        return {
            "status": "success",
            "message": "對話已啟動，agents 正在運行",
            "conversation_id": cli_uid
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"啟動對話失敗: {str(e)}")

@router.post("/send_message")
async def send_message(request: UserInputRequest):
    """
    發送用戶消息到 cache pool (HTTP 備用)
    """
    try:
        # 將用戶輸入添加到 cache pool
        await CachePool.add({"有人對你說話": request.message})
        
        # 記錄到日誌
        await Logger.log("chat", await CachePool.get_len(), {"有人對你說話": request.message})
        
        return {
            "status": "success",
            "message": f"消息已發送: {request.message}",
            "cache_pool_length": await CachePool.get_len()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"發送消息失敗: {str(e)}")

@router.get("/conversations")
async def get_conversations():
    """
    獲取所有對話列表 (HTTP 備用)
    """
    try:
        conversations = await ChatInterface.get_conversations()
        return {
            "status": "success",
            "conversations": conversations
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"獲取對話列表失敗: {str(e)}")

@router.get("/conversation/{conversation_id}")
async def get_conversation(conversation_id: str):
    """
    獲取特定對話的內容 (HTTP 備用)
    """
    try:
        chat_logs = await ChatInterface.read_logs_from_file("chat", conversation_id)
        think_logs = await ChatInterface.read_logs_from_file("think", conversation_id)
        
        return {
            "status": "success",
            "conversation_id": conversation_id,
            "chat_logs": chat_logs,
            "think_logs": think_logs
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"獲取對話內容失敗: {str(e)}")

@router.get("/cache_pool")
async def get_cache_pool():
    """
    獲取當前 cache pool 的內容 (HTTP 備用)
    """
    try:
        cache_content = await CachePool.get_all()
        return {
            "status": "success",
            "cache_pool": cache_content,
            "length": await CachePool.get_len()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"獲取 cache pool 失敗: {str(e)}")

@router.post("/stop_conversation")
async def stop_conversation():
    """
    停止當前對話 (HTTP 備用)
    """
    try:
        await ChatInterface.stop_conversation()
        return {
            "status": "success",
            "message": "對話已停止"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"停止對話失敗: {str(e)}")

@router.get("/status")
async def get_status():
    """
    獲取系統狀態 (HTTP 備用)
    """
    try:
        cache_length = await CachePool.get_len()
        conversations = await ChatInterface.get_conversations()
        
        return {
            "status": "success",
            "cache_pool_length": cache_length,
            "conversations_count": len(conversations),
            "system_status": "running"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"獲取狀態失敗: {str(e)}") 