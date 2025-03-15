import os
from dotenv import load_dotenv
from typing import List, Dict, Callable, Any
from serpapi import GoogleSearch
import re
import json

load_dotenv()
serp_api_key = os.getenv("SERP_API_KEY")

# 假設你已經安裝了 google-search-results 函式庫
def web_search(query: str) -> str:
    """使用 Google 搜尋指定查詢"""
    try:
        if query and query != "":
            search = GoogleSearch({"q": query, "api_key": serp_api_key})
            results = search.get_dict()["organic_results"]
            if results and len(results) > 0:
                first_result = results[0]
                title = first_result.get("title", "無標題")
                snippet = first_result.get("snippet", "無摘要")
                # link = first_result.get("link", "#")
                result = f"標題：{title}\n摘要：{snippet}"
                print(f"搜尋了:{query}\n{result}")
                return result
            else:
                return "找不到相關結果。"
    except Exception as e:
        return None
        # return f"搜尋失敗：{e}"

def express_as_sentence(sentence: str) -> str:
    """將一連串的想法轉化為一句話。"""
    if sentence and sentence != "":
        print(f"AI:{sentence}")
        return f"I say:{sentence}"
    return None
 
def observe_thought(target: str) -> str:
    """觀察自己的念頭，設定目標。"""
    if target and target != "":
        print(f"AI設定目標：{target}")
        return target
    return "想一下要做什麼。"

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

}

target_tool: Dict[str, Dict[str, Any]] = {
    "設定目標": {
        "func": observe_thought,
        "args": "target:string",
        "description": "觀察自己的念頭，決定是否要修改或設定目標。"
    },
}

def parse_args(json_string: str) -> dict:
    try:
        # 移除標記
        json_string = json_string.replace("`json", "").replace("`", "").strip()
        data = json.loads(json_string)
        return data.get("args", {})
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
        
        elif re.search(r"設定目標|設定|目標", model_output, re.IGNORECASE):
            # print(output_json.get("sentence"))
            return {"tool_name": "設定目標", "args": {"target": output_json.get("target")}}
        # 添加其他工具的選擇邏輯...
        return None
    except ValueError:
            return None