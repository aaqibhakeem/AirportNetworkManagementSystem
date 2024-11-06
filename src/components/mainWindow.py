import sys, os
sys.path.append(os.path.abspath(os.path.join('..', '..', 'imports')))
from imports import *
from src.components.customTitleBar import CustomTitleBar
from src.components.notification import Notification
from src.components.sideMenu import SideMenu
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

        # Add custom title bar
        self.title_bar = CustomTitleBar(self)
        self.main_layout.addWidget(self.title_bar)

        # Create content widget
        self.content_widget = QWidget()
        self.content_layout = QHBoxLayout(self.content_widget)
        self.main_layout.addWidget(self.content_widget)

        # Create and add side menu
        self.side_menu = SideMenu()
        self.content_layout.addWidget(self.side_menu)

        self.notification = Notification(self)

        # Create stacked widget for main content
        self.stacked_widget = QStackedWidget()
        self.content_layout.addWidget(self.stacked_widget)

        # Create pages
        self.pages = {}
        self.create_pages()

        # Connect side menu buttons
        for button in self.side_menu.buttons:
            button.clicked.connect(self.handle_menu_button_click)

        self.landing_page = self.create_landing_page()
        self.stacked_widget.addWidget(self.landing_page)
        self.stacked_widget.setCurrentWidget(self.landing_page)

        # Apply global stylesheet
        self.setStyleSheet("""
            * {
                color: black;
            }
            QMainWindow, QWidget {
                background-color: #5c4ca4;
                border-radius: 10px;
            }
            QLabel {
                color: #ffffff;
            }
            QPushButton {
                background-color: #483248;
                color: white;
                border: none;
                padding: 10px;
                border-radius: 5px;
                font-size: 14px;
            }
            QPushButton:checked {
                background-color: #702963;
            }
            QPushButton:hover {
                background-color: #301934;
            }
            QLineEdit, QTableWidget {
                border: 1px solid #bdc3c7;
                border-radius: 5px;
                padding: 5px;
                background-color: #ffffff;
            }
            QTableWidget {
                gridline-color: #d0d0d0;
            }
            QHeaderView::section {
                background-color: #201640;
                color: white;
                padding: 5px;
                border: 1px solid #301934;
            }
            QComboBox, QSpinBox {
                background-color: #ffffff;
                border: 1px solid #bdc3c7;
                border-radius: 5px;
                padding: 5px;
                min-height: 30px;
                font-size: 14px;
            }
            QComboBox::drop-down, QSpinBox::up-button, QSpinBox::down-button {
                width: 30px;
            }
            QScrollBar:vertical, QScrollBar:horizontal {
                background-color: #ffffff;
                width: 10px;
                height: 10px;
                border-radius: 2px;
                padding-left: 6px;
            }
            QScrollBar::handle:vertical, QScrollBar::handle:horizontal {
                background-color: #201640;
                border-radius: 2px;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical,
            QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {
                height: 0px;
                width: 0px;
            }
        """)

    def create_landing_page(self):
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

    def create_shortest_path_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)

        # Airport selection
        airport_form = QFormLayout()
        self.source_airport = QComboBox()
        self.destination_airport = QComboBox()
        self.stopovers = QSpinBox()
        self.stopovers.setRange(0, 10)
        self.source_airport.setFixedWidth(500)
        self.destination_airport.setFixedWidth(500)
        self.stopovers.setFixedWidth(100)
        
        self.source_airport.setStyleSheet("QComboBox::drop-down {border-width: 0px;} QComboBox::down-arrow {image: url(noimg); border-width: 0px;}")
        self.destination_airport.setStyleSheet("QComboBox::drop-down {border-width: 0px;} QComboBox::down-arrow {image: url(noimg); border-width: 0px;}")
        self.stopovers.setStyleSheet("QSpinBox::up-button, QSpinBox::down-button {width: 0px;}")
        
        airport_form.addRow("Source Airport:", self.source_airport)
        airport_form.addRow("Destination Airport:", self.destination_airport)
        airport_form.addRow("Number of Stopovers:", self.stopovers)
        layout.addLayout(airport_form)

        # Populate airport dropdowns
        airports = self.crud_operations.read_airports()
        for airport in airports:
            self.source_airport.addItem(f"{airport[0]} - {airport[1]}", airport[0])
            self.destination_airport.addItem(f"{airport[0]} - {airport[1]}", airport[0])

        # Find path button
        find_path_button = QPushButton("Find Shortest Path")
        find_path_button.clicked.connect(self.find_shortest_path)
        layout.addWidget(find_path_button)

        # White box for path details
        self.path_details_box = QTextEdit()
        self.path_details_box.setReadOnly(True)
        self.path_details_box.setStyleSheet("background-color: white; color: black; border: 1px solid #bdc3c7; border-radius: 5px; padding: 5px;")
        self.path_details_box.setFixedHeight(150)
        layout.addWidget(self.path_details_box)

        # Map display
        self.map_view = QGraphicsView()
        self.map_view.setMinimumHeight(400)
        layout.addWidget(self.map_view)

        # Store route button
        self.store_route_button = QPushButton("Store Route")
        self.store_route_button.clicked.connect(self.store_route)
        self.store_route_button.setVisible(False)
        layout.addWidget(self.store_route_button)

        return page

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

            # Display path details in the white box
            details = f"Shortest path: {' → '.join(self.shortest_path)}\n"
            details += f"Total distance: {self.shortest_distance:.2f} km\n"
            details += f"Number of stopovers: {len(self.shortest_path) - 2}\n"
            details += "Visualization building...\n"
            details += "Please check your browser for the interactive map."

            self.path_details_box.setPlainText(details)

            self.store_route_button.setVisible(True)
            self.notification.show_message(f"Shortest path found: {' → '.join(self.shortest_path)}")

            # Create and display the plotly map in a browser
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
        
        # Use the existing code from main.py to store the route
        conn = get_connection()
        ask_add_route_to_db(source, destination, self.shortest_path, self.shortest_distance, num_vias, None, conn)
        conn.close()

        self.notification.show_message("Route stored successfully")

    def create_pages(self):
        for table in ["Airports", "Airlines", "Flights", "Routes", "Shortest Path", "Advanced"]:
            if table == "Shortest Path":
                page = self.create_shortest_path_page()
            elif table == "Advanced":
                page = self.create_advanced_queries_page()
            else:
                page = self.create_table_page(table)
            self.pages[table] = page
            self.stacked_widget.addWidget(page)

    def create_advanced_queries_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)

        # Flights with Airline Info
        flights_button = QPushButton("Show Flights with Airline Info")
        flights_button.clicked.connect(self.show_flights_with_airline_info)
        layout.addWidget(flights_button)

        # Airport Flight Counts
        airport_counts_button = QPushButton("Show Airport Flight Counts")
        airport_counts_button.clicked.connect(self.show_airport_flight_counts)
        layout.addWidget(airport_counts_button)

        # Routes with Stopover Count
        routes_button = QPushButton("Show Routes with Stopover Count")
        routes_button.clicked.connect(self.show_routes_with_stopover_count)
        layout.addWidget(routes_button)

        # Flight Logs buttons container
        log_buttons_layout = QHBoxLayout()
        
        # Flight Logs
        flight_log_button = QPushButton("Show Flight Log")
        flight_log_button.clicked.connect(self.show_flight_logs)
        log_buttons_layout.addWidget(flight_log_button)
        
        # Clear Flight Logs
        clear_log_button = QPushButton("Clear Flight Log")
        clear_log_button.clicked.connect(self.clear_flight_logs)
        clear_log_button.setStyleSheet("""
            QPushButton {
                background-color: #e74c3c;
                color: white;
                border: none;
                padding: 10px;
                border-radius: 5px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #c0392b;
            }
        """)
        log_buttons_layout.addWidget(clear_log_button)
        
        layout.addLayout(log_buttons_layout)

        # Results Table
        self.results_table = QTableWidget()
        layout.addWidget(self.results_table)

        return page

    def clear_flight_logs(self):
        try:
            conn = get_connection()  # Get a new connection from dbdetails
            cursor = conn.cursor()
            cursor.execute("DELETE FROM FlightLogs")
            conn.commit()
            cursor.close()
            conn.close()
            
            # Clear the table if it's currently displaying logs
            self.results_table.setRowCount(0)
            self.results_table.setColumnCount(0)
            
            # Show success notification
            self.notification.show_message("Flight logs cleared successfully")
        except Exception as e:
            # Show error notification
            self.notification.show_message(f"Error clearing flight logs: {str(e)}")

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

    def show_routes_with_stopover_count(self):
        results = self.crud_operations.get_routes_with_stopover_count()
        self.display_results(results, ["Route ID", "Source", "Destination", "Stopover Count"])

    def display_results(self, results, headers):
        self.results_table.setRowCount(len(results))
        self.results_table.setColumnCount(len(headers))
        self.results_table.setHorizontalHeaderLabels(headers)

        for row, record in enumerate(results):
            for col, value in enumerate(record):
                self.results_table.setItem(row, col, QTableWidgetItem(str(value)))

        self.results_table.resizeColumnsToContents()
        self.results_table.show()

    def create_table_page(self, table):
        page = QWidget()
        layout = QVBoxLayout(page)

        # CRUD buttons (excluding Read)
        crud_layout = QHBoxLayout()
        crud_buttons = []
        for operation in ["Create", "Update", "Delete"]:
            if table == "Routes" and operation == "Update":
                continue
            btn = QPushButton(operation)
            btn.setCheckable(True)
            btn.clicked.connect(lambda checked, op=operation, t=table: self.handle_crud_operation(op, t))
            btn.setStyleSheet("""
                QPushButton {
                    background-color: #483248;
                    color: white;
                    border: none;
                    padding: 10px;
                    border-radius: 5px;
                    font-size: 14px;
                }
                QPushButton:pressed {
                    background-color: #702963;
                }
            """)
            crud_buttons.append(btn)
            crud_layout.addWidget(btn)
        layout.addLayout(crud_layout)

        # Search bar
        search_bar = QLineEdit()
        search_bar.setPlaceholderText("Search...")
        search_bar.textChanged.connect(lambda: self.filter_table(table))
        layout.addWidget(search_bar)

        # Table
        table_widget = QTableWidget()
        layout.addWidget(table_widget)

        # Store references to widgets
        page.table_widget = table_widget
        page.search_bar = search_bar

        return page

    def handle_menu_button_click(self):
        button = self.sender()
        
        if not hasattr(button, 'clicked_once'):
            button.clicked_once = False

        if button.clicked_once:
            # Revert to original color and show landing page
            button.setChecked(False)
            button.clicked_once = False
            self.stacked_widget.setCurrentWidget(self.landing_page)
        else:
            # First click behavior
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
                
                # Only populate table for pages that have a table_widget
                if table not in ["Shortest Path", "Advanced"] and hasattr(current_page, 'table_widget'):
                    self.populate_table(table, current_page.table_widget)
            else:
                print(f"Warning: '{table}' page not found")
                self.notification.show_message(f"Page '{table}' is not available.")

    def handle_crud_operation(self, operation, table):
        # Uncheck all CRUD buttons except the clicked one
        crud_buttons = self.find_crud_buttons(self.pages[table])
        for btn in crud_buttons:
            if btn.text() != operation:
                btn.setChecked(False)
        
        if table == "Routes" and operation == "Create":
            # Switch to the Shortest Path tab
            self.stacked_widget.setCurrentWidget(self.pages["Shortest Path"])
            # Reset the color of the Routes tab
            for btn in self.side_menu.buttons:
                if btn.text() == "Routes":
                    btn.setChecked(False)
                    btn.clicked_once = False
                elif btn.text() == "Shortest Path":
                    btn.setChecked(True)
                    btn.clicked_once = True
        elif operation != "Read" and not (table == "Routes" and operation == "Update"):
            self.show_crud_form(operation, table)

    def find_crud_buttons(self, page):
        crud_buttons = []
        for child in page.findChildren(QPushButton):
            if child.text() in ["Create", "Update", "Delete"]:
                crud_buttons.append(child)
        return crud_buttons

    def show_crud_form(self, operation, table):
        form = QWidget()
        form_layout = QFormLayout(form)

        fields = self.get_fields_for_table(table)
        self.form_fields = {}

        if operation == "Delete":
            primary_key_field = self.get_primary_key_field(table)
            self.form_fields[primary_key_field] = QLineEdit()
            form_layout.addRow(f"{primary_key_field.replace('_', ' ').title()}:", self.form_fields[primary_key_field])
        else:
            for label, field_name in fields:
                self.form_fields[field_name] = QLineEdit()
                form_layout.addRow(label + ":", self.form_fields[field_name])

        submit_button = QPushButton(f"Submit {operation}")
        submit_button.clicked.connect(lambda: self.handle_crud_action(operation, table))
        form_layout.addWidget(submit_button)

        back_button = QPushButton("Back")
        back_button.clicked.connect(lambda: self.stacked_widget.setCurrentWidget(self.pages[table]))
        form_layout.addWidget(back_button)

        self.stacked_widget.addWidget(form)
        self.stacked_widget.setCurrentWidget(form)

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

    def create_home_page(self):
        """Creates the Home page."""
        page = QWidget()
        layout = QVBoxLayout()

        label = QLabel("Airport Network Management")
        label.setAlignment(Qt.AlignCenter)
        label.setStyleSheet("font-size: 28px; font-weight: bold; color: #201640;")
        layout.addWidget(label)

        start_button = QPushButton("Start")
        start_button.setStyleSheet("background-color: #483248;")
        start_button.clicked.connect(lambda: self.change_page(self.table_selection_page))
        layout.addWidget(start_button)

        page.setLayout(layout)
        return page

    def create_table_selection_page(self):
        """Creates the Table selection page."""
        page = QWidget()
        layout = QVBoxLayout()

        label = QLabel("Select a Table:")
        label.setAlignment(Qt.AlignCenter)
        label.setStyleSheet("font-size: 20px;")
        layout.addWidget(label)

        self.combo_box = QComboBox()
        self.combo_box.addItems(["Airports", "Airlines", "Flights", "Routes", "Advanced"])
        self.combo_box.setStyleSheet("font-size: 16px; padding: 5px;")
        layout.addWidget(self.combo_box)

        next_button = QPushButton("Next")
        next_button.setStyleSheet("background-color: #2ecc71;")
        next_button.clicked.connect(self.handle_table_selection)
        layout.addWidget(next_button)

        back_button = QPushButton("Back")
        back_button.clicked.connect(lambda: self.change_page(self.home_page))
        layout.addWidget(back_button)

        page.setLayout(layout)
        return page

    def create_crud_selection_page(self):
        """Creates the CRUD operation selection page."""
        page = QWidget()
        layout = QVBoxLayout()

        label = QLabel("Select a CRUD Operation:")
        label.setAlignment(Qt.AlignCenter)
        label.setStyleSheet("font-size: 20px;")
        layout.addWidget(label)

        self.create_button = QPushButton("Create")
        self.create_button.setStyleSheet("background-color: #e67e22;")
        self.create_button.clicked.connect(lambda: self.show_crud_page("Create"))
        layout.addWidget(self.create_button)

        read_button = QPushButton("Read")
        read_button.setStyleSheet("background-color: #301934;")
        read_button.clicked.connect(self.read_records)
        layout.addWidget(read_button)

        self.update_button = QPushButton("Update")
        self.update_button.setStyleSheet("background-color: #e67e22;")
        self.update_button.clicked.connect(lambda: self.show_crud_page("Update"))
        layout.addWidget(self.update_button)

        delete_button = QPushButton("Delete")
        delete_button.setStyleSheet("background-color: #c0392b;")
        delete_button.clicked.connect(lambda: self.show_crud_page("Delete"))
        layout.addWidget(delete_button)

        back_button = QPushButton("Back")
        back_button.clicked.connect(lambda: self.change_page(self.table_selection_page))
        layout.addWidget(back_button)

        page.setLayout(layout)
        return page

    def show_crud_page(self, operation):
        """Creates and shows the appropriate CRUD page."""
        crud_page = self.create_crud_page(operation)
        self.stacked_widget.addWidget(crud_page)
        self.change_page(crud_page)

    def create_crud_page(self, operation):
        page = QWidget()
        layout = QVBoxLayout()

        if self.selected_table is None:
            label = QLabel("Please select a table first")
            layout.addWidget(label)
            back_button = QPushButton("Back")
            back_button.clicked.connect(lambda: self.change_page(self.table_selection_page))
            layout.addWidget(back_button)
            page.setLayout(layout)
            return page

        label = QLabel(f"{operation} {self.selected_table}")
        label.setStyleSheet("font-size: 18px; font-weight: bold;")
        layout.addWidget(label)

        form_layout = QFormLayout()
        self.form_fields = {}

        if operation == "Create" or operation == "Update":
            fields = self.get_fields_for_table(self.selected_table)
            for label, field_name in fields:
                self.form_fields[field_name] = QLineEdit()
                form_layout.addRow(label + ":", self.form_fields[field_name])
        elif operation == "Delete":
            primary_key_field = self.get_primary_key_field(self.selected_table)
            self.form_fields[primary_key_field] = QLineEdit()
            form_layout.addRow(f"{primary_key_field.replace('_', ' ').title()}:", self.form_fields[primary_key_field])

        layout.addLayout(form_layout)

        # Add button layout
        button_layout = QVBoxLayout()
        
        # Submit button
        submit_button = QPushButton(f"Submit {operation}")
        submit_button.clicked.connect(lambda: self.handle_crud_action(operation))
        submit_button.setStyleSheet("background-color: #2ecc71;")
        button_layout.addWidget(submit_button)

        # Back button
        back_button = QPushButton("Back")
        back_button.clicked.connect(lambda: self.change_page(self.crud_selection_page))
        back_button.setStyleSheet("background-color: #e74c3c;")
        button_layout.addWidget(back_button)

        layout.addLayout(button_layout)
        page.setLayout(layout)
        return page
    
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

    def handle_table_selection(self):
        """Handles the table selection and moves to the CRUD operation page."""
        self.selected_table = self.combo_box.currentText()
        self.update_crud_buttons()
        self.change_page(self.crud_selection_page)

    def update_crud_buttons(self):
        """Updates the visibility of CRUD buttons based on the selected table."""
        if self.selected_table == "Routes":
            self.create_button.setVisible(False)
            self.update_button.setVisible(False)
        else:
            self.create_button.setVisible(True)
            self.update_button.setVisible(True)

    def read_records(self):
        """Displays the data from the selected table with search functionality."""
        self.read_page = QWidget()
        layout = QVBoxLayout()

        label = QLabel(f"Read Records from {self.selected_table}")
        label.setAlignment(Qt.AlignCenter)
        label.setStyleSheet("font-size: 20px; font-weight: bold;")
        layout.addWidget(label)

        # Add search bar
        search_layout = QHBoxLayout()
        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText("Search...")
        self.search_bar.textChanged.connect(self.filter_table)
        search_layout.addWidget(self.search_bar)
        layout.addLayout(search_layout)

        self.table_widget = QTableWidget()
        self.records = []

        # Fetch records from the selected table
        if self.selected_table == "Airports":
            self.records = self.crud_operations.read_airports()
        elif self.selected_table == "Airlines":
            self.records = self.crud_operations.read_airlines()
        elif self.selected_table == "Flights":
            self.records = self.crud_operations.read_flights()
        elif self.selected_table == "Routes":
            self.records = self.crud_operations.read_routes()

        # Display records in the table
        if self.records:
            self.populate_table()
        else:
            error_label = QLabel("No records found.")
            layout.addWidget(error_label)

        layout.addWidget(self.table_widget)

        # Add back button
        back_button = QPushButton("Back")
        back_button.clicked.connect(lambda: self.change_page(self.crud_selection_page))
        layout.addWidget(back_button)

        self.read_page.setLayout(layout)
        self.stacked_widget.addWidget(self.read_page)
        self.change_page(self.read_page)

    def populate_table(self, table, table_widget=None):
        if table_widget is None:
            table_widget = self.pages[table].table_widget
        
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

        # Simple animation
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
