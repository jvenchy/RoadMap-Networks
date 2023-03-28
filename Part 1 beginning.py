from __future__ import annotations
from typing import Optional
from python_ta.contracts import check_contracts
NodeAddress = int | tuple[int, int]


@check_contracts
class Node:
    """A node that represents an intersection.

    Instance Attributes
    - address:
        The address (i.e., unique identifier) of this node.
        This replaces the "item" attribute in the _Vertex class from lecture.
    - channels:
        A mapping containing the channels for this node.
        Each key in the mapping is the address of a neighbour node,
        and the corresponding value is the channel leading to that node.
        This replaces the "neighbours" attribute in the _Vertex class from lecture.

    Representation Invariants:
    - ...
    """
    address: NodeAddress
    channels: dict[NodeAddress, Channel]  # Notes: Node address is the adress of the target node of the channel

    def __init__(self, address: NodeAddress) -> None:
        """Initialize this node with the given address and no connections to other nodes."""
        self.address = address
        self.channels = {}

    def __repr__(self) -> str:
        """Return a string representing this node.

        __repr__ is a special method that's called when the object is evaluated in the Python console.
        Provided to help with testing/debugging.

        >>> node = Node(0)
        >>> node
        Node(0)
        """
        return f'Node({self.address})'

    ###############################################################################################
    # Computing all paths (you only need to look at the method below in Part 4)
    ###############################################################################################
    def find_paths(self, destination: NodeAddress, visited: set[Node]) -> list[list[Channel]]:
        """Return a list of all possible paths from this vertex that do NOT use any nodes in visited.

        The paths may be returned in any order. NOTE: unlike lecture, where paths were defined as a
        sequence of vertices, here a path is defined as a sequence of Channels (i.e., edges). This
        representing a bit more helpful for this assignment.
        """
        possible_paths = []
        for item in self.channels:
            path = self.find_paths_helper(item, destination, visited, [])
            if path:
                possible_paths.append(path)
        return possible_paths

    def find_paths_helper(self, item: NodeAddress, destination: NodeAddress, visited: set[Node], path: list) \
            -> list[Channel]:
        """
        Helper Funtion to find the path for each item.
        """
        other_end_node = self.channels[item].get_other_endpoint(self)
        if other_end_node not in visited:
            temp = visited
            temp.add(self)
            path.append(self.channels[item])
            if item != destination:
                self.find_path_recursion_helper(destination, temp, path, other_end_node)
        return path

    def find_path_recursion_helper(self, destination: NodeAddress, temp: set[Node], path: list, other_end_node: Node) \
            -> None:
        """
        Helper funciton to find the path recursivly.
        """
        for x in other_end_node.channels:
            if other_end_node.channels[x] not in path:
                other_end_node.find_paths_helper(x, destination, temp, path)


@check_contracts
class Channel:
    """A link (or "edge") connecting two nodes in an interconnection network.

    Instance Attributes:
    - endpoints: The two nodes that are linked by this channel.
    - occupant:
        The packet that is currently being transmitted through this channel,
        or None if the channel is currently not in use.
    - buffer:
        A list of the packets that are currently waiting to use this channel, if any.
        Note: both endpoints of the channel use the same buffer.

    Representation Invariants:
    - ...
    """
    endpoints: set[Node]
    occupant: Optional[Packet]
    buffer: list[Packet]

    def __init__(self, node1: Node, node2: Node) -> None:
        """Initialize an empty channel with the two given nodes.

        Also add this channel to node1 and node2.

        Preconditions:
            - node1 != node2
            - node1 and node2 are not already connected by a channel
        """
        self.endpoints = {node1, node2}
        node1.channels[node2.address] = self
        node2.channels[node1.address] = self
        self.occupant = None
        self.buffer = []

    def add_packet(self, packet: Packet, start: Node) -> None:
        """Add the given packet to this channel and update the packet's next_stop attribute.

        If this channel is currently empty, the packet is added as its occupant.
        But if this channel is currently occupied, the packet as added to the channel's buffer.

        The packet starts from the given start node (which must be one of the endpoints of this channel).
        The packet's next_stop attribute is set to the other endpoint of this channel. This occurs
        whether the packet is added as an occupant or into this channel's buffer.

        Preconditions:
            - start in self.endpoints

        >>> node0 = Node(0)
        >>> node1 = Node(1)
        >>> my_channel = Channel(node0, node1)
        >>> new_packet = Packet(0, 0, 1)
        >>> my_channel.add_packet(new_packet, node0)
        >>> my_channel.occupant is new_packet
        True
        >>> new_packet.next_stop
        Node(1)
        """
        packet.next_stop = self.get_other_endpoint(start)
        if self.occupant is None:
            self.occupant = packet
        else:
            self.buffer.append(packet)

    def get_other_endpoint(self, node: Node) -> Node:
        """Return the endpoint of this channel that is not equal to the given node.

        Preconditions:
            - node in self.endpoints
        """
        return (self.endpoints - {node}).pop()

    def remove_packet(self) -> Packet:
        """Return this channel's current occupant.

        Move the first packet in this channel's buffer to be the new occupant.
        If the buffer is empty, set self.occupant to None.

        Preconditions:
            - self.occupant is not None
        """
        old_occupant = self.occupant
        if not self.buffer:
            self.occupant = None
        else:
            self.occupant = self.buffer.pop(0)
        return old_occupant

    def total_occupancy(self) -> int:
        """Return the number of packets in this channel's buffer and 'occupant' spot.

        (Useful in Part 4.)

        >>> my_channel = Channel(Node(0), Node(1))
        >>> my_channel.total_occupancy()
        0
        """
        if self.occupant is None:
            # In this case, self.buffer must be empty
            return 0
        else:
            return 1 + len(self.buffer)

    def __repr__(self) -> str:
        """Return a string representing this channel.

        __repr__ is a special method that's called when the object is evaluated in the Python console.

        >>> channel = Channel(Node(0), Node(1))
        >>> repr(channel) in {'Channel(Node(0), Node(1))', 'Channel(Node(1), Node(0))'}
        True
        """
        endpoints = list(self.endpoints)
        return f'Channel({endpoints[0]}, {endpoints[1]})'


@check_contracts
class Packet:
    """A packet containing data being communicated from one node to another in an interconnection network.

    Instance Attributes:
    - identifier: A unique identifier for this packet.
    - source: The ADDRESS of the node that sent this packet.
    - destination: The ADDRESS of the node that is meant to receive this packet.
    - next_stop: The next NODE that this packet is travelling to in the network,
        or None if the next node has not yet been set.
        (This is set by the network's *routing algorithm*; see Part 2 of this assignment.)

    Representation Invariants:
    - ...
    """
    identifier: int
    source: NodeAddress
    destination: NodeAddress
    next_stop: Optional[Node]

    def __init__(self, identifier: int, source: NodeAddress, destination: NodeAddress) -> None:
        """Initialize this packet with the given information.

        Preconditions:
            - source != destination
        """
        self.identifier = identifier
        self.source = source
        self.destination = destination
        self.next_stop = None

    def __repr__(self) -> str:
        """Return a string representation of this packet.

        __repr__ is a special method that's called when the object is evaluated in the Python console.

        >>> packet = Packet(100, 1, 2)
        >>> packet
        Packet(100, 1, 2)
        >>> packet = Packet(100, (1, 0), (0, 0))
        >>> packet
        Packet(100, (1, 0), (0, 0))
        """
        return f'Packet({self.identifier}, {self.source}, {self.destination})'


###############################################################################
# The AbstractNetwork class
###############################################################################
@check_contracts
class AbstractNetwork:
    """An abstract class for a network of nodes connected based on a topology,
    where packets in the network are routed by a routing algorithm.

    Private Instance Attributes (you should not access these directly!):
        - _nodes: A mapping from node address to Node in this network.

    Representation Invariants:
    - ...
    """
    _nodes: dict[NodeAddress, Node]

    def __init__(self) -> None:
        """Initialize an empty AbstractNetwork."""
        self._nodes = {}

    def add_node(self, address: NodeAddress) -> Node:
        """Add a new node with the given address to this network and return it.

        The new node is not adjacent to any other nodes. (This violates our assumption that
        interconnection networks are connected; but, we'll assume that whenever a new node
        is added, edges will also be added for that node.)

        Preconditions:
            - address not in self._nodes
        """
        new_node = Node(address)
        self._nodes[address] = new_node
        return new_node

    def add_channel(self, address1: NodeAddress, address2: NodeAddress) -> None:
        """Add a new channel between the nodes with the two given addresses.

        If a given address doesn't correspond to a node in this network, first create a new
        node for that address.

        Preconditions:
        - address1 != address2
        """
        if address1 not in self._nodes:
            self.add_node(address1)
        if address2 not in self._nodes:
            self.add_node(address2)

        Channel(self._nodes[address1], self._nodes[address2])

    def topology_to_dict(self) -> dict[NodeAddress, set[NodeAddress]]:
        """Return a dictionary containing the adjacency relationships for every node in this network.

        In the returned dictionary:
            - Each key is an address of a node in this network.
            - The corresponding value is the set of addresses of the nodes that are adjacent to
                the corresponding key's node in this network.

        We have mainly provided this method to help you test your work in generating topologies
        We have mainly provided this method to help you test your work in generating topologies
        (Part 1, Question 3), though of course you're free to use it throughout this assignment.
        """
        adjacencies_so_far = {}

        for address, node in self._nodes.items():
            adjacencies_so_far[address] = set(node.channels)

        return adjacencies_so_far

    def get_node_addresses(self) -> set[NodeAddress]:
        """Return the set of all node addresses in this network."""
        return set(self._nodes.keys())  # Note: calling dict.keys is technically unnecessary, but added for clarity

    ###############################################################################################
    # Packet routing methods (you only need to look at the methods below in Part 2)
    ###############################################################################################
    def add_new_packet(self, packet: Packet) -> Channel:
        """Add a new packet to this network. Return the channel this packet is added to.

        The packet begins at its source node, and is added to a channel using this network's
        routing algorithm. When a packet is added to a channel, it is either added as the channel's
        occupant (if the channel has no occupant), or added to the end of the channel's buffer.

        Preconditions:
        - packet.source in self._nodes
        - packet.destination in self._nodes
        """
        selected_channel = self.route_packet(packet.source, packet)
        selected_channel.add_packet(packet, self._nodes[packet.source])

        return selected_channel

    def activate_channel(self, channel: Channel) -> Optional[Channel]:
        """Move the occupant packet of the given channel to its next_stop and return the next channel
        that the packet is added to, if any.

        Return None if the packet has reached its destination after exiting the given channel.
        Do nothing if the given channel does not have an occupant.

        Additionally, move the first packet in the given channel's buffer (if any) to be its
        new occupant. (Implementation note: this happens in Channel.remove_packet method.)
        """
        packet = channel.remove_packet()

        if packet.next_stop.address == packet.destination:
            return None
        else:
            selected_channel = self.route_packet(packet.next_stop.address, packet)
            selected_channel.add_packet(packet, packet.next_stop)

            return selected_channel

    def route_packet(self, current_address: NodeAddress, packet: Packet) -> Optional[Channel]:
        """Return the channel that the packet should traverse next, given that it has
        just arrived at the node with address current_address.

        That is, the returned channel has the node corresponding to current_address as
        one of its endpoints. Ideally, but not necessarily, traversing the returned channel
        helps get the given packet closer to its destination.

        Return None if the current_address is equal to the packet's destination!

        Preconditions:
        - current_address in self._nodes
        - packet.source in self._nodes
        - packet.destination in self._nodes

        NOTE: This method is abstract, and is the reason why the AbstractNetwork class is
        abstract. You'll implement this method several different ways on this assignment!
        """
        raise NotImplementedError

    def transmit_packet(self, packet: Packet) -> list[NodeAddress]:
        """Communicate the given packet through this network, and return the path it took.

        The packet begins at its source node, and then (using route_packet) enters its first channel.
        Then, by repeatedly calling activate_channel, the packet moves through channels in this
        network until eventually it reaches its destination.

        Accumulate a list of all NodeAddresses visited by the packet, *including* its source and
        destination addresses. Return this list.

        Preconditions:
            - self has NO occupied channels (so you don't need to worry about the packet
              being stored in a buffer)
            - packet.source in self._nodes
            - packet.destination in self._nodes

        Implementation Hint:
            - You can use the packet.next_stop attribute to keep track of which nodes the packet
              is visiting
        """
        packet_path = [packet.source]
        selected_channel = self.add_new_packet(packet)
        while selected_channel is not None:
            packet_path.append(packet.next_stop.address)
            selected_channel = self.activate_channel(selected_channel)
        return packet_path

    ###############################################################################################
    # Computing all paths (you only need to look at the method below in Part 4)
    ###############################################################################################
    def find_paths(self, start: NodeAddress, end: NodeAddress) -> list[list[Channel]]:
        """Return a list of all paths in this network between start and end.

        Preconditions:
            - start in self._nodes
            - end in self._nodes

        NOTE: This method is implemented for you, and you should not change it.
        You are responsible for implementing the recursive method Node.find_paths.
        """
        start_node = self._nodes[start]
        return start_node.find_paths(end, set())


if __name__ == '__main__':
    import doctest

    doctest.testmod(verbose=True)

    # When you are ready to check your work with python_ta, uncomment the following lines.
    # (In PyCharm, select the lines below and press Ctrl/Cmd + / to toggle comments.)
    # You can use "Run file in Python Console" to run PythonTA,
    # and then also test your methods manually in the console.
    import python_ta
    python_ta.check_all(config={
        'max-line-length': 120,
        'disable': ['E9992', 'E9997']
    })
