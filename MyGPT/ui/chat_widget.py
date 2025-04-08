from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QScrollArea, QHBoxLayout, 
    QLabel, QComboBox, QTextEdit, QSlider, QSpinBox,
    QPushButton, QApplication, QFrame
    )
from PyQt6.QtCore import Qt

from utils.threading import GenerationThread
from .typing_indicator import TypingIndicatorWidget
from .markdown_message import MarkdownMessageWidget


class MessageWidget(QWidget):
    """Widget for displaying a single message in the chat"""
    def __init__(self, text, is_user=False, parent=None):
        super().__init__(parent)
        
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(10, 5, 10, 5)
        
        # Create frame with different styles for user vs assistant
        self.frame = QFrame()
        frame_layout = QVBoxLayout(self.frame)
        
        # Role indicator (User or Assistant)
        role_label = QLabel("You:" if is_user else "Assistant:")
        role_label.setStyleSheet("font-weight: bold;")
        frame_layout.addWidget(role_label)
        
        # Message content
        self.message = QLabel(text)
        self.message.setWordWrap(True)
        self.message.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
        frame_layout.addWidget(self.message)
        
        # Set different styles for user vs assistant messages
        if is_user:
            self.frame.setStyleSheet(
                "background-color: #E1F5FE; border-radius: 10px; padding: 10px;"
            )
            self.layout.setAlignment(Qt.AlignmentFlag.AlignRight)
        else:
            self.frame.setStyleSheet(
                "background-color: #F5F5F5; border-radius: 10px; padding: 10px;"
            )
            self.layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        
        self.layout.addWidget(self.frame)
        

class ChatWidget(QWidget):
    """Widget for displaying the chat interface"""
    def __init__(self, model_manager, parent=None):
        super().__init__(parent)
        self.model_manager = model_manager
        self.conversation = []  # Store conversation history
        self.typing_indicator = None
        self.setup_ui()
        
    def setup_ui(self):
        layout = QVBoxLayout(self)
        
        # Chat display area with scroll
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.scroll_content = QWidget()
        self.chat_layout = QVBoxLayout(self.scroll_content)
        self.chat_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.chat_layout.setSpacing(10)
        self.scroll_area.setWidget(self.scroll_content)
        
        # Input area
        input_layout = QVBoxLayout()
        
        # Model selection
        model_layout = QHBoxLayout()
        model_layout.addWidget(QLabel("Model:"))
        self.model_selector = QComboBox()
        self.model_selector.addItems(self.model_manager.get_model_list())
        model_layout.addWidget(self.model_selector)
        input_layout.addLayout(model_layout)
        
        # Text input
        self.input_text = QTextEdit()
        self.input_text.setPlaceholderText("Type your message here...")
        self.input_text.setMinimumHeight(100)
        self.input_text.setMaximumHeight(200)
        input_layout.addWidget(self.input_text)
        
        # Settings area
        settings_layout = QHBoxLayout()
        
        # Temperature setting
        temp_layout = QHBoxLayout()
        temp_layout.addWidget(QLabel("Temperature:"))
        self.temperature_slider = QSlider(Qt.Orientation.Horizontal)
        self.temperature_slider.setRange(0, 100)
        self.temperature_slider.setValue(70)  # Default temperature 0.7
        self.temperature_slider.setMaximumWidth(150)
        temp_layout.addWidget(self.temperature_slider)
        self.temperature_value = QLabel("0.7")
        temp_layout.addWidget(self.temperature_value)
        settings_layout.addLayout(temp_layout)
        
        # Max tokens setting
        tokens_layout = QHBoxLayout()
        tokens_layout.addWidget(QLabel("Max Tokens:"))
        self.max_tokens_spin = QSpinBox()
        self.max_tokens_spin.setRange(10, 4000)
        self.max_tokens_spin.setValue(1000)
        self.max_tokens_spin.setSingleStep(100)
        tokens_layout.addWidget(self.max_tokens_spin)
        settings_layout.addLayout(tokens_layout)
        
        # Add settings layout to input layout
        input_layout.addLayout(settings_layout)
        
        # Button layout
        button_layout = QHBoxLayout()
        
        # Clear button
        self.clear_button = QPushButton("Clear Chat")
        button_layout.addWidget(self.clear_button)
        
        # Send button
        self.send_button = QPushButton("Send")
        self.send_button.setDefault(True)
        button_layout.addWidget(self.send_button)
        
        # Add button layout to input layout
        input_layout.addLayout(button_layout)
        
        # Add all components to main layout
        layout.addWidget(self.scroll_area, 3)
        layout.addLayout(input_layout, 1)
        
        # Connect signals
        self.send_button.clicked.connect(self.send_message)
        self.input_text.textChanged.connect(self.adjust_input_height)
        self.clear_button.clicked.connect(self.clear_chat)
        self.temperature_slider.valueChanged.connect(self.update_temperature_label)
        self.model_selector.currentTextChanged.connect(self.change_model)
        
        # Welcome message
        self.add_message("Welcome to MyGPT! Select a model and start chatting.", is_user=False)
        
    def update_temperature_label(self, value):
        self.temperature_value.setText(f"{value/100:.1f}")
        
    def change_model(self, model_name):
        self.model_manager.set_current_model(model_name)
        self.add_message(f"Switched to {model_name} model.", is_user=False)
        
    def adjust_input_height(self):
        # Adjust input box height based on content
        document_height = self.input_text.document().size().height()
        if document_height < 100:
            self.input_text.setFixedHeight(100)
        elif document_height > 200:
            self.input_text.setFixedHeight(200)
        else:
            self.input_text.setFixedHeight(int(document_height) + 20)
            
    def add_message(self, text, is_user=True):
        message_widget = MarkdownMessageWidget(text, is_user)
        self.chat_layout.addWidget(message_widget)
        # Save to conversation history
        role = "user" if is_user else "assistant"
        self.conversation.append({"role": role, "content": text})
        # Scroll to bottom
        QApplication.processEvents()  # Force update
        scrollbar = self.scroll_area.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())
        
    def send_message(self):
        # Get message text
        message = self.input_text.toPlainText().strip()
        if not message:
            return
            
        # Display user message
        self.add_message(message, is_user=True)
        self.input_text.clear()
        
        # Get current model settings
        model = self.model_manager.get_current_model()
        max_tokens = self.max_tokens_spin.value()
        temperature = self.temperature_slider.value() / 100.0
        
        self.typing_indicator = TypingIndicatorWidget(model.model_type)
        self.chat_layout.addWidget(self.typing_indicator)
        
        # Scroll to the typing indicator
        QApplication.processEvents()
        scrollbar = self.scroll_area.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())
        
        # Disable UI while generating
        self.send_button.setEnabled(False)
        self.send_button.setText("Generating...")
        
        # Create and start generation thread
        self.generation_thread = GenerationThread(model, message, max_tokens, temperature)
        self.generation_thread.response_ready.connect(self.handle_response)
        self.generation_thread.error_occurred.connect(self.handle_error)
        self.generation_thread.finished.connect(self.generation_finished)
        self.generation_thread.start()
        
    def handle_response(self, response):
        if hasattr(self, 'typing_indicator') and self.typing_indicator is not None:
            self.typing_indicator.deleteLater()
            self.typing_indicator = None
        self.add_message(response, is_user=False)
        
    def handle_error(self, error_message):
        if hasattr(self, 'typing_indicator') and self.typing_indicator is not None:
            self.typing_indicator.deleteLater()
            self.typing_indicator = None
        self.add_message(f"Error: {error_message}", is_user=False)
        
    def generation_finished(self):
        # Re-enable UI
        self.send_button.setEnabled(True)
        self.send_button.setText("Send")
        if hasattr(self, 'typing_indicator') and self.typing_indicator is not None:
            self.typing_indicator.deleteLater()
            self.typing_indicator = None
        
    def clear_chat(self):
        # Clear UI
        while self.chat_layout.count():
            item = self.chat_layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()
        
        # Clear conversation history
        self.conversation = []
        
        # Add welcome message again
        self.add_message("Chat cleared. Ready for new conversation!", is_user=False)