import mysql.connector
from tabulate import tabulate

class CRUDOperations:
    def __init__(self):
        self.conn = None
        self.cursor = None

    def get_db_connection(self):
        self.conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="karad@83",
            database="anm"
        )
        self.cursor = self.conn.cursor()

    def close_db_connection(self):
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()

    ### CRUD Operations for Airports ###
    def create_airport(self, airport_code, airport_name, latitude_deg, longitude_deg, state, city):
        self.get_db_connection()
        query = """
            INSERT INTO Airports (airport_code, airport_name, latitude_deg, longitude_deg, state, city)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        self.cursor.execute(query, (airport_code, airport_name, latitude_deg, longitude_deg, state, city))
        self.conn.commit()
        print(f"Airport {airport_name} added successfully!")
        self.close_db_connection()

    def read_airports(self):
        self.get_db_connection()
        self.cursor.execute("SELECT * FROM Airports")
        airports = self.cursor.fetchall()
        self.close_db_connection()
        return airports

    def update_airport(self, airport_code, new_airport_name=None, new_latitude=None, new_longitude=None, new_state=None, new_city=None):
        self.get_db_connection()

        updates = []
        values = []
        if new_airport_name:
            updates.append("airport_name = %s")
            values.append(new_airport_name)
        if new_latitude:
            updates.append("latitude_deg = %s")
            values.append(new_latitude)
        if new_longitude:
            updates.append("longitude_deg = %s")
            values.append(new_longitude)
        if new_state:
            updates.append("state = %s")
            values.append(new_state)
        if new_city:
            updates.append("city = %s")
            values.append(new_city)

        if updates:
            query = f"UPDATE Airports SET {', '.join(updates)} WHERE airport_code = %s"
            values.append(airport_code)
            self.cursor.execute(query, tuple(values))
            self.conn.commit()

        print(f"Airport {airport_code} updated successfully!")
        self.close_db_connection()

    def delete_airport(self, airport_code):
        self.get_db_connection()
        query = "DELETE FROM Airports WHERE airport_code = %s"
        self.cursor.execute(query, (airport_code,))
        self.conn.commit()
        print(f"Airport {airport_code} deleted successfully!")
        self.close_db_connection()

    ### CRUD Operations for Airlines ###
    def create_airline(self, airline_code, airline_name, headquarters, fleet_size, country):
        self.get_db_connection()
        query = """
            INSERT INTO Airlines (airline_code, airline_name, headquarters, fleet_size, country)
            VALUES (%s, %s, %s, %s, %s)
        """
        self.cursor.execute(query, (airline_code, airline_name, headquarters, fleet_size, country))
        self.conn.commit()
        print(f"Airline {airline_name} added successfully!")
        self.close_db_connection()

    def read_airlines(self):
        self.get_db_connection()
        self.cursor.execute("SELECT * FROM Airlines")
        airlines = self.cursor.fetchall()
        self.close_db_connection()
        return airlines

    def update_airline(self, airline_code, new_airline_name=None, new_headquarters=None, new_fleet_size=None, new_country=None):
        self.get_db_connection()

        updates = []
        values = []
        if new_airline_name:
            updates.append("airline_name = %s")
            values.append(new_airline_name)
        if new_headquarters:
            updates.append("headquarters = %s")
            values.append(new_headquarters)
        if new_fleet_size:
            updates.append("fleet_size = %s")
            values.append(new_fleet_size)
        if new_country:
            updates.append("country = %s")
            values.append(new_country)

        if updates:
            query = f"UPDATE Airlines SET {', '.join(updates)} WHERE airline_code = %s"
            values.append(airline_code)
            self.cursor.execute(query, tuple(values))
            self.conn.commit()

        print(f"Airline {airline_code} updated successfully!")
        self.close_db_connection()

    def delete_airline(self, airline_code):
        self.get_db_connection()
        query = "DELETE FROM Airlines WHERE airline_code = %s"
        self.cursor.execute(query, (airline_code,))
        self.conn.commit()
        print(f"Airline {airline_code} deleted successfully!")
        self.close_db_connection()

    ### CRUD Operations for Flights ###
    def create_flight(self, flight_id, airline_code, source_airport, destination_airport, latitude_deg, longitude_deg, timestamp):
        self.get_db_connection()
        query = """
            INSERT INTO Flights (flight_id, airline_code, source_airport, destination_airport, latitude_deg, longitude_deg, timestamp)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        self.cursor.execute(query, (flight_id, airline_code, source_airport, destination_airport, latitude_deg, longitude_deg, timestamp))
        self.conn.commit()
        print(f"Flight {flight_id} added successfully!")
        self.close_db_connection()

    def read_flights(self):
        self.get_db_connection()
        self.cursor.execute("SELECT * FROM Flights")
        flights = self.cursor.fetchall()
        self.close_db_connection()
        return flights

    def update_flight(self, flight_id, new_airline_code=None, new_source_airport=None, new_destination_airport=None, new_latitude=None, new_longitude=None, new_timestamp=None):
        self.get_db_connection()

        updates = []
        values = []
        if new_airline_code:
            updates.append("airline_code = %s")
            values.append(new_airline_code)
        if new_source_airport:
            updates.append("source_airport = %s")
            values.append(new_source_airport)
        if new_destination_airport:
            updates.append("destination_airport = %s")
            values.append(new_destination_airport)
        if new_latitude:
            updates.append("latitude_deg = %s")
            values.append(new_latitude)
        if new_longitude:
            updates.append("longitude_deg = %s")
            values.append(new_longitude)
        if new_timestamp:
            updates.append("timestamp = %s")
            values.append(new_timestamp)

        if updates:
            query = f"UPDATE Flights SET {', '.join(updates)} WHERE flight_id = %s"
            values.append(flight_id)
            self.cursor.execute(query, tuple(values))
            self.conn.commit()

        print(f"Flight {flight_id} updated successfully!")
        self.close_db_connection()

    def delete_flight(self, flight_id):
        self.get_db_connection()
        query = "DELETE FROM Flights WHERE flight_id = %s"
        self.cursor.execute(query, (flight_id,))
        self.conn.commit()
        print(f"Flight {flight_id} deleted successfully!")
        self.close_db_connection()

    ### CRUD Operations for Routes ###
    def read_routes(self):
        self.get_db_connection()
        self.cursor.execute("SELECT * FROM Routes")
        routes = self.cursor.fetchall()
        self.close_db_connection()
        return routes

    def delete_route(self, route_id):
        self.get_db_connection()
        query = "DELETE FROM Routes WHERE route_id = %s"
        self.cursor.execute(query, (route_id,))
        self.conn.commit()
        print(f"Route {route_id} deleted successfully!")
        self.close_db_connection()
