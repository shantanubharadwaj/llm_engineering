from PyQt6.QtCore import QThread, pyqtSignal

class GenerationThread(QThread):
    """Thread for running model inference without blocking the UI"""
    response_ready = pyqtSignal(str)
    error_occurred = pyqtSignal(str)
    progress_update = pyqtSignal(str)
    
    def __init__(self, model, prompt, max_tokens, temperature):
        super().__init__()
        self.model = model
        self.prompt = prompt
        self.max_tokens = max_tokens
        self.temperature = temperature
        
    def run(self):
        try:
            if hasattr(self.model, 'generate_streaming'):
                # Example for a streaming-capable model
                for partial_response in self.model.generate_streaming(
                    self.prompt, 
                    max_tokens=self.max_tokens,
                    temperature=self.temperature
                ):
                    self.progress_update.emit(partial_response)
                
                # Final complete response
                final_response = self.model.get_full_response()
                self.response_ready.emit(final_response)
            else:
                response = self.model.generate(
                    self.prompt, 
                    max_tokens=self.max_tokens,
                    temperature=self.temperature
                )
                self.response_ready.emit(response)
        except Exception as e:
            self.error_occurred.emit(f"Error: {str(e)}")