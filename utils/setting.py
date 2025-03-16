import os
from dotenv import load_dotenv

load_dotenv()

class Setting():
    SERP_API_KEY = os.getenv("SERP_API_KEY")
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    MODEL_NAME = os.getenv("MODEL_NAME", "gemini-flash-2.0")
    MODEL_TYPE = os.getenv("MODEL_TYPE", "gemini") 
    THINK_INTERVAL= int(os.getenv("THINK_INTERVAL", 6))
    TARGET_INTERVAL= int(os.getenv("TARGET_INTERVAL", 60))
    TOOL_INTERVAL= int(os.getenv("TOOL_INTERVAL", 15))
    