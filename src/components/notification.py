import sys, os
from imports import *

class Notification(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        
        self.setStyleSheet("""
            QWidget#notificationWidget {
                background-color: #741b47;
                color: #333333;
                border-radius: 10px;
                padding: 10px;
            }
            QLabel {
                color: #ffffff;
                font-size: 14px;
                background-color: transparent;
                padding: 5px;
                border-radius: 10px;
            }
        """)
        
        self.container = QWidget(self)
        self.container.setObjectName("notificationWidget")
        
        self.label = QLabel(self.container)
        self.label.setWordWrap(True)
        
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.addWidget(self.container)
        
        self.container_layout = QHBoxLayout(self.container)
        self.container_layout.addWidget(self.label)
        
        self.setFixedHeight(50)
        
        self.timer = QTimer(self)
        self.timer.setSingleShot(True)
        self.timer.timeout.connect(self.hide_animation)
        
        self.geometry_animation = QPropertyAnimation(self, b"geometry")
        self.opacity_animation = QPropertyAnimation(self, b"windowOpacity")
        self.animation_group = QParallelAnimationGroup()
        self.animation_group.addAnimation(self.geometry_animation)
        self.animation_group.addAnimation(self.opacity_animation)
        self.animation_group.finished.connect(self.on_animation_finished)

        self.is_showing = False
        self.is_hiding = False
        self.hide()

    def show_message(self, message, duration=5000):
        if self.is_showing or self.is_hiding:
            return

        self.is_showing = True
        self.label.setText(message)
        self.adjustSize()
        
        parent_rect = self.parent().rect()
        width = min(400, parent_rect.width())
        x = 20
        y = parent_rect.height() - self.height() - 20
        
        self.setGeometry(x, parent_rect.height(), width, self.height())
        self.setWindowOpacity(0)
        
        self.geometry_animation.setDuration(300)
        self.geometry_animation.setStartValue(self.geometry())
        self.geometry_animation.setEndValue(QRect(x, y, width, self.height()))
        self.geometry_animation.setEasingCurve(QEasingCurve.OutCubic)

        self.opacity_animation.setDuration(300)
        self.opacity_animation.setStartValue(0.0)
        self.opacity_animation.setEndValue(1.0)
        self.opacity_animation.setEasingCurve(QEasingCurve.OutCubic)

        self.show()
        self.animation_group.start()
        self.timer.start(duration)

    def hide_animation(self):
        if self.is_hiding:
            return

        self.is_hiding = True
        current_geometry = self.geometry()
        
        self.geometry_animation.setDuration(300)
        self.geometry_animation.setStartValue(current_geometry)
        self.geometry_animation.setEndValue(QRect(current_geometry.x(), self.parent().height(), current_geometry.width(), self.height()))
        self.geometry_animation.setEasingCurve(QEasingCurve.InCubic)

        self.opacity_animation.setDuration(300)
        self.opacity_animation.setStartValue(1.0)
        self.opacity_animation.setEndValue(0.0)
        self.opacity_animation.setEasingCurve(QEasingCurve.InCubic)

        self.animation_group.start()

    def on_animation_finished(self):
        if self.is_hiding:
            self.hide()
            self.is_hiding = False
        elif self.is_showing:
            self.is_showing = False

    def paintEvent(self, event):
        super().paintEvent(event)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setGeometry(100, 100, 800, 600)
        self.notification = Notification(self)
        
        QTimer.singleShot(1000, lambda: self.show_test_notification("First notification", 3000))
        QTimer.singleShot(2000, lambda: self.show_test_notification("Second notification", 3000))
        QTimer.singleShot(3000, lambda: self.show_test_notification("Third notification", 3000))

    def show_test_notification(self, message, duration):
        self.notification.show_message(message, duration)