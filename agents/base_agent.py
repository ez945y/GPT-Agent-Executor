from typing import List, Optional
from utils.prompts import Prompt
from utils.setting import Setting
import asyncio
from utils.locks import agent_lock

class Agent:
    """
    代理抽象類別

    此類別定義了代理的基本結構和行為，包括設定模型、提示、啟動和執行步驟。
    """

    def __init__(self):
        """
        初始化代理

        設定模型名稱、提示和歷史記錄。
        """
        self.prompt: Optional[Prompt] = None  # 提示物件
        self.history: List[dict] = []  # 歷史記錄（快取池）
        self.running: bool = False  # 運行狀態
        self.sleep_time: int = 0  # 睡眠時間
        self.sequence: int = 0  # 序列號

    def set_prompt(self, template: str):
        """
        設定提示

        Args:
            template (str): 提示模板。
        """
        self.prompt = Prompt(template)

    def set_sleep_time(self, sleep_time: int):
        """
        設定睡眠時間
        """
        self.sleep_time = sleep_time

    def stop(self):
        """
        停止代理

        設置停止標誌，讓代理在下一次循環時退出。
        """
        self.running = False

    async def start(self, prompt: str = None, sleep_time: int = None):
        """
        啟動代理

        此方法在代理啟動時被呼叫，用於執行初始化操作。
        """
        self.running = True
        if prompt:
            self.set_prompt(prompt)
        if sleep_time:
            self.set_sleep_time(sleep_time)
        pass

    async def step(self):
        """
        執行代理步驟

        此方法用於執行代理的單一步驟。
        """
        pass

    async def _step(self):
        """執行工具代理步驟"""
        try:
            while self.running:
                with agent_lock:
                    try:
                        await self.step()
                    except Exception as e:
                        print(f"{self.__class__.__name__} 錯誤: {e}")
                if not self.running:
                    break
                await asyncio.sleep(self.sleep_time)
        except Exception as e:
            print(f"{self.__class__.__name__} 錯誤: {e}")
        finally:
            print(f"{self.__class__.__name__} 已停止")
            self.running = False