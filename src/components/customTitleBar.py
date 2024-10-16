import sys, os
sys.path.append(os.path.abspath(os.path.join('..', '..', 'imports')))
from imports import *

class CustomTitleBar(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.layout = QHBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.setFixedHeight(30)

        self.title = QLabel("Airport Network Management System")
        self.title.setStyleSheet("color: white; padding-left: 3px")
        
        self.btn_minimize = QPushButton(QIcon("icons/minimize.png"), "")
        self.btn_maximize = QPushButton(QIcon("icons/maximize1.png"), "")
        self.btn_close = QPushButton(QIcon("icons/close.png"), "")

        for btn in [self.btn_minimize, self.btn_maximize, self.btn_close]:
            btn.setFixedSize(30, 30)
            btn.setStyleSheet("""
                QPushButton {
                    background-color: transparent;
                    border: none;
                }
                QPushButton:hover {
                    background-color: rgba(255, 255, 255, 30);
                }
            """)

        self.layout.addWidget(self.title)
        self.layout.addStretch()
        self.layout.addWidget(self.btn_minimize)
        self.layout.addWidget(self.btn_maximize)
        self.layout.addWidget(self.btn_close)

        self.btn_minimize.clicked.connect(self.parent.showMinimized)
        self.btn_maximize.clicked.connect(self.toggle_maximize)
        self.btn_close.clicked.connect(self.parent.close)

        self.start = QPoint(0, 0)
        self.pressing = False

    def toggle_maximize(self):
        if self.parent.isMaximized():
            self.parent.showNormal()
        else:
            self.parent.showMaximized()

    def mousePressEvent(self, event):
        self.start = self.mapToGlobal(event.position().toPoint())
        self.pressing = True

    def mouseMoveEvent(self, event):
        if self.pressing:
            end = self.mapToGlobal(event.position().toPoint())
            movement = end - self.start
            self.parent.setGeometry(self.parent.pos().x() + movement.x(),
                                    self.parent.pos().y() + movement.y(),
                                    self.parent.width(),
                                    self.parent.height())
            self.start = end

    def mouseReleaseEvent(self, event):
        self.pressing = False