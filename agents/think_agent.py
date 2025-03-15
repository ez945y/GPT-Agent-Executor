from agents.base_agent import Agent
from utils.public_cache import CachePool
from utils.llm_model import Model
from utils.templates import think_prompt_template, personlitity_prompt_template
from utils.locks import agent_lock
import asyncio

class ThinkAgent(Agent):
    """思考代理"""

    async def start(self):
        """啟動思考代理"""
        print("Thinking Agent Start")
        with agent_lock:
            self.set_prompt(personlitity_prompt_template)
            prompt_text = self.prompt.format()
            response = Model.generate(prompt_text, self.model_name)
            # await CachePool.add({"你將扮演": prompt_text})
            # await CachePool.add({"我": response})
            self.set_prompt(think_prompt_template)
        await self.step()
        
    async def step(self):
        """執行思考代理步驟"""
        while True:
            with agent_lock:
                self.prompt.set_variable("cache_pool", CachePool.get())
                prompt_text = self.prompt.format()
                # print(prompt_text)

                response = Model.generate(prompt_text, self.model_name)
                await CachePool.add({"我": response})
            await asyncio.sleep(0.1)