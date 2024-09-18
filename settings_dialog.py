import json
import os
import sys
from PyQt5.QtWidgets import QDialog, QFormLayout, QLabel, QLineEdit, QVBoxLayout, QDialogButtonBox, QComboBox, QWidget
from PyQt5.QtGui import QIcon

DETAILS_FILE = "settings.details"
DB_FILE = "db.env"

class SettingsDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Settings")
        self.setGeometry(100, 100, 300, 150)
        self.setWindowIcon(QIcon("settings.png"))  # Set the window icon to settings.png

        # Form layout for processId and password
        self.form_layout = QFormLayout()

        self.selected_data = {}

        self.process_id_input = QLineEdit()
        self.process_password_input = QLineEdit()
        self.process_password_input.setEchoMode(QLineEdit.Password)  # Mask the password with asterisks

        self.form_layout.addRow(QLabel("Process ID:"), self.process_id_input)
        self.form_layout.addRow(QLabel("Process ID Password:"), self.process_password_input)

        # Dropdown for titles
        self.dropdown = QComboBox()
        self.dropdown.currentIndexChanged.connect(self.on_selection_changed)

        # Non-interactive text fields replaced with simple labels
        self.db_host_name = QLabel()
        self.db_port = QLabel()
        self.database = QLabel()
        # Load data from file
        try:
            self.load_data()
        except Exception as e:
            print(f"Error loading data: {e}", file=sys.stderr)

        # Load existing details if the file exists
        self.load_details()

        # Save button
        self.button_box = QDialogButtonBox(QDialogButtonBox.Save | QDialogButtonBox.Cancel)
        self.button_box.accepted.connect(self.save_details)
        self.button_box.rejected.connect(self.reject)

        layout = QVBoxLayout()
        layout.addLayout(self.form_layout)
        layout.addWidget(QLabel("Select DB"))
        layout.addWidget(self.dropdown)
        layout.addSpacing(10)  # Add space after dropdown

        # Form layout for the fields
        db_form_layout = QFormLayout()
        db_form_layout.addRow(QLabel("DB HostName:"), self.db_host_name)
        db_form_layout.addRow(QLabel("DB PORT:"), self.db_port)
        db_form_layout.addRow(QLabel("Database:"), self.database)

        # Create a container widget to handle spacing
        form_container = QWidget()
        form_container.setLayout(db_form_layout)

        # Add spacing to form container
        layout.addWidget(form_container)
        layout.addSpacing(10)  # Add space before the Configure button

        layout.addWidget(self.button_box)
        self.setLayout(layout)

        # Set fixed size for the settings window
        # self.setFixedSize(self.size())

    def load_details(self):
        """Load the processId and processIDPassword from the settings file."""
        if os.path.exists(DETAILS_FILE):
            with open(DETAILS_FILE, 'r') as f:
                details = json.load(f)
                self.process_id_input.setText(details.get('processId', ''))
                self.process_password_input.setText(details.get('processIDPassword', ''))

    def on_selection_changed(self, index):
        """Update labels based on the selected item in the dropdown."""
        if hasattr(self, 'data_list') and index >= 0:
            self.selected_data = self.data_list[index]
            self.db_host_name.setText(self.selected_data.get('DB hostname', ''))
            self.db_port.setText(self.selected_data.get('db port', ''))
            self.database.setText(self.selected_data.get('database', ''))
    def load_data(self):
        """Load data from the JSON file and populate the dropdown."""
        if os.path.exists(DB_FILE):
            try:
                with open(DB_FILE, 'r') as f:
                    data_list = json.load(f)
                    self.dropdown.addItems([item['title'] for item in data_list])
                    self.data_list = data_list

                    # Load default selection
                    if self.data_list:
                        self.dropdown.setCurrentIndex(0)
                        self.on_selection_changed(0)
            except json.JSONDecodeError as e:
                print(f"Error decoding JSON from {DB_FILE}: {e}", file=sys.stderr)
            except Exception as e:
                print(f"Error reading {DB_FILE}: {e}", file=sys.stderr)
        else:
            print(f"{DB_FILE} not found.", file=sys.stderr)

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
            if self.parent():
                main_window = self.parent()
                main_window.set_db_data(self.selected_data)
            self.accept()
        else:
            print("Process ID and Password cannot be empty.", file=sys.stderr)
