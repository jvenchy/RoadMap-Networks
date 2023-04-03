"""CSC111 Winter 2023 Group Project: RoadMap-Networks

Module Description
===============================
This python module contains the main runner functions.

Copyright and Usage Information
===============================

This file is open for public use.

This file is Copyright (c) 2023 Ayush Aran, Sai Swaroop Kaja, Muhammad Taha Usman, Josh Singh Shergill.
"""
import random
from typing import Optional

from python_ta.contracts import check_contracts

import project

@check_contracts
def starting_runner(file: str) -> None:
    """
    Visualize just the node network, recommended to be done first for determining which start and end addresses the
    user wants to use in the main runner.
    """
    network = project.load_road_network(file)
    project.visualize_graph(network)


@check_contracts
def main_runner(file: str, start: int, end: int, event: Optional[str] = None) -> None:
    """Main runner for visualizing shortest path between two intersections. Important Note: the nodes will not be in the
    same position every time as they are randomly drawn thanks to NetworkX.draw_random. This is only a visualization
    quirk and doesn't impact any other part of the project!

    Preconditions:
        - event == 'traffic' or event == 'closure' or event is None
        - start in network._nodes
        - end in network._nodes
    """
    network = project.load_road_network(file)
    if event is None:
        path = network.find_shortest_path(start, end)
        project.visualize_shortest_path_graph(network, path)
    else:
        road = random.choice(network.get_roads())
        updated_network = project.generate_network_with_event(network, road, event)
        updated_shortest_path = updated_network.find_shortest_path(start, end)
        print('most valuable road in', event, ':', project.most_valuable_road(network, start, end, event))
        project.visualize_shortest_path_graph(updated_network, updated_shortest_path)
