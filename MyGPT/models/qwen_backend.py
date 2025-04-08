import ollama
from .base_model_interface import MockModelInterface

class QwenModel(MockModelInterface):
    def __init__(self):
        super().__init__()
        self.model_type = "Qwen 2.5"
        self.model_info = "qwen2.5:14b"
        self.client = ollama.Client()
        
    def generate(self, prompt, max_tokens=1000, temperature=0.7):
        """Generates text using Qwen model"""
        messages = [
            {"role": "system", "content": self.system_prompt},
            {"role": "user", "content":prompt}
        ]

        response = self.client.chat(
            model=self.model_info,
            messages=messages, 
            options={"temperature": temperature, "tokens": max_tokens}
            )
        return response['message']['content']