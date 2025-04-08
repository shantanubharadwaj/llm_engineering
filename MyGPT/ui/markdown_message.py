import markdown
from PyQt6.QtWidgets import QTextBrowser, QWidget, QVBoxLayout, QFrame, QLabel, QSizePolicy
from PyQt6.QtGui import QFontMetrics
from PyQt6.QtCore import Qt

# Create a new widget to replace MessageWidget that supports Markdown
class MarkdownMessageWidget(QWidget):
    """Widget for displaying a single message with Markdown support"""
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
        
        # Message content with Markdown support
        if is_user:
            # For user messages, keep using QLabel (no Markdown needed)
            self.message = QLabel(text)
            self.message.setWordWrap(True)
            self.message.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
            
            self.message.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
            
            # Calculate an appropriate width for the message
            fm = QFontMetrics(self.message.font())
            text_width = min(fm.horizontalAdvance(text) + 40, 500)  # Cap at 500px
            
            # Set a minimum width for the frame based on content
            self.frame.setMinimumWidth(text_width)
            # Set maximum width to prevent overly wide messages
            self.frame.setMaximumWidth(500)
        else:
            # For assistant messages, use QTextBrowser with Markdown rendering
            self.message = QTextBrowser()
            self.message.setOpenExternalLinks(True)  # Allow clicking links
            
            # Convert Markdown to HTML
            html_content = markdown.markdown(
                text,
                extensions=['extra', 'codehilite', 'fenced_code']
            )
            
            # Add some CSS for better formatting
            styled_html = f"""
            <style>
                code {{
                    background-color: #f0f0f0;
                    padding: 2px 4px;
                    border-radius: 3px;
                    font-family: monospace;
                }}
                pre {{
                    background-color: #f5f5f5;
                    padding: 10px;
                    border-radius: 5px;
                    overflow-x: auto;
                    font-family: monospace;
                }}
                img {{ max-width: 100%; height: auto; }}
                table {{ border-collapse: collapse; width: 100%; }}
                th, td {{ border: 1px solid #ddd; padding: 8px; }}
                th {{ background-color: #f2f2f2; }}
                blockquote {{
                    border-left: 4px solid #ccc;
                    margin-left: 0;
                    padding-left: 15px;
                    color: #555;
                }}
            </style>
            {html_content}
            """
            
            self.message.setHtml(styled_html)
            
            # Set a reasonable initial size
            self.message.setMinimumHeight(50)
            fm = QFontMetrics(self.message.font())
            text_width = self.message.width() - 20  # Adjust for margins
            text_height = fm.lineSpacing() * (text.count('\n') + 1)
            self.message.setMinimumHeight(min(text_height + 30, 400))  # Cap at 400px
            
            # Remove scrollbar if content is small enough
            self.message.document().adjustSize()
            if self.message.document().size().height() < 400:
                self.message.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
            
        frame_layout.addWidget(self.message)
        
        # Set different styles for user vs assistant messages
        if is_user:
            self.frame.setStyleSheet(
                "background-color: #E1F5FE; border-radius: 10px; padding: 10px;"
            )
            self.layout.setAlignment(Qt.AlignmentFlag.AlignRight)
            self.frame.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        else:
            self.frame.setStyleSheet(
                "background-color: #F5F5F5; border-radius: 10px; padding: 10px;"
            )
            self.layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
            self.frame.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        
        self.layout.addWidget(self.frame)