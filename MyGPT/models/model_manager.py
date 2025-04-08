from .llama_backend import LlamaModel
from .qwen_backend import QwenModel
from .openai_api import OpenAIAPI


class ModelManager:
    """Manages different model backends"""
    def __init__(self):
        self.models = {
            "Llama 3.1": LlamaModel(),
            "Qwen 2.5": QwenModel(),
            "OpenAI (API)": OpenAIAPI()
        }
        self.current_model = "Llama 3.1"
        
    def get_model_list(self):
        return list(self.models.keys())
    
    def set_current_model(self, model_name):
        if model_name in self.models:
            self.current_model = model_name
            return True
        return False
    
    def get_current_model(self):
        return self.models[self.current_model]
    
    def set_api_key(self, model_name, api_key):
        if model_name in self.models and hasattr(self.models[model_name], "set_api_key"):
            self.models[model_name].set_api_key(api_key)
            return True
        return False
