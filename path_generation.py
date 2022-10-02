import random
import math

grid_size = 8

##the object that stores data about each node
class node():
    def __init__(self,name):
        self.nodes = []##list of connected nodes
        self.weights = []##list of weights of the connected nodes
        self.name = name##'name' of the node

        ##values used by djikstras algorithm
        self.working_value = None
        self.final_value = None
    def add_connection(self,connection,weight):##connect a node to the current one
        self.nodes.append(connection)
        self.weights.append(weight)

        connection.nodes.append(self)
        connection.weights.append(weight)


##get the weight between 2 given nodes numbers
def get_adjacent_weight(i,n):
    if i == n-1 and int(i/grid_size) != i/grid_size:#left and right
        return 10
    if i == n+1 and int(n/grid_size) != n/grid_size:
        return 10
    if i == n-grid_size:#forward
        return 1000000
    if i == n+grid_size:#backward
        return 10

    ##diagonals
    if get_row(i) == get_row(n)-1 and get_col(i) == get_col(n)-1:
        return 500000000
    if get_row(i) == get_row(n)+1 and get_col(i) == get_col(n)+1:
        return 50
    if get_row(i) == get_row(n)-1 and get_col(i) == get_col(n)+1:
        return 500000000
    if get_row(i) == get_row(n)+1 and get_col(i) == get_col(n)-1:
        return 50

    return False

##get the row from a node
def get_row(i):
    val = math.ceil(i / grid_size)
    if val == 0:
        val = 9
    if val == 10:
        val = 9
    return val

##get the column a node belongs to
def get_col(i):
    val = i % grid_size
    if val == 0:
        val = 9
    return val

def generate_path():
    graph = []

    for i in range(grid_size*grid_size):
        graph.append(node(i))

    for i in range(len(graph)):
        for n in range(len(graph)):
            if bool(get_adjacent_weight(n+1,i+1)):
                graph[i].add_connection(graph[n],random.randint(get_adjacent_weight(n+1,i+1) // 10,get_adjacent_weight(n+1,i+1)))

    start = graph[random.randint(0,grid_size-1)]
    end = graph[random.randint(grid_size*(grid_size-1),grid_size*grid_size-1)]

    current_node = start
    current_node.final_value = 0

    assigned_final_values = False##if all the ndoes have final values
    while assigned_final_values == False:
        for i in range(len(current_node.nodes)):
            if current_node.nodes[i].final_value == None:
                weight = current_node.final_value + current_node.weights[i]
                if current_node.nodes[i].working_value == None or weight < current_node.nodes[i].working_value:
                    current_node.nodes[i].working_value = weight

        ##find the smallest working value
        next_node = None
        for i in range(len(graph)):
            if (graph[i].working_value != None) and ((next_node == None and graph[i].working_value != None) or (next_node != None and next_node.working_value > graph[i].working_value)):
                if graph[i].final_value == None:
                    next_node = graph[i]

        next_node.final_value = next_node.working_value

        current_node = next_node

        assigned_final_values = True
        for i in range(len(graph)):
            if graph[i].final_value == None:
                assigned_final_values = False

    print(graph[5].final_value)

    ##find the path
    current_node = end
    path = [current_node.name]
    done = False

    while done == False:
        for i in range(len(current_node.nodes)):
            if current_node.nodes[i].final_value == current_node.final_value - current_node.weights[i]:
                next_node = current_node.nodes[i]
            
        current_node = next_node
        path.append(current_node.name)
        if current_node == start:
            done = True

    print(path)

    pattern = []
    for i in range(len(path)):
        pattern.append([get_col(path[i])-1,get_row(path[i])-1])

    return pattern