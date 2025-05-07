# ui/pages/HomePage.py

from PyQt6.QtWidgets import QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QFileDialog
from PyQt6.QtGui import QFont, QCursor, QIcon
from PyQt6.QtCore import Qt, QSize

class HomePage(QWidget):
    def __init__(self, navigate_to_text_page, navigate_to_file_page, toggle_theme_callback):
        super().__init__()
        self.navigate_to_text_page = navigate_to_text_page
        self.navigate_to_file_page = navigate_to_file_page
        self.toggle_theme_callback = toggle_theme_callback

        self.setObjectName("HomePage")
        self.setStyleSheet("""
            #HomePage {
                background-color: transparent;
            }
            QLabel#header {
                font-size: 40px;
                font-weight: bold;
                color: white;
            }
            QPushButton {
                padding: 14px;
                border-radius: 20px;
                background-color: black;
                color: white;
                font-size: 16px;
                font-weight: bold;
                box-shadow: 0px 0px 10px lavender;
            }
            QPushButton:hover {
                background-color: #2e2e2e;
                transform: scale(1.05);
            }
            QPushButton#themeButton {
                border-radius: 20px;
                min-width: 40px;
                min-height: 40px;
                max-width: 40px;
                max-height: 40px;
                background-color: #444;
            }
            QPushButton#themeButton:hover {
                background-color: #777;
               
            }
        """)

        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.setSpacing(40)

        # Top bar with theme toggle
        top_bar = QHBoxLayout()
        top_bar.setContentsMargins(20, 20, 20, 0)
        top_bar.setAlignment(Qt.AlignmentFlag.AlignLeft)

        self.theme_button = QPushButton("🌓")
        self.theme_button.setObjectName("themeButton")
        self.theme_button.clicked.connect(self.toggle_theme_callback)
        self.theme_button.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        top_bar.addWidget(self.theme_button)

        layout.addLayout(top_bar)

        # Header text
        header = QLabel("Welcome to Email Fraud Detection App")
        header.setObjectName("header")
        header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(header)

        # Buttons
        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(40)
        buttons_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.text_button = QPushButton("Email Text")
        self.text_button.clicked.connect(self.navigate_to_text_page)
        self.text_button.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.file_button = QPushButton("Email File")
        self.file_button.clicked.connect(self.navigate_to_file_page)
        self.file_button.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        buttons_layout.addWidget(self.text_button)
        buttons_layout.addWidget(self.file_button)

        layout.addLayout(buttons_layout)
        self.setLayout(layout)
