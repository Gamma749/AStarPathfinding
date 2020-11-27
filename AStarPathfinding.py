from Square import Square
import math
import pygame
#Heuristics constant that determines nature of pathfinding
#Decides how much weight to give to f_cost versues g_cost
h_const = 0.01

def reconstruct_path(came_from, end)->list:
    """
    Creates the path from source to target using the came_from matrix
    created during pathfinding

    Parameters:
    ----------------
    came_from: 2D (int, int) array
        matrix of coordinates detailing the previous square for each square on a path

    end: Square
        The final square of a path

    Returns
    ---------------
    list
        a list of coordinates (int, int) representing a path from source to target
    """
    path = list()
    current_index = end.index
    while current_index!=(-1,-1):
        path.append(current_index)
        current_index = came_from[current_index[0]][current_index[1]]
    path.reverse()
    return path

def get_square(squares, state)->Square:
    """
    Get the first square with a defined state

    Parameters:
    ----------------
    squares: 2D matrix of Square objects
        The Matrix of squares to search through

    state: Square.STATE
        The state to serach for

    Returns:
    ----------------
    Square
        The first square to have the state required
    """
    for x in range(len(squares)):
        for y in range(len(squares[x])):
            if(squares[x][y].state == state):               
                return squares[x][y]
            
def pathfind(screen, squares)->list:
    """
    Find a path from source to target using the board defined in the squares parameter,
    drawing to screen each time

    Parameters:
    ----------------
    screen: pygame.surface
        The surface to draw the path and intermediates to
    
    squares: 2D matrix of Square objects
        The Matrix of squares to pathfind through

    Returns:
    ----------------
    list
        The list of (int, int) tuples representing indices along the path

    None
        None if no path can be found from source to target

    """

    #Determine the source and target
    source = get_square(squares, Square.STATE.SOURCE)
    target = get_square(squares, Square.STATE.TARGET)   
                
    #the open set is the nodes yet to be considered
    open_nodes = list()           
    source.set_state(Square.STATE.OPEN)
    open_nodes.append(source)


    #the closed set is the nodes already examined
    closed_nodes = list()

    f_costs = list()
    g_costs = list()
    came_from = list()
    for x in range(len(squares)):
        f_costs.append([])
        g_costs.append([])
        came_from.append([])
        for y in range(len(squares)):
            f_costs[x].append(math.inf)
            g_costs[x].append(math.inf)
            came_from[x].append((-1,-1))
            
    f_costs[source.index[0]][source.index[1]] = h_cost(target,source)
    g_costs[source.index[0]][source.index[1]] = 0

    while len(open_nodes)!=0:
        #First we need to determine the f_costs of our open_nodes and sort them
        open_nodes = sorted(open_nodes, key=lambda n:
               f_costs[n.index[0]][n.index[1]])
##        for n in open_nodes:
##            print(f'{n.index}: {f_costs[n.index[0]][n.index[1]]}')
##        input()
        #Get the node with the lowest f_cost       
        current = open_nodes.pop(0)
        current.set_state(Square.STATE.CLOSED)
        current.draw(screen)
        pygame.display.update()
        
        if current == target:
            return reconstruct_path(came_from, current)

        #For each neighbour of current
        neighbours=list()
        current_x = current.index[0]
        current_y = current.index[1]
        current_g_cost = g_costs[current_x][current_y]
       
        if current_x-1>=0:
            if squares[current_x-1][current_y].state!=Square.STATE.WALL:
                neighbours.append(squares[current_x-1][current_y])
        if current_x+1<len(squares):
            if squares[current_x+1][current_y].state!=Square.STATE.WALL:
                neighbours.append(squares[current_x+1][current_y])
        if current_y-1>=0:
            if squares[current_x][current_y-1].state!=Square.STATE.WALL:
                neighbours.append(squares[current_x][current_y-1])
        if current_y+1<len(squares[x]):
            if squares[current_x][current_y+1].state!=Square.STATE.WALL:
                neighbours.append(squares[current_x][current_y+1])

        for n in neighbours:
            #neighbour tenative g cost = current g_cost + 1
            tenative_g_cost =  + 1
            if tenative_g_cost < g_costs[n.index[0]][n.index[1]]:
                #We have found a better path to this neighbour!
                came_from[n.index[0]][n.index[1]] = (current_x, current_y)
                g_costs[n.index[0]][n.index[1]] = tenative_g_cost
                f_costs[n.index[0]][n.index[1]] = g_costs[n.index[0]][n.index[1]]+h_cost(target, n)
                if n not in open_nodes:
                    n.set_state(Square.STATE.OPEN)
                    open_nodes.append(n)
                    n.draw(screen)
                    pygame.display.update()

    #We have emptied the open_nodes but we haven't made it to target. Failed
    return None               


def h_cost(target, node)->float:
    """
    The estimated cost from node to the target

    Parameters:
    ----------------
    target: Square
        The square to use as the endpoint

    node: Square
        The square to use as the source

    Returns:
    ----------------
    float
        The h_cost of the node in relation to the target. For more on h_cost see https://en.wikipedia.org/wiki/A*_search_algorithm

    """
    dx = abs(target.index[0] - node.index[0])
    dy = abs(target.index[1] - node.index[1])
    return h_const * math.sqrt(dx**2+dy**2)
