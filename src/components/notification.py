import sys, os
sys.path.append(os.path.abspath(os.path.join('..', '..', 'imports')))
from imports import *

class Notification(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        # Set window flags to remove window frame and stay on top
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
        
        # Create main container widget to apply styles
        self.container = QWidget(self)
        self.container.setObjectName("notificationWidget")
        
        # Create and style the label
        self.label = QLabel(self.container)
        self.label.setWordWrap(True)
        
        # Setup layout
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.addWidget(self.container)
        
        self.container_layout = QHBoxLayout(self.container)
        self.container_layout.addWidget(self.label)
        
        # Set fixed height but allow for width adjustment
        self.setFixedHeight(50)
        
        # Setup animations and timer
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.hide_animation)
        self.geometry_animation = QPropertyAnimation(self, b"geometry")
        self.opacity_animation = QPropertyAnimation(self, b"windowOpacity")
        self.animation_group = QParallelAnimationGroup()
        self.animation_group.addAnimation(self.geometry_animation)
        self.animation_group.addAnimation(self.opacity_animation)

        # Initially hide the notification
        self.hide()

    def show_message(self, message, duration=5000):
        self.label.setText(message)
        self.adjustSize()
        
        # Calculate the position to appear at the bottom left of the parent window
        parent_rect = self.parent().rect()
        width = min(400, parent_rect.width())  # Limit maximum width
        x = 20  # 20 pixel offset from left edge
        y = parent_rect.height() - self.height() - 20  # 20 pixel offset from bottom edge
        
        # Set the initial position off-screen
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

        # Show the widget before starting the animation
        self.show()
        self.animation_group.start()
        self.timer.start(duration)

    def hide_animation(self):
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
        self.animation_group.finished.connect(self.hide)
        self.timer.stop()