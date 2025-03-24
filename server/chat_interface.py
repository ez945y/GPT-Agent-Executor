
import os
import csv
import json
import agents
import asyncio
from utils.timestamp import TimestampGenerator
from utils.logger import Logger
class ChatInterface():
    active_websockets = {}
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
        if conversation_id in cls.active_websockets:
                chat_logs = await cls.read_latest_logs("chat")
                think_logs = await cls.read_latest_logs("think")
                await cls.active_websockets[conversation_id].send_json({
                "type": "logs_update",
                "chat_logs": chat_logs,
                "think_logs": think_logs,
            })
                
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
        Logger.set_conversation(cls, uid)
        await TimestampGenerator.generate_timestamp()

        think_agent = agents.ThinkAgent()
        tool_agent = agents.ToolAgent()
        target_agent = agents.TargetAgent()

        cls.agent_tasks = [
            think_agent.start(),
            tool_agent.start(),
            target_agent.start(),
        ]

        await asyncio.gather(*cls.agent_tasks)  # 啟動 agent

        await cls.send_conversation_list(uid)  # 通知前端要刷新 list

    @classmethod
    async def stop_conversation(cls):
        if hasattr(cls, 'agent_tasks'):
            for task in cls.agent_tasks:
                if not task.done():
                    task.cancel()
            cls.agent_tasks = []
   
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
        
    @staticmethod 
    async def read_latest_logs(log_type):
        log_dir = f"log/{log_type}"
        try:
            files = [f for f in os.listdir(log_dir) if f.endswith('.csv')]
            if not files:
                return []
            
            latest_file = sorted(files)[-1]  # Get the most recent file
            logs = []
            
            with open(os.path.join(log_dir, latest_file), 'r', encoding='utf-8') as f:
                import csv
                reader = csv.DictReader(f)
                logs = [{"timestamp": row["timestamp"], "sequence": row["sequence"], "message": row["message"]} 
                    for row in reader]
            
            # Return the last 20 logs
            return logs[-20:] if len(logs) > 20 else logs
        
        except Exception as e:
            print(f"Error reading logs: {e}")
            return []

    @staticmethod   
    async def read_logs_from_file(log_type, filename):
        """
        Reads logs from a specified file.

        Args:
            log_type (str): The type of log (used for directory).
            filename (str): The name of the log file.

        Returns:
            list: A list of log dictionaries, or an empty list if an error occurs.
        """
        log_dir = f"log/{log_type}"
        log_path = os.path.join(log_dir, log_type + "_log_"+filename + ".csv")

        try:
            logs = []
            with open(log_path, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                logs = [{"timestamp": row["timestamp"], "sequence": row["sequence"], "message": row["message"]} for row in reader]

            # Return the last 20 logs
            return logs[-20:] if len(logs) > 20 else logs

        except FileNotFoundError:
            print(f"Error: File '{filename}' not found in '{log_dir}'.")
            return []
        except Exception as e:
            print(f"Error reading logs from '{filename}': {e}")
            return []