from typing import List, Optional
from utils.prompts import Prompt
from utils.setting import Setting

class Agent:
    """
    代理抽象類別

    此類別定義了代理的基本結構和行為，包括設定模型、提示、啟動和執行步驟。
    """

    def __init__(self, model_name: str = Setting.MODEL_NAME):
        """
        初始化代理

        設定模型名稱、提示和歷史記錄。
        """
        self.model_name: Optional[str] = model_name  # 模型名稱
        self.prompt: Optional[Prompt] = None  # 提示物件
        self.history: List[dict] = []  # 歷史記錄（快取池）

    def set_model(self, model_name: str):
        """
        設定模型

        Args:
            model_name (str): 模型名稱。
        """
        self.model_name = model_name

    def set_prompt(self, template: str):
        """
        設定提示

        Args:
            template (str): 提示模板。
        """
        self.prompt = Prompt(template)

    async def start(self):
        """
        啟動代理

        此方法在代理啟動時被呼叫，用於執行初始化操作。
        """
        pass

    async def step(self):
        """
        執行代理步驟

        此方法用於執行代理的單一步驟。
        """
        pass