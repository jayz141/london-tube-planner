import pandas as pd
from bellman_ford import bellman_ford
from adjacency_list_graph import AdjacencyListGraph

def load_london_underground_graph(csv_file):
    # Reading the station data from the spreadsheet.
    df = pd.read_csv(csv_file)
    # Getting a list of all different stations.
    stations = set(df['Station A']).union(set(df['Station B']))
    # Giving each station a unique number for tracking.
    station_index = {station: i for i, station in enumerate(stations)}
    # Setting up a graph that shows how stations are connected.
    graph = AdjacencyListGraph(len(stations), True, True)
    # Linking each station in the graph based on the data.
    for _, row in df.iterrows():
        graph.insert_edge(station_index[row['Station A']], station_index[row['Station B']], 1)

    return graph, station_index

def find_shortest_path(graph, station_index, start_station, end_station):
    # Finding the positions of the start and end stations in the graph.
    start_index = station_index.get(start_station)
    end_index = station_index.get(end_station)
    # Making sure both stations are part of our map.
    if start_index is None or end_index is None:
        print(f"Error: Can't find one or both of the stations.")
        return None, None

    # Using the Bellman-Ford algorithm to find the shortest path.
    results = bellman_ford(graph, start_index)

    # Checking the results for any issues.
    if len(results) > 2 and not results[2]:
        print("Problem in the network, like a never-ending loop.")
        return None, None

    # If there's no path found, let the user know.
    if results[1][end_index] is None:
        print(f"No way to get from {start_station} to {end_station}.")
        return None, None

    # Working out the steps of the journey from end to start.
    path = []
    current = end_index
    while current != start_index:
        for station, index in station_index.items():
            if index == current:
                path.append(station)
                break
        current = results[1][current]
    path.append(start_station)
    # Making sure the path is in the right order, from start to finish.
    path.reverse()

    # Counting how many stops are in the journey.
    num_stops = len(path) - 1

    return path, num_stops

def main():
    # Load the station data to set up our graph.
    csv_file = 'london_underground_graph.csv'
    graph, station_index = load_london_underground_graph(csv_file)

    # Asking the user where they're starting and ending their journey.
    start_station = input("Enter start station: ")
    end_station = input("Enter end station: ")

    # Finding the shortest route and how many stops it includes.
    path, num_stops = find_shortest_path(graph, station_index, start_station, end_station)
    if path:
        print("Shortest path from", start_station, "to", end_station, ":", ' -> '.join(path))
        print("Total number of stops:", num_stops)
    else:
        print("Couldn't figure out the path. Please check the station names again.")

# Running the program.
if __name__ == "__main__":
    main()
