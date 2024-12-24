from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QWidget, QLineEdit, QLabel, QScrollArea, QPushButton
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
import sys
import os
from dotenv import load_dotenv
import google.generativeai as genai
load_dotenv()
genai.configure(api_key=os.getenv("API_KEY"))
model = genai.GenerativeModel("gemini-1.5-flash")

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("jolly-joysticks")
        self.setGeometry(200, 200, 1200, 800)

        # Main widget and layout
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)

        # Scrollable container for processed text display
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setStyleSheet(
            """
            QScrollArea {
                border: none;
                background-color: #6d6d9e; /* Purple background */
            }
            QScrollBar:vertical {
                background: #4c4c6d;
                width: 12px;
                margin: 10px 0 10px 0;
            }
            QScrollBar::handle:vertical {
                background: #8a8abc;
                min-height: 30px;
                border-radius: 5px;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                background: none;
                border: none;
            }
            """
        )

        self.output_container = QWidget()
        self.output_layout = QVBoxLayout()
        self.output_layout.setSpacing(15)  # Increased spacing between output bubbles
        self.output_container.setLayout(self.output_layout)
        self.scroll_area.setWidget(self.output_container)
        self.layout.addWidget(self.scroll_area)

        # Input text box
        self.input_box = QLineEdit()
        self.input_box.setPlaceholderText("Type your prompt here and press Enter...")
        self.input_box.setStyleSheet(
            """
            QLineEdit {
                background-color: #4c4c6d;
                color: white;
                border: 2px solid #8a8abc;
                border-radius: 15px;
                padding: 12px;
                font-family: 'Segoe UI', sans-serif;
                font-size: 18px;
                transition: all 0.3s ease;
            }
            QLineEdit:hover {
                border: 2px solid #a39cd4;
            }
            QLineEdit:focus {
                border: 2px solid #a39cd4;
                background-color: #5a5a7d;
                outline: none;
                box-shadow: 0 0 15px rgba(163, 156, 212, 0.6); /* Subtle glowing effect */
            }
            """
        )
        self.input_box.returnPressed.connect(self.process_input)
        self.layout.addWidget(self.input_box)

        # Set overall window style
        self.setStyleSheet(
            """
            QMainWindow {
                background-color: #6d6d9e; /* Purple background for the entire window */
                border-radius: 15px;
            }
            """
        )

    def process_input(self):
        prompt = self.input_box.text().strip()
        if not prompt:
            return

        # User's input bubble
        user_label = QLabel(prompt)
        user_label.setWordWrap(True)
        user_label.setAlignment(Qt.AlignRight)
        user_label.setStyleSheet(
            """
            QLabel {
                background-color: #8a8abc; /* Light purple for user text */
                color: black;
                border-radius: 25px;
                padding: 15px;
                font-family: 'Segoe UI', sans-serif;
                font-size: 16px;
                margin-bottom: 15px;
            }
            """
        )
        self.output_layout.addWidget(user_label)

        # Simulate system response
        response = f"{model.generate_content(prompt).text}"  # Replace with your processing logic
        response_label = QLabel(response)
        response_label.setWordWrap(True)
        response_label.setAlignment(Qt.AlignLeft)
        response_label.setStyleSheet(
            """
            QLabel {
                background-color: #3e3e5e; /* Grey for system text */
                color: white;
                border-radius: 25px;
                padding: 15px;
                font-family: 'Segoe UI', sans-serif;
                font-size: 16px;
                margin-bottom: 15px;
            }
            """
        )
        self.output_layout.addWidget(response_label)

        # Scroll to bottom
        QApplication.processEvents()  # Ensure all events are processed
        self.scroll_area.verticalScrollBar().setValue(self.scroll_area.verticalScrollBar().maximum())

        # Clear the input box
        self.input_box.clear()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
