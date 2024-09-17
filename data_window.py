import json
import os
import sys
from PyQt5.QtWidgets import QDialog, QFormLayout, QLabel, QComboBox, QPushButton, QVBoxLayout, QWidget
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt

DATA_FILE = "data.env"


class DataWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Select Alert Type")  # Set the window title
        self.setGeometry(100, 100, 300, 250)
        self.setWindowIcon(QIcon("data_window_title.png"))  # Set the window icon to data_window_title.png

        self.selected_data = {}

        # Dropdown for titles
        self.dropdown = QComboBox()
        self.dropdown.currentIndexChanged.connect(self.on_selection_changed)

        # Non-interactive text fields replaced with simple labels
        self.alert_name_label = QLabel()
        self.alert_text_label = QLabel()
        self.creator_id_label = QLabel()
        self.category_code_label = QLabel()

        # Load data from file
        try:
            self.load_data()
        except Exception as e:
            print(f"Error loading data: {e}", file=sys.stderr)

        # Configure button
        self.configure_button = QPushButton("Configure")
        self.configure_button.clicked.connect(self.configure)

        # Layout
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Select Alert Type"))
        layout.addWidget(self.dropdown)
        layout.addSpacing(10)  # Add space after dropdown

        # Form layout for the fields
        form_layout = QFormLayout()
        form_layout.addRow(QLabel("Alert Name:"), self.alert_name_label)
        form_layout.addRow(QLabel("Alert Text:"), self.alert_text_label)
        form_layout.addRow(QLabel("Creator Id:"), self.creator_id_label)
        form_layout.addRow(QLabel("Category Code:"), self.category_code_label)

        # Create a container widget to handle spacing
        form_container = QWidget()
        form_container.setLayout(form_layout)

        # Add spacing to form container
        layout.addWidget(form_container)
        layout.addSpacing(10)  # Add space before the Configure button
        layout.addWidget(self.configure_button)

        self.setLayout(layout)

        # Set fixed size for the data window
        self.setFixedSize(self.size())

    def load_data(self):
        """Load data from the JSON file and populate the dropdown."""
        if os.path.exists(DATA_FILE):
            try:
                with open(DATA_FILE, 'r') as f:
                    data_list = json.load(f)
                    self.dropdown.addItems([item['title'] for item in data_list])
                    self.data_list = data_list

                    # Load default selection
                    if self.data_list:
                        self.dropdown.setCurrentIndex(0)
                        self.on_selection_changed(0)
            except json.JSONDecodeError as e:
                print(f"Error decoding JSON from {DATA_FILE}: {e}", file=sys.stderr)
            except Exception as e:
                print(f"Error reading {DATA_FILE}: {e}", file=sys.stderr)
        else:
            print(f"{DATA_FILE} not found.", file=sys.stderr)

    def on_selection_changed(self, index):
        """Update labels based on the selected item in the dropdown."""
        if hasattr(self, 'data_list') and index >= 0:
            self.selected_data = self.data_list[index]
            self.alert_name_label.setText(self.selected_data.get('Alert Name', ''))
            self.alert_text_label.setText(self.selected_data.get('Alert Text', ''))
            self.creator_id_label.setText(self.selected_data.get('Creator Id', ''))
            self.category_code_label.setText(self.selected_data.get('Category Code', ''))

    def configure(self):
        """Pass the selected data to the main window."""
        if self.parent():
            main_window = self.parent()
            main_window.set_alert_data(self.selected_data)
        self.accept()
