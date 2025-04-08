import time

class MockModelInterface:
    def __init__(self):
        self.model_type = "base"
        self.system_prompt = """You are a helpful technical tutor who answers questions about all kinds of code, 
        software engineering, data science, logic, aptitude, mathematics and LLMs. 
        Your response should be very descriptive and detailed and should expect audience to not know anything about the topic.
        Your response should also include code snippet wherever applicable in python language by default unless any other language that the user prefers.
        Unless otherwise specified by the user to be brief in your response."""

        
    def generate(self, prompt, max_tokens=100, temperature=0.7):
        """Mock generation - replace with actual model calls"""
        time.sleep(1)  # Simulate processing time
        return f"This is a response from the {self.model_type} model to: {prompt}"