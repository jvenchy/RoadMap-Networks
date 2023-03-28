Github: 

Proposal:
Take road network data (of a city preferably) and parse it into a graph network. Determine the shortest path. Allow the ability to generate traffic (slower weightage of edge) and road closures (no access to that edge) to determine updated shortest path. Compare the two and make insightful data observations.


Program Requirements and Reproducibility:
Requirements.txt
List of external libraries our program relies on:


Main.py module 
Load the necessary files from the datasets (if applicable).
Perform your computations on the data.
Produce an output (which may or may not be interactive).

Functions List To Implement:
A function to parse road network files into a node and edges network

Function for generating road-node network
Network class
Road/Channel class
Node Class

Functions for randomly generating road closures + traffic throughout the node-road network
		
Functions for determining efficiency of path based on most optimal shortest path vs. path with traffic/road closure
		
Function for determining which individual roads impact efficiency the most due to traffic vs. road closures

Function for calculating the shortest path (DFS)
Function for calculating the shortest path (Dijkstras)
Function for calculating the shortest path between the two algorithms

Function [Using PyGame] to visualize graph road network along with shortest path (either DFS or Dijkstras and make them different colors)

Another function to graph (using Plotly) to graph efficiency based on traffic/road closure map.
