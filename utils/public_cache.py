import threading
from collections import deque
from typing import Any, Deque, List, Dict

class CachePool:
    """
    快取池類別，用於儲存和管理快取資料。
    """

    _pool: Deque[Any] = deque(maxlen=25)  # 快取池，最大長度為 25
    _lock: threading.Lock = threading.Lock()  # 線程鎖，用於保證線程安全
    _current_target: str = "目前還沒有目標"  # 當前目標，預設為 "目前還沒有目標"
    _check_list: List[Dict[str, str]] = []  # 檢查清單，格式: [{"item": "描述", "status": "pending/completed"}]
    _image_url: str = None  # 當前圖片 URL

    @classmethod
    async def add(cls, input: Any) -> None:
        """
        向快取池中新增一個元素。

        Args:
            input (Any): 要新增的元素。
        """
        with cls._lock:
            cls._pool.append(input)

        # 動態導入 Logger 避免循環依賴
        from utils.logger import Logger
        await Logger.log("think", len(cls._pool), input)

    @classmethod
    async def add_think(cls, input: Any) -> None:
        """
        向快取池中新增一個 think 元素（不觸發 Logger.log）。

        Args:
            input (Any): 要新增的 think 元素。
        """
        with cls._lock:
            cls._pool.append(input)

    @classmethod
    async def get_len(cls) -> int:
        """
        獲取快取池的長度。

        Returns:
            int: 快取池的長度。
        """
        return len(cls._pool)

    @classmethod
    def get(cls, length: int = 20) -> str:
        """
        從快取池中獲取指定長度的元素，並將其轉換為字串。

        Args:
            length (int, optional): 要獲取的元素長度，預設為 20。

        Returns:
            str: 快取池中指定長度的元素，以逗號分隔的字串形式返回。
        """
        with cls._lock:
            length = min(length, len(cls._pool))
            items: List[Any] = list(cls._pool)[-length:]
            # 將列表中的每個元素轉換為字串，並連接起來
            return ", ".join(map(str, items))  # 將 list 轉成字串

    @classmethod
    async def get_all(cls) -> List[Any]:
        """
        獲取快取池中的所有元素。

        Returns:
            List[Any]: 快取池中的所有元素列表。
        """
        with cls._lock:
            return list(cls._pool)

    @classmethod
    def get_target(cls) -> str:
        """
        獲取當前目標。

        Returns:
            str: 當前目標。
        """
        return cls._current_target

    @classmethod
    def get_check_list(cls) -> List[Dict[str, str]]:
        """
        獲取當前檢查清單。

        Returns:
            List[Dict[str, str]]: 當前檢查清單，格式為 [{"item": "描述", "status": "pending/completed"}]
        """
        with cls._lock:
            return cls._check_list.copy()

    @classmethod
    def set_check_list(cls, check_list: List[Dict[str, str]]) -> None:
        """
        設置檢查清單。

        Args:
            check_list (List[Dict[str, str]]): 新的檢查清單，格式為 [{"item": "描述", "status": "pending/completed"}]
        """
        with cls._lock:
            cls._check_list = check_list.copy()

    @classmethod
    def get_image_url(cls) -> str:
        """
        獲取當前圖片 URL。

        Returns:
            str: 當前圖片 URL。
        """
        url = cls._image_url
        cls._image_url = None
        return url
    
    @classmethod
    def set_image_url(cls, image_url: str) -> None:
        """
        設置當前圖片 URL。

        Args:
            image_url (str): 新的圖片 URL。
        """
        with cls._lock:
            cls._image_url = image_url