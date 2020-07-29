Teammates:
Jeff Yao
Alec Zhang


Our algorithm uses A*/ modified Dijkstras to iterate through different possible states and find the shortest possible "path" of states to craft what the goal requires.
We use a heapq to act as a priority queue to help with functionality, as well as several dicts/lists to help store data. To ensure our algorithm doesn't explore paths
beyond the goal, we terminated the search when either 1) the "frontier" is empty or 2) the current cost returned by the queue exceeds our shortest cost to the goal.

Our heuristic function mainly checks to make sure our search doesn't craft too many items that we won't use. We set item and tool limits and checked to make sure that 
the state that was being checked didn't exceed those limits. For example, you don't need more than one bench or furnace, so once we have already made one, we shouldn't
explore any states that involve making another.


NOTE:
The total cost(in-game time) and the total number of states visited are printed out before the path