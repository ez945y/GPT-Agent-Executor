import os
from dotenv import load_dotenv
from typing import List, Dict, Callable, Any
from serpapi import GoogleSearch
import re

load_dotenv()
serp_api_key = os.getenv("SERP_API_KEY")

# 假設你已經安裝了 google-search-results 函式庫
def web_search(query: str) -> str:
    """使用 Google 搜尋指定查詢"""
    try:
        search = GoogleSearch({"q": query, "api_key": serp_api_key})
        results = search.get_dict()["organic_results"]
        if results and len(results) > 0:
            first_result = results[0]
            title = first_result.get("title", "無標題")
            snippet = first_result.get("snippet", "無摘要")
            # link = first_result.get("link", "#")
            return f"標題：{title}\n摘要：{snippet}"
        else:
            return "找不到相關結果。"
    except Exception as e:
        return f"搜尋失敗：{e}"
    
# 工具清單
tools: Dict[str, Dict[str, Any]] = {
    "網路搜尋": {
        "func": web_search,
        "args": ["query"],
        "description": "使用 Google 搜尋指定查詢。"
    },
}

def choose_tool(model_output: str) -> Dict[str, Any]:
    """根據模型輸出選擇工具並返回工具資訊"""
    if re.search(r"網路搜尋|google搜尋|搜尋網路", model_output, re.IGNORECASE): #更靈活的選擇方式
        #使用正則表達式提取搜尋查詢
        match = re.search(r"搜尋：(.*)", model_output)
        if match:
            query = match.group(1).strip()
            return {"tool_name": "網路搜尋", "args": {"query": query}}
        else:
            return {"tool_name": "網路搜尋", "args": {"query": "預設搜尋詞"}} #預設搜尋詞
    # 添加其他工具的選擇邏輯...
    return None