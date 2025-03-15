import threading
from collections import deque
import asyncio
from typing import Any
from utils.logger import think_logger

class CachePool:
    _pool: deque[Any] = deque(maxlen=100)  # 最大長度為 100
    _lock: threading.Lock = threading.Lock()

    @classmethod
    async def add(cls, input: Any) -> None:
        with cls._lock:
            cls._pool.append(input)
        print(input)
        await think_logger.log("think", len(cls._pool), input)

    @classmethod
    def get(cls, length: int = 10) -> str:
        with cls._lock:
            length = min(length, len(cls._pool))
            items = list(cls._pool)[-length:]
            # 將列表中的每個元素轉換為字串，並連接起來
            return ", ".join(map(str, items)) #將list轉成字串