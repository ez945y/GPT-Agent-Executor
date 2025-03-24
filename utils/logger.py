import os
import csv
import datetime
import asyncio
from utils.timestamp import TimestampGenerator

class Logger:
    _instance = None
    _lock = asyncio.Lock()
    log_dir = "log"

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Logger, cls).__new__(cls)
            os.makedirs(cls.log_dir, exist_ok=True)
        return cls._instance
    
    @classmethod
    async def set_conversation(cls, chat_interface, uid):
        cls.chat_interface = chat_interface
        cls.uid = uid

    @classmethod
    async def log(cls, log_type, sequence, message):
        async with cls._lock:
            if log_type == "think":
                filename = os.path.join(cls.log_dir, f"think_log_{TimestampGenerator.get_timestamp()}.csv")
            elif log_type == "tool":
                filename = os.path.join(cls.log_dir, f"tool_log_{TimestampGenerator.get_timestamp()}.csv")
            elif log_type == "chat":
                filename = os.path.join(cls.log_dir, f"chat_log_{TimestampGenerator.get_timestamp()}.csv")
                print(message)
            else:
                raise ValueError("log_type must be 'think', 'tool' or 'chat'")

            if filename is None:
                raise ValueError("Conversation ID must be set before logging.")

            file_exists = os.path.isfile(filename)
            with open(filename, "a", newline="", encoding="utf-8") as csvfile:
                writer = csv.writer(csvfile)
                if not file_exists:
                    writer.writerow(["timestamp", "sequence", "message"])

                timestamp = datetime.datetime.now().isoformat()
                writer.writerow([timestamp, sequence, message])

            if log_type != "tool":
                await cls.chat_interface.send_conversation(cls.uid)