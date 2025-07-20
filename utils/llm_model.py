import ollama
import google.generativeai as genai
from google.api_core.exceptions import GoogleAPIError
from abc import ABC, abstractmethod
from utils.setting import Setting
import requests
import openai

class BaseModel(ABC):
    """模型抽象類別"""
    _model_name = None

    @abstractmethod
    def generate(self, prompt, model_name, image_url=None):
        """生成文本的抽象方法"""
        pass

    @abstractmethod
    async def generate_async(self, prompt, model_name, image_url=None):
        """非同步生成文本的抽象方法"""
        pass

class OpenAIModel(BaseModel):
    """OpenAI 模型類別"""
    def __init__(self, model_name, api_base=None):
        self._model_name = model_name
        self.client = openai.OpenAI(
            api_key=Setting.OPENAI_API_KEY,
            base_url=api_base
        )

    def generate(self, prompt, image_url=None):
        messages = [{"role": "user", "content": []}]
        messages[0]["content"].append({"type": "text", "text": prompt})

        if image_url and Setting.SUPPORT_IMAGE != "false":
            messages[0]["content"].append({"type": "image_url", "image_url": {"url": image_url}})
        
        try:
            response = self.client.chat.completions.create(
                model=self._model_name,
                messages=messages,
                max_tokens=1024,
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"OpenAI API error: {e}"

    async def generate_async(self, prompt, image_url=None):
        # For simplicity, using the synchronous method here.
        # A full async implementation would use an async OpenAI client.
        return self.generate(prompt, image_url)


class OllamaModel(BaseModel):
    """Ollama 模型類別"""
    def __init__(self, model_name): 
        self._model_name = model_name

    def generate(self, prompt, image_url=None):
        if not image_url or Setting.SUPPORT_IMAGE == "false":
            response = ollama.generate(model=self._model_name, prompt=prompt)
            return response['response']
        else:
            try:
                response = requests.get(image_url)
                response.raise_for_status()  # Raise an exception for bad status codes
                image_bytes = response.content
                response = ollama.generate(model=self._model_name, prompt=prompt, images=[image_bytes])
                return response['response']
            except Exception as e:
                print(f"Error downloading image: {e}")
                response = ollama.generate(model=self._model_name, prompt=prompt)
                return response['response']

    async def generate_async(self, prompt, image_url=None):
        """非同步使用 Ollama 模型生成文本（Ollama 不直接支援非同步）"""
        # Ollama 目前沒有直接支援非同步，這裡使用同步方法
        response = self.generate(prompt, self._model_name)
        return response
    
class GeminiModel(BaseModel):
    """Gemini 模型類別"""

    def __init__(self, model_name):
        """初始化 Gemini 模型，可選擇性設置 API 金鑰"""
        self._model_name = model_name
        self.api_key = Setting.GEMINI_API_KEY
        genai.configure(api_key=self.api_key)
        # for model in genai.list_models():
        #     print(model)

    def generate(self, prompt, image_url=None):
        """使用 Gemini 模型生成文本"""
        try:
            model = genai.GenerativeModel(self._model_name)
            response = model.generate_content(prompt)
            if response.candidates and response.candidates[0].content.parts:
                return response.candidates[0].content.parts[0].text
            else:
                return "無法生成回應"
        except GoogleAPIError as e:
            return f"API錯誤: {str(e)}"
        except Exception as e:
            return f"生成錯誤: {str(e)}"

    async def generate_async(self, prompt, image_url=None):
        """非同步使用 Gemini 模型生成文本"""
        try:
            model = genai.GenerativeModel(self._model_name)
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
    def create_model(model_type, model_name):
        """根據模型類型創建模型實例"""
        if model_type.lower() == "ollama":
            return OllamaModel(model_name)
        elif model_type.lower() == "gemini":
            return GeminiModel(model_name)
        elif model_type.lower().startswith("openai"):
            parts = model_type.split('@', 1)
            api_base = parts[1] if len(parts) > 1 else None
            return OpenAIModel(model_name, api_base=api_base)
        else:
            raise ValueError(f"不支持的模型類型: {model_type}")

think_model = ModelFactory.create_model(Setting.THINK_MODEL_TYPE, Setting.THINK_MODEL_NAME)
target_model = ModelFactory.create_model(Setting.TARGET_MODEL_TYPE, Setting.TARGET_MODEL_NAME)
tool_model = ModelFactory.create_model(Setting.TOOL_MODEL_TYPE, Setting.TOOL_MODEL_NAME)