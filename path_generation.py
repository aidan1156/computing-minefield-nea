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
    if i == n-grid_size:#backwards
        return 10
    if i == n+grid_size:#forward
        return 1000000

    ##diagonals
    if get_row(i) == get_row(n)-1 and get_col(i) == get_col(n)-1:
        return 500
    if get_row(i) == get_row(n)+1 and get_col(i) == get_col(n)+1:
        return 500000000
    if get_row(i) == get_row(n)-1 and get_col(i) == get_col(n)+1:
        return 500
    if get_row(i) == get_row(n)+1 and get_col(i) == get_col(n)-1:
        return 500000000

    return False

##get the row from a node
def get_row(i):
    val = math.ceil(i / grid_size)
    if val == 0:
        val = grid_size
    if val == grid_size+1:
        val = grid_size
    return val

##get the column a node belongs to
def get_col(i):
    val = i % grid_size
    if val == 0:
        val = grid_size
    return val

def apply_djikstras_algorithm(graph,start,end):
    for i in range(len(graph)):
        graph[i].working_value = None
        graph[i].final_value = None

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

    return path
def generate_path():
    graph = []

    for i in range(grid_size*grid_size):
        graph.append(node(i+1))

    for i in range(len(graph)):
        for n in range(len(graph)):
            if bool(get_adjacent_weight(i+1,n+1)):
                graph[i].add_connection(graph[n],random.randint(get_adjacent_weight(graph[i].name,graph[n].name) // 10,get_adjacent_weight(graph[i].name,graph[n].name)))

    start = random.randint(0,grid_size-1)
    end = random.randint(grid_size*(grid_size-1),grid_size*grid_size-1)

    path = apply_djikstras_algorithm(graph,graph[start],graph[end])

    graph = []
    for i in range(len(path)):
        graph.append(node(path[i]))
    for i in range(len(graph)):
        for n in range(len(graph)):
            if bool(get_adjacent_weight(int(graph[i].name),int(graph[n].name))):
                graph[i].add_connection(graph[n],1)
    
    for i in range(len(graph)):
        if graph[i].name == start+1:
            start_node = graph[i]
        if graph[i].name == end+1:
            end_node = graph[i]

    path = apply_djikstras_algorithm(graph,start_node,end_node)

    pattern = []
    for i in range(len(path)):
        pattern.append([get_col(path[i])-1,get_row(path[i])-1])

    
    ##check if there is variation in the path
    regenerate = False
    for i in range(2,len(pattern)):
        if pattern[i][0] == pattern[i-1][0] == pattern[i-2][0]:
            regenerate = True

    if regenerate:
        pattern = generate_path()

    # if len(pattern) < grid_size+3:
    #     pattern = generate_path()


    return pattern