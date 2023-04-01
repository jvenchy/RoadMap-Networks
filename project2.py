"""
Part2
"""
from project1 import RoadNetwork
import csv
from typing import Any


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
