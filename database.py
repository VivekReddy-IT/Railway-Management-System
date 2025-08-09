import os
import mysql.connector
from dotenv import load_dotenv
from logger import setup_logger

logger = setup_logger(__name__)

# Load environment variables from .env file
load_dotenv()

def create_db_connection():
    """Creates and returns a database connection."""
    try:
        connection = mysql.connector.connect(
            host=os.getenv("MYSQL_HOST"),
            database=os.getenv("MYSQL_DATABASE"),
            user=os.getenv("MYSQL_USER"),
            password=os.getenv("MYSQL_PASSWORD")
        )
        if connection.is_connected():
            logger.info("Successfully connected to MySQL database")
            return connection
    except mysql.connector.Error as e:
        logger.error(f"Error connecting to MySQL database: {e}")
        return None

def get_all_trains():
    """Retrieves all train IDs and names from the database."""
    connection = None
    cursor = None
    try:
        connection = create_db_connection()
        if connection:
            cursor = connection.cursor()
            # Select train_id and train_name from the Trains table
            query = "SELECT train_id, train_name FROM Trains"
            logger.debug(f"Executing query: {query}")
            cursor.execute(query)
            
            # Fetch all results
            trains = cursor.fetchall()
            logger.info(f"Retrieved {len(trains)} trains")
            return trains # Returns a list of tuples: [(train_id, train_name), ...]
            
    except mysql.connector.Error as e:
        logger.error(f"Error retrieving trains: {e}")
        return []
        
    finally:
        # Close cursor and connection
        if cursor:
            cursor.close()
        if connection and connection.is_connected():
            connection.close()
            logger.info("MySQL connection closed")

def search_stations(query):
    """Searches for stations based on name or code."""
    connection = None
    cursor = None
    try:
        connection = create_db_connection()
        if connection:
            cursor = connection.cursor()
            # Search for stations by name or code (case-insensitive search)
            sql_query = "SELECT station_code, station_name FROM Stations WHERE station_name LIKE %s OR station_code LIKE %s"
            search_term = f"%{query}%"
            logger.debug(f"Executing query: {sql_query} with search term: {search_term}")
            cursor.execute(sql_query, (search_term, search_term))
            
            stations = cursor.fetchall()
            logger.info(f"Found {len(stations)} matching stations for query: {query}")
            return stations # Returns a list of tuples: [(station_code, station_name), ...]
            
    except mysql.connector.Error as e:
        logger.error(f"Error searching stations: {e}")
        return []
        
    finally:
        # Close cursor and connection
        if cursor:
            cursor.close()
        if connection and connection.is_connected():
            connection.close()
            logger.info("MySQL connection closed")

def get_train_route(train_id):
    """Retrieves the route for a specific train, including all stops."""
    connection = None
    cursor = None
    try:
        connection = create_db_connection()
        if connection:
            cursor = connection.cursor()
            # Get the route_id for the given train_id
            route_query = "SELECT route_id FROM TrainSchedules WHERE train_id = %s LIMIT 1"
            logger.debug(f"Executing query: {route_query} with train_id: {train_id}")
            cursor.execute(route_query, (train_id,))
            route_result = cursor.fetchone()
            
            if not route_result:
                logger.warning(f"No route found for train_id: {train_id}")
                return []
                
            route_id = route_result[0]
            
            # Get all stations on this route in sequence order
            stations_query = "SELECT s.station_code, s.station_name, rs.sequence_number FROM RouteStations rs JOIN Stations s ON rs.station_code = s.station_code WHERE rs.route_id = %s ORDER BY rs.sequence_number"
            logger.debug(f"Executing query: {stations_query} with route_id: {route_id}")
            cursor.execute(stations_query, (route_id,))
            
            route_stations = cursor.fetchall()
            logger.info(f"Retrieved {len(route_stations)} stations for route_id: {route_id}")
            return route_stations # Returns a list of tuples: [(station_code, station_name, sequence_number), ...]
            
    except mysql.connector.Error as e:
        logger.error(f"Error retrieving train route: {e}")
        return []
        
    finally:
        # Close cursor and connection
        if cursor:
            cursor.close()
        if connection and connection.is_connected():
            connection.close()
            logger.info("MySQL connection closed")

def categorize_age(age: int) -> str:
    """Categorizes passenger age."""
    if age < 12:
        return "Child"
    elif age >= 60:
        return "Senior"
    else:
        return "Adult"

def create_reservation(train_id: str, journey_date: str, source_station_code: str, destination_station_code: str, passengers: list):
    """Creates a new reservation in the database and returns booking details, including PNR."""
    connection = None
    cursor = None
    try:
        connection = create_db_connection()
        if connection:
            cursor = connection.cursor()
            
            # Generate a simple dummy PNR (replace with a more robust method in a real app)
            import uuid
            pnr = str(uuid.uuid4())[:8].upper()
            
            # Check if train, source, and destination exist and are valid for the route (basic check)
            # In a real application, you would perform more thorough validation here,
            # including checking if source and destination are on the route and in correct order.
            
            # Example: Check if train_id exists (simplified)
            cursor.execute("SELECT train_id FROM Trains WHERE train_id = %s", (train_id,))
            if not cursor.fetchone():
                return {"success": False, "error": f"Invalid Train ID: {train_id}"}
                
            # Example: Check if source_station_code exists (simplified)
            cursor.execute("SELECT station_code FROM Stations WHERE station_code = %s", (source_station_code,))
            if not cursor.fetchone():
                return {"success": False, "error": f"Invalid Source Station Code: {source_station_code}"}
                
            # Example: Check if destination_station_code exists (simplified)
            cursor.execute("SELECT station_code FROM Stations WHERE station_code = %s", (destination_station_code,))
            if not cursor.fetchone():
                 return {"success": False, "error": f"Invalid Destination Station Code: {destination_station_code}"}
            
            # TODO: Add more robust validation: Check if source and destination are on the route and in order using get_train_route.
            # TODO: Implement seat availability check and selection.
            
            # Insert into Reservations table
            reservation_query = "INSERT INTO Reservations (pnr, train_id, journey_date, source_station_code, destination_station_code, booking_time, status) VALUES (%s, %s, %s, %s, %s, NOW(), %s)"
            reservation_values = (pnr, train_id, journey_date, source_station_code, destination_station_code, "Confirmed") # Assuming Confirmed status on booking
            cursor.execute(reservation_query, reservation_values)
            
            # Insert into Passengers table
            passenger_query = "INSERT INTO Passengers (pnr, name, age, category) VALUES (%s, %s, %s, %s)"
            passenger_records = []
            for passenger in passengers:
                age = passenger.get('age')
                category = categorize_age(age) if age is not None else "Unknown"
                passenger_records.append((pnr, passenger.get('name'), age, category))
                
            cursor.executemany(passenger_query, passenger_records)
            
            # Commit the transaction
            connection.commit()
            logger.info(f"Reservation created successfully with PNR: {pnr}")
            
            # Retrieve the saved booking details for the ticket
            # This is a simplified retrieval; a real app might join tables to get full details
            booking_details_query = "SELECT r.pnr, r.train_id, t.train_name, r.journey_date, r.source_station_code, s_src.station_name AS source_station_name, r.destination_station_code, s_dest.station_name AS destination_station_name, r.booking_time, r.status FROM Reservations r JOIN Trains t ON r.train_id = t.train_id JOIN Stations s_src ON r.source_station_code = s_src.station_code JOIN Stations s_dest ON r.destination_station_code = s_dest.station_code WHERE r.pnr = %s"
            cursor.execute(booking_details_query, (pnr,))
            reservation_details = cursor.fetchone()
            
            passenger_details_query = "SELECT name, age, category FROM Passengers WHERE pnr = %s"
            cursor.execute(passenger_details_query, (pnr,))
            passenger_details = cursor.fetchall()
            
            booking_summary = {
                "pnr": reservation_details[0],
                "train_id": reservation_details[1],
                "train_name": reservation_details[2],
                "journey_date": reservation_details[3].strftime('%Y-%m-%d'), # Format date
                "source_station_code": reservation_details[4],
                "source_station_name": reservation_details[5],
                "destination_station_code": reservation_details[6],
                "destination_station_name": reservation_details[7],
                "booking_time": reservation_details[8].strftime('%Y-%m-%d %H:%M:%S'), # Format datetime
                "status": reservation_details[9],
                "passengers": []
            }
            
            for p in passenger_details:
                booking_summary["passengers"].append({"name": p[0], "age": p[1], "category": p[2]})

            return {"success": True, "booking_details": booking_summary}
            
    except mysql.connector.Error as e:
        if connection:
            connection.rollback()
        logger.error(f"Error creating reservation: {e}")
        return {"success": False, "error": str(e)}
        
    finally:
        # Close cursor and connection
        if cursor:
            cursor.close()
        if connection and connection.is_connected():
            connection.close()
            logger.info("MySQL connection closed")

# Example usage (for testing purposes, can be removed later)
if __name__ == "__main__":
    all_trains = get_all_trains()
    if all_trains:
        print("All Trains:")
        for train in all_trains:
            print(f"ID: {train[0]}, Name: {train[1]}")
    else:
        print("Could not retrieve trains or no trains found.")

    # Example usage for search_stations
    search_term = "Sample"
    matching_stations = search_stations(search_term)
    if matching_stations:
        print(f"\nStations matching '{search_term}':")
        for station in matching_stations:
            print(f"Code: {station[0]}, Name: {station[1]}")
    else:
        print(f"\nNo stations found matching '{search_term}'.")

    # Example usage for get_train_route
    train_id_to_check = "TRN101" # Replace with a valid train_id from your database
    train_route = get_train_route(train_id_to_check)
    if train_route:
        print(f"\nRoute for Train ID {train_id_to_check}:")
        for station in train_route:
            print(f"Sequence: {station[2]}, Code: {station[0]}, Name: {station[1]}")
    else:
        print(f"\nCould not retrieve route for Train ID {train_id_to_check} (check if train exists or has a schedule).") 