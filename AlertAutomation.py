import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QAction, QToolBar, QWidget, QFormLayout, QLabel,
    QLineEdit, QPushButton, QVBoxLayout, QFileDialog, QSizePolicy, QDialog,
    QVBoxLayout, QCalendarWidget, QHBoxLayout
)
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
import json
import os

from settings_dialog import SettingsDialog
from theme import set_dark_theme
from data_window import DataWindow

DETAILS_FILE = "settings.details"
DATA_FILE = "data.env"
DB_FILE = "db.env"


class CalendarDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Select Date")
        self.setGeometry(200, 200, 300, 200)
        self.setWindowModality(Qt.ApplicationModal)

        self.calendar = QCalendarWidget(self)
        self.calendar.setGridVisible(True)
        self.calendar.clicked.connect(self.date_selected)

        self.ok_button = QPushButton("OK", self)
        self.ok_button.clicked.connect(self.accept)

        layout = QVBoxLayout()
        layout.addWidget(self.calendar)
        layout.addWidget(self.ok_button)
        self.setLayout(layout)

        self.selected_date = None

    def date_selected(self, date):
        self.selected_date = date.toString("yyyy-MM-dd")

    def get_selected_date(self):
        return self.selected_date


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.processId = ""
        self.processIDPassword = ""
        self.alert_name = ""
        self.alert_text = ""
        self.creator_id = ""
        self.category_code = ""
        self.data_file_path = ""
        self.column_name = ""
        self.remove_alert_date = ""  # New variable for remove alert date
        self.db_HostName = ""
        self.db_Port = ""
        self.database = ""

        # Window settings
        self.setWindowTitle("Alerts Automation")
        self.setGeometry(100, 100, 400, 300)
        self.setWindowIcon(QIcon("automation.png"))  # Set the window icon to automation.png

        # Create the toolbar with settings and data icons
        toolbar = QToolBar()
        self.addToolBar(Qt.TopToolBarArea, toolbar)

        # Align the icons to the right by adding a spacer
        spacer = QWidget()
        spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        toolbar.addWidget(spacer)  # Pushes the icons to the right

        # Create settings action with a gear icon
        settings_action = QAction(QIcon("gear_icon.png"), "Settings", self)
        settings_action.triggered.connect(self.open_settings)
        toolbar.addAction(settings_action)

        # Create data action with a data icon
        data_action = QAction(QIcon("data_icon.png"), "Data", self)
        data_action.triggered.connect(self.open_data_window)
        toolbar.addAction(data_action)

        toolbar.setMovable(False)
        toolbar.setStyleSheet("QToolBar { border: 0px }")  # Remove toolbar border

        # Create the central widget
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        # Load details and create the initial UI

        self.create_initial_ui()
        self.load_details()

    def create_initial_ui(self):
        layout = QVBoxLayout()

        # Create the new form elements
        self.form_layout = QFormLayout()

        # Select Data File
        self.data_file_label = QLabel("Select Data File:")
        self.browse_button = QPushButton("Browse")
        self.browse_button.clicked.connect(self.browse_file)

        # Column Name
        self.column_name_input = QLineEdit()
        self.column_name_input.textChanged.connect(self.update_column_name)

        # Select End Date
        self.end_date_label = QLabel("End Date:")
        self.select_end_date_button = QPushButton("Select End Date")
        self.select_end_date_button.clicked.connect(self.open_calendar_dialog)

        # Labels to display alert details
        self.alert_name_label = QLabel("Alert Name:")
        self.alert_name_value = QLabel()
        self.alert_text_label = QLabel("Alert Text:")
        self.alert_text_value = QLabel()
        self.creator_id_label = QLabel("Creator Id:")
        self.creator_id_value = QLabel()
        self.category_code_label = QLabel("Category Code:")
        self.category_code_value = QLabel()

        # Add widgets to form layout
        self.form_layout.addRow(self.data_file_label, self.browse_button)
        self.form_layout.addRow(QLabel("Column Name:"), self.column_name_input)
        self.form_layout.addRow(self.end_date_label, self.select_end_date_button)
        self.form_layout.addRow(self.alert_name_label, self.alert_name_value)
        self.form_layout.addRow(self.alert_text_label, self.alert_text_value)
        self.form_layout.addRow(self.creator_id_label, self.creator_id_value)
        self.form_layout.addRow(self.category_code_label, self.category_code_value)

        # Create Process and Verify buttons
        button_layout = QHBoxLayout()
        self.process_button = QPushButton("Process")
        self.verify_button = QPushButton("Verify")
        button_layout.addWidget(self.process_button)
        button_layout.addWidget(self.verify_button)

        # Add form layout and button layout to the main layout
        layout.addLayout(self.form_layout)
        layout.addLayout(button_layout)

        self.central_widget.setLayout(layout)

        # Initially hide the form and button
        self.update_ui()

    def browse_file(self):
        """Open file dialog to select an xlsx or csv file."""
        file_dialog = QFileDialog(self, "Select Data File", "", "Excel Files (*.xlsx);;CSV Files (*.csv)")
        if file_dialog.exec_():
            selected_file = file_dialog.selectedFiles()[0]
            if selected_file:
                self.data_file_path = selected_file
                self.browse_button.setText(self.data_file_path)

    def update_column_name(self, text):
        """Update the column name variable when text changes."""
        self.column_name = text

    def open_calendar_dialog(self):
        """Open calendar dialog to select a date."""
        calendar_dialog = CalendarDialog(self)
        if calendar_dialog.exec_():
            selected_date = calendar_dialog.get_selected_date()
            if selected_date:
                self.remove_alert_date = selected_date
                self.select_end_date_button.setText(selected_date)
                self.select_end_date_button.clicked.disconnect()  # Remove button click handler
                self.select_end_date_button.setEnabled(False)  # Disable button

    def load_details(self):
        """Load processId, processIDPassword, and alert data from the file on startup."""
        if os.path.exists(DETAILS_FILE):
            try:
                with open(DETAILS_FILE, 'r') as f:
                    details = json.load(f)
                    self.processId = details.get('processId', '')
                    self.processIDPassword = details.get('processIDPassword', '')
            except json.JSONDecodeError as e:
                print(f"Error decoding JSON from {DETAILS_FILE}: {e}")
            except Exception as e:
                print(f"Error loading details: {e}")

        if os.path.exists(DATA_FILE):
            try:
                with open(DATA_FILE, 'r') as f:
                    data = json.load(f)
                    if isinstance(data, list) and data:
                        first_item = data[0]
                        self.alert_name = first_item.get('Alert Name', '')
                        self.alert_text = first_item.get('Alert Text', '')
                        self.creator_id = first_item.get('Creator Id', '')
                        self.category_code = first_item.get('Category Code', '')
                        self.update_ui()
            except json.JSONDecodeError as e:
                print(f"Error decoding JSON from {DATA_FILE}: {e}")
            except Exception as e:
                print(f"Error loading data: {e}")

        if os.path.exists(DB_FILE):
            try:
                with open(DB_FILE, 'r') as f:
                    data = json.load(f)
                    if isinstance(data, list) and data:
                        first_item = data[0]
                        self.db_HostName = first_item.get('DB hostname', '')
                        self.db_Port = first_item.get('db port', '')
                        self.database = first_item.get('database', '')
                        self.update_ui()
            except json.JSONDecodeError as e:
                print(f"Error decoding JSON from {DB_FILE}: {e}")
            except Exception as e:
                print(f"Error loading data: {e}")



    def update_ui(self):
        """Update UI based on the current state."""
        # Always display the form, regardless of validations
        self.form_layout.setEnabled(True)
        self.central_widget.layout().addLayout(self.form_layout)

        # Update the alert details in the form
        self.alert_name_value.setText(self.alert_name)
        self.alert_text_value.setText(self.alert_text)
        self.creator_id_value.setText(self.creator_id)
        self.category_code_value.setText(self.category_code)

    def open_settings(self):
        """Open the settings dialog."""
        try:
            settings_dialog = SettingsDialog(self)
            if settings_dialog.exec_():
                self.update_ui()
        except Exception as e:
            print(f"Error opening settings dialog: {e}")

    def open_data_window(self):
        """Open the data window."""
        try:
            data_window = DataWindow(self)
            if data_window.exec_():
                # Fetch alert data after selecting from the data window
                self.update_ui()
        except Exception as e:
            print(f"Error opening data window: {e}")

    def set_alert_data(self, data):
        """Set alert data received from the data window."""
        self.alert_name = data.get('Alert Name', '')
        self.alert_text = data.get('Alert Text', '')
        self.creator_id = data.get('Creator Id', '')
        self.category_code = data.get('Category Code', '')
        self.update_ui()
    def set_db_data(self, data):
        """Set alert data received from the data window."""
        self.db_HostName = data.get('DB hostname', '')
        self.db_Port = data.get('db port', '')
        self.database = data.get('database', '')
        self.update_ui()
        self.print_alert_data()


if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Apply dark theme globally
    set_dark_theme(app)

    window = MainWindow()
    window.show()

    sys.exit(app.exec_())
