from agents.base_agent import Agent
from utils.public_cache import CachePool
from utils.llm_model import model
from utils.templates import decision_prompt_template
from utils.tools import choose_tool, tools
from utils.logger import Logger
import asyncio
import dotenv
import os

dotenv.load_dotenv()


class ToolAgent(Agent):
    """工具代理，根據快取池內容選擇工具"""

    async def start(self, init_target):
        """啟動工具代理"""
        await super().start(decision_prompt_template, int(os.getenv("TOOL_INTERVAL")))

        if init_target is None:
            init_target = "我肚子餓了，想吃飯，要吃什麼"
        self.prompt.set_variable("current_target", init_target)

        tool_list_str = self._format_tool_list()
        self.prompt.set_variable("tool_list", tool_list_str)
        await asyncio.sleep(self.sleep_time)
        await self._step()

    async def step(self):
        """執行工具代理步驟"""
        self.prompt.set_variable("cache_pool", CachePool.get())
        self.prompt.set_variable("check_list", CachePool.get_check_list())
        think_prompt_text = self.prompt.format()
        response = model.generate(think_prompt_text)
        tool_info = choose_tool(response)

        await Logger.log("tool", self.sequence, think_prompt_text) 
        await Logger.log("tool", self.sequence, response) 
        
        self.sequence += 1  # 序列號遞增
        if tool_info:
            tool = tools[tool_info["tool_name"]]["func"]
            tool_output = await tool(**tool_info['args'])
            if tool_output:
                await CachePool.add({"我得知": tool_output})


    def _format_tool_list(self) -> str:
        """格式化工具清單為字串"""
        tool_list_str = ""
        for tool_name, tool_info in tools.items():
            tool_list_str += f"- {tool_name}: {tool_info['description']} 需要參數 {tool_info['args']}\n"
        return tool_list_str