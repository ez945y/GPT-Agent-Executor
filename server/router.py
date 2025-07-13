from fastapi import APIRouter, HTTPException, WebSocket, WebSocketDisconnect
import uuid
import json
import csv
import os
from server.chat_interface import ChatInterface
from utils.logger import Logger
from utils.public_cache import CachePool
import uuid
from fastapi.responses import FileResponse

router = APIRouter()

@router.get(
    "/{file_path:path}",
    summary="Get File",
)
async def get_file(file_path: str):
    full_path = f'./snapshot/{file_path}'
    if not os.path.exists(full_path):
        raise FileNotFoundError(file_path=full_path)
    return FileResponse(full_path)

@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    uid = uuid.uuid4()
    await websocket.accept()
    ChatInterface.active_websockets[uid] = websocket
    try:
        while True:
            data = await websocket.receive_text()
            message = json.loads(data)
            task = message.get("type")
            content = message.get("content")

            if message.get("type") == "user_input":
                received_text = message.get("content").get("message")
                await CachePool.add({"有人對你說話": received_text})
                await Logger.log("chat", await CachePool.get_len(), {"有人對你說話": received_text})

            await ChatInterface.handel_message(websocket, uid, task, content)

    except WebSocketDisconnect:
        await ChatInterface.stop_conversation()
        if  websocket in ChatInterface.active_websockets.get(uid, None):
            del ChatInterface.active_websockets[uid]

@router.get("/api/conversations")
async def get_conversations():
    return await ChatInterface.get_conversations()

@router.get("/api/conversations/{conversation_id}")
async def get_conversation(conversation_id: str):
    chat_filepath = f"log/chat/{conversation_id}.csv"
    think_filepath = f"log/think/{conversation_id}.csv"

    if not os.path.exists(chat_filepath) or not os.path.exists(think_filepath):
        raise HTTPException(status_code=404, detail="Conversation data not found")

    try:
        with open(chat_filepath, 'r', encoding='utf-8') as chat_f, \
                open(think_filepath, 'r', encoding='utf-8') as think_f:

            chat_reader = csv.DictReader(chat_f)
            chat_messages = list(chat_reader)

            think_reader = csv.DictReader(think_f)
            think_messages = list(think_reader)

        return {
            "id": conversation_id,
            "title": think_messages[0]["message"][:20] + "...",
            "chat_messages": chat_messages,
            "think_messages": think_messages,
            "created_at": chat_messages[0]["timestamp"]
        }

    except Exception as e:
        return {"error": f"Error reading conversation data: {str(e)}"}