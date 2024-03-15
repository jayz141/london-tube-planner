import pandas as pd
from dijkstra import dijkstra
from adjacency_list_graph import AdjacencyListGraph
import matplotlib.pyplot as plt

def load_london_underground_graph(csv_file):
    # Load station data from the spreadsheet, creating a list of all stations.
    df = pd.read_csv(csv_file)
    stations = set(df['Station A']).union(set(df['Station B']))
    # Assign a unique index to each station for easy reference in the graph.
    station_index = {station: i for i, station in enumerate(stations)}
    # Set up the graph to represent the layout of the Underground network.
    graph = AdjacencyListGraph(len(stations), True, True)
    # Add connections between stations based on the data.
    for _, row in df.iterrows():
        graph.insert_edge(station_index[row['Station A']], station_index[row['Station B']], 1)

    return graph, station_index

def find_shortest_path(graph, station_index, start_station, end_station):
    # Get the numbers for where the stations starts and ends.
    start_index = station_index.get(start_station)
    end_index = station_index.get(end_station)
    # Confirm that both the starting and ending stations are present in the network.
    if start_index is None or end_index is None:
        return None, None

    # Apply Dijkstra's algorithm to find the shortest path.
    d, pi = dijkstra(graph, start_index)
    # If no path is found, return None.
    if pi[end_index] is None:
        return None, None

    # Construct the route by tracing it backwards from the end station to the start.
    path = []
    current = end_index
    while current != start_index:
        for station, index in station_index.items():
            if index == current:
                path.append(station)
                break
        current = pi[current]
    path.append(start_station)
    # Arrange the path from start to destination.
    path.reverse()

    # Calculate the total number of stops on the path.
    num_stops = len(path) - 1
    return path, num_stops

def analyze_journeys(graph, station_index):
    # Analyze and count the number of stops for all journey combinations.
    journey_counts = []
    for start_station in station_index:
        for end_station in station_index:
            if start_station != end_station:
                path, num_stops = find_shortest_path(graph, station_index, start_station, end_station)
                if path:
                    journey_counts.append(num_stops)

    return journey_counts

def main():
    # Load the graph with London Underground data.
    csv_file = 'london_underground_graph.csv'
    graph, station_index = load_london_underground_graph(csv_file)
    # Analyze all journeys and get their stop counts.
    journey_counts = analyze_journeys(graph, station_index)

    # Plot a histogram of the journey counts.
    plt.hist(journey_counts, bins=range(max(journey_counts)+1), edgecolor='black')
    plt.title('Histogram of Journey Counts Between Stations')
    plt.xlabel('Number of Stops')
    plt.ylabel('Number of Station Pairs')
    plt.show()

# Execute the main function to run the program.
if __name__ == "__main__":
    main()
