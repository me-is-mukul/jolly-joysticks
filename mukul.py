import markdown
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QMovie
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QWidget, QTextEdit, QLabel, QScrollArea, 
    QPushButton, QHBoxLayout
)
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

        self.setWindowTitle("ChatGPT-like Interface")
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
        self.send_button = QPushButton("Send")
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
        self.send_button.clicked.connect(self.process_input)
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


    def generate_response(self, prompt):
        try:
            # Simulate AI response (Replace with actual model logic)
            response = f"{model.generate_content(prompt).text}"

            # Convert markdown to HTML
            html_response = markdown.markdown(response)

            # Prepare the response edit field with HTML content
            self.current_text = html_response
            self.index = 0
            self.response_edit = QTextEdit()
            self.response_edit.setReadOnly(True)
            self.response_edit.setAlignment(Qt.AlignLeft)
            self.response_edit.setStyleSheet(
                """
                QTextEdit {
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
            self.response_edit.setHtml(self.current_text)
            self.output_layout.addWidget(self.response_edit)

            # Stop spinner before starting the typing effect
            self.spinner.stop()
            self.overlay.setVisible(False)

            # Start typing effect
            self.response_edit.clear()
            self.typing_timer.start(self.typing_speed)

        except Exception as e:
            # If an error occurs, display it as a regular message
            response = f"Error: {e}"
            self.current_text = response
            self.index = 0
            self.typing_timer.start(self.typing_speed)

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
