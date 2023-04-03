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
def runner(file: str, start: int, end: int, event: Optional[str] = None) -> None:
    """Main runner

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
