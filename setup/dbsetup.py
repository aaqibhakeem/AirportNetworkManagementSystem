import sys
import os
import pandas as pd
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from dbdetails import get_connection

airports_csv_file = "airports.csv"
airlines_csv_file = "airlines.csv"
flights_csv_file = "flights.csv"
routes_csv_file = "routes.csv"

airports_df = pd.read_csv(airports_csv_file)
airlines_df = pd.read_csv(airlines_csv_file)
flights_df = pd.read_csv(flights_csv_file)
routes_df = pd.read_csv(routes_csv_file)

conn = get_connection()

cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS Airports (
        airport_code VARCHAR(10) PRIMARY KEY,
        airport_name VARCHAR(255),
        latitude_deg DECIMAL(10, 6),
        longitude_deg DECIMAL(10, 6),
        state VARCHAR(255),
        city VARCHAR(255)
    )
''')

for row in airports_df.itertuples(index=False):
    cursor.execute('''
        INSERT INTO Airports (airport_code, airport_name, latitude_deg, longitude_deg, state, city)
        VALUES (%s, %s, %s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE 
        airport_name=VALUES(airport_name), 
        latitude_deg=VALUES(latitude_deg), 
        longitude_deg=VALUES(longitude_deg), 
        state=VALUES(state), 
        city=VALUES(city)
    ''', (row.airport_code, row.airport_name, row.latitude_deg, row.longitude_deg, row.state, row.city))

cursor.execute('''
    CREATE TABLE IF NOT EXISTS Airlines (
        airline_code VARCHAR(10) PRIMARY KEY,
        airline_name VARCHAR(255),
        headquarters VARCHAR(255),
        fleet_size INT,
        country VARCHAR(255)
    )
''')

for row in airlines_df.itertuples(index=False):
    cursor.execute('''
        INSERT INTO Airlines (airline_code, airline_name, headquarters, fleet_size, country)
        VALUES (%s, %s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE 
        airline_name=VALUES(airline_name), 
        headquarters=VALUES(headquarters), 
        fleet_size=VALUES(fleet_size), 
        country=VALUES(country)
    ''', (row.airline_code, row.airline_name, row.headquarters, row.fleet_size, row.country))

cursor.execute('''
    CREATE TABLE IF NOT EXISTS Flights (
        flight_id INT PRIMARY KEY,
        airline_code VARCHAR(10),
        source_airport VARCHAR(10),
        destination_airport VARCHAR(10),
        latitude_deg DECIMAL(10, 6),
        longitude_deg DECIMAL(10, 6),
        timestamp DATETIME,
        FOREIGN KEY (airline_code) REFERENCES Airlines(airline_code),
        FOREIGN KEY (source_airport) REFERENCES Airports(airport_code),
        FOREIGN KEY (destination_airport) REFERENCES Airports(airport_code)
    )
''')

for row in flights_df.itertuples(index=False):
    cursor.execute('''
        INSERT INTO Flights (flight_id, airline_code, source_airport, destination_airport, latitude_deg, longitude_deg, timestamp)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE 
        airline_code=VALUES(airline_code),
        source_airport=VALUES(source_airport),
        destination_airport=VALUES(destination_airport),
        latitude_deg=VALUES(latitude_deg),
        longitude_deg=VALUES(longitude_deg),
        timestamp=VALUES(timestamp)
    ''', (row.flight_id, row.airline_code, row.source_airport, row.destination_airport, row.latitude_deg, row.longitude_deg, row.timestamp))

cursor.execute('''
    CREATE TABLE IF NOT EXISTS Routes (
        route_id INT PRIMARY KEY,
        source_airport VARCHAR(10),
        destination_airport VARCHAR(10),
        distance DECIMAL(10, 2),
        duration TIME,
        stopovers INT,
        FOREIGN KEY (source_airport) REFERENCES Airports(airport_code),
        FOREIGN KEY (destination_airport) REFERENCES Airports(airport_code)
    )
''')

cursor.execute('''
    ALTER TABLE Routes MODIFY COLUMN route_id INT AUTO_INCREMENT;
''')

if not routes_df.empty:
    for row in routes_df.itertuples(index=False):
        cursor.execute('''
            INSERT INTO Routes (route_id, source_airport, destination_airport, distance, duration, stopovers)
            VALUES (%s, %s, %s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE 
            source_airport=VALUES(source_airport),
            destination_airport=VALUES(destination_airport),
            distance=VALUES(distance),
            duration=VALUES(duration),
            stopovers=VALUES(stopovers)
        ''', (row.route_id, row.source_airport, row.destination_airport, row.distance, row.duration))

conn.commit()
conn.close()
