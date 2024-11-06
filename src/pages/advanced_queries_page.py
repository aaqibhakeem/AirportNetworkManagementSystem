from imports import *
from dbdetails import get_connection

def create_advanced_queries_page(self):
    page = QWidget()
    layout = QVBoxLayout(page)

    flights_button = QPushButton("Show Flights with Airline Info")
    flights_button.clicked.connect(self.show_flights_with_airline_info)
    layout.addWidget(flights_button)

    airport_counts_button = QPushButton("Show Airport Flight Counts")
    airport_counts_button.clicked.connect(self.show_airport_flight_counts)
    layout.addWidget(airport_counts_button)

    busiest_airports_button = QPushButton("Show Busiest Airports")
    busiest_airports_button.clicked.connect(self.show_busiest_airports)
    layout.addWidget(busiest_airports_button)

    log_buttons_layout = QHBoxLayout()
    
    flight_log_button = QPushButton("Show Flight Log")
    flight_log_button.clicked.connect(self.show_flight_logs)
    log_buttons_layout.addWidget(flight_log_button)
    
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

    self.results_table = QTableWidget()
    layout.addWidget(self.results_table)

    return page

