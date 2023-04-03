"""
Part 1
"""

from __future__ import annotations


# from python_ta.contracts import check_contracts

# @check_contracts
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
                if u not in new_visited:
                    rec_value = u.find_paths(destination, new_visited)
                    if rec_value == [[]]:
                        paths.append([road])
                    else:
                        paths.extend([[road] + path for path in rec_value])
            return paths    


# @check_contracts
class Road:
    """An edge that connects two intersections."""
    endpoints: set[Node]
    length: float
    traffic: list

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
        self.traffic = []

    def get_other_endpoint(self, node: Node) -> Node:
        """Return the endpoint of this road that is not equal to the given node.

        Preconditions:
            - node in self.endpoints
        """
        return (self.endpoints - {node}).pop()

    def __repr__(self) -> str:
        """Return a string representing this channel.

        __repr__ is a special method that's called when the object is evaluated in the Python console.

        >>> road = Road(Node(0), Node(1))
        >>> repr(road) in {'Road(Node(0), Node(1))', 'Road(Node(1), Node(0))'}
        True
        """
        endpoints = list(self.endpoints)
        return f'Road({endpoints[0]}, {endpoints[1]})'


# @check_contracts
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
        
        
# @check_contracts
def compute_path_distance(path: list[Road]) -> float:
    """Return the total length of path.

    Preconditions:
    - path != []
    """
    distance = 0.0
    for road in path:
        distance += road.length
    return distance


# @check_contracts
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


if __name__ == '__main__':
    import doctest

    doctest.testmod(verbose=True)

    # import python_ta
    #
    # python_ta.check_all(config={
    #     'max-line-length': 120,
    #     'disable': ['E9992', 'E9997']
    # })
