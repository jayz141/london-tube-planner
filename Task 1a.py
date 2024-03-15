import pandas as pd
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

def main():
    # Loading graph and stations dictionary
    graph, stations = create_graph('london_underground_graph.csv')

    # Asking the user to enter his start and his destination
    start, end = input("Enter start station: "), input("Enter end station: ")

    # Finding the shortest path between the start and end
    path, time = find_shortest_path(graph, stations, start, end)

    # Showing the path and total travel time
    print(f"Path: {' -> '.join(path)}\nDuration: {time} minutes")

if __name__ == "__main__":
    main()
