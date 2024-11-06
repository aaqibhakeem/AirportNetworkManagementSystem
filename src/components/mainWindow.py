import sys, os
sys.path.append(os.path.abspath(os.path.join('..', '..', 'imports')))
from imports import *
from src.components.customTitleBar import CustomTitleBar
from src.components.notification import Notification
from src.components.sideMenu import SideMenu
from src.pages.landing_page import create_landing_page
from src.pages.shortest_path_page import create_shortest_path_page
from src.pages.advanced_queries_page import create_advanced_queries_page
from src.pages.table_page import create_table_page
from src.ui.crud_form import show_crud_form
from src.ui.styles import set_styles
from dbdetails import get_connection

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowFlags(Qt.FramelessWindowHint)

        self.setWindowTitle("Airport Network Management System")
        screen = QApplication.primaryScreen().availableGeometry()
        self.setGeometry(screen)
        self.setGeometry(100, 100, 1000, 300)
        self.crud_operations = CRUDOperations()
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_layout = QVBoxLayout(self.central_widget)
        self.main_layout.setContentsMargins(0, 0, 0, 0)

        self.title_bar = CustomTitleBar(self)
        self.main_layout.addWidget(self.title_bar)

        self.content_widget = QWidget()
        self.content_layout = QHBoxLayout(self.content_widget)
        self.main_layout.addWidget(self.content_widget)

        self.side_menu = SideMenu()
        self.content_layout.addWidget(self.side_menu)

        self.notification = Notification(self)

        self.stacked_widget = QStackedWidget()
        self.content_layout.addWidget(self.stacked_widget)

        self.pages = {}
        self.create_pages()

        for button in self.side_menu.buttons:
            button.clicked.connect(self.handle_menu_button_click)

        self.landing_page = create_landing_page()
        self.stacked_widget.addWidget(self.landing_page)
        self.stacked_widget.setCurrentWidget(self.landing_page)

        set_styles(self)

    def create_pages(self):
        for table in ["Airports", "Airlines", "Flights", "Routes", "Shortest Path", "Advanced"]:
            if table == "Shortest Path":
                page = create_shortest_path_page(self)
            elif table == "Advanced":
                page = create_advanced_queries_page(self)
            else:
                page = create_table_page(table, self)
            self.pages[table] = page
            self.stacked_widget.addWidget(page)

    def handle_menu_button_click(self):
        button = self.sender()
        
        if not hasattr(button, 'clicked_once'):
            button.clicked_once = False

        if button.clicked_once:
            button.setChecked(False)
            button.clicked_once = False
            self.stacked_widget.setCurrentWidget(self.landing_page)
        else:
            for btn in self.side_menu.buttons:
                if btn != button:
                    btn.setChecked(False)
                    btn.clicked_once = False
            
            button.setChecked(True)
            button.clicked_once = True
            
            table = button.original_text
            if table in self.pages:
                current_page = self.pages[table]
                self.stacked_widget.setCurrentWidget(current_page)
                
                if table not in ["Shortest Path", "Advanced"] and hasattr(current_page, 'table_widget'):
                    self.populate_table(table, current_page.table_widget)
            else:
                print(f"Warning: '{table}' page not found")
                self.notification.show_message(f"Page '{table}' is not available.")

    def handle_crud_operation(self, operation, table):
        crud_buttons = self.find_crud_buttons(self.pages[table])
        for btn in crud_buttons:
            if btn.text() != operation:
                btn.setChecked(False)
        
        if table == "Routes" and operation == "Create":
            self.stacked_widget.setCurrentWidget(self.pages["Shortest Path"])
            for btn in self.side_menu.buttons:
                if btn.text() == "Routes":
                    btn.setChecked(False)
                    btn.clicked_once = False
                elif btn.text() == "Shortest Path":
                    btn.setChecked(True)
                    btn.clicked_once = True
        elif operation != "Read" and not (table == "Routes" and operation == "Update"):
            show_crud_form(self, operation, table)

    def find_crud_buttons(self, page):
        crud_buttons = []
        for child in page.findChildren(QPushButton):
            if child.text() in ["Create", "Update", "Delete"]:
                crud_buttons.append(child)
        return crud_buttons

    def filter_table(self, table):
        current_page = self.pages[table]
        search_text = current_page.search_bar.text().lower()
        table_widget = current_page.table_widget
        
        for row in range(table_widget.rowCount()):
            match = False
            for column in range(table_widget.columnCount()):
                item = table_widget.item(row, column)
                if item and search_text in item.text().lower():
                    match = True
                    break
            table_widget.setRowHidden(row, not match)

    def populate_table(self, table, table_widget):
        records = []
        if table == "Airports":
            records = self.crud_operations.read_airports()
        elif table == "Airlines":
            records = self.crud_operations.read_airlines()
        elif table == "Flights":
            records = self.crud_operations.read_flights()
        elif table == "Routes":
            records = self.crud_operations.read_routes()

        if not records:
            table_widget.setRowCount(0)
            table_widget.setColumnCount(0)
            return

        table_widget.setRowCount(len(records))
        table_widget.setColumnCount(len(records[0]))

        headers = self.get_fields_for_table(table)
        table_widget.setHorizontalHeaderLabels([h[0] for h in headers])

        for row, record in enumerate(records):
            for col, value in enumerate(record):
                table_widget.setItem(row, col, QTableWidgetItem(str(value)))

        table_widget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

    def get_fields_for_table(self, table):
        fields = {
            "Airports": [
                ("Airport Code", "airport_code"),
                ("Airport Name", "airport_name"),
                ("Latitude", "latitude_deg"),
                ("Longitude", "longitude_deg"),
                ("State", "state"),
                ("City", "city")
            ],
            "Airlines": [
                ("Airline Code", "airline_code"),
                ("Airline Name", "airline_name"),
                ("Headquarters", "headquarters"),
                ("Fleet Size", "fleet_size"),
                ("Country", "country")
            ],
            "Flights": [
                ("Flight ID", "flight_id"),
                ("Airline Code", "airline_code"),
                ("Source Airport", "source_airport"),
                ("Destination Airport", "destination_airport"),
                ("Latitude", "latitude_deg"),
                ("Longitude", "longitude_deg"),
                ("Timestamp", "timestamp")
            ],
            "Routes": [
                ("Route ID", "route_id"),
                ("Source Airport", "source_airport"),
                ("Destination Airport", "destination_airport"),
                ("Distance", "distance"),
                ("Duration", "duration"),
                ("Stopovers", "stopovers")
            ]
        }
        return fields.get(table, [])

    def handle_crud_action(self, operation, table):
        if operation == "Create":
            if table == "Airports":
                airport_code = self.form_fields['airport_code'].text().strip() or None
                airport_name = self.form_fields['airport_name'].text().strip() or None
                latitude = self.form_fields['latitude_deg'].text().strip() or None
                longitude = self.form_fields['longitude_deg'].text().strip() or None
                state = self.form_fields['state'].text().strip() or None
                city = self.form_fields['city'].text().strip() or None
                
                if not airport_code:
                    raise ValueError("Airport code is required")
                
                self.crud_operations.create_airport(
                    airport_code, airport_name, latitude, longitude, state, city
                )
                
            elif table == "Airlines":
                airline_code = self.form_fields['airline_code'].text().strip() or None
                airline_name = self.form_fields['airline_name'].text().strip() or None
                headquarters = self.form_fields['headquarters'].text().strip() or None
                fleet_size = self.form_fields['fleet_size'].text().strip() or None
                country = self.form_fields['country'].text().strip() or None
                
                if not airline_code:
                    raise ValueError("Airline code is required")
                
                self.crud_operations.create_airline(
                    airline_code, airline_name, headquarters, fleet_size, country
                )

            elif table == "Flights":
                flight_id = self.form_fields['flight_id'].text().strip() or None
                airline_code = self.form_fields['airline_code'].text().strip() or None
                source_airport = self.form_fields['source_airport'].text().strip() or None
                destination_airport = self.form_fields['destination_airport'].text().strip() or None
                latitude = self.form_fields['latitude_deg'].text().strip() or None
                longitude = self.form_fields['longitude_deg'].text().strip() or None
                timestamp = self.form_fields['timestamp'].text().strip() or None

                if not flight_id:
                    raise ValueError("Flight ID is required")
                
                self.crud_operations.create_flight(
                    flight_id, airline_code, source_airport, destination_airport, latitude, longitude, timestamp
                )

        elif operation == "Update":
            if table == "Airports":
                airport_code = self.form_fields['airport_code'].text().strip()
                if not airport_code:
                    raise ValueError("Airport code is required for update")
                
                self.crud_operations.update_airport(
                    airport_code,
                    new_airport_name=self.form_fields['airport_name'].text().strip() or None,
                    new_latitude=self.form_fields['latitude_deg'].text().strip() or None,
                    new_longitude=self.form_fields['longitude_deg'].text().strip() or None,
                    new_state=self.form_fields['state'].text().strip() or None,
                    new_city=self.form_fields['city'].text().strip() or None
                )
                
            elif table == "Airlines":
                airline_code = self.form_fields['airline_code'].text().strip()
                if not airline_code:
                    raise ValueError("Airline code is required for update")
                
                self.crud_operations.update_airline(
                    airline_code,
                    new_airline_name=self.form_fields['airline_name'].text().strip() or None,
                    new_headquarters=self.form_fields['headquarters'].text().strip() or None,
                    new_fleet_size=self.form_fields['fleet_size'].text().strip() or None,
                    new_country=self.form_fields['country'].text().strip() or None
                )
            
            elif table == "Flights":
                flight_id = self.form_fields['flight_id'].text().strip() or None
                if not flight_id:
                    raise ValueError("Flight ID is required")
                
                self.crud_operations.update_flight(
                    flight_id,
                    new_airline_code=self.form_fields['airline_code'].text().strip() or None,
                    new_source_airport=self.form_fields['source_airport'].text().strip() or None,
                    new_destination_airport=self.form_fields['destination_airport'].text().strip() or None,
                    new_latitude=self.form_fields['latitude_deg'].text().strip() or None,
                    new_longitude=self.form_fields['longitude_deg'].text().strip() or None,
                    new_timestamp=self.form_fields['timestamp'].text().strip() or None
                )

        elif operation == "Delete":
            primary_key_field = self.get_primary_key_field(table)
            primary_key_value = self.form_fields[primary_key_field].text().strip()
            
            if not primary_key_value:
                raise ValueError(f"{primary_key_field.replace('_', ' ').title()} is required for deletion")
            
            if table == "Airports":
                self.crud_operations.delete_airport(primary_key_value)
            elif table == "Airlines":
                self.crud_operations.delete_airline(primary_key_value)
            elif table == "Flights":
                self.crud_operations.delete_flight(primary_key_value)
            elif table == "Routes":
                self.crud_operations.delete_route(primary_key_value)

        self.notification.show_message(f"{operation} operation completed successfully.")
        self.stacked_widget.setCurrentWidget(self.pages[table])

    def get_primary_key_field(self, table):
        primary_keys = {
            "Airports": "airport_code",
            "Airlines": "airline_code",
            "Flights": "flight_id",
            "Routes": "route_id"
        }
        return primary_keys.get(table, "")

    def change_page(self, new_page):
        """Transitions to a new page with animation."""
        current_index = self.stacked_widget.currentIndex()
        new_index = self.stacked_widget.indexOf(new_page)

        self.animation = QPropertyAnimation(self.stacked_widget, b"geometry")
        self.animation.setDuration(500)
        if new_index > current_index:
            self.animation.setStartValue(QRect(self.stacked_widget.width(), 0, self.stacked_widget.width(), self.stacked_widget.height()))
            self.animation.setEndValue(QRect(0, 0, self.stacked_widget.width(), self.stacked_widget.height()))
        else:
            self.animation.setStartValue(QRect(-self.stacked_widget.width(), 0, self.stacked_widget.width(), self.stacked_widget.height()))
            self.animation.setEndValue(QRect(0, 0, self.stacked_widget.width(), self.stacked_widget.height()))

        self.stacked_widget.setCurrentWidget(new_page)
        self.animation.start()
        
    def find_shortest_path(self):
        source = self.source_airport.currentData()
        destination = self.destination_airport.currentData()
        num_vias = self.stopovers.value()

        try:
            airports = load_airport_coordinates()
            G = create_graph_from_airports(airports)

            if num_vias == 0:
                shortest_paths = ShortestPathAlgorithms.compute_all_shortest_paths(G, source, destination)
                shortest_path_algorithm = min(shortest_paths, key=lambda k: shortest_paths[k][1])
                self.shortest_path, self.shortest_distance = shortest_paths[shortest_path_algorithm]
            else:
                self.shortest_path, self.shortest_distance = ShortestPathAlgorithms.compute_shortest_path_with_exact_vias(G, source, destination, num_vias)

            details = f"Shortest path: {' → '.join(self.shortest_path)}\n"
            details += f"Total distance: {self.shortest_distance:.2f} km\n"
            details += f"Number of stopovers: {len(self.shortest_path) - 2}\n"
            details += "Visualization building...\n"
            details += "Please check your browser for the interactive map."

            self.path_details_box.setPlainText(details)

            self.store_route_button.setVisible(True)
            self.notification.show_message(f"Shortest path found: {' → '.join(self.shortest_path)}")

            fig = draw_graph(G, [self.shortest_path])
            plotly.offline.plot(fig, filename='shortest_path_map.html', auto_open=True)

        except Exception as e:
            error_message = f"An error occurred while finding the shortest path: {str(e)}"
            self.notification.show_message(error_message)
            self.path_details_box.setPlainText(error_message)
            print(error_message)

    def store_route(self):
        source = self.source_airport.currentData()
        destination = self.destination_airport.currentData()
        num_vias = self.stopovers.value()
        
        conn = get_connection()
        ask_add_route_to_db(source, destination, self.shortest_path, self.shortest_distance, num_vias, None, conn)
        conn.close()

        self.notification.show_message("Route stored successfully")

    def read_flight_logs(self):
        self.crud_operations.get_db_connection()
        self.crud_operations.cursor.execute("SELECT * FROM FlightLogs ORDER BY timestamp DESC")
        logs = self.crud_operations.cursor.fetchall()
        self.crud_operations.close_db_connection()
        return logs

    def show_flight_logs(self):
        logs = self.read_flight_logs()
        self.display_results(logs, ["Log ID", "Flight ID", "Action", "Timestamp"])

    def show_flights_with_airline_info(self):
        results = self.crud_operations.get_flights_with_airline_info()
        self.display_results(results, ["Flight ID", "Source", "Destination", "Airline", "Headquarters"])

    def show_airport_flight_counts(self):
        results = self.crud_operations.get_airport_flight_counts()
        self.display_results(results, ["Airport Code", "Airport Name", "Flight Count"])

    def show_busiest_airports(self):
        results = self.crud_operations.get_busiest_airports()
        self.display_results(results, ["Airport Code", "Airport Name", "Total Flights"])

    def clear_flight_logs(self):
        try:
            conn = get_connection()  
            cursor = conn.cursor()
            cursor.execute("DELETE FROM FlightLogs")
            conn.commit()
            cursor.close()
            conn.close()
            
            self.results_table.setRowCount(0)
            self.results_table.setColumnCount(0)
            
            self.notification.show_message("Flight logs cleared successfully")
        except Exception as e:
            self.notification.show_message(f"Error clearing flight logs: {str(e)}") 
            
    def display_results(self, results, headers):
        self.results_table.setRowCount(len(results))
        self.results_table.setColumnCount(len(headers))
        self.results_table.setHorizontalHeaderLabels(headers)

        for row, record in enumerate(results):
            for col, value in enumerate(record):
                self.results_table.setItem(row, col, QTableWidgetItem(str(value)))

        self.results_table.resizeColumnsToContents()
        self.results_table.show()