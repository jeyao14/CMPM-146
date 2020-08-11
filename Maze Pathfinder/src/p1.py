from p1_support import load_level, show_level, save_level_costs
from math import inf, sqrt
from heapq import heappop, heappush
from operator import itemgetter


def dijkstras_shortest_path(initial_position, destination, graph, adj):
	""" Searches for a minimal cost path through a graph using Dijkstra's algorithm.

	Args:
		initial_position: The initial cell from which the path extends.
		destination: The end location for the path.
		graph: A loaded level, containing walls, spaces, and waypoints.
		adj: An adjacency function returning cells adjacent to a given cell as well as their respective edge costs.

	Returns:
		If a path exits, return a list containing all cells from initial_position to destination.
		Otherwise, return None.

	"""

	"""
	v = next node in frontier?
	move_cost = dist
	new_cost = alt
	"""

	frontier = [(initial_position, 0)]
	previous = {}
	move_cost = {}
	previous[initial_position] = None
	move_cost[initial_position] = 0

	while frontier:
		current_pos, current_cost = heappop(frontier)

		if current_pos == destination:
			path = []
			current_path = destination
			while current_path != None:
				path.insert(0, current_path)
				current_path = previous[current_path]
			return path

		for next_node, next_cost in adj(graph, current_pos):
			new_cost = move_cost[current_pos] + next_cost
			if next_node not in move_cost or new_cost < move_cost[next_node]:
				move_cost[next_node] = new_cost
				temp_cost = new_cost
				heappush(frontier, (next_node, temp_cost))
				previous[next_node] = current_pos

	return None




def dijkstras_shortest_path_to_all(initial_position, graph, adj):
	""" Calculates the minimum cost to every reachable cell in a graph from the initial_position.

	Args:
		initial_position: The initial cell from which the path extends.
		graph: A loaded level, containing walls, spaces, and waypoints.
		adj: An adjacency function returning cells adjacent to a given cell as well as their respective edge costs.

	Returns:
		A dictionary, mapping destination cells to the cost of a path from the initial_position.
	"""
	frontier = [(initial_position, 0)]
	previous = {}
	move_cost = {}
	previous[initial_position] = None
	move_cost[initial_position] = 0

	while frontier:
		current_pos, current_cost = heappop(frontier)

		for next_node, next_cost in adj(graph, current_pos):
			new_cost = move_cost[current_pos] + next_cost
			if next_node not in move_cost or new_cost < move_cost[next_node]:
				move_cost[next_node] = new_cost
				temp_cost = new_cost
				heappush(frontier, (next_node, temp_cost))
				previous[next_node] = move_cost[next_node]

	return move_cost


def navigation_edges(level, cell):
	""" Provides a list of adjacent cells and their respective costs from the given cell.

	Args:
		level: A loaded level, containing walls, spaces, and waypoints.
		cell: A target location.

	Returns:
		A list of tuples containing an adjacent cell's coordinates and the cost of the edge joining it and the
		originating cell.

		E.g. from (0,0):
			[((0,1), 1),
			 ((1,0), 1),
			 ((1,1), 1.4142135623730951),
			 ... ]
	"""
	x1 = cell[0]
	x2 = cell[1]
	adj_cells = []
	finallist = []
	adj_cells_dist = {}
	xcost = level['spaces'][cell]

	max_width = max(level['walls'],key=itemgetter(0))[0]

	max_height = max(level['walls'],key=itemgetter(1))[1]

	#a-c
	nw = (x1 - 1, x2 - 1)
	n = (x1, x2 - 1)
	ne = (x1 + 1, x2 -1)

	#d,e
	w = (x1 - 1, x2)
	e = (x1 + 1, x2)

	#f-h
	sw = (x1 - 1, x2 + 1)
	s = (x1, x2 + 1)
	se = (x1 + 1, x2 + 1)

	if x2 > 0:
		adj_cells.append(n)
		if x1 > 0:
			adj_cells.append(nw)
		if x1 < max_width:
			adj_cells.append(ne)

	if x1 > 0:
		adj_cells.append(w)
	if x1 < max_width:
		adj_cells.append(e)

	if x2 < max_height:
		adj_cells.append(s)
		if x1 > 0:
			adj_cells.append(sw)
		if x1 < max_width:
			adj_cells.append(se)
	

	for item in adj_cells:
		if item in level['walls']:
			continue
		elif item in level['spaces']:
			vcost = level['spaces'][item]
			v1 = item[0]
			v2 = item[1]
			if item == nw or item == ne or item == sw or item == se:
				dist = (0.5 * sqrt(2)) * (xcost + vcost)
			elif item == n or item == w or item == e or item == s:
				dist = (0.5) * (xcost + vcost)
			adj_cells_dist[item] = dist

	finallist = list(adj_cells_dist.items())

	return finallist



def test_route(filename, src_waypoint, dst_waypoint):
	""" Loads a level, searches for a path between the given waypoints, and displays the result.

	Args:
		filename: The name of the text file containing the level.
		src_waypoint: The character associated with the initial waypoint.
		dst_waypoint: The character associated with the destination waypoint.

	"""

	# Load and display the level.
	level = load_level(filename)
	show_level(level)

	# Retrieve the source and destination coordinates from the level.
	src = level['waypoints'][src_waypoint]
	dst = level['waypoints'][dst_waypoint]

	# Search for and display the path from src to dst.
	path = dijkstras_shortest_path(src, dst, level, navigation_edges)
	if path:
		show_level(level, path)
	else:
		print("No path possible!")


def cost_to_all_cells(filename, src_waypoint, output_filename):
	""" Loads a level, calculates the cost to all reachable cells from 
	src_waypoint, then saves the result in a csv file with name output_filename.

	Args:
		filename: The name of the text file containing the level.
		src_waypoint: The character associated with the initial waypoint.
		output_filename: The filename for the output csv file.

	"""
	
	# Load and display the level.
	level = load_level(filename)
	show_level(level)

	# Retrieve the source coordinates from the level.
	src = level['waypoints'][src_waypoint]
	
	# Calculate the cost to all reachable cells from src and save to a csv file.
	costs_to_all_cells = dijkstras_shortest_path_to_all(src, level, navigation_edges)
	save_level_costs(level, costs_to_all_cells, output_filename)


if __name__ == '__main__':
	filename, src_waypoint, dst_waypoint = 'example.txt', 'a','e'

	# Use this function call to find the route between two waypoints.
	test_route(filename, src_waypoint, dst_waypoint)

	# Use this function to calculate the cost to all reachable cells from an origin point.
	cost_to_all_cells(filename, src_waypoint, 'my_costs.csv')
