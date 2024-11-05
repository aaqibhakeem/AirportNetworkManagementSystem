from imports import *
from src.components.mainWindow import MainWindow
from src.crud import CRUDOperations

if __name__ == "__main__":
    crud = CRUDOperations()
    crud.ensure_flight_logs_table_exists()
    crud.create_flight_log_trigger()
    crud.create_update_route_duration_procedure()
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())