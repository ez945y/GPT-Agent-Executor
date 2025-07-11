from typing import List, Dict, Callable, Any
from serpapi import GoogleSearch
from utils.setting import Setting
import re
import json
from utils.logger import Logger
from utils.public_cache import CachePool

# 假設你已經安裝了 google-search-results 函式庫
async def web_search(query: str) -> str:
    """使用 Google 搜尋指定查詢"""
    try:
        if query and query != "":
            search = GoogleSearch({"q": query, "api_key": Setting.SERP_API_KEY})
            results = search.get_dict()["organic_results"]
            if results and len(results) > 0:
                first_result = results[0]
                title = first_result.get("title", "無標題")
                snippet = first_result.get("snippet", "無摘要")
                # link = first_result.get("link", "#")
                result = f"標題： {title}\n摘要：{snippet}"
                await Logger.log("chat", await CachePool.get_len() + 1, f"搜尋了: {query}\n{result}")
                return result
            else:
                return "找不到相關結果。"
    except Exception as e:
        return None
        # return f"搜尋失敗：{e}"

async def express_as_sentence(sentence: str) -> str:
    """將一連串的想法轉化為一句話。"""
    if sentence and sentence != "":
        await Logger.log("chat", await CachePool.get_len() + 1, f"AI: {sentence}")
        return f"I say: {sentence}"
    return None
 
async def observe_thought(check_list: str) -> str:
    """觀察自己的念頭，設定目標清單。"""
    if check_list and check_list != "":
        await Logger.log("chat", await CachePool.get_len() + 1, f"AI設定了目標: {check_list}")
        return check_list
    return "想一下要做什麼。"

async def summarize(result: str) -> str:
    """摘要指定內容。"""
    if result and result != "":
        await Logger.log("chat", await CachePool.get_len() + 1, f"總結來說: {result}")
        return result
    return "摘要失敗。"

# 工具清單
tools: Dict[str, Dict[str, Any]] = {
    "自然表達": {
    "func": express_as_sentence,
    "args": "sentence:string",
    "description": "根據想法或概念，像人類一樣說出一句話。"
    },
    "網路搜尋": {
        "func": web_search,
        "args": "query:string",
        "description": "使用 Google 搜尋指定一個查詢。"
    },
    "摘要": {
        "func": summarize,
        "args": "result:string",
        "description": "摘要指定內容。"
    },
}

target_tool: Dict[str, Dict[str, Any]] = {
    "更新檢查清單": {
        "func": observe_thought,
        "args": "check_list:string",
        "description": "觀察自己的念頭，決定是否要修改或設定目標清單。"
    },
}

def parse_args(json_string: str) -> dict:
    try:
        # 移除標記
        json_string = json_string.replace("`json", "").replace("`", "").strip()
        data = json.loads(json_string)
        return data.get("args", {})
    except AttributeError:
        return None
    except ValueError:
        return {}

    

def choose_tool(model_output: str) -> Dict[str, Any]:
    """根據模型輸出選擇工具並返回工具資訊"""
    try:
        output_json = parse_args(model_output)
        if not output_json:
            return None
        if re.search(r"網路搜尋|搜尋|網路", model_output, re.IGNORECASE): #更靈活的選擇方式
            return {"tool_name": "網路搜尋", "args": {"query": output_json.get("query")}}
            
        elif re.search(r"自然表達|表達", model_output, re.IGNORECASE):
            # print(output_json.get("sentence"))
            return {"tool_name": "自然表達", "args": {"sentence": output_json.get("sentence")}}
        
        elif re.search(r"更新檢查清單|更新|檢查清單", model_output, re.IGNORECASE):
            # print(output_json.get("sentence"))
            return {"tool_name": "更新檢查清單", "args": {"check_list": output_json.get("check_list")}}
        elif re.search(r"摘要|summarize", model_output, re.IGNORECASE):
            return {"tool_name": "摘要", "args": {"result": output_json.get("result")}}
        return None
    except ValueError:
            return None