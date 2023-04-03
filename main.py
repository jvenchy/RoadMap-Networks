"""CSC111 Winter 2023 Group Project: RoadMap-Networks

Module Description
===============================
This python module contains the main runner functions.

Copyright and Usage Information
===============================

This file is provided solely for the personal and private use of students
taking CSC111 at the University of Toronto St. George campus. All forms of
distribution of this code, whether as given or with any changes, are
expressly prohibited. For more information on copyright for CSC111 materials,
please consult our Course Syllabus.

This file is Copyright (c) 2023 Mario Badr, David Liu, and Isaac Waller.
"""
import project
import random
from python_ta.contracts import check_contracts
from typing import Optional


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
        project.visualize_shortest_path_graph(updated_network, updated_shortest_path)
