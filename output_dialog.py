# output_dialog.py
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QTextEdit
from PyQt5.QtGui import QIcon

class OutputDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Output")
        self.setGeometry(100, 100, 400, 300)
        self.setWindowIcon(QIcon("output_icon.png"))

        self.text_edit = QTextEdit()
        self.text_edit.setReadOnly(True)  # Make text box read-only

        layout = QVBoxLayout()
        layout.addWidget(self.text_edit)
        self.setLayout(layout)

    def append_text(self, text):
        """Append text to the QTextEdit."""
        self.text_edit.append(text)

# output_redirection.py
import sys

class OutputRedirector:
    def __init__(self, text_edit):
        self.text_edit = text_edit

    def write(self, text):
        if text.strip():  # Only append non-empty text
            self.text_edit.append(text)
        sys.stdout.flush()  # Ensure real-time output

    def flush(self):
        pass  # Required for file-like object compatibility
