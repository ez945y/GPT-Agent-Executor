import agents
import asyncio
import threading
from server.app import run_fastapi_server  # 導入 FastAPI 伺服器函數

async def main():
    """主函數"""
    print("start")
    think_agent = agents.ThinkAgent()
    tool_agent = agents.ToolAgent()
    target_agent = agents.TargetAgent()
    await asyncio.gather(
        tool_agent.start(),
        think_agent.start(),
        target_agent.start(),
    )

# 運行主函數
if __name__ == "__main__":
    server_thread = threading.Thread(target=run_fastapi_server)
    server_thread.start()
    # run_fastapi_server()
    asyncio.run(main())