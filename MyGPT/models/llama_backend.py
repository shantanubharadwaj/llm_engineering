import ollama

from .base_model_interface import MockModelInterface

class LlamaModel(MockModelInterface):
    def __init__(self):
        super().__init__()
        self.model_type = "Llama 3.1"
        self.model_info = "llama3.1:8b"
        # In a real implementation, you would load the model here
        # Example: self.model = llama_cpp.Llama(model_path="models/llama-7b.gguf")
        self.client = ollama.Client()
        # self.model = ollama.chat(model=self.model_info)
        
    def generate(self, prompt, max_tokens=1000, temperature=0.7):
        """Generates text using Llama model"""
        # In a real implementation:
        # response = self.model.generate(prompt, max_tokens=max_tokens, temperature=temperature)
        # return response
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
    
    def generate_full(self, prompt, max_tokens=1000, temperature=0.7):
        """Generates complete text without streaming"""
        messages = [
            {"role": "system", "content": self.system_prompt},
            {"role": "user", "content": prompt}
        ]
        
        response = self.client.chat(
            model=self.model_info, 
            messages=messages, 
            options={"temperature": temperature, "num_predict": max_tokens}
        )
        
        return response['message']['content']