import pandas as pd
from dijkstra import dijkstra
from adjacency_list_graph import AdjacencyListGraph

def load_london_underground_graph(csv_file):
    # Load station data from the file to set up the network.
    df = pd.read_csv(csv_file)
    # Collecting all station names to create a comprehensive list.
    stations = set(df['Station A']).union(set(df['Station B']))
    # Mapping each station to a unique index for graph representation.
    station_index = {station: i for i, station in enumerate(stations)}
    # Initiating our graph structure to represent the tube system.
    graph = AdjacencyListGraph(len(stations), True, True)
    # Adding connections (edges) between stations to our graph.
    for _, row in df.iterrows():
        graph.insert_edge(station_index[row['Station A']], station_index[row['Station B']], 1)

    return graph, station_index

def find_shortest_path(graph, station_index, start_station, end_station):
    # Getting indexes for start and end stations.
    start_index = station_index.get(start_station)
    end_index = station_index.get(end_station)
    # Checking if the stations actually exist in our network.
    if start_index is None or end_index is None:
        print(f"Error: Can't find one or both stations in the network.")
        return None, None

    # Applying Dijkstra's algorithm to determine the shortest path.
    d, pi = dijkstra(graph, start_index)

    # Handling cases where no path is available.
    if pi[end_index] is None:
        print(f"No available path from {start_station} to {end_station}.")
        return None, None

    # Mapping the route from the destination back to the starting point.
    path = []
    current = end_index
    while current != start_index:
        for station, index in station_index.items():
            if index == current:
                path.append(station)
                break
        current = pi[current]
    path.append(start_station)
    path.reverse()  # Arranging the path in the correct order, beginning from the start station.

    # Calculating the number of stops on the path.
    num_stops = len(path) - 1

    return path, num_stops

def main():
    # Define where to find the station data.
    csv_file = 'london_underground_graph.csv'
    # Set up the network graph from the CSV data.
    graph, station_index = load_london_underground_graph(csv_file)

    # Ask the user for their journey's start and end stations.
    start_station = input("Enter start station: ")
    end_station = input("Enter end station: ")

    # Compute and output the shortest journey and number of stops.
    path, num_stops = find_shortest_path(graph, station_index, start_station, end_station)
    if path:
        print("Shortest path from", start_station, "to", end_station, ":", ' -> '.join(path))
        print("Total number of stops:", num_stops)
    else:
        print("Couldn't generate a path. Please check the station names.")

# Execute the program.
if __name__ == "__main__":
    main()
