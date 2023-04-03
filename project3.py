"""
Part 3
"""
import math
import random

from project1 import RoadNetwork, Road
import project2
import project1


def generate_network_with_event(network: RoadNetwork, road: Road, event: str) -> RoadNetwork:
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
        insert_traffic(event_network, road)
    else:
        insert_closure(event_network, road)

    return event_network


def insert_traffic(network: RoadNetwork, road_to_edit: Road) -> None:
    """
    Insert traffic on this road by setting the road to have traffic (which we define as DOUBLE the edge distance)

    Preconditions:
        - all(endpoint in network._nodes for endpoint in road.endpoints)
    """
    for road in network.get_roads():
        if road == road_to_edit:
            road.length *= 2


def insert_closure(network: RoadNetwork, road_to_edit: Road) -> None:
    """
    Insert closure on this road by setting road.closed to True, essentially erasing it from the network while the
    boolean is set to true.

    Preconditions:
            - all(endpoint in network._nodes for endpoint in road.endpoints)
    """
    for road in network.get_roads():
        if road == road_to_edit:
            road.closed = True


def visualize_shortest_path_graph_with_event(network: RoadNetwork, start: int, end: int, event: str):
    """
    Visualize the network's shortest path given the event on a random road.
    Preconditions:
        - event == 'traffic' or event == 'closure'
        - start in network._nodes
        - end in network._nodes
    """
    road_chosen = random.choice(network.get_roads())
    updated_network = generate_network_with_event(network, road_chosen, event)
    updated_shortest_path = updated_network.find_shortest_path(start, end)

    project2.visualize_shortest_path_graph(updated_network, updated_shortest_path)


def most_valuable_road(network: RoadNetwork, start: int, end: int, event: str) -> Road | None:
    """
    For each road in network, compares original shortest path to the shortest_path with a network
    where some given road has an event, and returns most valuable road in terms of distance difference for the given
    event. If no road differs in shortest_path given an event (when if statement is never evaluated to true),
    return None. If two roads are of the same importance, it will return the first one it found.
    Preconditions:
    - event == 'traffic' or event == 'closure'
    """
    most_valuable_road = None
    largest_distance_difference_so_far = 0

    for road in network.get_roads():
        event_network = generate_network_with_event(network, road, event)
        updated_distance = project1.compute_path_distance(event_network.find_shortest_path(start, end))
        original_distance = project1.compute_path_distance(network.find_shortest_path(start, end))

        if updated_distance - original_distance > largest_distance_difference_so_far:
            most_valuable_road = road

    return most_valuable_road
