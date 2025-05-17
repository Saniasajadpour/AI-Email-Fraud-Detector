# app.py

import sys
import os
from PyQt6.QtWidgets import QApplication, QMainWindow, QStackedWidget
from PyQt6.QtGui import QPalette, QBrush, QPixmap, QIcon
from PyQt6.QtCore import Qt

from ui.pages.HomePage import HomePage
from ui.pages.EmailTextPage import EmailTextPage
from ui.pages.EmailFilePage import EmailFilePage
from ui.pages.ResultPage import ResultPage


class FraudDetectionApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("📧 Email Fraud Detection System")

        # ✅ Dynamic and portable icon path
        icon_path = os.path.join(os.getcwd(), "icons", "app_icon.ico")
        self.setWindowIcon(QIcon(icon_path))

        self.setGeometry(100, 100, 1000, 700)

        self.dark_background = "assets/background_dark.png"
        self.light_background = "assets/background_light.png"
        self.current_theme = "dark"

        # Central widget as a stacked layout
        self.stack = QStackedWidget()
        self.setCentralWidget(self.stack)

        # Pages
        self.home_page = HomePage(
            navigate_to_text_page=self.show_text_page,
            navigate_to_file_page=self.show_file_page,
            toggle_theme_callback=self.toggle_theme
        )
        self.text_page = EmailTextPage(
            analyze_callback=self.show_result_page,
            go_home_callback=self.show_home_page,
            toggle_theme=self.toggle_theme
        )
        self.file_page = EmailFilePage(
            analyze_callback=self.show_result_page,
            go_home_callback=self.show_home_page,
            toggle_theme=self.toggle_theme
        )
        self.result_page = ResultPage(
            go_home_callback=self.show_home_page,
            toggle_theme_callback=self.toggle_theme
        )

        self.stack.addWidget(self.home_page)
        self.stack.addWidget(self.text_page)
        self.stack.addWidget(self.file_page)
        self.stack.addWidget(self.result_page)

        self.stack.setCurrentWidget(self.home_page)
        self.set_background(self.dark_background)

    def set_background(self, path):
        if path and QPixmap(path).isNull() is False:
            pixmap = QPixmap(path).scaled(
                self.size(),
                Qt.AspectRatioMode.IgnoreAspectRatio,
                Qt.TransformationMode.SmoothTransformation
            )
            palette = QPalette()
            palette.setBrush(QPalette.ColorRole.Window, QBrush(pixmap))
            self.setPalette(palette)

    def toggle_theme(self):
        self.current_theme = "light" if self.current_theme == "dark" else "dark"
        new_path = self.light_background if self.current_theme == "light" else self.dark_background
        self.set_background(new_path)

    def resizeEvent(self, event):
        self.set_background(self.light_background if self.current_theme == "light" else self.dark_background)
        super().resizeEvent(event)

    def show_home_page(self):
        self.stack.setCurrentWidget(self.home_page)

    def show_text_page(self):
        self.stack.setCurrentWidget(self.text_page)

    def show_file_page(self):
        self.stack.setCurrentWidget(self.file_page)

    def show_result_page(self, prediction_result: dict):
        self.result_page.set_results(
            prediction_result["fraud_score"],
            prediction_result["safe_score"],
            prediction_result["fraud_reason"],
            prediction_result["safe_reason"],
            prediction_result["suggestion"]
        )
        self.stack.setCurrentWidget(self.result_page)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = FraudDetectionApp()
    window.show()
    sys.exit(app.exec())
