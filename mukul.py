import markdown
from markdown.extensions.fenced_code import FencedCodeExtension
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QMovie
from PyQt5.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, QWidget, QTextEdit, QLabel, QScrollArea, QPushButton, QHBoxLayout)
import sys
import os
from final import *

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Jolly-Joysticks")
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
                background-color: #2a2d37; /* Dark background */
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
            """
        )

        self.output_container = QWidget()
        self.output_layout = QVBoxLayout()
        self.output_layout.setSpacing(15)  # Increased spacing between output bubbles
        self.output_container.setLayout(self.output_layout)
        self.scroll_area.setWidget(self.output_container)
        self.layout.addWidget(self.scroll_area)

        # Input and control container
        self.input_control_container = QHBoxLayout()
        self.layout.addLayout(self.input_control_container)

        # Input text box (multiline)
        self.input_box = QTextEdit()
        self.input_box.setPlaceholderText("Type your message...")
        self.input_box.setFixedHeight(75)  # Adjusted height of the input box
        self.input_box.setStyleSheet(
            """
            QTextEdit {
                background-color: #3c3f50;
                color: white;
                border: 1px solid #505c6b;
                border-radius: 15px;
                padding: 12px;
                font-family: 'Segoe UI', sans-serif;
                font-size: 18px;
                transition: all 0.3s ease;
            }
            QTextEdit:hover {
                border: 1px solid #76c3ff;
            }
            QTextEdit:focus {
                border: 1px solid #76c3ff;
                background-color: #4a4f63;
                outline: none;
                box-shadow: 0 0 15px rgba(118, 195, 255, 0.6); /* Subtle glowing effect */
            }
            """
        )
        self.input_box.keyPressEvent = self.custom_key_press_event  # Override key press event
        self.input_control_container.addWidget(self.input_box)

        # Send button
        self.send_button = QPushButton("Refine Prompt + Send")
        self.send_button.setStyleSheet(
            """
            QPushButton {
                background-color: #4c8eaf;
                color: white;
                border-radius: 15px;
                padding: 10px 20px;
                font-family: 'Segoe UI', sans-serif;
                font-size: 16px;
            }
            QPushButton:hover {
                background-color: #6fa4c9;
            }
            """
        )
        self.send_button.clicked.connect(self.process_input_new)
        self.input_control_container.addWidget(self.send_button)

        # Clear Chat button
        self.clear_button = QPushButton("Clear Chat")
        self.clear_button.setStyleSheet(
            """
            QPushButton {
                background-color: #ff6347;
                color: white;
                border-radius: 15px;
                padding: 10px 20px;
                font-family: 'Segoe UI', sans-serif;
                font-size: 16px;
            }
            QPushButton:hover {
                background-color: #ff7d68;
            }
            """
        )
        self.clear_button.clicked.connect(self.clear_chat)
        self.input_control_container.addWidget(self.clear_button)

        # Overlay for progress indicator
        self.overlay = QWidget(self)
        self.overlay.setGeometry(self.rect())
        self.overlay.setVisible(False)

        self.progress_label = QLabel(self.overlay)
        self.progress_label.setAlignment(Qt.AlignCenter)
        self.spinner = QMovie("media/animation.gif")  # Replace with a valid spinner GIF path
        self.progress_label.setMovie(self.spinner)

        # Set overall window style
        self.setStyleSheet(
            """
            QMainWindow {
                background-color: #1e222d; /* Dark background for the entire window */
                border-radius: 15px;
            }
            """
        )

        # Typing effect setup
        self.typing_timer = QTimer(self)
        self.typing_timer.timeout.connect(self.typing_effect)

        self.current_text = ""
        self.index = 0
        self.typing_speed = 50  # Speed of typing in milliseconds

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.overlay.setGeometry(self.rect())
        self.progress_label.setGeometry(0, 0, self.overlay.width(), self.overlay.height())

    def custom_key_press_event(self, event):
        if event.key() == Qt.Key_Return and not event.modifiers() == Qt.ShiftModifier:
            self.process_input()
        elif event.key() == Qt.Key_Return and event.modifiers() == Qt.ShiftModifier:
            cursor = self.input_box.textCursor()
            cursor.insertText("\n")
        else:
            QTextEdit.keyPressEvent(self.input_box, event)

    def process_input(self):
        prompt = self.input_box.toPlainText().strip()
        if not prompt:
            return

        # User's input bubble
        user_label = QLabel(prompt)
        user_label.setWordWrap(True)
        user_label.setAlignment(Qt.AlignRight)
        user_label.setStyleSheet(
            """
            QLabel {
                background-color: #4c8eaf; /* Chat bubble color */
                color: white;
                border-radius: 25px;
                padding: 15px;
                font-family: 'Segoe UI', sans-serif;
                font-size: 16px;
                margin-bottom: 15px;
            }
            """
        )
        self.output_layout.addWidget(user_label)

        # Show progress indicator
        self.overlay.setVisible(True)
        self.spinner.start()
        QApplication.processEvents()

        # Clear the input box after processing the input
        self.input_box.clear()  # This line clears the text box

        # Simulate system response with a delay
        QTimer.singleShot(2000, lambda: self.generate_response(prompt))

    def process_input_new(self):
        prompt = self.input_box.toPlainText().strip()
        if not prompt:
            return

        # User's input bubble
        user_label = QLabel(f"User Prompt: {prompt}\nRefined prompt: {simplify_prompt(prompt)}")
        user_label.setWordWrap(True)
        user_label.setAlignment(Qt.AlignRight)
        user_label.setStyleSheet(
            """
            QLabel {
                background-color: #4c8eaf; /* Chat bubble color */
                color: white;
                border-radius: 25px;
                padding: 15px;
                font-family: 'Segoe UI', sans-serif;
                font-size: 16px;
                margin-bottom: 15px;
            }
            """
        )
        self.output_layout.addWidget(user_label)

        # Show progress indicator
        self.overlay.setVisible(True)
        self.spinner.start()
        QApplication.processEvents()

        # Clear the input box after processing the input
        self.input_box.clear()  # This line clears the text box

        # Simulate system response with a delay
        QTimer.singleShot(2000, lambda: self.generate_response(simplify_prompt(prompt)))



    def generate_response(self, prompt):
        try:
            # Generate AI response
            response =response_from_gemini(prompt)

            # Convert markdown to HTML with fenced code support
            html_response = markdown.markdown(
                response, extensions=["fenced_code"]
            )

            # Add custom CSS for styling code blocks
            styled_html = f"""
            <html>
            <head>
                <style>
                    body {{
                        color: white;
                        font-family: 'Segoe UI', sans-serif;
                    }}
                    pre {{
                        background-color: #2d2d2d;
                        color: #dcdcdc;
                        border-radius: 8px;
                        padding: 10px;
                        overflow-x: auto;
                    }}
                    code {{
                        font-family: 'Courier New', monospace;
                        font-size: 14px;
                    }}
                </style>
            </head>
            <body>
                {html_response}
            </body>
            </html>
            """

            # Create a QLabel to display the formatted response
            response_label = QLabel()
            response_label.setWordWrap(True)
            response_label.setAlignment(Qt.AlignLeft)
            response_label.setStyleSheet(
                """
                QLabel {
                    background-color: #3e3e5e;
                    color: white;
                    border-radius: 25px;
                    padding: 15px;
                    font-family: 'Segoe UI', sans-serif;
                    font-size: 16px;
                    margin-bottom: 15px;
                }
                """
            )
            response_label.setTextInteractionFlags(Qt.NoTextInteraction)  # Prevent text selection

            # Set the styled HTML content
            response_label.setText(styled_html)
            self.output_layout.addWidget(response_label)

            # Stop spinner
            self.spinner.stop()
            self.overlay.setVisible(False)

        except Exception as e:
            # Handle exceptions gracefully
            error_label = QLabel(f"Error: {e}")
            error_label.setStyleSheet("color: red;")
            self.output_layout.addWidget(error_label)



    def typing_effect(self):
        if self.index < len(self.current_text):
            self.response_edit.insertPlainText(self.current_text[self.index])
            self.index += 1
        else:
            # Stop the timer once the text is fully typed out
            self.typing_timer.stop()

    def clear_chat(self):
        # Remove all widgets from the output layout
        while self.output_layout.count():
            widget = self.output_layout.takeAt(0).widget()
            if widget:
                widget.deleteLater()
        self.scroll_area.verticalScrollBar().setValue(0)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
    