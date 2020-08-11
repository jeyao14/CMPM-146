from heapq import heappop, heappush
from math import inf, sqrt
def reverse(obj):
    temp = []
    for key in obj:
        if key == obj[0] or key == obj[len(obj)-1]:
            temp.append(key)
            continue
        temp.append((key[1],key[0]))
    return temp

def dimens(boxes):
    boxpoints = {}
    for current in boxes:
        x1 = current[2]
        x2 = current[3]
        y1 = current[0]
        y2 = current[1]
        #print("x1: ", x1, "\n x2: ", x2, "\n y1: ", y1, "\n y2: ", y2)
        width = x2 -x1
        height = y2 - y1
        boxpoints[current] = ((x1,y1),(x1+width,y1),(x1,y1+height),(x2,y2))
    return boxpoints 

def get_detail_point(starting_points, next_box):
    x, y = starting_points
    next_x1 = next_box[2]
    next_x2 = next_box[3]
    next_y1 = next_box[0]
    next_y2 = next_box[1]

    detail_point = (min(next_x2, max(next_x1, x)), min(next_y2, max(next_y1, y)))
    return detail_point

def pythag(coord1, coord2):
	x1 = coord1[0]
	x2 = coord2[0]
	y1 = coord1[1]
	y2 = coord2[1]

	diagonal = sqrt((x1 - x2) ** 2 + (y2 - y1) ** 2) * 0.5
	return diagonal

def navigation_edges(level, cell):
    """ Provides a list of adjacent cells and their respective costs from the given cell.

    Args:
        level: adjacent cells to cell
        cell: A target location.

    Returns:
        A list of costs and adjacent boxes
    """


    edges = []
    # Visit all adjacent cells
    for box in level:
        half1x = (box[3]+box[2])/2
        half1y = (box[1]+box[0])/2
        half2x = (cell[3]+cell[2])/2
        half2y = (cell[1]+cell[0])/2

        dist = sqrt((half1x - half2x) ** 2 + (half1y-half2y) ** 2) * 0.5
        test = (dist,box)
        # calculate cost and add it to the dict of adjacent cells
        edges.append(test)
    return edges

def heuristic(box, dest_point):

    cell = dest_point
    half1x = (box[3]+box[2])/2
    half1y = (box[1]+box[0])/2
    half2x = (cell[3]+cell[2])/2
    half2y = (cell[1]+cell[0])/2

    dist = sqrt((half1x - half2x) ** 2 + (half1y-half2y) ** 2) * 0.5
    
    return dist

def find_path (source_point, destination_point, mesh):

    """
    Searches for a path from source_point to destination_point through the mesh

    Args:
        source_point: starting point of the pathfinder
        destination_point: the ultimate goal the pathfinder must reach
        mesh: pathway constraints the path adheres to

    Returns:

        A path (list of points) from source_point to destination_point if exists
        A list of boxes explored by the algorithm
    """
    boxes = mesh["boxes"]
    adj = mesh["adj"]
    result = []
    #key[0] = x1 key[1] = y1 key[2] = x2 key[3] = y2
    
    sx = source_point[1]
    sy = source_point[0]
    dx = destination_point[1]
    dy = destination_point[0]

    print("source_point: ", sx, ", ", sy)
    print("destination_point: ", dx, ", ", dy)

    for key in boxes:
        x1 = key[2]
        x2 = key[3]
        y1 = key[0]
        y2 = key[1]
        
        #if x2 > 900:
            #print("yes")
        #source box
        if sx >= x1 and sx < x2:
            if sy >= y1 and sy < y2:
                sourcebox = key
            
                #result.append(key)

        #dest box
        if dx >= x1 and dx < x2:
            if dy >= y1 and dy < y2:
                destinationbox = key
                
                #result.append(key)

    #print("found boxes: ", result)
     

    # The priority queue
    queue = []

    heappush(queue,(heuristic(sourcebox, destinationbox),sourcebox,"destination"))
    # The dictionary that will be returned with the costs
    distances = {}
    distances[sourcebox] = 0


    # The dictionary that will store the backpointers
    backpointers = {}
    backpointers[sourcebox] = None

    #stuff that starts at back
    #heappush(queue,(heuristic(destinationbox,sourcebox),destinationbox,"source"))
    
    #distancesback = {}
    #distancesback[destinationbox] = 0

    #pointersback = {}
    #pointersback[destinationbox] = None
    

    #references that keep track of last nodes
    startgoal = destinationbox
    destinationgoal = sourcebox
    startfinal = destinationbox
    backfinal = sourcebox
    done = 0
    while queue:
        # the current node can be either back 
        current_node = heappop(queue)
        print(current_node[2])
        #print(len(queue))

        # Check if current node is overlapping with the other backtable
        if current_node[2]=="destination" and current_node[1] == startgoal:
            done = 1
            break
        elif current_node[2]== "source"and current_node[1] == destinationgoal:
            done = 1
            break
        #if (current_node[2]=="destination" and current_node[1] == destinationbox)or(current_node[2]== "source"and current_node[1] == sourcebox )or(current_node[2] == "source" and current_node[1] in backpointers ) or (current_node[2] == "destination" and current_node[1] in pointersback )    :
            

            # List containing all cells from initial_position to destination
            #path = [current_node]

            # Go backwards from destination until the source using backpointers
            # and add all the nodes in the shortest path into a list
            #current_back_node = backpointers[current_node[1]]
            #while current_back_node is not None:
             #   print(current_back_node)
              #  path.append(current_back_node)
              #  current_back_node = backpointers[current_back_node]
        
        # Calculate cost from current note to all the adjacent ones
        
        if current_node[2] == "destination":
                startfinal = current_node[1]    
                adjacents = navigation_edges(adj[current_node[1]],current_node[1])
                for next in adjacents :
                    pathcost = distances[current_node[1]] + next[0] # their is going to some errors because i am just adding them all together

                    if next[1] not in distances or pathcost < distances[next[1]]:
                        #print("do we go here")
                        distances[next[1]] = pathcost + heuristic(next[1], destinationbox)
                        backpointers[next[1]] = current_node[1]
                        heappush(queue, (distances[next[1]], next[1],"destination"))
                        break

        else:
                backfinal = current_node[1]
                adjacents = navigation_edges(adj[current_node[1]],current_node[1])
                for next in adjacents :
                    pathcost = distancesback[current_node[1]] + next[0] # their is going to some errors because i am just adding them all together


                    if next[1] not in distancesback or pathcost < distancesback[next[1]]:
                        #print("do we go here")
                        distancesback[next[1]] = pathcost + heuristic(next[1], sourcebox)
                        pointersback[next[1]] = current_node[1]
                        heappush(queue, (distancesback[next[1]], next[1],"source"))
                        break

    if done == 1:
        endlist = []
        goback = []
        current =  backfinal
        point = source_point
        print("these are forward :",backpointers)
        #print("\n \nthese are back :",pointersback)
        #backpointers.update(pointersback)
        #goback = backpointers.keys()
        goback = backpointers.keys()
        print(goback)
        return endlist, goback
        while current != None:
            goback.append(current)
            #print("current box: ", current)
            current = pointersback[current]
        #goback.append(destinationbox)
        current = startfinal
        while current != None:
            goback.insert(0,current)
            #print("current box: ", current)
            current = backpointers[current]
        #goback.insert(0,sourcebox)

        finaldistance = dimens(goback)   
        endlist.append(source_point)
        #print("this is :",source_point)
        #print("goback contains: ", goback)
        i = 0
        prevkey = goback[0]
        box1mn = 0
        box1mx = 0
        for key in goback:
            i = i+1
            if i ==1:
                prevkey = key
                continue 
            point = get_detail_point(point, key)
            endlist.append(point)
            
            """currdistance = 0
            maxdistance = 0
            largestpoint = point
            for val  in finaldistance[key]:
                currdistance = pythag(val, point)
                #print("currdistance: ", currdistance)
                if currdistance < maxdistance or maxdistance == 0:
                    
                    maxdistance = currdistance
                    #print("max distance updated: ", maxdistance)
                    largestpoint = val
                    #print("largestpoint: ", largestpoint)

            point = largestpoint
            prevkey = key
            print("this is point : ", point) 
            endlist.append(point)"""

        #endlist.pop()
        endlist.append(destination_point)        
        print("endlist: ", endlist)
        endlist = reverse(endlist)
        if not endlist:
            print("No path!")
            return endlist, goback
        else:
            return endlist, goback
    # path = []
    #boxes = {}

    #return path, boxes.keys()
