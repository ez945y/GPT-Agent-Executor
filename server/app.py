from fastapi import FastAPI, HTTPException, Request, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse, JSONResponse
from utils.logger import chat_logger
from pydantic import BaseModel
import os
import uuid
import json
import asyncio
from typing import List, Dict, Optional
import datetime

import csv
from server.chat_interface import ChatInterface
from utils.public_cache import CachePool
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],  # 允許的 HTTP 方法
    allow_headers=["*"],  # 允許的 HTTP 標頭
)


# WebSocket endpoint for real-time updates
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    conversation_id = None

    try:
        while True:
            data = await websocket.receive_text()
            message = json.loads(data)
            task = message.get("type")
            content = message.get("content")

            if  task == "get_conversation":
                conversation_id = content.get('conversation_id')
                print(conversation_id)
            if message.get("type") == "user_input":    
                received_text = message.get("content").get("message")
                await CachePool.add({"有人對你說話":received_text})
                await chat_logger.log("chat", await CachePool.get_len(), {"有人對你說話":received_text})
                print(f"你：{received_text}\n")

            await ChatInterface.handel_message(websocket, conversation_id, task, content)

    except WebSocketDisconnect:
        if ChatInterface.conversation_id and websocket in ChatInterface.active_websockets.get(conversation_id, None):
            del ChatInterface.active_websockets[conversation_id]

class Message(BaseModel):
    message: str

class Conversation(BaseModel):
    id: str
    title: Optional[str] = "New Conversation"
    messages: List[Dict] = []
    think_logs: List[Dict] = []
    created_at: str = datetime.datetime.now().isoformat()

# @app.get("/", response_class=HTMLResponse)
# async def get_html(request: Request):
#     # This endpoint should return your HTML page
#     with open("templates/index.html", "r", encoding="utf-8") as f:
#         html_content = f.read()
#     return HTMLResponse(content=html_content)

# # API endpoints for conversations
# @app.post("/api/conversations", response_class=JSONResponse)
# async def create_conversation():
#     conversation_id = str(uuid.uuid4())
#     conversations[conversation_id] = {
#         "id": conversation_id,
#         "title": "New Conversation",
#         "messages": [],
#         "think_logs": [],
#         "chat_logs": [],
#         "created_at": datetime.datetime.now().isoformat()
#     }
#     return {"conversation_id": conversation_id}

@app.get("/api/conversations", response_class=JSONResponse)
async def get_conversations():
    return await ChatInterface.get_conversations()
    
@app.get("/api/conversations/{conversation_id}", response_class=JSONResponse)
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
        return JSONResponse({"error": f"Error reading conversation data: {str(e)}"}, status_code=500)


# @app.delete("/api/conversations/{conversation_id}", response_class=JSONResponse)
# async def delete_conversation(conversation_id: str):
#     filepath = f"log/chat/{conversation_id}.csv"
#     if os.path.exists(filepath):
#         os.remove(filepath)
#         return {"message": "Conversation deleted"}
#     else:
#         raise HTTPException(status_code=404, detail="Conversation not found")


# # Message sending endpoint
# @app.post("/api/send_message", response_class=JSONResponse)
# async def send_message(data: Message, conversation_id: Optional[str] = None):
#     user_message = data.message
#     sequence = str(uuid.uuid4())[:8]
#     timestamp = datetime.datetime.now().isoformat()

#     # 紀錄使用者訊息
#     await chat_logger.log("chat", sequence, f"User: {user_message}")

#     # 處理訊息（模擬 LLM）
#     await asyncio.sleep(0.5)
#     bot_response = f"I received your message: {user_message}"
#     await chat_logger.log("chat", sequence, f"Assistant: {bot_response}")

#     # 如果有 conversation_id，則存入 chat CSV
#     if conversation_id:
#         filepath = f"log/chat/{conversation_id}.csv"

#         file_exists = os.path.isfile(filepath)
#         with open(filepath, "a", newline="", encoding="utf-8") as f:
#             writer = csv.writer(f)
#             if not file_exists:
#                 writer.writerow(["timestamp", "sequence", "message"])
#             writer.writerow([timestamp, sequence, f"User: {user_message}"])
#             writer.writerow([timestamp, sequence, f"Assistant: {bot_response}"])

#     return {"response": bot_response, "sequence": sequence}




# # Search functionality
# @app.get("/api/search", response_class=JSONResponse)
# async def search_conversations(query: str):
#     results = []
#     for conv_id, data in conversations.items():
#         # Search in messages
#         for msg in data["messages"]:
#             if query.lower() in msg["content"].lower():
#                 results.append({
#                     "conversation_id": conv_id,
#                     "conversation_title": data["title"],
#                     "match_type": "message",
#                     "content": msg["content"],
#                     "timestamp": msg["timestamp"]
#                 })
    
#     return results

# # Export conversation
# @app.get("/api/export/{conversation_id}", response_class=JSONResponse)
# async def export_conversation(conversation_id: str, format: str = "json"):
#     if conversation_id not in conversations:
#         raise HTTPException(status_code=404, detail="Conversation not found")
    
#     conversation_data = conversations[conversation_id]
    
#     if format == "json":
#         return conversation_data
#     elif format == "text":
#         # Convert to plain text format
#         text_content = f"Conversation: {conversation_data['title']}\n"
#         text_content += f"Date: {conversation_data['created_at']}\n\n"
        
#         for msg in conversation_data["messages"]:
#             text_content += f"{msg['role'].capitalize()}: {msg['content']}\n\n"
        
#         return JSONResponse(content={"text": text_content})
#     else:
#         raise HTTPException(status_code=400, detail="Unsupported format")

# # Settings API endpoint
# @app.get("/api/settings", response_class=JSONResponse)
# async def get_settings():
#     # This would typically load from a database or file
#     return {
#         "theme": "light",
#         "notification_sound": True,
#         "max_history": 50
#     }

# @app.put("/api/settings", response_class=JSONResponse)
# async def update_settings(settings: dict):
#     # This would typically save to a database or file
#     return {"message": "Settings updated", "settings": settings}

def run_fastapi_server():
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000, log_level="info")

if __name__ == "__main__":
    run_fastapi_server()