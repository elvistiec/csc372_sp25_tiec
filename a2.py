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
    #Rotates a 2x2 face clockwise in-place.
    face[0], face[1], face[2], face[3] = face[2], face[0], face[3], face[1]
    

def rotate_face_counterclockwise(face):
    #Rotates a 2x2 face counterclockwise in-place.
    face[0], face[1], face[2], face[3] = face[1], face[3], face[0], face[2]
    


#rotates the specified front face clockwise and shifts adjacent edges.
def rotate_right(cube, face):
    rotate_face_clockwise(cube.state[face])  # Rotate the selected face itself

    # Define adjacent face mappings
    adjacent_faces = {
        0: [1, 2, 3, 4, 5],  
        1: [5, 2, 0, 4, 3],  
        2: [5, 3, 0, 1, 4],  
    }

    if face not in adjacent_faces:
        print("Invalid face index")
        return

    a, b, c, d, e = adjacent_faces[face]  # Get adjacent faces

    if face == 0:
        # Save original stickers before overwriting them
        temp = [cube.state[a][0], cube.state[a][1]]

        # Move stickers in a cycle (correct order)
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

def rotate_left(cube, face):
    # Define adjacent face mappings (same as clockwise)
    adjacent_faces = {
        0: [1, 2, 3, 4, 5],  
        1: [5, 2, 0, 4, 3],  
        2: [5, 3, 0, 1, 4],  
    }

    if face not in adjacent_faces:
        print("Invalid face index")
        return

    a, b, c, d, e = adjacent_faces[face]  # Get adjacent faces

    # Rotate the selected face itself (counterclockwise)
    rotate_face_counterclockwise(cube.state[face])

    if face == 0:
        # Save the original stickers to avoid overwriting
        temp = [cube.state[b][0], cube.state[b][1]]

        # Move stickers in a cycle (counterclockwise direction)
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
def randomize(cube, moves):
    last_move = None  # store previous move
    
    for _ in range(moves):
        while True:
            face = random.randint(0, 2)  
            direction = random.choice([rotate_right, rotate_left])  # Randomly choose CW or CCW rotation
            
            # Ensure the move is not the direct inverse of the last one
            if last_move is None or not (last_move[0] == face and last_move[1] != direction):
                break  # Valid move found
        
        direction(cube, face)  # Apply the rotation
        last_move = (face, direction)  # Update last move
        print(last_move)
    
    print("cube randomized")

actions = ['top_cw', 'top_ccw', 'left_cw', 'left_ccw', 'right_cw', 'right_ccw']

reverse_move = {
    'top_cw': 'top_ccw',
    'top_ccw': 'top_cw',
    'left_cw': 'left_ccw',
    'left_ccw': 'left_cw',
    'right_cw': 'right_ccw',
    'right_ccw': 'right_cw'
}

def apply_move(cube, move):
    print(f"Applying move: {move}")  # Log which move is being applied
    if isinstance(cube, Cube):  # Ensure the object is a Cube instance
        if move == 'top_cw':
            rotate_right(cube, 0)
        elif move == 'top_ccw':
            rotate_left(cube, 0)
        elif move == 'left_cw':
            rotate_right(cube, 1)
        elif move == 'left_ccw':
            rotate_left(cube, 1)
        elif move == 'right_cw':
            rotate_right(cube, 2)
        elif move == 'right_ccw':
            rotate_left(cube, 2)
        
        return cube  # Return the updated state after applying the move
    else:
        print("Error: 'cube' is not an instance of the Cube class")
        return None


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
