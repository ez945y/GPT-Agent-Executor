import os
from dotenv import load_dotenv

load_dotenv()

class Setting():
    SERP_API_KEY = os.getenv("SERP_API_KEY")
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    THINK_MODEL_NAME = os.getenv("THINK_MODEL_NAME", "gemini-flash-2.0")
    THINK_MODEL_TYPE = os.getenv("THINK_MODEL_TYPE", "gemini") 
    SUPPORT_IMAGE = os.getenv("SUPPORT_IMAGE", "false")
    TARGET_MODEL_NAME = os.getenv("TARGET_MODEL_NAME", "gemini-flash-2.0")
    TARGET_MODEL_TYPE = os.getenv("TARGET_MODEL_TYPE", "gemini") 
    TOOL_MODEL_NAME = os.getenv("TOOL_MODEL_NAME", "gemini-flash-2.0")
    TOOL_MODEL_TYPE = os.getenv("TOOL_MODEL_TYPE", "gemini") 
    THINK_INTERVAL= int(os.getenv("THINK_INTERVAL", 6))
    TARGET_INTERVAL= int(os.getenv("TARGET_INTERVAL", 60))
    TOOL_INTERVAL= int(os.getenv("TOOL_INTERVAL", 15))
    