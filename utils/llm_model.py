import ollama

class Model:
    """模型抽象類別"""

    @classmethod
    def generate(cls, prompt, model_name="llama3.2-1b"):
        """使用模型生成文本"""
        response = ollama.generate(model=model_name, prompt=prompt)
        return response['response']