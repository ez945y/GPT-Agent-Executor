from agents.base_agent import Agent
from utils.public_cache import CachePool
from utils.llm_model import think_model as model
from utils.templates import think_prompt_template, personlitity_prompt_template
from utils.setting import Setting
import asyncio

class ThinkAgent(Agent):
    """思考代理"""

    async def start(self):
        """啟動思考代理"""
        await super().start(think_prompt_template, Setting.THINK_INTERVAL)
        # self.set_prompt(personlitity_prompt_template)
        await asyncio.sleep(2)
        await self._step()
        
    async def step(self):
        """執行思考代理步驟"""
        print("think....")
        self.prompt.set_variable("cache_pool", CachePool.get())
        prompt_text = self.prompt.format()
        
        response = model.generate(prompt_text, image_url=CachePool.get_image_url())
        await CachePool.add({"我": response})