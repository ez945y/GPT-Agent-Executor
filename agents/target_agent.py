from agents.base_agent import Agent
from utils.public_cache import CachePool
from utils.llm_model import model
from utils.templates import target_prompt_template
from utils.tools import choose_tool, target_tool
from utils.locks import agent_lock
from utils.logger import Logger
import asyncio
import dotenv
import os

dotenv.load_dotenv()

class TargetAgent(Agent):
    """工具代理，根據快取池內容選擇工具"""

    async def start(self, init_target):
        """啟動工具代理"""
        await super().start(target_prompt_template, int(os.getenv("TARGET_INTERVAL")))
        if init_target is None:
            init_target = "我肚子餓了，想吃飯，要吃什麼"
        self.prompt.set_variable("current_target", init_target)
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

        if tool_info:
            tool = target_tool[tool_info["tool_name"]]["func"]
            tool_output = await tool(**tool_info['args'])
            if tool_output:
                await CachePool.add({"我決定": tool_output})
                self.prompt.set_variable("check_list", tool_output)

    def _format_tool_list(self) -> str:
        """格式化工具清單為字串"""
        tool_list_str = ""
        for tool_name, tool_info in target_tool.items():
            tool_list_str += f"- {tool_name}: {tool_info['description']} 需要參數 {tool_info['args']}\n"
        return tool_list_str