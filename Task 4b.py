from adjacency_list_graph import AdjacencyListGraph
from dijkstra import dijkstra
import matplotlib.pyplot as plt
import numpy as np


# Function to read CSV file for creating a graph
def read_csv(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()[1:]  # Skip the header line
        data = [line.strip().split(',') for line in lines]
    return data


# To open the CSV file
csv_data = read_csv("london_underground_graph.csv")


# Function to interpret CSV data and create a graph
def create_graph_from_graph(graph_data):
    station_to_indices = {}
    index_counter = 0
    for row in graph_data:
        for station in row[:2]:  # Only consider station names
            if station not in station_to_indices:
                station_to_indices[station] = index_counter
                index_counter += 1

    # Initialize the graph here, after all stations have been accounted for
    data_graph = AdjacencyListGraph(index_counter, directed=False, weighted=True)

    for row in csv_data:
        station_a = station_to_indices[row[0]]
        station_b = station_to_indices[row[1]]
        weight = int(row[2].strip().strip('"'))
        if not data_graph.has_edge(station_a, station_b):
            data_graph.insert_edge(station_a, station_b, weight)

    return data_graph, station_to_indices


# To create the initial graph
graph, station_to_index = create_graph_from_graph(csv_data)


# Function to calculate all-pairs shortest route using Dijkstra's algorithm
def calculate_all_pairs_shortest_paths(data_graph, station_to_indices):
    shortest_paths = {}
    for station, index in station_to_indices.items():
        distances, _ = dijkstra(data_graph, index)
        shortest_paths[station] = {s: distances[station_to_indices[s]] for s in station_to_indices}
    return shortest_paths


# Calculate shortest route for all pairs (pre-closure)
pre_closure_shortest_paths = calculate_all_pairs_shortest_paths(graph, station_to_index)

# To add the edges to remove based on my closure list from task 4a
edges_to_remove = [
    ('Edgware Road', 'Baker Street'), ('Edgware Road', 'Baker Street'),
    ('Baker Street', 'Finchley Road'), ('Bond Street', 'Oxford Circus'),
    ('Finchley Road', 'Wembley Park'), ('Finchley Road', 'Harrow-on-the-Hill'),
    ('Oxford Circus', 'Green Park'), ('Piccadilly Circus', 'Charing Cross'),
    ('Piccadilly Circus', 'Green Park'), ('Green Park', 'Westminster'),
    ('Leicester Square', 'Tottenham Court Road'), ('Waterloo', 'Westminster'),
    ('Waterloo', 'Kennington'), ('Waterloo', 'Bank'),
    ('Lambeth North', 'Elephant & Castle'), ('Grange Hill', 'Hainault'),
    ('Stratford', 'Mile End'), ('Liverpool Street', 'Aldgate'),
    ('Liverpool Street', 'Moorgate'), ('Liverpool Street', 'Aldgate East'),
    ('Aldgate East', 'Tower Hill'), ('St. Paul\'s', 'Chancery Lane'),
    ('Marble Arch', 'Lancaster Gate'), ('High Street Kensington', 'Gloucester Road'),
    ('High Street Kensington', 'Earl\'s Court'), ('Ealing Broadway', 'Ealing Common'),
    ('Earl\'s Court', 'Barons Court'), ('Knightsbridge', 'Hyde Park Corner'),
    ('Victoria', 'St. James\'s Park'), ('Barbican', 'Farringdon'),
    ('King\'s Cross St. Pancras', 'Euston'), ('King\'s Cross St. Pancras', 'Angel'),
    ('Euston', 'Camden Town'), ('Barons Court', 'Hammersmith'),
    ('Hammersmith', 'Acton Town'), ('Hammersmith', 'Turnham Green'),
    ('Acton Town', 'Turnham Green'), ('Wembley Park', 'Harrow-on-the-Hill'),
    ('Harrow-on-the-Hill', 'Moor Park'), ('Canary Wharf', 'North Greenwich'),
    ('Rayners Lane', 'South Harrow'), ('Covent Garden', 'Holborn Central'),
    ('Stockwell', 'Vauxhall')
]

# To remove edges from the graph
for edge in edges_to_remove:
    u, v = edge
    graph.delete_edge(station_to_index[u], station_to_index[v], delete_undirected=True)

# To calculate shortest paths for all pairs (post-closure)
post_closure_shortest_paths = calculate_all_pairs_shortest_paths(graph, station_to_index)


# A function to prepare data for creating a histogram
def prepare_histogram_data(shortest_paths):
    journey_times = []
    for source in shortest_paths:
        for target in shortest_paths[source]:
            if shortest_paths[source][target] != float('inf'):
                journey_times.append(shortest_paths[source][target])
    return journey_times


# A function to prepare data for creating a histogram
def preparing_histogram_data(shortest_paths):
    return [time for paths in shortest_paths.values() for time in paths.values() if time != float('inf')]


pre_closure_times = prepare_histogram_data(pre_closure_shortest_paths)
post_closure_times = prepare_histogram_data(post_closure_shortest_paths)

# To determine the common range for both datasets
time_min = min(min(pre_closure_times), min(post_closure_times))
time_max = max(max(pre_closure_times), max(post_closure_times))

# To define the number of bins for the histogram, and explicitly set the bin edges
bin_edges = np.linspace(time_min, time_max, num=30)  # 30 bins

# To determine the figure size
plt.figure(figsize=(16, 8))


# Creating a histogram for Pre-Closure Times
plt.subplot(1, 2, 1)
plt.hist(pre_closure_times, bins=bin_edges, alpha=0.75, label='Pre-Closure', color='#2B8BBA', edgecolor='black', density=True)
plt.title('Distribution of Journey Times Before Closure', fontsize=15)
plt.xlabel('Journey Time (minutes)', fontsize=12)
plt.ylabel('Density of Station Pairs', fontsize=12)
plt.legend(fontsize=12)
plt.grid(True, linestyle='--', alpha=0.5)

# Creating a histogram for Post-Closure Times
plt.subplot(1, 2, 2)
plt.hist(post_closure_times, bins=bin_edges, alpha=0.75, label='Post-Closure', color='#BA2B2B', edgecolor='black', density=True)
plt.title('Distribution of Journey Times After Closure', fontsize=15)
plt.xlabel('Journey Time (minutes)', fontsize=12)
plt.ylabel('Density of Station Pairs', fontsize=12)
plt.legend(fontsize=12)
plt.grid(True, linestyle='--', alpha=0.5)
# To display the histograms
plt.show()
