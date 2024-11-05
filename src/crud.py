import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from dbdetails import get_connection

class CRUDOperations:
    def __init__(self):
        self.conn = None
        self.cursor = None

    def get_db_connection(self):
        self.conn = get_connection()
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

    ### CRUD Operations for Airlines with Flight Counts ###
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
        
        try:
            # Execute the stored procedure to get flight counts
            self.cursor.callproc('CountFlightsByAirline')
            flight_counts = {row[0]: row[1] for row in self.cursor.fetchall()}  # Map airline_code to flight count

            # Query airline details
            self.cursor.execute("SELECT * FROM Airlines")
            airlines = self.cursor.fetchall()

            # Combine airline details with flight counts
            airlines_with_counts = []
            for airline in airlines:
                airline_code = airline[0]
                flight_count = flight_counts.get(airline_code, 0)
                airlines_with_counts.append(airline + (flight_count,))  # Append flight count to each airline's details

            return airlines_with_counts

        except ValueError as e:
            print(f"Error: {e}")
            # If the stored procedure doesn't exist, return airlines without flight counts
            if e.errno == 1305:  # Error number for "PROCEDURE does not exist"
                self.cursor.execute("SELECT * FROM Airlines")
                return self.cursor.fetchall()
            else:
                raise  # Re-raise the exception if it's not the "procedure doesn't exist" error

        finally:
            self.close_db_connection()

    def ensure_count_flights_procedure_exists(self):
        self.get_db_connection()
        try:
            # Check if the procedure exists
            self.cursor.execute("SHOW PROCEDURE STATUS WHERE Name = 'CountFlightsByAirline'")
            if not self.cursor.fetchone():
                # Create the procedure if it doesn't exist
                create_procedure_query = """
                CREATE PROCEDURE CountFlightsByAirline()
                BEGIN
                    SELECT a.airline_code, COUNT(f.flight_id) as flight_count
                    FROM Airlines a
                    LEFT JOIN Flights f ON a.airline_code = f.airline_code
                    GROUP BY a.airline_code;
                END
                """
                self.cursor.execute(create_procedure_query)
                self.conn.commit()
                
        except ValueError as e:
            print(f"Error ensuring CountFlightsByAirline procedure: {e}")
        finally:
            self.close_db_connection()

    def ensure_flight_logs_table_exists(self):
        self.get_db_connection()
        try:
            create_table_query = """
            CREATE TABLE IF NOT EXISTS FlightLogs (
                log_id INT AUTO_INCREMENT PRIMARY KEY,
                flight_id VARCHAR(50),
                action VARCHAR(20),
                timestamp DATETIME
            )
            """
            self.cursor.execute(create_table_query)
            self.conn.commit()
        except ValueError as e:
            print(f"Error ensuring FlightLogs table: {e}")
            self.conn.rollback()
        finally:
            self.close_db_connection()

    def create_flight_log_trigger(self):
        self.get_db_connection()
        try:
            trigger_query = """
            CREATE TRIGGER IF NOT EXISTS after_flight_insert
            AFTER INSERT ON Flights
            FOR EACH ROW
            BEGIN
                INSERT INTO FlightLogs (flight_id, action, timestamp)
                VALUES (NEW.flight_id, 'INSERT', NOW());
            END;
            """
            self.cursor.execute(trigger_query)
            self.conn.commit()
        except ValueError as e:
            print(f"Error creating flight log trigger: {e}")
            self.conn.rollback()
        finally:
            self.close_db_connection()

    def create_update_route_duration_procedure(self):
        self.get_db_connection()
        try:
            # Drop the procedure if it exists
            drop_procedure_query = "DROP PROCEDURE IF EXISTS UpdateRouteDuration"
            self.cursor.execute(drop_procedure_query)
            
            # Create the procedure
            procedure_query = """
            CREATE PROCEDURE UpdateRouteDuration(IN route_id INT)
            BEGIN
                UPDATE Routes r
                SET r.duration = (
                    SELECT TIMESTAMPDIFF(MINUTE, f1.timestamp, f2.timestamp)
                    FROM Flights f1
                    JOIN Flights f2 ON f1.destination_airport = f2.source_airport
                    WHERE f1.source_airport = r.source_airport
                    AND f2.destination_airport = r.destination_airport
                    LIMIT 1
                )
                WHERE r.route_id = route_id;
            END
            """
            self.cursor.execute(procedure_query)
            self.conn.commit()
        except ValueError as e:
            print(f"Error creating update route duration procedure: {e}")
            self.conn.rollback()
        finally:
            self.close_db_connection()

    def get_flights_with_airline_info(self):
        self.get_db_connection()
        query = """
        SELECT f.flight_id, f.source_airport, f.destination_airport, 
               a.airline_name, a.headquarters
        FROM Flights f
        JOIN Airlines a ON f.airline_code = a.airline_code
        """
        self.cursor.execute(query)
        flights_with_airline_info = self.cursor.fetchall()
        self.close_db_connection()
        return flights_with_airline_info

    def get_airport_flight_counts(self):
        self.get_db_connection()
        query = """
        SELECT a.airport_code, a.airport_name, 
               COUNT(f.flight_id) as flight_count
        FROM Airports a
        LEFT JOIN Flights f ON a.airport_code = f.source_airport
        GROUP BY a.airport_code, a.airport_name
        """
        self.cursor.execute(query)
        airport_flight_counts = self.cursor.fetchall()
        self.close_db_connection()
        return airport_flight_counts

    def get_routes_with_stopover_count(self):
        self.get_db_connection()
        query = """
        SELECT r.route_id, r.source_airport, r.destination_airport,
               (SELECT COUNT(DISTINCT f.destination_airport)
                FROM Flights f
                WHERE f.source_airport = r.source_airport
                AND f.destination_airport != r.destination_airport) as stopover_count
        FROM Routes r
        """
        self.cursor.execute(query)
        routes_with_stopover_count = self.cursor.fetchall()
        self.close_db_connection()
        return routes_with_stopover_count    

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
