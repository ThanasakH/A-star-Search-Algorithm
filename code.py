import argparse as ap
import re
import platform
import math

######## RUNNING THE CODE ####################################################
#   You can run this code from terminal by executing the following command
#   python code.py <INPUT/input#.txt> <OUTPUT/output#.txt> <iteration_number>
#   for example: python code.py INPUT/input1.txt OUTPUT/output1.txt 100
#   NOTE: THIS IS JUST ONE EXAMPLE INPUT DATA
###############################################################################


################## YOUR CODE GOES HERE ########################################
class Position:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return 'x:' + str(self.x) + ', y:' + str(self.y)


class Node:
    run_no = -1

    def __init__(self, path, x, y, g, g_pos, gen_by):
        Node.run_no += 1
        self.id = 'N' + str(Node.run_no)
        self.gen_by = gen_by
        self.exp_no = 0
        self.path = path
        self.g = g

        self.h = round(math.sqrt(abs(x - g_pos.x)**2 + abs(y - g_pos.y)**2 ), 2)   # calculate h value via Euclidean Distance
        self.f = round(self.g + self.h, 2)
        self.type = ''
        self.pos = Position(x, y)
        self.children = []

    def __str__(self):
        return self.id + ':' + self.path + " " + str(self.exp_no) + " " + str(self.g) + " " + str(self.h) + " " + str(self.f)


def graphsearch(map, flag):
    # initial variables
    o_l = []
    c_l = []
    solution = ""
    s_pos = find_node('S', map)
    g_pos = find_node('G', map)
    if s_pos is None or g_pos is None:  # check not found Start or Goal point
        print('Input error! No starting point or Goal point.')
        return

    # create starting node.
    n0 = Node('S', s_pos.x, s_pos.y, 0, g_pos, '')

    # find a solution.
    n_goal = investigate(n0, c_l, o_l, map, g_pos, flag, 1)

    # print a result
    if n_goal is not None:
        print('Found a solution!')
        print(n_goal)
        solution = demonstrate_solution(n_goal.path, map)
    else:
        print('Not found a solution!')
    return solution


def demonstrate_solution(path, map):    # track back a solution from a path result
    display = ''
    cur_path = 'S-'
    sum_cost = 0
    cost_1 = ('LU','LD','RU','RD')
    cost_2 = ('L','R','U','D')
    path = path.split('-')          # split path to list
    cur_pos = find_node('S', map)   # current position

    # create a starting step
    display += display_map(map,Position(-1,-1)) + '\n'
    display += cur_path[:-1] + ' ' + str(sum_cost) + '\n\n'

    for i in range(len(path)-1):
        # create a current path
        if path[i+1] == 'L':
            cur_pos.x -= 1
        elif path[i+1] == 'R':
            cur_pos.x += 1
        elif path[i+1] == 'U':
            cur_pos.y -= 1
        elif path[i + 1] == 'D':
            cur_pos.y += 1
        elif path[i + 1] == 'LU':
            cur_pos.x -= 1
            cur_pos.y -= 1
        elif path[i + 1] == 'LD':
            cur_pos.x -= 1
            cur_pos.y += 1
        elif path[i + 1] == 'RU':
            cur_pos.x += 1
            cur_pos.y -= 1
        elif path[i + 1] == 'RD':
            cur_pos.x += 1
            cur_pos.y += 1

        # summarise a cost
        if path[i+1] in cost_1:
            sum_cost += 1
        elif path[i+1] in cost_2:
            sum_cost += 2

        if not i+1 == len(path)-1:  # not last round, generate map with current position.
            display += display_map(map, cur_pos) + '\n'
            cur_path += path[i+1] + '-'
        else:                       # last round,  generate map only (no current position)
            display += display_map(map, Position(-1,-1)) + '\n'
            cur_path += 'G-'

        display += cur_path[:-1] + ' ' + str(sum_cost) + '\n\n'

    return display


def display_map(map, cur_pos):      # generate a map in string with a current position
    n_size = len(map)
    s = ''
    for r in range(n_size):
        for c in range(n_size):
            if cur_pos.x == c and cur_pos.y == r:
                s += '*'
            else:
                s += map[r][c]
        s += '\n'
    return s


def investigate(node, c_l, o_l, map, g_pos, flag, exp_no):
    if flag > 0 and exp_no > flag:
        return None

    c_l.append(node)    # add a node in CLOSED list
    node.exp_no = exp_no
    if len(o_l) > 0:    # remove node from the OPEN list
        o_l.pop()

    # get children from the node
    get_children(node, c_l, o_l, map, g_pos)

    # add children in the OPEN list
    add_open_list(o_l, c_l, node.children)

    # log status when diagnostic mode is on (flag > 0)
    if flag > 0:
        print_log(node, o_l, c_l)

    if len(o_l) == 0:   # no solution when OPEN list is empty
        return None
    else:
        # select next node
        next_node = len(o_l) - 1

        if o_l[next_node].h == 0:       # found solution
            return o_l[next_node]
        else:                           # investigate more
            return investigate(o_l[next_node], c_l, o_l, map, g_pos, flag, exp_no + 1)


def add_open_list(o_l, c_l, children):
    for c in children:
        if (not exist_in_list(c, c_l)) and (not exist_in_list(c, o_l)):     # node should not be in OPEN or CLOSED list
            if len(o_l) == 0:
                o_l.append(c)
            else:
                index = -1      # insert new node and order by desc f value
                for i in range(len(o_l)):
                    if c.f > o_l[i].f:
                        index = i
                        break
                if index == -1:
                    o_l.append(c)
                else:
                    o_l.insert(index, c)
    return


def get_children(node, c_l, o_l, map, g_pos):
    x = node.pos.x
    y = node.pos.y
    g = node.g
    path = node.path
    child_l = []

    # cost = 2
    l_pos = Position(x-1, y)
    r_pos = Position(x+1, y)
    u_pos = Position(x, y-1)
    d_pos = Position(x, y+1)

    if is_moveable(l_pos, map):
        n = Node(path+'-L', l_pos.x, l_pos.y, g + 2, g_pos, node.id)
        child_l.append(n)
    if is_moveable(r_pos, map):
        n = Node(path+'-R', r_pos.x, r_pos.y, g + 2, g_pos, node.id)
        child_l.append(n)
    if is_moveable(u_pos, map):
        n = Node(path+'-U', u_pos.x, u_pos.y, g + 2, g_pos, node.id)
        child_l.append(n)
    if is_moveable(d_pos, map):
        n = Node(path+'-D', d_pos.x, d_pos.y, g + 2, g_pos, node.id)
        child_l.append(n)

    # cost = 1
    lu_pos = Position(x - 1, y-1)
    ru_pos = Position(x + 1, y-1)
    ld_pos = Position(x - 1, y + 1)
    rd_pos = Position(x + 1, y + 1)

    if is_moveable(lu_pos, map) and is_moveable(l_pos, map) and is_moveable(u_pos, map):
        n = Node(path+'-LU', lu_pos.x, lu_pos.y, g + 1, g_pos, node.id)
        child_l.append(n)
    if is_moveable(ru_pos, map) and is_moveable(r_pos, map) and is_moveable(u_pos, map):
        n = Node(path+'-RU', ru_pos.x, ru_pos.y, g + 1, g_pos, node.id)
        child_l.append(n)
    if is_moveable(ld_pos, map) and is_moveable(l_pos, map) and is_moveable(d_pos, map):
        n = Node(path+'-LD', ld_pos.x, ld_pos.y, g + 1, g_pos, node.id)
        child_l.append(n)
    if is_moveable(rd_pos, map) and is_moveable(r_pos, map) and is_moveable(d_pos, map):
        n = Node(path+'-RD', rd_pos.x, rd_pos.y, g + 1, g_pos, node.id)
        child_l.append(n)

    node.children = child_l
    return


def is_moveable(pos, map):
    size = len(map)
    if 0 <= pos.x < size and 0 <= pos.y < size:   # should be in the range of map (x,y)
        if map[pos.y][pos.x].upper() != 'X':      # should not be 'X' type
            return 1
    return 0


def print_log(node, o_l, c_l):
    print(node)
    print('Children: ' + print_list(node.children, 'SHORT'))
    print('OPEN: ' + print_list(o_l, 'FULL'))
    print('CLOSED: ' + print_list(c_l, 'FULL'))
    print()


def print_list(li, version):
    s = ''
    if version == 'FULL':
        for l in li:
            s += '(' + str(l) + '), '
    elif version == 'SHORT':
        for l in li:
            s += l.id + ':' + l.path + ', '
    return '{' + s[:-2] + '}'


def exist_in_list(node, li):    # check whether node is exist in the given list
    for l in li:
        if l.pos.x == node.pos.x and l.pos.y == node.pos.y:
            return 1
    return 0


def read_from_file(file_name):
    file_handle = open(file_name)
    f = file_handle.readlines()
    m_size = int(f[0])
    # initial map into n x n size
    map = [[0] * m_size for i in range(m_size)]
    # add all values into map
    for r in range(m_size):
        for c in range(m_size):
            map[r][c] = f[r+1][c]
    return map


def find_node(node_type, map):      # find a position by given type in the map
    n_size = len(map)
    for r in range(n_size):
        for c in range(n_size):
            if map[r][c] == node_type.upper():
                return Position(c, r)
    return None

###############################################################################
########### DO NOT CHANGE ANYTHING BELOW ######################################
###############################################################################

def write_to_file(file_name, solution):
    file_handle = open(file_name, 'w')
    file_handle.write(solution)

def main():
    # create a parser object
    parser = ap.ArgumentParser()

    # specify what arguments will be coming from the terminal/commandline
    parser.add_argument("input_file_name", help="specifies the name of the input file", type=str)
    parser.add_argument("output_file_name", help="specifies the name of the output file", type=str)
    parser.add_argument("flag", help="specifies the number of steps that should be printed", type=int)
    # parser.add_argument("procedure_name", help="specifies the type of algorithm to be applied, can be D, A", type=str)


    # get all the arguments
    arguments = parser.parse_args()

##############################################################################
# these print statements are here to check if the arguments are correct.
#    print("The input_file_name is " + arguments.input_file_name)
#    print("The output_file_name is " + arguments.output_file_name)
#    print("The flag is " + str(arguments.flag))
#    print("The procedure_name is " + arguments.procedure_name)
##############################################################################

    # Extract the required arguments

    operating_system = platform.system()

    if operating_system == "Windows":
        input_file_name = arguments.input_file_name
        input_tokens = input_file_name.split("\\")
        if not re.match(r"(INPUT\\input)(\d)(.txt)", input_file_name):
            print("Error: input path should be of the format INPUT\input#.txt")
            return -1

        output_file_name = arguments.output_file_name
        output_tokens = output_file_name.split("\\")
        if not re.match(r"(OUTPUT\\output)(\d)(.txt)", output_file_name):
            print("Error: output path should be of the format OUTPUT\output#.txt")
            return -1
    else:
        input_file_name = arguments.input_file_name
        input_tokens = input_file_name.split("/")
        if not re.match(r"(INPUT/input)(\d)(.txt)", input_file_name):
            print("Error: input path should be of the format INPUT/input#.txt")
            return -1

        output_file_name = arguments.output_file_name
        output_tokens = output_file_name.split("/")
        if not re.match(r"(OUTPUT/output)(\d)(.txt)", output_file_name):
            print("Error: output path should be of the format OUTPUT/output#.txt")
            return -1

    flag = arguments.flag
    # procedure_name = arguments.procedure_name


    try:
        map = read_from_file(input_file_name) # get the map
    except FileNotFoundError:
        print("input file is not present")
        return -1
    # print(map)


    solution_string = graphsearch(map, flag)


    # call function write to file only in case we have a solution
    if not solution_string == '':
        write_to_file(output_file_name, solution_string)

if __name__ == "__main__":
    main()


