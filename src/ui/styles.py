def set_styles(main_window):
    main_window.setStyleSheet("""
        * {
            color: black;
        }
        QMainWindow, QWidget {
            background-color: #5c4ca4;
            border-radius: 10px;
        }
        QLabel {
            color: #ffffff;
        }
        QPushButton {
            background-color: #483248;
            color: white;
            border: none;
            padding: 10px;
            border-radius: 5px;
            font-size: 14px;
        }
        QPushButton:checked {
            background-color: #702963;
        }
        QPushButton:hover {
            background-color: #301934;
        }
        QLineEdit, QTableWidget {
            border: 1px solid #bdc3c7;
            border-radius: 5px;
            padding: 5px;
            background-color: #ffffff;
        }
        QTableWidget {
            gridline-color: #d0d0d0;
        }
        QHeaderView::section {
            background-color: #201640;
            color: white;
            padding: 5px;
            border: 1px solid #301934;
        }
        QComboBox, QSpinBox {
            background-color: #ffffff;
            border: 1px solid #bdc3c7;
            border-radius: 5px;
            padding: 5px;
            min-height: 30px;
            font-size: 14px;
        }
        QComboBox::drop-down, QSpinBox::up-button, QSpinBox::down-button {
            width: 30px;
        }
        QScrollBar:vertical, QScrollBar:horizontal {
            background-color: #ffffff;
            width: 10px;
            height: 10px;
            border-radius: 2px;
            padding-left: 6px;
        }
        QScrollBar::handle:vertical, QScrollBar::handle:horizontal {
            background-color: #201640;
            border-radius: 2px;
        }
        QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical,
        QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {
            height: 0px;
            width: 0px;
        }
    """)