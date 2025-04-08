from PyQt6.QtWidgets import (
    QVBoxLayout, QFormLayout, QLineEdit, QPushButton, QDialog
)

class APIKeyDialog(QDialog):
    """Dialog for setting API keys"""
    def __init__(self, model_manager, parent=None):
        super().__init__(parent)
        self.model_manager = model_manager
        self.setWindowTitle("Configure API Keys")
        self.setup_ui()
        
    def setup_ui(self):
        layout = QVBoxLayout(self)
        
        form_layout = QFormLayout()
        
        # Claude API Key
        self.claude_key = QLineEdit()
        self.claude_key.setEchoMode(QLineEdit.EchoMode.Password)
        form_layout.addRow("Claude API Key:", self.claude_key)
        
        # OpenAI API Key
        self.openai_key = QLineEdit()
        self.openai_key.setEchoMode(QLineEdit.EchoMode.Password)
        form_layout.addRow("OpenAI API Key:", self.openai_key)
        
        layout.addLayout(form_layout)
        
        # Save button
        self.save_button = QPushButton("Save")
        self.save_button.clicked.connect(self.save_keys)
        layout.addWidget(self.save_button)
        
    def save_keys(self):
        # Set API keys in the model manager
        claude_key = self.claude_key.text().strip()
        if claude_key:
            self.model_manager.set_api_key("Claude (API)", claude_key)
            
        openai_key = self.openai_key.text().strip()
        if openai_key:
            self.model_manager.set_api_key("OpenAI (API)", openai_key)
            
        self.accept()