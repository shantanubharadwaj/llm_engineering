from openai import OpenAI
import os
from .base_model_interface import MockModelInterface

class OpenAIAPI(MockModelInterface):
    def __init__(self):
        super().__init__()
        self.model_type = "OpenAI (API)"
        self.model_info = "gpt-4o-mini"
        self.openai = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        
    # def set_api_key(self, key):
    #     self.api_key = key
        
    def generate(self, prompt, max_tokens=1000, temperature=0.7):
        """Generates text using OpenAI API"""
        messages = [
            {"role": "system", "content": self.system_prompt},
            {"role": "user", "content":prompt}
        ]
        
        response = self.openai.chat.completions.create(
            model=self.model_info,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens
            )
        return response.choices[0].message.content