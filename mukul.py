from PyQt5.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, QWidget, QLineEdit, QLabel, QScrollArea)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
import sys


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
        self.output_layout.setSpacing(15)  # Increased spacing between output bubbles for a more spacious feel
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
                box-shadow: 0 0 15px rgba(163, 156, 212, 0.6); /* Subtle glowing effect on focus */
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
        # Get the user input
        prompt = self.input_box.text().strip()  # Remove leading/trailing whitespace
        if not prompt:
            return  # Ignore empty input

        # Process the prompt (you can customize this part)
        output = f"{prompt}"

        # Create a styled QLabel for the output
        output_label = QLabel(output)
        output_label.setWordWrap(True)  # Allow multiline text
        output_label.setAlignment(Qt.AlignLeft)
        output_label.setStyleSheet(
            """
            QLabel {
                background-color: #3e3e5e; /* Grey background for the text bubble */
                color: white; /* Text color */
                border: none; /* No border for simplicity */
                border-radius: 25px; /* Oval shape */
                padding: 15px; /* Space around text */
                font-family: 'Segoe UI', sans-serif;
                font-size: 16px;
                width: auto; /* Dynamically adjust the width */
                min-width: 150px; /* Minimum width for a single line */
                margin-bottom: 15px; /* Spacing between text bubbles */
                transition: all 0.3s ease-in-out; /* Smooth transition for hover effect */
            }
            QLabel:hover {
                background-color: #5a5a7d; /* Slightly lighter color on hover */
                box-shadow: 0 0 10px rgba(255, 255, 255, 0.3); /* Glow effect on hover */
            }
            """
        )
        output_label.setFont(QFont("Segoe UI", 16))

        # Add the label to the layout
        self.output_layout.addWidget(output_label)

        # Clear the input box
        self.input_box.clear()

