from agents.base_agent import Agent
from utils.public_cache import CachePool
from utils.llm_model import model
from utils.templates import think_prompt_template, personlitity_prompt_template
from utils.locks import agent_lock
import asyncio

class ThinkAgent(Agent):
    """思考代理"""

    async def start(self, initial_task: str = None):
        """啟動思考代理"""
        await super().start()
        with agent_lock:
            self.set_prompt(personlitity_prompt_template)
            # prompt_text = self.prompt.format()
            # response = model.generate(prompt_text, self.model_name)
            # await CachePool.add({"你將扮演": prompt_text})
            
            default_task = "我肚子餓了，想吃飯，要吃什麼"
            task_to_use = initial_task if initial_task else default_task
            await CachePool.add({"我": task_to_use})
            
            self.set_prompt(think_prompt_template)
        await self.step()
        
    async def step(self):
        """執行思考代理步驟"""
        try:
            while self.running:
                with agent_lock:
                    self.prompt.set_variable("cache_pool", CachePool.get())
                    prompt_text = self.prompt.format()
                    # print(prompt_text)

                    response = model.generate(prompt_text)
                    await CachePool.add({"我": response})
                
                # 檢查是否應該停止
                if not self.running:
                    break
                    
                await asyncio.sleep(6)
        except Exception as e:
            print(f"❌ ThinkAgent 錯誤: {e}")
        finally:
            print("🛑 ThinkAgent 已停止")
            self.running = False