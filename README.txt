The objective of this project is to create a system that determines the quickest and most effective
route across a city’s road network, and provides insight on which roads are the most valuable given an
event like traffic or a road closure. 

Real World Use: Stakeholders may see how various communities are
evolving over time and where additional affordable housing or community services may be required by displaying
population growth and demographic data. Visualizing city models may help stakeholders get support and buy-in for
various projects in addition to assisting them in identifying areas that need development. People are more willing to
support a change or intervention and devote their time, money, and effort to make it happen when they can clearly
see the advantages of doing so


Program Reproducibility:

- We use graphs as the main data type to represent the whole roadmap, with its intersections represented
by graph nodes and each edge showing the way for the roads connecting these intersections. 

- We first read a .csv file whose data we then use to create a road network of nodes and edges. 

- We use a shortest path finder by recursively finding all paths and selecting the path with the minimum length.

- We visualize the road network using the libraries NetworkX and Matplotlib to draw the graph. 
NetworkX created the actual graph, while Matplotlib was used to draw the graph along with NetworkX. 

- We generate events on roads by creating a copy of the network and assigning either traffic or road closure on a given road. 
These events impact the shortest path algorithm. Traffic doubles the total distance and closures make the road unreachable. 
We implemented the latter by first adding a boolean instance attribute for the Road class and then going into the recursive function 
for find paths and adding a condition to not check roads that are ”closed”. 

- After creating an updated network with events, we then run a function called most valuable road to iterate through all roads 
in the network and calculate the difference in distance that exists between that road having an event versus the original clean path. 
This way, we can find which roads have the largest change in overall distance by the existence of an event. 

- The visualization for shortest event paths can then be done using the same functions created for normal shortest paths. 

- In addition to visualizations being the results of our computation, our program also prints the most valuable road given the event.
