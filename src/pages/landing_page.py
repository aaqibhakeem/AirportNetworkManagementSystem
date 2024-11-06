from imports import *

def create_landing_page():
    page = QWidget()
    layout = QVBoxLayout(page)

    welcome_label = QLabel("Welcome to the Airport Network Management System")
    welcome_label.setAlignment(Qt.AlignCenter)
    welcome_label.setStyleSheet("font-size: 24px; font-weight: bold; color: #ffffff;")
    layout.addWidget(welcome_label)

    description_label = QLabel("This system allows you to manage airports, airlines, flights, and routes. You can also find the shortest path between airports.")
    description_label.setAlignment(Qt.AlignCenter)
    description_label.setWordWrap(True)
    description_label.setStyleSheet("font-size: 16px; color: #ffffff; margin: 20px;")
    layout.addWidget(description_label)

    return page