from PyQt6.QtWidgets import QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QTextEdit, QGraphicsDropShadowEffect
from PyQt6.QtGui import QFont, QCursor, QColor
from PyQt6.QtCore import Qt
from utils.visualization import plot_pie_chart

class ResultPage(QWidget):
    def __init__(self, go_home_callback, toggle_theme_callback):
        super().__init__()
        self.go_home_callback = go_home_callback
        self.toggle_theme_callback = toggle_theme_callback
        self.init_ui()

    def init_ui(self):
        self.setStyleSheet("""
            QLabel#header {
                font-size: 28px;
                color: white;
            }
            QLabel, QTextEdit {
                color: white;
                font-size: 14px;
            }
            QTextEdit {
                background-color: rgba(0, 0, 0, 0.2);
                padding: 10px;
                border-radius: 10px;
            }
            QPushButton {
                padding: 10px 20px;
                font-size: 16px;
                background-color: black;
                color: white;
                border-radius: 8px;
            }
            QPushButton:hover {
                background-color: #333;
            }
        """)

        layout = QVBoxLayout()
        layout.setSpacing(30)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Theme toggle
        top_bar = QHBoxLayout()
        theme_button = QPushButton("🌓")
        theme_button.setFixedSize(40, 40)
        theme_button.clicked.connect(self.toggle_theme_callback)
        self.add_shadow(theme_button)
        top_bar.addWidget(theme_button)
        top_bar.setAlignment(Qt.AlignmentFlag.AlignLeft)
        layout.addLayout(top_bar)

        header = QLabel("Result")
        header.setObjectName("header")
        header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(header)

        # Main result layout
        result_layout = QHBoxLayout()
        self.pie_chart_label = QLabel()
        self.pie_chart_label.setFixedSize(300, 300)
        result_layout.addWidget(self.pie_chart_label)

        text_layout = QVBoxLayout()
        self.fraud_text = QTextEdit()
        self.safe_text = QTextEdit()
        self.suggestion_text = QTextEdit()

        for box in [self.fraud_text, self.safe_text, self.suggestion_text]:
            box.setReadOnly(True)
            self.add_shadow(box)

        text_layout.addWidget(QLabel("Fraudulent Score & Reasons:"))
        text_layout.addWidget(self.fraud_text)
        text_layout.addWidget(QLabel("Safety Score & Reasons:"))
        text_layout.addWidget(self.safe_text)
        text_layout.addWidget(QLabel("System Suggestion:"))
        text_layout.addWidget(self.suggestion_text)

        result_layout.addLayout(text_layout)
        layout.addLayout(result_layout)

        # Home button
        home_btn = QPushButton("HOME PAGE")
        home_btn.clicked.connect(self.go_home_callback)
        self.add_shadow(home_btn)
        layout.addWidget(home_btn)

        self.setLayout(layout)

    def update_result(self, fraud_score, safe_score, fraud_reason, safe_reason, suggestion):
        plot_pie_chart(self.pie_chart_label, fraud_score, safe_score)
        self.fraud_text.setText(fraud_reason)
        self.safe_text.setText(safe_reason)
        self.suggestion_text.setText(suggestion)
    
    def add_shadow(self, widget):
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(20)
        shadow.setColor(QColor("#B57EDC"))
        shadow.setOffset(0, 0)
        widget.setGraphicsEffect(shadow)
    def set_results(self, fraud_score, safe_score, fraud_reason, safe_reason, suggestion):
        self.update_result(fraud_score, safe_score, fraud_reason, safe_reason, suggestion)
