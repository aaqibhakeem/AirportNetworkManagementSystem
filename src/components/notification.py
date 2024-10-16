import sys, os
sys.path.append(os.path.abspath(os.path.join('..', '..', 'imports')))
from imports import *

class Notification(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet("""
            Notification {
                font-size: 14px;
                background-color: #87CEFA;
                color: #333333;
                border-radius: 10px;
                padding: 10px;
            }
            QLabel {
                background-color: transparent;
            }
        """)
        self.label = QLabel(self)
        layout = QHBoxLayout(self)
        layout.addWidget(self.label)
        self.setFixedHeight(50)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.hide_animation)
        self.animation = QPropertyAnimation(self, b"geometry")

    def show_message(self, message, duration=5000):
        self.label.setText(message)
        self.adjustSize()
        self.show()
        self.animation.setDuration(300)
        self.animation.setStartValue(QRect(0, self.parent().height(), self.width(), self.height()))
        self.animation.setEndValue(QRect(0, self.parent().height() - self.height(), self.width(), self.height()))
        self.animation.setEasingCurve(QEasingCurve.OutCubic)
        self.animation.start()
        self.timer.start(duration)

    def hide_animation(self):
        self.animation.setDuration(300)
        self.animation.setStartValue(QRect(0, self.parent().height() - self.height(), self.width(), self.height()))
        self.animation.setEndValue(QRect(0, self.parent().height(), self.width(), self.height()))
        self.animation.setEasingCurve(QEasingCurve.InCubic)
        self.animation.start()
        self.timer.stop()