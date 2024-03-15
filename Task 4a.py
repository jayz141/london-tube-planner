from adjacency_list_graph import AdjacencyListGraph
from mst import kruskal
from bfs import bfs


# To read CSV file for creating a graph
def read_csv(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()[1:]  # To skip the header line from the CSV file
        data = [line.strip().split(',') for line in lines]
    return data


# To create a graph with station names to unique indices
def create_and_process_graph(london_underground_data):
    station_to_indices = {}
    index_counter = 0
    for row in london_underground_data:
        for station in row[:2]:  # Only takes data from the first two columns as station names
            if station not in station_to_indices:
                station_to_indices[station] = index_counter
                index_counter += 1

    num_stations = len(station_to_indices)
    data_graph = AdjacencyListGraph(num_stations, directed=False, weighted=True)  # To initialize graph with the number of stations

    # Add edges to the graph
    for row in csv_data:
        u = station_to_indices[row[0]]
        v = station_to_indices[row[1]]
        weight = int(row[2].strip().strip('"'))
        if not data_graph.has_edge(u, v):
            data_graph.insert_edge(u, v, weight)

    return data_graph, station_to_indices


# To find the minimum spanning tree using Kruskal's algorithm from the library and identify the edges to shut
def determine_and_display_shutdowns(data_graph, station_to_indices):
    mst = kruskal(data_graph)
    edges_to_shut = [edge for edge in data_graph.get_edge_list() if edge not in mst.get_edge_list()]
    index_to_station = {index: station for station, index in station_to_indices.items()}
    edges_to_remove_names = [(index_to_station[u], index_to_station[v]) for u, v in edges_to_shut]

    # To verify that the connection still remains feasible
    is_connected = True
    for starting_node in range(len(station_to_indices)):
        distances, _ = bfs(data_graph, starting_node)
        if float('inf') in distances:
            is_connected = False
            break

    # To print the result
    if is_connected:
        print("Recommended Tube Line Shutdowns for Operational Efficiency:")
        print(f"{'No.':<10} {'Shutdown Segment':<60}")
        print("-" * 70)
        for i, (station_a, station_b) in enumerate(edges_to_remove_names, 1):
            shutdown_segment = f"{station_a} -- {station_b}"
            print(f"{i:<10} {shutdown_segment:<60}")
    else:
        print("Unable to recommend shutdowns: Network connectivity cannot be maintained with any tube line closures.")


# To open the CSV file
if __name__ == "__main__":
    csv_data = read_csv("london_underground_graph.csv")
    if csv_data:
        graph, station_to_index = create_and_process_graph(csv_data)
        determine_and_display_shutdowns(graph, station_to_index)
