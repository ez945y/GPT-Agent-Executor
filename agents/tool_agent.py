from agents.base_agent import Agent
from utils.public_cache import CachePool
from utils.llm_model import Model
from utils.templates import decision_prompt_template
from utils.tools import choose_tool, tools
from utils.locks import agent_lock
from utils.logger import tool_logger
import asyncio

class ToolAgent(Agent):
    """工具代理，根據快取池內容選擇工具"""

    async def start(self):
        """啟動工具代理"""
        print("Tool Agent Start")
        self.set_prompt(decision_prompt_template)
        tool_list_str = self._format_tool_list()
        self.prompt.set_variable("tool_list", tool_list_str)
        await asyncio.sleep(2)
        await self.step()

    async def step(self):
        """執行工具代理步驟"""
        sequence = 1  # 初始化序列號
        while True:
            with agent_lock:
                self.prompt.set_variable("cache_pool", CachePool.get())
                think_prompt_text = self.prompt.format()
                response = Model.generate(think_prompt_text, self.model_name)
                tool_info = choose_tool(response)
                await tool_logger.log("tool", sequence, think_prompt_text) 
                await tool_logger.log("tool", sequence, response) 
                sequence += 1  # 序列號遞增
                if tool_info:
                    tool = tools[tool_info["tool_name"]]["func"]
                    args = {}
                    for arg_name in tool_info["args"]:
                        args[arg_name] = response
                    # tool_output = tool(**args)
                    # await CachePool.add({"我得知": tool_output})
            await asyncio.sleep(0.1)

    def _format_tool_list(self) -> str:
        """格式化工具清單為字串"""
        tool_list_str = ""
        for tool_name, tool_info in tools.items():
            tool_list_str += f"- {tool_name}: {tool_info['description']} 需要參數 {tool_info['args']}\n"
        return tool_list_str