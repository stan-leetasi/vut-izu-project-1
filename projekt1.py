# Implementation of the Unified Cost Search algorithm
# Stanislav Letaši

import sys
import re

class Coordinates:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Node:
    """Stores all information about a node"""
    def __init__(self, location: Coordinates, cost: int, parent: Coordinates):
        self.location = location 
        self.cost = cost
        self.parent = parent

    def update_cost(self, new_cost):
        self.cost = new_cost

######################################################################################
# Place your input here
data = """
7 7 7 5 Z 8 7 8 7 9
6 6 5 7 Z Z Z Z 7 8
9 9 8 8 Z 9 2 Z 8 9
3 3 3 3 3 9 4 Z 9 7
9 Z 5 4 Z 3 3 3 3 3
9 Z 6 2 Z 8 9 9 9 6
9 Z Z Z Z Z Z Z 9 7
9 9 9 9 Z 9 9 9 9 9
8 8 6 7 Z 9 9 9 9 9
8 8 8 8 Z 9 7 7 8 9
"""
# Z - wall, cannot traverse
# Other - cost of traversal to the coordinate

# Starting point for traversal
start_c = Coordinates(6,2) #location    
start_p = Coordinates(0,0) #parent coordinates (leave as 0)
start = Node(start_c, 0, start_p)

# Goal point for traversal
goal_c = Coordinates(3,5) #location 
goal_p = Coordinates(0,0) #parent coordinates (leave as 0)
goal = Node(goal_c, 0, goal_p)
######################################################################################

# Split the input into cells
input = [line.split() for line in data.strip().split('\n')]
inverse_data = ""

# Transpose input
x = 0
y = 0
while y < len(input):
    while x < len(input[0]):
        inverse_data += str(input[x][y]) + " "
        x += 1

    inverse_data += "\n"
    y += 1
    x = 0

# Insert transposed input back into original variable
input = [line.split() for line in inverse_data.strip().split('\n')]

Open = [] # List of open nodes
Closed = [] # List of visited nodes

def is_closed(x:int, y:int):
    """Search for a node in the Closed list"""
    for item in Closed:
        if (item.location.x == x and 
            item.location.y == y):
            return True

    return False

def is_opened(x:int, y:int, cost:int):
    """Search for a node in the Opened list"""
    for item in Open:
        if (item.location.x == x and 
            item.location.y == y):
            # Update cost if a lower cost for the node was found
            if cost < item.cost:
                item.update_cost(cost)

            return True
                
def find_cheapest():
    """Finds the cheapest node in the Open list, returns its index"""
    min = Open[0].cost
    minIndex = 0
    index = 0
    while index < len(Open):
        if Open[index].cost < min:
            minIndex = index
            min = Open[index].cost

        index += 1
    
    return minIndex

def find_node(cords:Coordinates):
    """Finds a node in the Closed list, returns it's index"""
    index = len(Closed)-1
    while index >= 0:
        if (Closed[index].location.x == cords.x and 
            Closed[index].location.y == cords.y):
            return index
        index -= 1
    
def close_node(index):
    """Remove node Open[index] from the list and append it to the Closed list"""
    Closed.append(Open.pop(index))

def open_node(shiftX:int, shiftY:int, parentCost:int, parentX:int, parentY:int ):
    """Explore a new node"""
    node_cord = Coordinates(parentX + shiftX , parentY + shiftY)

    # Test if node is not out of bounds
    if (node_cord.x > 9 or 
        node_cord.x < 0 or 
        node_cord.y > 9 or 
        node_cord.y < 0):
        return
    
    # Test if node has been explored already
    elif is_closed(node_cord.x, node_cord.y):
        return

    # Test if node is not a "Wall"
    elif input[node_cord.x][node_cord.y] == "Z":
        return
    else:
        # Calculate new cost
        node_cost = parentCost + int(input[node_cord.x][node_cord.y])

    if is_opened(node_cord.x, node_cord.y, node_cost):
        return

    node_parent = Coordinates(parentX, parentY)
    newNode = Node(node_cord, node_cost, node_parent)
    Open.append(newNode) # Add node to the Open list

def open_neighbours(node: Node):
    """Explore all neighbouring nodes"""
    open_node(-1, -1, node.cost, node.location.x, node.location.y)
    open_node(-1, 0, node.cost, node.location.x, node.location.y)
    open_node(-1, 1, node.cost, node.location.x, node.location.y)
    open_node(0, 1, node.cost, node.location.x, node.location.y)
    open_node(1, 1, node.cost, node.location.x, node.location.y)
    open_node(1, 0, node.cost, node.location.x, node.location.y)
    open_node(1, -1, node.cost, node.location.x, node.location.y)
    open_node(0, -1, node.cost, node.location.x, node.location.y)

def add_cords(cords: Coordinates):
    """Appends coordinates values into string and returns it"""
    CoordsString = ""
    if cords.x == 0:
        CoordsString += "NULL"
    else:
        CoordsString += "[" + str(cords.x) + ", " + str(cords.y) + "]"

    return CoordsString

def add_node(node: Node):
    """Appends node to string and returns it"""
    CoordsString = "("
    CoordsString += add_cords(node.location)
    CoordsString += ", " + str(node.cost) + ", "
    CoordsString += add_cords(node.parent)
    CoordsString += ")"

    return CoordsString

def add_nodes(list):
    """Appends nodes from list into CoordsString and returns it"""
    CoordsString = ""
    for item in list:
        CoordsString += add_node(item)
        if item != list[len(list)-1]:
            CoordsString += ", "

    return CoordsString

def visualize_iteration(OpenStr, ClosedStr, OC:bool):
    """Prints the location of open and closed nodes into a field on stdout"""
    if len(sys.argv) > 1:
        if sys.argv[1] != "--visualize":
            return
    else:
        return
    print()
    # Parse input and extract coordinates
    open_axis = []
    closed_axis = []

    if len(OpenStr) != 0:
        nodes_text = re.findall(r'\(\[(\d+), (\d+)\]', OpenStr)
        for node_text in nodes_text:
            x, y = map(int, node_text)
            open_axis.append((x, y))

    if len(ClosedStr) != 0:
        nodes_text = re.findall(r'\(\[(\d+), (\d+)\]', ClosedStr)
        for node_text in nodes_text:
            x, y = map(int, node_text)
            closed_axis.append((x, y))

    field = [[" " for _ in range(10)] for _ in range(10)]

    # Mark coordinates of optimal path
    if OC == False:
        for coord in open_axis:
            y, x = coord
            field[x][y] = "P"

    # Mark coordinates of Open and Closed nodes
    else:
        # Mark given coordinates
        for coord in open_axis:
            y, x = coord
            field[x][y] = "o"

        for coord in closed_axis:
            y, x = coord
            field[x][y] = "x"

    # Print column indices
    print(" ", end=" ")
    for col in range(10):
        print(col, end=" ")
    print()

    # Print field with row indices
    for row in range(10):
        print(row, end=" ")
        for col in range(10):
            print(field[row][col], end=" ")
        print()


# Main
Open.append(start)
OpenString = add_nodes(Open)
ClosedString = ""
print(f"Iteration 0:")
print(f"Open: {OpenString}")
print("Closed: ")
iterationCounter = 1

visualize_iteration(OpenString, ClosedString, True)
print()

# Traverse the map, find the optimal path
while True:

    # Goal was found or all options have been exhausted
    if is_closed(goal.location.x, goal.location.y) or len(Open) == 0:
        break

    currentNodeIndex = find_cheapest()
    currentNode = Open[currentNodeIndex]

    open_neighbours(currentNode)
    close_node(currentNodeIndex)

    print(f"\nIteration {iterationCounter}:")
    OpenString = add_nodes(Open)
    ClosedString = add_nodes(Closed)
    print(f"Open: {OpenString}")
    print(f"Closed: {ClosedString}")
    iterationCounter += 1
    visualize_iteration(OpenString, ClosedString, True)

print()

if len(Open) == 0:
    print("Goal node was not found")
    sys.exit(0)

print(f"Optimal traversal cost: {Closed[-1].cost}")

path = []
currentNode = Closed.pop(-1) # Goal node is last in the Closed list

# Find the list of nodes on the optimal path
while currentNode.location != start_c:

    path.append(currentNode)
    currentNode = Closed.pop(find_node(currentNode.parent))

path.append(start)
path.reverse()

# Print the optimal path
for item in path:
    print(f"[{item.location.x}, {item.location.y}]", end="")
    if item != path[-1]:
        print(", ", end="")
print()
pathString = add_nodes(path)
visualize_iteration(pathString, pathString, False)

print()
sys.exit(0)
    