import os
import csv
import datetime
from server.chat_interface import ChatInterface
import asyncio
class Logger:
    def __init__(self, log_dir):
        self.log_dir = log_dir
        os.makedirs(log_dir, exist_ok=True)
        self.think_filename = self.generate_filename("think_log.csv")
        self.tool_filename = self.generate_filename("tool_log.csv")
        self.chat_filename = self.generate_filename("chat_log.csv") #新增chat_filename

    def generate_filename(self, base_filename):
        """產生帶有時間戳的檔案名稱"""
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        name, ext = os.path.splitext(base_filename)
        return f"{name}_{timestamp}{ext}"

    async def log(self, log_type, sequence, message):
        if log_type == "think":
            filename = self.think_filename
        elif log_type == "tool":
            filename = self.tool_filename
        elif log_type == "chat": #新增chat log type
            filename = self.chat_filename
            print(message)
        else:
            raise ValueError("log_type must be 'think', 'tool' or 'chat'")

        filepath = os.path.join(self.log_dir, filename)

        file_exists = os.path.isfile(filepath)
        with open(filepath, "a", newline="", encoding="utf-8") as csvfile:
            writer = csv.writer(csvfile)
            if not file_exists:
                writer.writerow(["timestamp", "sequence", "message"])

            timestamp = datetime.datetime.now().isoformat()
            writer.writerow([timestamp, sequence, message])

        if log_type != "tool":
            await ChatInterface.send_conversation(filename.split("_log_")[1].replace(".csv", ''))

# 建立 think, tool, chat 的 logger 物件
think_logger = Logger("log/think")
tool_logger = Logger("log/tool")
chat_logger = Logger("log/chat")