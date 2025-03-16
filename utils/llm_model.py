import ollama
import google.generativeai as genai
from google.api_core.exceptions import GoogleAPIError
from abc import ABC, abstractmethod
from utils.setting import Setting

class BaseModel(ABC):
    """模型抽象類別"""

    @abstractmethod
    def generate(self, prompt, model_name):
        """生成文本的抽象方法"""
        pass

    @abstractmethod
    async def generate_async(self, prompt, model_name):
        """非同步生成文本的抽象方法"""
        pass
class OllamaModel(BaseModel):
    """Ollama 模型類別"""

    def generate(self, prompt, model_name=Setting.MODEL_NAME):
        """使用 Ollama 模型生成文本"""
        response = ollama.generate(model=model_name, prompt=prompt)
        return response['response']

    async def generate_async(self, prompt, model_name="llama3.2-1b"):
        """非同步使用 Ollama 模型生成文本（Ollama 不直接支援非同步）"""
        # Ollama 目前沒有直接支援非同步，這裡使用同步方法
        response = self.generate(prompt, model_name)
        return response
    
class GeminiModel(BaseModel):
    """Gemini 模型類別"""

    def __init__(self, api_key=None):
        """初始化 Gemini 模型，可選擇性設置 API 金鑰"""
        self.api_key = api_key or Setting.GEMINI_API_KEY
        genai.configure(api_key=self.api_key)
        # for model in genai.list_models():
        #     print(model)

    def generate(self, prompt, model_name=Setting.MODEL_NAME):
        """使用 Gemini 模型生成文本"""
        try:
            model = genai.GenerativeModel(model_name)
            response = model.generate_content(prompt)
            if response.candidates and response.candidates[0].content.parts:
                return response.candidates[0].content.parts[0].text
            else:
                return "無法生成回應"
        except GoogleAPIError as e:
            return f"API錯誤: {str(e)}"
        except Exception as e:
            return f"生成錯誤: {str(e)}"

    async def generate_async(self, prompt, model_name=Setting.MODEL_NAME):
        """非同步使用 Gemini 模型生成文本"""
        try:
            model = genai.GenerativeModel(model_name)
            import asyncio
            loop = asyncio.get_event_loop()
            response = await loop.run_in_executor(
                None, lambda: model.generate_content(prompt)
            )
            if response.candidates and response.candidates[0].content.parts:
                return response.candidates[0].content.parts[0].text
            else:
                return "無法生成回應"
        except GoogleAPIError as e:
            return f"API錯誤: {str(e)}"
        except Exception as e:
            return f"生成錯誤: {str(e)}"

class ModelFactory:
    """模型工廠類別"""

    @staticmethod
    def create_model(model_type, api_key=None):
        """根據模型類型創建模型實例"""
        if model_type.lower() == "ollama":
            return OllamaModel()
        elif model_type.lower() == "gemini":
            return GeminiModel(api_key=api_key)
        else:
            raise ValueError(f"不支持的模型類型: {model_type}")

model = ModelFactory.create_model(Setting.MODEL_TYPE)