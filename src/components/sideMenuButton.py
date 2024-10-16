import sys, os
sys.path.append(os.path.abspath(os.path.join('..', '..', 'imports')))
from imports import *

class SideMenuButton(QPushButton):
    def __init__(self, text, icon, collapsed_icon, parent=None):
        super().__init__(text, parent)
        self.setIcon(icon)
        self.collapsed_icon = collapsed_icon
        self.original_text = text
        self.setIconSize(QSize(24, 24))
        self.setCheckable(True)
        self.setFixedHeight(50)
        self.setStyleSheet("""
            QPushButton {
                border: none;
                border-radius: 5px;
                text-align: left;
                padding-left: 10px;
                color: #ffffff;
                background-color: #483248;
            }
            QPushButton:hover {
                background-color: #301934;
            }
            QPushButton:checked {
                background-color: #702963;
            }
        """)

    def setCollapsed(self, collapsed):
        if collapsed:
            self.setIcon(self.collapsed_icon)
            self.setText("")
        else:
            self.setIcon(self.icon())
            self.setText(self.original_text)