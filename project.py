"""CSC111 Winter 2023 Group Project: RoadMap-Networks

Module Description
===============================
This python module contains all the functions and classes implemented for this project.

Copyright and Usage Information
===============================

This file is provided solely for the personal and private use of students
taking CSC111 at the University of Toronto St. George campus. All forms of
distribution of this code, whether as given or with any changes, are
expressly prohibited. For more information on copyright for CSC111 materials,
please consult our Course Syllabus.

This file is Copyright (c) 2023 Mario Badr, David Liu, and Isaac Waller.
"""
from __future__ import annotations
import csv
import random
from typing import Any, Optional
import matplotlib.pyplot as plt
import networkx as nx
# You should comment out check contracts when running functions on large dataset.
from python_ta.contracts import check_contracts


@check_contracts
class Node:
    """A node that represents an intersection in a road network.

    Instance Attributes
    - address:
        The address (i.e., unique identifier) of this node.
    - channels:
        A mapping containing the roads connected to this node.
        Each key in the mapping is the address of a neighbour node,
        and the corresponding value is the road leading to that node.

    Representation Invariants:
    - self.address not in self.roads
    - all(self in r.endpoints for r in self.roads.values())
    """
    address: int
    roads: dict[int, Road]

    def __init__(self, address: int) -> None:
        """Initialize this node with the given address and no connections to other nodes."""
        self.address = address
        self.roads = {}

    def __repr__(self) -> str:
        """Return a string representing this node.

        __repr__ is a special method that's called when the object is evaluated in the Python console.
        Provided to help with testing/debugging.

        >>> node = Node(0)
        >>> node
        Node(0)
        """
        return f'Node({self.address})'

    def find_paths(self, destination: int, visited: set[Node]) -> list[list[Road]]:
        """Return a list of all possible paths from this vertex to the given destination that do NOT use any nodes in
        visited.

        Preconditions:
        - self not in visited
        """
        paths = []
        if self.address == destination:
            return [[]]
        else:
            new_visited = visited.union({self})
            for address in self.roads:
                road = self.roads[address]
                u = road.get_other_endpoint(self)
                if u not in new_visited and not road.closed:
                    rec_value = u.find_paths(destination, new_visited)
                    if rec_value == [[]]:
                        paths.append([road])
                    else:
                        paths.extend([[road] + path for path in rec_value])
            return paths


@check_contracts
class Road:
    """An edge that connects two intersections."""
    endpoints: set[Node]
    length: float
    closed: bool

    def __init__(self, node1: Node, node2: Node, length: float) -> None:
        """Initialize an empty road with the two given nodes.
        Also add this road to node1 and node2.
        Preconditions:
            - node1 != node2
        """
        self.endpoints = {node1, node2}
        self.length = length
        node1.roads[node2.address] = self
        node2.roads[node1.address] = self
        self.closed = False

    def get_other_endpoint(self, node: Node) -> Node:
        """Return the endpoint of this road that is not equal to the given node.

        Preconditions:
            - node in self.endpoints
        """
        return (self.endpoints - {node}).pop()

    def __repr__(self) -> str:
        """Return a string representing this channel.

        __repr__ is a special method that's called when the object is evaluated in the Python console.

        >>> road = Road(Node(0), Node(1), 0.0)
        >>> repr(road) in {'Road(Node(0), Node(1))', 'Road(Node(1), Node(0))'}
        True
        """
        endpoints = list(self.endpoints)
        return f'Road({endpoints[0]}, {endpoints[1]})'


@check_contracts
class RoadNetwork:
    """A network consisting of nodes connected to each other which represents a road network.

     Private Instance Attributes:
        - _nodes: A mapping from node address to Node in this network.

    Representation Invariants:
    - all(a == self._nodes[a].address for a in self._nodes)
    """
    _nodes: dict[int, Node]

    def __init__(self) -> None:
        """Initialize an empty RoadNetwork."""
        self._nodes = {}

    def add_node(self, address: int) -> Node:
        """Add a new node with the given address to this network and return it.

        The new node is not adjacent to any other nodes.
        Preconditions:
            - address not in self._nodes
        """
        new_node = Node(address)
        self._nodes[address] = new_node
        return new_node

    def add_road(self, address1: int, address2: int, length: float) -> None:
        """Add a new road between the nodes with the two given addresses.

        If a given address doesn't correspond to a node in this network, first create a new
        node for that address.

        Preconditions:
        - address1 != address2
        """
        if address1 not in self._nodes:
            self.add_node(address1)
        if address2 not in self._nodes:
            self.add_node(address2)

        Road(self._nodes[address1], self._nodes[address2], length)

    def topology_to_dict(self) -> dict[int, set[int]]:
        """Return a dictionary containing the adjacency relationships for every node in this network.

        In the returned dictionary:
            - Each key is an address of a node in this network.
            - The corresponding value is the set of addresses of the nodes that are adjacent to
                the corresponding key's node in this network.
        """
        adjacencies_so_far = {}

        for address, node in self._nodes.items():
            adjacencies_so_far[address] = set(node.roads)

        return adjacencies_so_far

    def get_node_addresses(self) -> list[int]:
        """Return the list of all node addresses in this network."""
        return list(self._nodes.keys())

    def get_roads(self) -> list[Road]:
        """Return a list of all the roads in this network."""
        roads = set()
        for node in self._nodes.values():
            for road in node.roads.values():
                roads.add(road)
        return list(roads)

    def find_paths(self, start: int, end: int) -> list[list[Road]]:
        """Return a list of all paths in this network between start and end.

        Preconditions:
            - start in self._nodes
            - end in self._nodes
        """
        start_node = self._nodes[start]
        return start_node.find_paths(end, set())

    def find_shortest_path(self, start: int, end: int) -> list[Road]:
        """Find the path with the minimum distance from start node to end node.

        Preconditions:
        - start in self._nodes
        - end in self._nodes
        """
        paths = self.find_paths(start, end)
        if start == end or paths == []:
            return []
        else:
            return shortest_path(paths)

    def insert_traffic(self, road_to_edit: Road) -> None:
        """
        Insert traffic on this road by setting the road to have traffic (which we define as DOUBLE the edge distance)

        Preconditions:
            - all(endpoint.address in network._nodes for endpoint in road.endpoints)
        """
        endpoints = tuple(road_to_edit.endpoints)
        self._nodes[endpoints[0].address].roads[endpoints[1].address].length *= 2

    def insert_closure(self, road_to_edit: Road) -> None:
        """
        Insert closure on this road by setting road.closed to True, essentially erasing it from the network while the
        boolean is set to true.

        Preconditions:
                - all(endpoint.address in network._nodes for endpoint in road.endpoints)
        """
        endponits = tuple(road_to_edit.endpoints)
        self._nodes[endponits[0].address].roads[endponits[1].address].closed = True


@check_contracts
def compute_path_distance(path: list[Road]) -> float:
    """Return the total length of path.

    Preconditions:
    - path != []
    """
    distance = 0.0
    for road in path:
        distance += road.length
    return distance


@check_contracts
def shortest_path(paths: list[list[Road]]) -> list[Road]:
    """Returns the path with the shortest length.

    Preconditions:
    - paths != []
    """
    selected_path = paths[0]
    shortest_distance = compute_path_distance(paths[0])
    for path in paths:
        path_distance = compute_path_distance(path)
        if path_distance < shortest_distance:
            shortest_distance = path_distance
            selected_path = path
    return selected_path


def load_road_network(file: str) -> RoadNetwork:
    """Create a road network by using data from a CSV file.
    """
    network = RoadNetwork()
    with open(file) as csv_file:
        reader = csv.reader(csv_file)
        next(reader)
        for row in reader:
            network.add_road(int(row[2]), int(row[3]), float(row[5]))
    return network


def visualize_graph(network: RoadNetwork) -> None:
    """Visualize the given network"""
    graph = nx.Graph()
    edges = path_to_edges(network.get_roads())
    graph.add_edges_from(edges)
    nx.draw_random(graph, with_labels=True)
    plt.show()


def visualize_shortest_path_graph(network: RoadNetwork, shortes_path: list[Road]) -> None:
    """Visualize the given network highlighting the shortest path in red.
    """
    highlighted_edges = path_to_edges(shortes_path)
    graph = nx.Graph()
    edges = path_to_edges(network.get_roads())
    for edge in edges:
        graph.add_edge(edge[0], edge[1], color='r' if edge in highlighted_edges else 'b')
    colors = nx.get_edge_attributes(graph, 'color').values()
    nx.draw_random(graph, edge_color=colors, with_labels=True)
    plt.show()


def path_to_edges(path: list[Road]) -> list[tuple]:
    """Converts a path of roads into a list of edges.
    """
    edges = []
    for road in path:
        endpoints = tuple(road.endpoints)
        edges.append((endpoints[0].address, endpoints[1].address))
    return edges


@check_contracts
def generate_network_with_event(network: RoadNetwork, selected_road: Road, event: str) -> RoadNetwork:
    """
    Generate a duplicate network where a specific road has a specific event. Useful for most_valuable_road function.

    Preconditions:
        - event == 'traffic' or event == 'closure'
    """
    # build a duplicate network ground up
    event_network = RoadNetwork()
    for road in network.get_roads():
        end_lst = list(road.endpoints)
        address1 = end_lst[0].address
        address2 = end_lst[1].address
        event_network.add_road(address1, address2, road.length)

    # add event
    if event == 'traffic':
        event_network.insert_traffic(selected_road)
    else:
        event_network.insert_closure(selected_road)

    return event_network


@check_contracts
def most_valuable_road(network: RoadNetwork, start: int, end: int, event: str) -> Any:
    """
    For each road in network, compares original shortest path to the shortest_path with a network
    where some given road has an event, and returns most valuable road in terms of distance difference for the given
    event. If no road differs in shortest_path given an event (when if statement is never evaluated to true),
    return None. If two roads are of the same importance, it will return the first one it found.

    Preconditions:
    - event == 'traffic' or event == 'closure'
    """
    selected_road = None
    max_distance = 0

    for road in network.get_roads():
        event_network = generate_network_with_event(network, road, event)
        updated_distance = compute_path_distance(event_network.find_shortest_path(start, end))
        original_distance = compute_path_distance(network.find_shortest_path(start, end))

        if updated_distance - original_distance > max_distance:
            selected_road = road

    return selected_road


if __name__ == '__main__':
    import doctest

    doctest.testmod(verbose=True)

    import python_ta

    python_ta.check_all(config={
        'max-line-length': 120,
        'extra-imports': ['networkx', 'matplotlib.pyplot', 'random', 'csv'],
        'allowed-io': ['load_road_network'],
        'disable': ['too-many-nested-blocks']
    })
