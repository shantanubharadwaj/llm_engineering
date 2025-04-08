import os
import json
from datetime import datetime
from PyQt6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QMessageBox, QFileDialog

from models.model_manager import ModelManager
from .chat_widget import ChatWidget
from .settings import APIKeyDialog

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.model_manager = ModelManager()
        self.setup_ui()
        # self.config_file = os.path.join(os.path.expanduser("~"), ".key_config.json")
        # print(self.config_file)
        # self.load_config()
        
    def setup_ui(self):
        self.setWindowTitle("MyGPT")
        self.setMinimumSize(800, 600)
        
        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main layout
        layout = QVBoxLayout(central_widget)
        
        # Chat widget
        self.chat_widget = ChatWidget(self.model_manager)
        layout.addWidget(self.chat_widget)
        
        # Create menu bar
        self.create_menu_bar()
        
    def create_menu_bar(self):
        menu_bar = self.menuBar()
        
        # File menu
        file_menu = menu_bar.addMenu("&File")
        
        # Save conversation
        save_action = file_menu.addAction("&Save Conversation")
        save_action.triggered.connect(self.save_conversation)
        
        # Load conversation
        load_action = file_menu.addAction("&Load Conversation")
        load_action.triggered.connect(self.load_conversation)
        
        file_menu.addSeparator()
        
        # Exit
        exit_action = file_menu.addAction("E&xit")
        exit_action.triggered.connect(self.close)
        
        # # Settings menu
        # settings_menu = menu_bar.addMenu("&Settings")
        
    #     # API Keys
    #     api_keys_action = settings_menu.addAction("Configure &API Keys")
    #     api_keys_action.triggered.connect(self.configure_api_keys)
        
    # def configure_api_keys(self):
    #     dialog = APIKeyDialog(self.model_manager, self)
    #     dialog.exec()
    #     self.save_config()
        
    def save_conversation(self):
        """Save the current conversation to a file"""
        if not self.chat_widget.conversation:
            QMessageBox.information(self, "No Conversation", "There is no conversation to save.")
            return
            
        # Get file path
        file_path, _ = QFileDialog.getSaveFileName(
            self, "Save Conversation", "", "JSON Files (*.json);;All Files (*)"
        )
        
        if not file_path:
            return
            
        if not file_path.endswith(".json"):
            file_path += ".json"
            
        save_data = {
            "timestamp": datetime.now().isoformat(),
            "messages": self.chat_widget.conversation
        }
        
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(save_data, f, indent=2)
                
            QMessageBox.information(self, "Success", "Conversation saved successfully.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to save conversation: {str(e)}")
            
    def load_conversation(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Load Conversation", "", "JSON Files (*.json);;All Files (*)"
        )
        
        if not file_path:
            return
            
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                
            self.chat_widget.clear_chat()
            
            if "messages" in data:
                for message in data["messages"]:
                    if "role" in message and "content" in message:
                        is_user = message["role"] == "user"
                        self.chat_widget.add_message(message["content"], is_user=is_user)
                        
            QMessageBox.information(self, "Success", "Conversation loaded successfully.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load conversation: {str(e)}")
            
    def save_config(self):
        config = {
            "api_keys": {}
        }
        
        claude_model = self.model_manager.models["Claude (API)"]
        if hasattr(claude_model, "api_key") and claude_model.api_key:
            config["api_keys"]["claude"] = claude_model.api_key
            
        openai_model = self.model_manager.models["OpenAI (API)"]
        if hasattr(openai_model, "api_key") and openai_model.api_key:
            config["api_keys"]["openai"] = openai_model.api_key
            
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(config, f)
        except Exception as e:
            print(f"Failed to save config: {str(e)}")
            
    def load_config(self):
        os.environ['OPENAI_API_KEY'] = os.getenv('OPENAI_API_KEY')
        # if not os.path.exists(self.config_file):
        #     return
            
        # try:
        #     with open(self.config_file, 'r', encoding='utf-8') as f:
        #         config = json.load(f)
                
        #     # Load API keys
        #     if "api_keys" in config:
        #         if "claude" in config["api_keys"]:
        #             self.model_manager.set_api_key("Claude (API)", config["api_keys"]["claude"])
        #         if "openai" in config["api_keys"]:
        #             self.model_manager.set_api_key("OpenAI (API)", config["api_keys"]["openai"])
        # except Exception as e:
        #     print(f"Failed to load config: {str(e)}")
            
    def closeEvent(self, event):
        # self.save_config()
        super().closeEvent(event)