"""
Part2
"""
from project1 import RoadNetwork, Road
import csv
import networkx as nx
import matplotlib.pyplot as plt


def load_road_network(file: str) -> Any:
    """Create a road network by using data from a CSV file.
    """
    network = RoadNetwork()
    with open(file) as csv_file:
        reader = csv.reader(csv_file)
        next(reader)
        for row in reader:
            network.add_road(int(row[2]), int(row[3]), float(row[5]))
    return network

def visualize_graph(network: RoadNetwork):
    """Visualize the given network"""
    graph = nx.Graph()
    edges = path_to_edges(network.get_roads())
    graph.add_edges_from(edges)
    nx.draw(graph, with_labels=True)
    plt.show()


def visualize_shortest_path_graph(network: RoadNetwork, shortes_path: list[Road]):
    """Visualize the given network highlighting the shortest path in red.
    """
    highlighted_edges = path_to_edges(shortes_path)
    graph = nx.Graph()
    edges = path_to_edges(network.get_roads())
    for edge in edges:
        graph.add_edge(edge[0], edge[1], color='r' if edge in highlighted_edges else 'b')
    colors = nx.get_edge_attributes(graph, 'color').values()
    nx.draw(graph, edge_color=colors, with_labels=True)
    plt.show()


def path_to_edges(path: list[Road]) -> list[tuple]:
    """Converts a path of roads into a list of edges.
    """
    edges = []
    for road in path:
        endpoints = tuple(road.endpoints)
        edges.append((endpoints[0].address, endpoints[1].address))
    return edges
