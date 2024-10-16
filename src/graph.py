import networkx as nx
import plotly.graph_objects as go
import mysql.connector
from src.shortestpath import ShortestPathAlgorithms

def load_airport_coordinates():
    airports = {}

    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="karad@83",
        database="anm"
    )

    cursor = conn.cursor(dictionary=True)

    query = "SELECT airport_code, airport_name, latitude_deg, longitude_deg, state, city FROM Airports"
    cursor.execute(query)

    rows = cursor.fetchall()

    for row in rows:
        airport_code = row['airport_code']
        airport_name = row['airport_name']
        latitude = float(row['latitude_deg'])
        longitude = float(row['longitude_deg'])
        region = row['state']
        city = row['city']
        
        if airport_code in airports:
            suffix = 1
            new_airport_code = f"{airport_code}_{suffix}"
            while new_airport_code in airports:
                suffix += 1
                new_airport_code = f"{airport_code}_{suffix}"
            airport_code = new_airport_code

        airports[airport_code] = {
            'airport_name': airport_name,
            'latitude': latitude,
            'longitude': longitude,
            'region': region,
            'city': city
        }

    cursor.close()
    conn.close()

    return airports

def get_number_of_vias():
    while True:
        try:
            num_vias = int(input("Enter the number of via points (0 for direct route): "))
            if num_vias >= 0:
                return num_vias
            else:
                print("Please enter a non-negative integer.")
        except ValueError:
            print("Invalid input. Please enter a number.")

def create_graph_from_airports(airports):
    G = nx.Graph()
    
    for airport_code, data in airports.items():
        G.add_node(airport_code, pos=(data['longitude'], data['latitude']), airport_name=data['airport_name'], region=data['region'], city=data['city'])
    
    airport_codes = list(airports.keys())
    for i in range(len(airport_codes)):
        for j in range(i + 1, len(airport_codes)):
            distance = ShortestPathAlgorithms.calculate_custom_distance(G.nodes[airport_codes[i]]['pos'], G.nodes[airport_codes[j]]['pos'])
            G.add_edge(airport_codes[i], airport_codes[j], distance=distance)
    
    return G

def draw_graph(G, paths=None):
    pos = nx.get_node_attributes(G, 'pos')
    
    node_lon = []
    node_lat = []
    node_text = []
    for node in G.nodes():
        lon, lat = pos[node]
        node_lon.append(lon)
        node_lat.append(lat)
        node_text.append(node)
    
    trace_nodes = go.Scattergeo(
        lon=node_lon,
        lat=node_lat,
        mode='markers+text',
        text=node_text,
        marker=dict(size=15, color='darkblue'),
        textposition='top center',
        name='Airports'
    )
    
    fig = go.Figure(data=[trace_nodes])
    
    if paths:
        colors = ['red', 'blue']
        airport_names = ['Shortest Path', 'Shortest Path (excluding direct route)']
        for idx, path in enumerate(paths):
            path_edges_x = []
            path_edges_y = []
            for u, v in zip(path, path[1:]):
                x0, y0 = pos[u]
                x1, y1 = pos[v]
                path_edges_x.extend([x0, x1, None])
                path_edges_y.extend([y0, y1, None])
            
            trace_path = go.Scattergeo(
                lon=path_edges_x,
                lat=path_edges_y,
                mode='lines',
                line=dict(width=2, color=colors[idx]),
                name=airport_names[idx]
            )
            fig.add_trace(trace_path)
    
    fig.update_layout(
        showlegend=True,
        margin=dict(l=0, r=0, b=0, t=0),
        title='Airport Network',
        geo=dict(
            scope='world',
            projection_type='mercator',
            showland=True,
            landcolor='rgb(220, 220, 220)',
            countrycolor='rgb(204, 204, 204)',
            coastlinecolor='rgb(150, 150, 150)',
            showocean=True,
            oceancolor='rgb(180, 180, 255)',
            showlakes=True,
            lakecolor='rgb(200, 200, 255)',
            center=dict(lat=20.5937, lon=78.9629),
            projection_scale=1,
            lataxis=dict(range=[5, 35]),
            lonaxis=dict(range=[60, 100])
        )
    )
    return fig  # Return the figure object instead of showing it

def get_source_destination(airports):
    print("Available airports:")
    for idx, airport_code in enumerate(airports.keys()):
        print(f"{idx}: {airport_code} ({airports[airport_code]['airport_name']})")
    
    source_idx = int(input("Enter the source airport index: "))
    destination_idx = int(input("Enter the destination airport index: "))
    
    airport_codes = list(airports.keys())
    source = airport_codes[source_idx]
    destination = airport_codes[destination_idx]
    
    return source, destination

def ask_add_route_to_db(source, destination, path, distance, num_vias, G, conn):
    cursor = conn.cursor()

    # Check if the route already exists
    check_query = """
        SELECT COUNT(*) FROM Routes 
        WHERE source_airport = %s 
        AND destination_airport = %s 
        AND stopovers = %s
    """
    cursor.execute(check_query, (source, destination, num_vias))
    route_exists = cursor.fetchone()[0] > 0

    if route_exists:
        print(f"A route from {source} to {destination} with {num_vias} stopovers already exists in the database. Not adding a duplicate.")
        return

    duration = distance / 900
    hours = int(duration)
    minutes = int((duration * 60) % 60)
    seconds = int((duration * 3600) % 60)
    duration_str = f"{hours:02}:{minutes:02}:{seconds:02}"

    query = """
        INSERT INTO Routes (source_airport, destination_airport, distance, duration, stopovers)
        VALUES (%s, %s, %s, %s, %s)
    """
    cursor.execute(query, (source, destination, distance, duration_str, num_vias))
    conn.commit()

    print(f"Route from {source} to {destination} added to the Routes table with distance {distance:.2f} km, duration {duration_str}, and {num_vias} stopovers.")

    cursor.close()

if __name__ == "__main__":
    airports = load_airport_coordinates()
    G = create_graph_from_airports(airports)
    source, destination = get_source_destination(airports)
    
    num_vias = get_number_of_vias()

    if num_vias == 0:
        shortest_paths = ShortestPathAlgorithms.compute_all_shortest_paths(G, source, destination)
        shortest_path_algorithm = min(shortest_paths, key=lambda k: shortest_paths[k][1])
        shortest_path, shortest_distance = shortest_paths[shortest_path_algorithm]
        print(f"\nThe shortest path from {source} to {destination} is found by {shortest_path_algorithm}: {shortest_path} with total distance {shortest_distance:.2f} km")
    else:
        shortest_path, shortest_distance = ShortestPathAlgorithms.compute_shortest_path_with_exact_vias(G, source, destination, num_vias)
        print(f"\nThe shortest path from {source} to {destination} with {num_vias} via points is: {shortest_path} with total distance {shortest_distance:.2f} km")

    draw_graph(G, [shortest_path])

    # Ask the user if they want to add the route to the Routes table
    conn = mysql.connector.connect(
        host="localhost",         
        user="root",              
        password="karad@83", 
        database="anm"  
    )
    ask_add_route_to_db(source, destination, shortest_path, shortest_distance, num_vias, G, conn)

    conn.close()