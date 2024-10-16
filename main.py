from imports import *
from src.components.customTitleBar import CustomTitleBar
from src.components.mainWindow import MainWindow
from src.components.notification import Notification
from src.components.sideMenu import SideMenu
from src.components.sideMenuButton import SideMenuButton

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())