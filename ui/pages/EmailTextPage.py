from PyQt6.QtWidgets import (
    QWidget, QLabel, QPushButton, QTextEdit, QVBoxLayout, QHBoxLayout, QGraphicsDropShadowEffect
)
from PyQt6.QtGui import QColor, QCursor
from PyQt6.QtCore import Qt
from core.preprocess import preprocess_email
from core.model import predict_email


class EmailTextPage(QWidget):
    def __init__(self, go_home_callback, analyze_callback, toggle_theme):
        super().__init__()
        self.go_home_callback = go_home_callback
        self.analyze_callback = analyze_callback
        self.toggle_theme = toggle_theme
        self.init_ui()

    def init_ui(self):
        self.setObjectName("EmailTextPage")
        self.setStyleSheet("""
            #EmailTextPage {
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

        main_layout = QVBoxLayout()
        main_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.setSpacing(30)

        # === Top Bar ===
        top_bar = QHBoxLayout()
        top_bar.setContentsMargins(20, 20, 20, 0)
        top_bar.setAlignment(Qt.AlignmentFlag.AlignLeft)

        self.theme_button = QPushButton("🌓")
        self.theme_button.setFixedSize(40, 40)
        self.theme_button.clicked.connect(self.toggle_theme)
        self.add_shadow(self.theme_button)
        top_bar.addWidget(self.theme_button)
        main_layout.addLayout(top_bar)

        # === Header ===
        header = QLabel("Please paste your Email")
        header.setObjectName("header")
        header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(header)

        # === Email Input ===
        self.text_edit = QTextEdit()
        self.text_edit.setPlaceholderText("Write or paste the email body here...")
        main_layout.addWidget(self.text_edit)

        # === Buttons ===
        button_layout = QHBoxLayout()
        button_layout.setSpacing(40)
        button_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.home_button = QPushButton("HOME PAGE")
        self.analyze_button = QPushButton("Analyze")

        for btn in [self.home_button, self.analyze_button]:
            btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
            self.add_shadow(btn)

        self.home_button.clicked.connect(self.go_home_callback)
        self.analyze_button.clicked.connect(self.run_analysis)

        button_layout.addWidget(self.home_button)
        button_layout.addWidget(self.analyze_button)
        main_layout.addLayout(button_layout)

        self.setLayout(main_layout)

    def run_analysis(self):
        raw_text = self.text_edit.toPlainText().strip()
        if not raw_text:
            return

        cleaned = preprocess_email(raw_text)
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
