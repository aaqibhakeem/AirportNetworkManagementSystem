from imports import *

def create_table_page(table, main_window):
    page = QWidget()
    layout = QVBoxLayout(page)

    crud_layout = QHBoxLayout()
    crud_buttons = []
    for operation in ["Create", "Update", "Delete"]:
        if table == "Routes" and operation == "Update":
            continue
        btn = QPushButton(operation)
        btn.setCheckable(True)
        btn.clicked.connect(lambda checked, op=operation, t=table: main_window.handle_crud_operation(op, t))
        btn.setStyleSheet("""
            QPushButton {
                background-color: #483248;
                color: white;
                border: none;
                padding: 10px;
                border-radius: 5px;
                font-size: 14px;
            }
            QPushButton:pressed {
                background-color: #702963;
            }
        """)
        crud_buttons.append(btn)
        crud_layout.addWidget(btn)
    layout.addLayout(crud_layout)

    search_bar = QLineEdit()
    search_bar.setPlaceholderText("Search...")
    search_bar.textChanged.connect(lambda: main_window.filter_table(table))
    layout.addWidget(search_bar)

    table_widget = QTableWidget()
    layout.addWidget(table_widget)

    page.table_widget = table_widget
    page.search_bar = search_bar

    return page