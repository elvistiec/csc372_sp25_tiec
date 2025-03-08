import random, time
from collections import deque

# 6 arrays to represent 6 faces (object)
# white, green, blue, orange, red, yellow

# numbers represent the location of the sticker on the cube
# [1,2]
# [3,4]

class Cube:
    def __init__(self):
        self.state = [  # store the cube state as an attribute
            ['w1', 'w2', 'w3', 'w4'],
            ['r1', 'r2', 'r3', 'r4'],
            ['b1', 'b2', 'b3', 'b4'],
            ['o1', 'o2', 'o3', 'o4'],
            ['g1', 'g2', 'g3', 'g4'],
            ['y1', 'y2', 'y3', 'y4'],
        ]

    def get_state(self):
        return self.state  # method to retrieve the state

# 2d depiction of 3d cube
# --00----
# --00----
# 11223344
# 11223344
# --55----
# --55----

def print_cube(Cube):
    color_map = {
        'w': '\033[97m',   # White
        'g': '\033[92m',   # Greencle
        'b': '\033[94m',   # Blue
        'o': '\033[38;5;214m',   # Orange
        'r': '\033[91m',   # Red
        'y': '\033[93m',   # Yellow
        'reset': '\033[0m' # Reset color
    }

    def colorize(sticker):
        return color_map[sticker[0]] + sticker + color_map['reset']

    print("    " + colorize(Cube.state[0][0]) + colorize(Cube.state[0][1]))
    print("    " + colorize(Cube.state[0][2]) + colorize(Cube.state[0][3]))
    print(colorize(Cube.state[1][0]) + colorize(Cube.state[1][1]) + colorize(Cube.state[2][0]) + colorize(Cube.state[2][1]) + 
          colorize(Cube.state[3][0]) + colorize(Cube.state[3][1]) + colorize(Cube.state[4][0]) + colorize(Cube.state[4][1]))
    print(colorize(Cube.state[1][2]) + colorize(Cube.state[1][3]) + colorize(Cube.state[2][2]) + colorize(Cube.state[2][3]) + 
          colorize(Cube.state[3][2]) + colorize(Cube.state[3][3]) + colorize(Cube.state[4][2]) + colorize(Cube.state[4][3]))
    print("    " + colorize(Cube.state[5][0]) + colorize(Cube.state[5][1]))
    print("    " + colorize(Cube.state[5][2]) + colorize(Cube.state[5][3]))
    print("\n")

#reset cube to solved state (void)
def reset_cube(input_cube):
    input_cube[:] = [
    ['w1', 'w2', 'w3', 'w4'],
    ['r1', 'r2', 'r3', 'r4'],
    ['b1', 'b2', 'b3', 'b4'],
    ['o1', 'o2', 'o3', 'o4'],
    ['g1', 'g2', 'g3', 'g4'],
    ['y1', 'y2', 'y3', 'y4'],
]

#check if the cube is solved (bool)
def is_solved(cube):
    for i in range(6):
        first_sticker = cube[i][0]
        for j in range(1,4):
            if cube[i][j][0] != first_sticker[0]:
                return False
    return True

#helper functions to rotate face
def rotate_face_clockwise(face):
    #rotates a 2x2 face clockwise in-place.
    face[0], face[1], face[2], face[3] = face[2], face[0], face[3], face[1]
    

def rotate_face_counterclockwise(face):
    #rotates a 2x2 face counterclockwise in-place.
    face[0], face[1], face[2], face[3] = face[1], face[3], face[0], face[2]
    

#rotates the specified front face clockwise and shifts adjacent edges.
def rotate_right(cube, face):
    rotate_face_clockwise(cube.state[face])  # rotate the selected face itself

    # faces connected to the specified face
    adjacent_faces = {
        0: [1, 2, 3, 4, 5],  
        1: [5, 2, 0, 4, 3],  
        2: [5, 3, 0, 1, 4],  
    }

    if face not in adjacent_faces:
        print("Invalid face index")
        return

    a, b, c, d, e = adjacent_faces[face]  # get adjacent faces

    # move adjacent stickers for the face being rotated
    if face == 0:
        temp = [cube.state[a][0], cube.state[a][1]]

        cube.state[a][0], cube.state[a][1] = cube.state[b][0], cube.state[b][1]
        cube.state[b][0], cube.state[b][1] = cube.state[c][0], cube.state[c][1]
        cube.state[c][0], cube.state[c][1] = cube.state[d][0], cube.state[d][1]
        cube.state[d][0], cube.state[d][1] = temp[0], temp[1]

    elif face == 1:
        temp = [cube.state[d][1], cube.state[d][3]]

        cube.state[d][1], cube.state[d][3] = cube.state[a][2], cube.state[a][0]
        cube.state[a][2], cube.state[a][0] = cube.state[b][2], cube.state[b][0]
        cube.state[b][2], cube.state[b][0] = cube.state[c][2], cube.state[c][0]
        cube.state[c][2], cube.state[c][0] = temp[0], temp[1]

    elif face == 2:
        temp = [cube.state[a][0], cube.state[a][1]]
        cube.state[a][0], cube.state[a][1] = cube.state[b][2], cube.state[b][0]
        cube.state[b][2], cube.state[b][0] = cube.state[c][3], cube.state[c][2]
        cube.state[c][3], cube.state[c][2] = cube.state[d][1], cube.state[d][3]
        cube.state[d][1], cube.state[d][3] = temp[0], temp[1]

#rotate the face left
def rotate_left(cube, face):
    # faces connected to the specified face
    adjacent_faces = {
        0: [1, 2, 3, 4, 5],  
        1: [5, 2, 0, 4, 3],  
        2: [5, 3, 0, 1, 4],  
    }

    if face not in adjacent_faces:
        print("Invalid face index")
        return

    a, b, c, d, e = adjacent_faces[face]  # get adjacent faces

    # rotate the selected face itself (counterclockwise)
    rotate_face_counterclockwise(cube.state[face])

    # move adjacent stickers for the face being rotated
    if face == 0:
        temp = [cube.state[b][0], cube.state[b][1]]

        cube.state[b][0], cube.state[b][1] = cube.state[a][0], cube.state[a][1]  
        cube.state[a][0], cube.state[a][1] = cube.state[d][0], cube.state[d][1]  
        cube.state[d][0], cube.state[d][1] = cube.state[c][0], cube.state[c][1]  
        cube.state[c][0], cube.state[c][1] = temp[0], temp[1]  

    elif face == 1:
        temp = [cube.state[b][0], cube.state[b][2]]
        cube.state[b][0], cube.state[b][2] = cube.state[a][0], cube.state[a][2]
        cube.state[a][0], cube.state[a][2] = cube.state[d][3], cube.state[d][1]
        cube.state[d][3], cube.state[d][1] = cube.state[c][0], cube.state[c][2]
        cube.state[c][0], cube.state[c][2] = temp[0], temp[1]
    
    elif face == 2:
        temp = [cube.state[c][3], cube.state[c][2]]

        cube.state[c][2], cube.state[c][3] = cube.state[b][0], cube.state[b][2]
        cube.state[b][0], cube.state[b][2] = cube.state[a][1], cube.state[a][0]
        cube.state[a][1], cube.state[a][0] = cube.state[d][3], cube.state[d][1]
        cube.state[d][1], cube.state[d][3] = temp[0], temp[1]

#randomizes the cube.state by performing a given number of random rotations.
def randomize(cube, num_moves):
    last_move = None  # store previous move as (face, direction)

    for _ in range(num_moves):
        while True:
            face = random.randint(0, 2)  # randomly choose a face (0, 1, or 2)
            direction = random.choice([rotate_right, rotate_left])  # randomly choose left or right rotation

            # ensure the move is not the direct inverse of the last one
            if last_move is not None: 
                last_face, last_direction = last_move  # get last move

                # check if the same face was last moved, and if the direction is the reverse
                if face == last_face:
                    if (last_direction == rotate_right and direction == rotate_left) or (last_direction == rotate_left and direction == rotate_right):
                        continue  
            
            # perform the move
            direction(cube, face)
            last_move = (face, direction) 
            break  # valid move, exit the loop


#helper function to convert the cube's state to a tuple 
def state_to_tuple(cube):
    return tuple(tuple(face) for face in cube.state)

#bfs solver
def bfs_solver(initial_cube):
    #keep track of nodes expanded and queue size for experiments
    global nodes_expanded, priority_queue_size

    # create a queue
    queue = deque([(initial_cube, [])])  # each entry is a tuple (cube, sequence_of_moves)
    
    # set of visited states
    visited = set()

    # convert the initial state to a tuple
    initial_state = state_to_tuple(initial_cube)
    visited.add(initial_state)

    while queue:
        current_cube, move_sequence = queue.popleft()
        nodes_expanded += 1 #track nodes expanded
        priority_queue_size = len(queue) #track queue size

        # if the current state is solved, return the solution sequence
        if is_solved(current_cube.state):
            #reverse the generated sequence
            return move_sequence[::-1]

        # explore all possible moves from the current state
        for face in range(3):  # exploiting symmetry so only working 3 faces
            for direction in [rotate_right, rotate_left]:
                # make a copy of the cube to apply the move (to avoid modifying the original)
                new_cube = Cube()
                new_cube.state = [face[:] for face in current_cube.state] 

                direction(new_cube, face)
                
                # convert the new state to a tuple
                new_state = state_to_tuple(new_cube)

                # if this state hasn't been visited before, add it to the queue
                if new_state not in visited:
                    visited.add(new_state)
                    queue.append((new_cube, move_sequence + [f"Face {face}, {'Right' if direction == rotate_right else 'Left'}"]))

    return None

# dls to gradually increase depth limit
def dls(cube, depth, path, visited):
    global nodes_expanded #track nodes expanded

    #no need to reverse sequence as it is already in solved order.
    if is_solved(cube.state):
        return path
    if depth == 0:
        return None

    visited.add(state_to_tuple(cube))  # store visited states

    for face in range(3):  
        for direction in [rotate_right, rotate_left]:
            # copy cube
            new_cube = Cube()
            new_cube.state = [row[:] for row in cube.state]  

            # apply the move
            direction(new_cube, face)
            
            new_state = state_to_tuple(new_cube)

            nodes_expanded += 1 #increment nodes expanded

            if new_state not in visited:
                result = dls(
                    new_cube, depth - 1, 
                    path + [f"Face {face}, {'Right' if direction == rotate_right else 'Left'}"], 
                    visited
                )
                if result:
                    return result

    return None  

#iddfs solver
def iddfs_solver(initial_cube):
    global nodes_expanded #track nodes expanded from dls

    depth = 0
    while True:
        visited = set()
        result = dls(initial_cube, depth, [], visited)
        if result:
            return result
        depth += 1
        if depth > 10:  # set a limit of depth 10
            return None

# heuristic for ida* algorithm
def misplaced_heuristic(cube):
    # add up all the stickers that are out of place
    goal_state = Cube().state 
    return sum(
        1 for i in range(len(cube.state)) for j in range(len(cube.state[i]))
        if cube.state[i][j] != goal_state[i][j]
    )

#iterative deepning function for ida*
def ida_star_dls(cube, path, g, threshold):
    global nodes_expanded #track nodes expanded
    
    f = g + misplaced_heuristic(cube)  # f = g + h

    if f > threshold:
        return f  # return next threshold suggestion
    if is_solved(cube.state):
        # similar to iddfs the moves do not need to be reversed
        return path  

    #track the lowest f score
    min_threshold = float('inf')  

    for face in range(3):
        for direction in [rotate_right, rotate_left]:
            #copy cube
            new_cube = Cube()
            new_cube.state = [row[:] for row in cube.state] 

            # apply the move
            direction(new_cube, face)

            nodes_expanded += 1 #incremenet node expanded

            # recursive search
            result = ida_star_dls(
                new_cube, 
                path + [f"Face {face}, {'Right' if direction == rotate_right else 'Left'}"], 
                g + 1, threshold
            )

            if isinstance(result, list): 
                return result 
            min_threshold = min(min_threshold, result)

    return min_threshold  #returns threshold score

# ida* solver
def ida_star_solver(initial_cube):
    global nodes_expanded #global variable for node expansion count from ida dls
    
    threshold = misplaced_heuristic(initial_cube)  # start with f score

    while True:
        result = ida_star_dls(initial_cube, [], 0, threshold)

        if isinstance(result, list):  
            return result  
        if result == float('inf'):  # no solution
            return None  

        threshold = result  # update threshold and continue search


#experiment
def reset_metrics():
    global nodes_expanded, cpu_time, priority_queue_size
    nodes_expanded = 0
    cpu_time = 0
    priority_queue_size = 0

def experiment():
    # save to a file for writing (append mode) at the start of the experiment
    with open('/Users/elvis/Desktop/results.txt', 'a') as f:
        for k in range(1, 26):  # 1 - 10 random turns
            f.write(f"\nRunning experiment for k={k} random turns\n")  # save the current depth
            f.flush()
            print(f"\nRunning experiment for k={k} random turns") #keep track of progress in terminal

            for i in range(20):  # 20 randomized cubes
                init_cube = Cube()
                randomize(init_cube, k)

                # BFS
                reset_metrics()
                start_time = time.time()
                bfs_solver(init_cube)
                cpu_time_bfs = time.time() - start_time
                nodes_expanded_bfs = nodes_expanded
                queue_size_bfs = priority_queue_size
                f.write(f"Cube {i + 1} - BFS: Nodes Expanded: {nodes_expanded_bfs}, CPU Time: {cpu_time_bfs:.4f} sec, Queue Size: {queue_size_bfs}\n")
                f.flush()

                # IDDFS
                reset_metrics()
                start_time = time.time()
                iddfs_solver(init_cube)
                cpu_time_iddfs = time.time() - start_time
                nodes_expanded_iddfs = nodes_expanded
                f.write(f"Cube {i + 1} - IDDFS: Nodes Expanded: {nodes_expanded_iddfs}, CPU Time: {cpu_time_iddfs:.4f} sec\n")
                f.flush()

                # IDA*
                reset_metrics()
                start_time = time.time()
                ida_star_solver(init_cube)
                cpu_time_ida = time.time() - start_time
                nodes_expanded_ida = nodes_expanded
                queue_size_ida = priority_queue_size
                f.write(f"Cube {i + 1} - IDA*: Nodes Expanded: {nodes_expanded_ida}, CPU Time: {cpu_time_ida:.4f} sec, Queue Size: {queue_size_ida}\n")
                f.flush()

# Run the experiment
print("running experiment")
experiment()

'''def main():
    init_cube = Cube()
    print("this is the current state of the cube.")
    print_cube(init_cube)
    while True:
        print("input the move you want to use; R = rotate right, L = rotate left, S = scramble, C = check if solved, Q = quit")
        user_input = input("input a move: ")

        if user_input == "Q":
            print("bye!")
            break
        elif user_input == "S":
            moves = int(input("how many random actions do you want to scramble the cube? "))
            randomize(init_cube, moves)
            print_cube()
        elif user_input == "C":
            if is_solved(init_cube):
                print("the cube is solved!")
            else:
                print("the cube is not solved.")
        elif user_input == "R" or user_input == "L":
            face = int(input("enter face number (0 to 5): "))
            if user_input == "R":
                rotate_right(init_cube, face)
            elif user_input == "L":
                rotate_left(init_cube, face)
            print_cube(init_cube)

if __name__ == "__main__":
    main()
    '''
