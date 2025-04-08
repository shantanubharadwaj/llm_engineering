import sys
from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QFont
from dotenv import load_dotenv

from ui.main_window import MainWindow

load_dotenv()


def main():
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    font = QFont("Menlo")
    app.setFont(font)
    
    app.setApplicationName("MyGPT")
    app.setOrganizationName("<SDB Labs>")
    
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec())


if __name__ == "__main__":
    main()