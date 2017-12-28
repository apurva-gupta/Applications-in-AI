Path Finding Problem
To find good driving directions between US cities given by user.
Path Finding problem is implemented using various algorithms like BFS,DFS,Uniform Cost Search and A* algorithms.

DATA
Dataset of North American (though mostly U.S.) major roads

Description of Files
1. city-gps.txt contains one line per city, with three fields per line, 
delimited by spaces. The first field is the city, followed by the latitude,
followed by the longitude.
2. road-segments.txt has one line per road segment connecting two cities.
The space delimited fields are:

- first city
- second city
- length (in miles)
- speed limit (in miles per hour)
- name of highway
3. route.py comtains the actual code for problem written in python.

To Run Program:
./route.py [start-city] [end-city] [routing-algorithm] [cost-function]

-->start-city and end-city are the cities we need a route between.
-->routing-algorithm is one of:
– bfs uses breadth-first search (which ignores edge weights in the state graph)
– uniform is uniform cost search (the variant of bfs that takes edge weights into consideration)
– dfs uses depth-first search
– astar uses A* search, with a suitable heuristic function
-->cost-function is one of:
– segments tries to find a route with the fewest number of “turns” (i.e. edges of the graph)
– distance tries to find a route with the shortest total distance
– time tries to find the fastest route, for a car that always travels at the speed limit

OUTPUT FORMAT
[total-distance-in-miles] [total-time-in-hours] [start-city] [city-1] [city-2] ... [end-city]

ASSUMPTIONS
1. All roads are bi-directional.
2. If data is missing in data files, there is no route between those cities.
   Example-if speed given is 0 or null, we can say that there is no path between those two cities.
3. We do not have exact speed from current node to destination, so we assumed that we are going to reach the goal node with the same speed as we came from the previous city to current city.
4. Since, we didn’t have exact co-ordinates for highway intersections; we calculated heuristic from each connecting city of highway to goal.

PROBLEM ABSTRACTION

1. Initial state : source state and all adjacent states connecting to start state
2. Goal state : Source state and the path connecting goal state
3. successsor function : It finds path from current city to all adjacent cities(depending on cost function)
4. Set of states : Path from every city to all cities
5. Cost function : BFS and DFS : 1
		   Uniform Distance and Astar distance : distance from one city to next city
		   Uniform Time and Astar time: Time taken from one city to next city
		   Uniform Segment and Astar segment : 1
		   Uniform Longtour and A star Longtour : distance from one city to next city

ROUTING ALGORITHMS
BFS
It traverses the state space breadth wise; therefore, it finds the path with minimum number of segments.

DFS
It goes till the bottom of tree, exploring all nodes till leaf node. Therefore, it finds a very long path.
It is same for all cost functions.

Uniform
For different cost functions, we consider different costs’ as priority.
1. Distance: We take the cumulative distance from city to next city as cost function
2. Time: We take the cumulative distance/speed from one city to next city as the cost function
3. Segments: We add 1 every time we traverse a node. So, Number of segments traversed till that city becomes the cost to find path with minimum number of segments.

A star
It uses a heuristic function to reduce the state space and find nodes which help us reach close to goal. The better heuristic function is, it explores less space.
1.	Distance: For distance, we use heuristic as great circle distance between current city to goal. For highway intersections, we find all connecting cities to highway and find great circle distance of goal from those cities. The great circle distance is the shortest distance between two points on the surface of sphere (earth).Therefore, it always estimates the cheapest distance to goal. Thus, heuristic function is admissible.
2.	Time: For shortest time, we take heuristic as the great circle distance from current city to goal and divide by speed from current city’s previous city to current city, assuming that we are going to reach goal with the same speed. The heuristic is admissible because the shortest distance from current city to destination is always the great circle distance. The speed is a reasonably good estimate to find the time taken to reach from current city to goal. 
3.	Segments: To find the shortest number of segments, we take heuristic as 1. G determines the number of edges we traversed so far. We cannot estimate the number of edges required to reach goal from current city when we don’t have the path. H=1 never overestimates. Therefore, we can take H as 1, to find the minimum number of segments. It runs like uniform cost search and does not reduce the state space.

RESULTS AND OBSERVATIONS
1.	Best Performance Algorithm

A-star works best for path finding problem. It gives the result in less amount of time with accuracy. It uses heuristic which helps us to reach goal exploring minimum state space.

Test Case 1:
Source: Bloomington,_Indiana
Destination: Chicago,_Illinois

Algorithm	        	   
A star Distance; Distance(miles)-209 ; Number of explored nodes: 22
Uniform	Distance; Distance(miles) -209;Number of explored nodes:546
Uniform	Time ;Distance(miles) - 224 ;Number of explored nodes :531
BFS	Distance; Distance(miles)- 220 ;Number of explored nodes : 1569
DFS Distance.Distance(miles)- 13115 ;Number of explored nodes :1624

We can observe that A star has widely reduced the number of states to explore.

2.	Fastest Algorithm
Here are my test results to find that which algorithm is fastest.
Source_city = Bloomington,_Indiana
Destination_city = Bloomington,_Minnesota
	  	
A star Time;  Distance(miles) - 633; Time(sec)-10.922 ;Computation Time-5.872s     	
Uniform	Time ; Distance(miles) - 639; Time(sec)- 10.35;Computation Time-6.824s         	
BFS Time ; Distance(miles) - 758; Time(sec)- 14.76;Computation Time-8.809s          
DFS	Time ; Distance(miles) - 47028 ; Time(sec)- 976.73;Computation Time-9.099s          

From my test case,
A-star runs fastest of all the routing algorithms.

3.	Algorithm which requires least amount of memory

Here are my test results to find that which algorithm requires least amount of memory. I have used /usr/bin/time -v ./route.py 
Bloomington,_Indiana Bloomington,_Minnesota <routing algo> <cost function> to run the command.
Source_city = Bloomington,_Indiana
Destination_city = Bloomington,_Minnesota

A star Time ; Distance(miles) - 633; Time(sec)- 10.922s;	number of visited nodes - 8452
Uniform	Time ; Distance(miles) - 639 ; Time(sec)-10.35s ; number of visited nodes- 344
BFS	Time ; Distance(miles) - ;758 Time(sec)- 14.76s; number of visited nodes - 10886        
DFS Time  ; Distance(miles) - 47028; Time(sec)-976.763s ; number of visited nodes -8452       	

From the above test case, A star requires the least amount of memory.

Improvement in Heuristic function
Heuristic function for segments did not reduce much search space. We should use a better heuristics for finding a path with least number of segments.

