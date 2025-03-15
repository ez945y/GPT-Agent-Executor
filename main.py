import agents
import asyncio

async def main():
    """主函數"""
    think_agent = agents.ThinkAgent()
    tool_agent = agents.ToolAgent()
    await asyncio.gather(
        tool_agent.start(),
        think_agent.start(),
    )

# 運行主函數
if __name__ == "__main__":
    asyncio.run(main())