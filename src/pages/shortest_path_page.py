from dbdetails import get_connection
from imports import *

def create_shortest_path_page(main_window):
    page = QWidget()
    layout = QVBoxLayout(page)

    airport_form = QFormLayout()
    main_window.source_airport = QComboBox()
    main_window.destination_airport = QComboBox()
    main_window.stopovers = QSpinBox()
    main_window.stopovers.setRange(0, 10)
    main_window.source_airport.setFixedWidth(500)
    main_window.destination_airport.setFixedWidth(500)
    main_window.stopovers.setFixedWidth(100)
    
    main_window.source_airport.setStyleSheet("QComboBox::drop-down {border-width: 0px;} QComboBox::down-arrow {image: url(noimg); border-width: 0px;}")
    main_window.destination_airport.setStyleSheet("QComboBox::drop-down {border-width: 0px;} QComboBox::down-arrow {image: url(noimg); border-width: 0px;}")
    main_window.stopovers.setStyleSheet("QSpinBox::up-button, QSpinBox::down-button {width: 0px;}")
    
    airport_form.addRow("Source Airport:", main_window.source_airport)
    airport_form.addRow("Destination Airport:", main_window.destination_airport)
    airport_form.addRow("Number of Stopovers:", main_window.stopovers)
    layout.addLayout(airport_form)

    airports = main_window.crud_operations.read_airports()
    for airport in airports:
        main_window.source_airport.addItem(f"{airport[0]} - {airport[1]}", airport[0])
        main_window.destination_airport.addItem(f"{airport[0]} - {airport[1]}", airport[0])

    find_path_button = QPushButton("Find Shortest Path")
    find_path_button.clicked.connect(main_window.find_shortest_path)
    layout.addWidget(find_path_button)

    main_window.path_details_box = QTextEdit()
    main_window.path_details_box.setReadOnly(True)
    main_window.path_details_box.setStyleSheet("background-color: white; color: black; border: 1px solid #bdc3c7; border-radius: 5px; padding: 5px;")
    main_window.path_details_box.setFixedHeight(150)
    layout.addWidget(main_window.path_details_box)

    main_window.map_view = QGraphicsView()
    main_window.map_view.setMinimumHeight(400)
    layout.addWidget(main_window.map_view)

    main_window.store_route_button = QPushButton("Store Route")
    main_window.store_route_button.clicked.connect(main_window.store_route)
    main_window.store_route_button.setVisible(False)
    layout.addWidget(main_window.store_route_button)

    return page