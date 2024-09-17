import json
import os
import sys
from PyQt5.QtWidgets import QDialog, QFormLayout, QLabel, QLineEdit, QVBoxLayout, QDialogButtonBox
from PyQt5.QtGui import QIcon

DETAILS_FILE = "settings.details"

class SettingsDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Settings")
        self.setGeometry(100, 100, 300, 150)
        self.setWindowIcon(QIcon("settings.png"))  # Set the window icon to settings.png

        # Form layout for processId and password
        self.form_layout = QFormLayout()

        self.process_id_input = QLineEdit()
        self.process_password_input = QLineEdit()
        self.process_password_input.setEchoMode(QLineEdit.Password)  # Mask the password with asterisks

        self.form_layout.addRow(QLabel("Process ID:"), self.process_id_input)
        self.form_layout.addRow(QLabel("Process ID Password:"), self.process_password_input)

        # Load existing details if the file exists
        self.load_details()

        # Save button
        self.button_box = QDialogButtonBox(QDialogButtonBox.Save | QDialogButtonBox.Cancel)
        self.button_box.accepted.connect(self.save_details)
        self.button_box.rejected.connect(self.reject)

        layout = QVBoxLayout()
        layout.addLayout(self.form_layout)
        layout.addWidget(self.button_box)
        self.setLayout(layout)

        # Set fixed size for the settings window
        self.setFixedSize(self.size())

    def load_details(self):
        """Load the processId and processIDPassword from the settings file."""
        if os.path.exists(DETAILS_FILE):
            with open(DETAILS_FILE, 'r') as f:
                details = json.load(f)
                self.process_id_input.setText(details.get('processId', ''))
                self.process_password_input.setText(details.get('processIDPassword', ''))

    def save_details(self):
        """Save the processId and processIDPassword to the settings file."""
        process_id = self.process_id_input.text().strip()
        process_password = self.process_password_input.text().strip()
        if process_id and process_password:  # Ensure fields are not empty
            details = {
                'processId': process_id,
                'processIDPassword': process_password
            }
            with open(DETAILS_FILE, 'w') as f:
                json.dump(details, f)
            self.accept()
        else:
            print("Process ID and Password cannot be empty.", file=sys.stderr)
