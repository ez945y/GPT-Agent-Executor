import os
import csv
import datetime
import asyncio
from utils.timestamp import TimestampGenerator
from utils.public_cache import CachePool

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
                subdir = "think"
            elif log_type == "tool":
                subdir = "tool"
            elif log_type == "chat":
                subdir = "chat"
            else:
                raise ValueError("log_type must be 'think', 'tool' or 'chat'")

            # 產生正確的路徑
            log_dir = os.path.join(cls.log_dir, subdir)
            os.makedirs(log_dir, exist_ok=True)
            filename = os.path.join(log_dir, f"{log_type}_log_{TimestampGenerator.get_timestamp()}.csv")

            if log_type == "think":
                await CachePool.add_think({"思考": message})
            elif log_type == "chat":
                print(message)

            file_exists = os.path.isfile(filename)
            with open(filename, "a", newline="", encoding="utf-8") as csvfile:
                writer = csv.writer(csvfile)
                if not file_exists:
                    writer.writerow(["timestamp", "sequence", "message"])

                timestamp = datetime.datetime.now().isoformat()
                writer.writerow([timestamp, sequence, message])

            if log_type != "tool":
                await cls.chat_interface.send_conversation(cls.uid)