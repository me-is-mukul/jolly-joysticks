from openai import OpenAI
from dotenv import load_dotenv
import os
from PyQt5.QtWidgets import (QApplication, QMainWindow, QPlainTextEdit, QTabWidget, QTreeView, QFileSystemModel, QSplitter, QVBoxLayout, QWidget)
from PyQt5.QtCore import Qt

load_dotenv()
client = OpenAI( api_key = os.getenv('API_KEY') )


class App(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Jolly-JoySticks")
        self.setGeometry(100, 100, 1200, 800)

        # Main splitter (to divide sidebar and main area)
        main_splitter = QSplitter(Qt.Horizontal)

        # Sidebar for file navigation
        self.sidebar = QTreeView()
        self.file_model = QFileSystemModel()
        self.file_model.setRootPath("")  # Set root path for file system
        self.sidebar.setModel(self.file_model)
        self.sidebar.setRootIndex(self.file_model.index("file path"))  # Show current directory
        self.sidebar.setHeaderHidden(False)
        main_splitter.addWidget(self.sidebar)

        # Tab Widget for Editor Area
        self.tab_widget = QTabWidget()
        main_splitter.addWidget(self.tab_widget)
        main_splitter.setStretchFactor(2, 3)  # Sidebar:Main area = 1:3
    
        # Set main splitter as the central widget
        container = QWidget()
        layout = QVBoxLayout()
        layout.addWidget(main_splitter)
        container.setLayout(layout)
        self.setCentralWidget(container)

        # Add an initial editor tab
        self.add_new_tab("New File")

        # Set the theme (purple and grey)
        self.set_stylesheet()

    def add_new_tab(self, filename):
        editor = QPlainTextEdit()
        editor.setPlaceholderText(f"Editing {filename}")
        self.tab_widget.addTab(editor, filename)

    def set_stylesheet(self):
        # Define the stylesheet for the purple and grey theme
        stylesheet = """
            QMainWindow {
                background-color: #2E2E2E;  /* Dark grey background */
            }
            QTabWidget::pane {
                border: 1px solid #444444;
            }
            QTabBar::tab {
                background-color: #444444;
                color: #FFFFFF;
                padding: 5px;
                border: 1px solid #333333;
                margin-right: 2px;
            }
            QTabBar::tab:selected {
                background-color: #6A4C9C;  /* Purple when selected */
                color: #FFFFFF;
            }
            QPlainTextEdit {
                background-color: #2E2E2E;  /* Dark grey background */
                color: #D0D0D0;  /* Light grey text */
                border: none;
                font-family: Consolas, Monaco, 'Courier New', monospace;
                font-size: 14px;
                padding: 5px;
            }
            QTreeView {
                background-color: #333333;  /* Darker grey */
                color: #D0D0D0;  /* Light grey text */
                border: 1px solid #444444;
                font-size: 12px;
            }
            QTreeView::item {
                background-color: #333333;
                padding: 3px;
            }
            QTreeView::item:selected {
                background-color: #6A4C9C;  /* Purple selection */
                color: #FFFFFF;
            }
        """
        self.setStyleSheet(stylesheet)



# Run the application
if __name__ == "__main__":
    app = QApplication([])
    window = App()
    window.show()
    app.exec()
