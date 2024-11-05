import sys, os
sys.path.append(os.path.abspath(os.path.join('..', '..', 'imports')))
from imports import *
from src.components.sideMenuButton import SideMenuButton

class SideMenu(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedWidth(200)
        self.setStyleSheet("background-color: #702963;")
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(5)

        self.buttons = []
        icons = [
            (QIcon("icons/airports.png"), QIcon("icons/airports.png")),
            (QIcon("icons/airlines.png"), QIcon("icons/airlines.png")),
            (QIcon("icons/flights.png"), QIcon("icons/flights.png")),
            (QIcon("icons/routes.png"), QIcon("icons/routes.png")),
            (QIcon("icons/shortestpath.png"), QIcon("icons/shortestpath.png")),
            (QIcon("icons/advanced.png"), QIcon("icons/advanced.png"))  # Added icon for Advanced
        ]
        
        menu_items = ["Airports", "Airlines", "Flights", "Routes", "Shortest Path", "Advanced"]
        
        for table, (icon, collapsed_icon) in zip(menu_items, icons):
            btn = SideMenuButton(table, icon, collapsed_icon)
            self.buttons.append(btn)
            layout.addWidget(btn)

        layout.addStretch()

        self.toggle_button = QPushButton(QIcon("icons/menu.png"), "")
        self.toggle_button.setStyleSheet("""
            QPushButton {
                background-color: #201640;
                border: none;
                font-size: 24px;
            }
        """)
        self.toggle_button.clicked.connect(self.toggle_menu)
        layout.addWidget(self.toggle_button)

        self.animation = QPropertyAnimation(self, b"minimumWidth")
        self.animation.setDuration(300)
        self.animation.setEasingCurve(QEasingCurve.InOutQuad)

    def toggle_menu(self):
        if self.width() == 200:
            self.animation.setStartValue(200)
            self.animation.setEndValue(50)
            for button in self.buttons:
                button.setText("")
                button.setCollapsed(True)
        else:
            self.animation.setStartValue(50)
            self.animation.setEndValue(200)
            for button, text in zip(self.buttons, ["Airports", "Airlines", "Flights", "Routes", "Shortest Path", "Advanced"]):
                button.setText(text)
                button.setCollapsed(False)
        self.animation.start()