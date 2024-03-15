import pandas as pd
import matplotlib.pyplot as plt
from bellman_ford import bellman_ford
from adjacency_list_graph import AdjacencyListGraph

def load_london_underground_graph(csv_file):
    # Reading station data from the spreadsheet.
    df = pd.read_csv(csv_file)
    # Creating a unique set of station names.
    stations = set(df['Station A']).union(set(df['Station B']))
    # Mapping each station to an index for graph-related operations.
    station_index = {station: i for i, station in enumerate(stations)}
    # Initializing a graph to represent connections between stations.
    graph = AdjacencyListGraph(len(stations), True, True)
    # Adding edges to the graph to represent the tube connections.
    for _, row in df.iterrows():
        graph.insert_edge(station_index[row['Station A']], station_index[row['Station B']], 1)

    return graph, station_index

def find_shortest_path(graph, station_index, start_station, end_station):
    # Finding the index values of the start and end stations.
    start_index = station_index.get(start_station)
    end_index = station_index.get(end_station)
    # Making sure both stations are in the graph.
    if start_index is None or end_index is None:
        print(f"Error: Station '{start_station}' or '{end_station}' not in our system.")
        return None, None

    # Running Bellman-Ford algorithm to find the shortest path.
    results = bellman_ford(graph, start_index)

    # Checking for issues like negative cycles in the graph.
    if len(results) > 2 and not results[2]:
        print("Issue detected in the graph, possibly a negative cycle.")
        return None, None

    # Building the shortest path if one exists.
    if results[1][end_index] is None:
        print(f"No route found from {start_station} to {end_station}.")
        return None, None

    # Mapping the route in reverse, from the destination station back to the starting point.
    path = []
    current = end_index
    while current != start_index:
        for station, index in station_index.items():
            if index == current:
                path.append(station)
                break
        current = results[1][current]
    path.append(start_station)
    # Ordering the path from start to end.
    path.reverse()

    # Counting the total stops in the journey.
    num_stops = len(path) - 1

    return path, num_stops

def generate_histogram(graph, station_index):
    journey_counts = []

    # Going through each possible station pair for analysis.
    for start_station in station_index:
        for end_station in station_index:
            if start_station != end_station:
                # Calculating the shortest path for each pair.
                path, num_stops = find_shortest_path(graph, station_index, start_station, end_station)
                if path:
                    # Recording the number of stops for each journey.
                    journey_counts.append(num_stops)

    # Creating a histogram to visualize the frequency of journey lengths.
    plt.hist(journey_counts, bins=range(max(journey_counts)+1), edgecolor='black')
    plt.title('Histogram of Journey Counts Between Stations')
    plt.xlabel('Number of Stops')
    plt.ylabel('Number of Station Pairs')
    plt.show()

def main():
    # Load the station data and prepare the graph.
    csv_file = 'london_underground_graph.csv'
    graph, station_index = load_london_underground_graph(csv_file)
    # Generate and display the histogram of journey counts.
    generate_histogram(graph, station_index)

# Start the program.
if __name__ == "__main__":
    main()
