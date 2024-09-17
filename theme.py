def set_dark_theme(app):
    """Apply dark theme globally to the application."""
    dark_style = """
        QMainWindow {
            background-color: #2e2e2e;
        }
        QToolBar {
            background-color: #2e2e2e;
        }
        QLabel {
            color: white;
            font-size: 14px;
        }
        QLineEdit {
            background-color: #3c3c3c;
            color: white;
            border: 1px solid #5a5a5a;
            padding: 5px;
            border-radius: 5px;
        }
        QPushButton {
            background-color: #3c3c3c;
            color: white;
            border: 1px solid #5a5a5a;
            padding: 7px 15px;
            border-radius: 5px;
        }
        QPushButton:hover {
            background-color: #5a5a5a;
        }
        QDialog {
            background-color: #2e2e2e;
        }
        QDialogButtonBox QPushButton {
            background-color: #3c3c3c;
            color: white;
        }
        QDialogButtonBox QPushButton:hover {
            background-color: #5a5a5a;
        }
        QToolBar QToolButton {
            background-color: transparent;
            color: white;
        }
        QToolBar QToolButton:hover {
            background-color: #5a5a5a;
        }
        QComboBox {
            background-color: #3c3c3c;
            color: white;
            border: 1px solid #5a5a5a;
            padding: 5px;
            border-radius: 5px;
        }
        QComboBox::drop-down {
            background-color: #3c3c3c;
            border-left: 1px solid #5a5a5a;
        }
        QComboBox QAbstractItemView {
            background-color: #3c3c3c;
            color: white;
            border: 1px solid #5a5a5a;
        }
        QComboBox QAbstractItemView::item:selected {
            background-color: #5a5a5a;
        }
    """
    app.setStyleSheet(dark_style)
