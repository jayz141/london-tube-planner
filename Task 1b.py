import pandas as pd
import matplotlib.pyplot as plt
from dijkstra import dijkstra
from adjacency_list_graph import AdjacencyListGraph

def create_graph(csv_file):
    # Reading the CSV file into a DataFrame
    df = pd.read_csv(csv_file)

    # Creating a dictionary, mapping each station to a unique index
    stations = {station: idx for idx, station in enumerate(pd.unique(df[['Station A', 'Station B']].values.ravel('K')))}

    # Starting the graph with the number of unique stations
    graph = AdjacencyListGraph(len(stations), True, True)

    # Adding edges to the graph from the DataFrame
    for _, row in df.iterrows():
        graph.insert_edge(stations[row['Station A']], stations[row['Station B']], row['Travel Time (minutes)'])

    return graph, stations

def find_shortest_path(graph, stations, start, end):
    # Starting an empty path and setting the current node to the end station
    path, current = [], stations[end]

    # Applying Dijkstra's algorithm to find the shortest path
    distances, predecessors = dijkstra(graph, stations[start])

    # Backtracking from the end station to the start station
    while current != None:
        # Inserting the station name at the beginning of the path
        path.insert(0, next(station for station, idx in stations.items() if idx == current))
        # Moves to the predecessor of the current node
        current = predecessors[current]

    return path, distances[stations[end]]

def calculate_all_journey_times(graph, stations):
    journey_times = []
    for start_idx in stations.values():
        distances, _ = dijkstra(graph, start_idx)
        journey_times.extend(distances)
    return journey_times


def plot_histogram(journey_times):
    plt.hist(journey_times, bins=range(0, max(journey_times) + 1, 5), edgecolor='black')
    plt.title('Histogram of Journey Times Between Station Pairs')
    plt.xlabel('Journey Time in Minutes')
    plt.ylabel('Number of Station Pairs')
    plt.show()

def main():
    graph, stations = create_graph('london_underground_graph.csv')

    # I am no longer using the code below so I have put it in comments
    # start, end = input("Enter start station: "), input("Enter end station: ")
    # path, time = find_shortest_path(graph, stations, start, end)
    # print(f"Path: {' -> '.join(path)}\nDuration: {time} minutes")

    # Calculating journey times for all station pairs and plotting the histogram
    all_journey_times = calculate_all_journey_times(graph, stations)
    plot_histogram(all_journey_times)

if __name__ == "__main__":
    main()
