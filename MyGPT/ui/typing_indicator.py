from PyQt6.QtCore import QTimer, QPropertyAnimation, QEasingCurve, Qt
from PyQt6.QtWidgets import QProgressBar, QLabel, QWidget, QVBoxLayout,QFrame, QHBoxLayout

# Add this new class for a typing indicator message
class TypingIndicatorWidget(QWidget):
    """Widget for showing a typing/thinking indicator"""
    def __init__(self, model_name, parent=None):
        super().__init__(parent)
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(10, 5, 10, 5)
        
        # Create frame with assistant styling
        self.frame = QFrame()
        frame_layout = QVBoxLayout(self.frame)
        
        # Role indicator
        role_label = QLabel(f"Assistant ({model_name}):")
        role_label.setStyleSheet("font-weight: bold;")
        frame_layout.addWidget(role_label)
        
        # Loading indicator container
        indicator_layout = QHBoxLayout()
        
        # Thinking text
        self.thinking_label = QLabel("Thinking")
        indicator_layout.addWidget(self.thinking_label)
        
        # Animated dots
        self.dots_label = QLabel("")
        indicator_layout.addWidget(self.dots_label)
        
        # Add spacer to push everything to the left
        indicator_layout.addStretch()
        
        frame_layout.addLayout(indicator_layout)
        
        # Progress bar (optional)
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 0)  # Makes it an "indeterminate" progress bar
        self.progress_bar.setMaximumHeight(4)  # Make it thin
        self.progress_bar.setTextVisible(False)
        frame_layout.addWidget(self.progress_bar)
        
        # Style the frame like assistant messages
        self.frame.setStyleSheet(
            "background-color: #F5F5F5; border-radius: 10px; padding: 10px;"
        )
        self.layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.layout.addWidget(self.frame)
        
        # Setup animation timer
        self.dot_count = 0
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_dots)
        self.timer.start(500)  # Update every 500ms
    
    def update_dots(self):
        """Animate the dots to show activity"""
        self.dot_count = (self.dot_count + 1) % 4
        self.dots_label.setText("." * self.dot_count)