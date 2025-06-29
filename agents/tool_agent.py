from agents.base_agent import Agent
from utils.public_cache import CachePool
from utils.llm_model import model
from utils.templates import decision_prompt_template
from utils.tools import choose_tool, tools
from utils.locks import agent_lock
from utils.logger import Logger
import asyncio

class ToolAgent(Agent):
    """工具代理，根據快取池內容選擇工具"""

    async def start(self):
        """啟動工具代理"""
        await super().start()
        self.set_prompt(decision_prompt_template)

        tool_list_str = self._format_tool_list()
        self.prompt.set_variable("tool_list", tool_list_str)
        await asyncio.sleep(4)
        await self.step()

    async def step(self):
        """執行工具代理步驟"""
        sequence = 1  # 初始化序列號
        try:
            while self.running:
                with agent_lock:
                    self.prompt.set_variable("cache_pool", CachePool.get())
                    self.prompt.set_variable("current_target", CachePool.get_target())
                    think_prompt_text = self.prompt.format()
                    response = model.generate(think_prompt_text)
                    tool_info = choose_tool(response)

                    await Logger.log("tool", sequence, think_prompt_text) 
                    await Logger.log("tool", sequence, response) 
                    
                    sequence += 1  # 序列號遞增
                    if tool_info:
                        tool = tools[tool_info["tool_name"]]["func"]
                        tool_output = await tool(**tool_info['args'])
                        if tool_output:
                            await CachePool.add({"我得知": tool_output})
                
                # 檢查是否應該停止
                if not self.running:
                    break
                    
                await asyncio.sleep(15)
        except Exception as e:
            print(f"❌ ToolAgent 錯誤: {e}")
        finally:
            print("🛑 ToolAgent 已停止")
            self.running = False

    def _format_tool_list(self) -> str:
        """格式化工具清單為字串"""
        tool_list_str = ""
        for tool_name, tool_info in tools.items():
            tool_list_str += f"- {tool_name}: {tool_info['description']} 需要參數 {tool_info['args']}\n"
        return tool_list_str