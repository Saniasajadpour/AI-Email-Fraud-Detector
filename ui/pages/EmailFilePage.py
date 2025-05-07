# ui/pages/EmailFilePage.py

from PyQt6.QtWidgets import (
    QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout,
    QFileDialog, QTextEdit, QGraphicsDropShadowEffect
)
from PyQt6.QtGui import QColor, QCursor
from PyQt6.QtCore import Qt
from core.model import predict_email
from core.preprocess import preprocess_email
from utils.file_handler import read_email_file


class EmailFilePage(QWidget):
    def __init__(self, go_home_callback, analyze_callback, toggle_theme):
        super().__init__()
        self.go_home_callback = go_home_callback
        self.analyze_callback = analyze_callback
        self.toggle_theme = toggle_theme
        self.init_ui()

    def init_ui(self):
        self.setObjectName("EmailFilePage")
        self.setStyleSheet("""
            #EmailFilePage {
                background-color: transparent;
            }
            QLabel#header {
                font-size: 26px;
                font-weight: bold;
                color: white;
            }
            QTextEdit {
                background-color: rgba(255, 255, 255, 0.1);
                border: 2px solid #ccc;
                color: white;
                font-size: 14px;
                padding: 14px;
                border-radius: 10px;
            }
            QPushButton {
                padding: 12px 24px;
                font-size: 16px;
                background-color: #000;
                color: white;
                border-radius: 10px;
            }
            QPushButton:hover {
                background-color: #2c2c2c;
            }
        """)

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.setSpacing(30)

        # === Theme toggle ===
        top_bar = QHBoxLayout()
        top_bar.setContentsMargins(20, 20, 20, 0)
        top_bar.setAlignment(Qt.AlignmentFlag.AlignLeft)

        theme_button = QPushButton("🌓")
        theme_button.setFixedSize(40, 40)
        theme_button.clicked.connect(self.toggle_theme)
        self.add_shadow(theme_button)
        top_bar.addWidget(theme_button)
        layout.addLayout(top_bar)

        # === Header ===
        header = QLabel("Upload an Email File (.txt or .eml)")
        header.setObjectName("header")
        header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(header)

        # === File Preview ===
        self.text_preview = QTextEdit()
        self.text_preview.setPlaceholderText("Email file preview will appear here...")
        self.text_preview.setReadOnly(True)
        layout.addWidget(self.text_preview)

        # === Buttons ===
        button_layout = QHBoxLayout()
        button_layout.setSpacing(40)
        button_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.home_button = QPushButton("HOME PAGE")
        self.upload_button = QPushButton("Choose File")
        self.analyze_button = QPushButton("Analyze")

        for btn in [self.home_button, self.upload_button, self.analyze_button]:
            btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
            self.add_shadow(btn)

        self.home_button.clicked.connect(self.go_home_callback)
        self.upload_button.clicked.connect(self.select_file)
        self.analyze_button.clicked.connect(self.analyze_file)

        button_layout.addWidget(self.home_button)
        button_layout.addWidget(self.upload_button)
        button_layout.addWidget(self.analyze_button)

        layout.addLayout(button_layout)
        self.setLayout(layout)

        self.email_text = ""

    def select_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Open Email File", "", "Email Files (*.txt *.eml)")
        if file_path:
            try:
                with open(file_path, "rb") as f:
                    self.email_text = read_email_file(f)
                    self.text_preview.setText(self.email_text)
            except Exception as e:
                self.text_preview.setText(f"⚠️ Failed to read file:\n{e}")
                self.email_text = ""

    def analyze_file(self):
        if not self.email_text.strip():
            self.text_preview.setText("⚠️ No valid email content to analyze.")
            return

        cleaned = preprocess_email(self.email_text)
        label, confidence = predict_email(cleaned)

        fraud_score = round(confidence * 100, 2) if label == 1 else round((1 - confidence) * 100, 2)
        safe_score = 100 - fraud_score

        fraud_reason = "Suspicious patterns, possible phishing links, or known spam keywords detected." if label == 1 else "Low risk indicators."
        safe_reason = "Standard language, no suspicious phrases or behavior." if label == 0 else "Lack of strong safety indicators."
        suggestion = "Do not click any links or respond to this email." if label == 1 else "Email looks safe, but always double-check sender identity."

        result_dict = {
            "fraud_score": fraud_score,
            "safe_score": safe_score,
            "fraud_reason": fraud_reason,
            "safe_reason": safe_reason,
            "suggestion": suggestion
        }

        self.analyze_callback(result_dict)

    def add_shadow(self, widget):
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(25)
        shadow.setOffset(0, 0)
        shadow.setColor(QColor("#B57EDC"))  # Lavender shadow
        widget.setGraphicsEffect(shadow)
