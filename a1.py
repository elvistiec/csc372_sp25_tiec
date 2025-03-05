import random

# 6 arrays to represent 6 faces (object)
# white, green, blue, orange, red, yellow

# numbers represent the location of the sticker on the cube
# [1,2]
# [3,4]

cube = [
    ['w1', 'w2', 'w3', 'w4'],
    ['g1', 'g2', 'g3', 'g4'],
    ['b1', 'b2', 'b3', 'b4'],
    ['o1', 'o2', 'o3', 'o4'],
    ['r1', 'r2', 'r3', 'r4'],
    ['y1', 'y2', 'y3', 'y4'],
]

# 2d depiction of 3d cube
# --00----
# --00----
# 11223344
# 11223344
# --55----
# --55----

def print_cube():
    color_map = {
        'w': '\033[97m',   # White
        'g': '\033[92m',   # Green
        'b': '\033[94m',   # Blue
        'o': '\033[38;5;214m',   # Orange
        'r': '\033[91m',   # Red
        'y': '\033[93m',   # Yellow
        'reset': '\033[0m' # Reset color
    }

    def colorize(sticker):
        return color_map[sticker[0]] + sticker + color_map['reset']

    print("    " + colorize(cube[0][0]) + colorize(cube[0][1]))
    print("    " + colorize(cube[0][2]) + colorize(cube[0][3]))
    print(colorize(cube[1][0]) + colorize(cube[1][1]) + colorize(cube[2][0]) + colorize(cube[2][1]) + 
          colorize(cube[3][0]) + colorize(cube[3][1]) + colorize(cube[4][0]) + colorize(cube[4][1]))
    print(colorize(cube[1][2]) + colorize(cube[1][3]) + colorize(cube[2][2]) + colorize(cube[2][3]) + 
          colorize(cube[3][2]) + colorize(cube[3][3]) + colorize(cube[4][2]) + colorize(cube[4][3]))
    print("    " + colorize(cube[5][0]) + colorize(cube[5][1]))
    print("    " + colorize(cube[5][2]) + colorize(cube[5][3]))
    print("\n")

#reset cube to solved state (void)
def reset_cube(input_cube):
    input_cube[:] = [
    ['w1', 'w2', 'w3', 'w4'],
    ['g1', 'g2', 'g3', 'g4'],
    ['b1', 'b2', 'b3', 'b4'],
    ['o1', 'o2', 'o3', 'o4'],
    ['r1', 'r2', 'r3', 'r4'],
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
def rotate_right(cube, front):
    rotate_face_clockwise(cube[front])  # Rotate the selected face itself

    # Define adjacent face mappings
    adjacent_faces = {
        0: [1, 2, 3, 4],  
        1: [5, 2, 0, 4],  
        2: [5, 3, 0, 1],  
        3: [5, 2, 0, 4],  
        4: [5, 3, 0, 1],  
        5: [3, 4, 1, 2],  
    }

    if front not in adjacent_faces:
        print("Invalid face index")
        return

    a, b, c, d = adjacent_faces[front]  # Get adjacent faces

    # Save original stickers before overwriting them
    temp = [cube[a][0], cube[a][1]]

    # Move stickers in a cycle (correct order)
    cube[a][0], cube[a][1] = cube[b][0], cube[b][1]
    cube[b][0], cube[b][1] = cube[c][0], cube[c][1]
    cube[c][0], cube[c][1] = cube[d][0], cube[d][1]
    cube[d][0], cube[d][1] = temp[0], temp[1]


#rotates the specified front face counterclockwise and shifts adjacent edges.
def rotate_left(cube, front):
    rotate_face_counterclockwise(cube[front])  # Rotate the selected face itself

    # Define adjacent face mappings (same as clockwise)
    adjacent_faces = {
        0: [1, 2, 3, 4],  
        1: [5, 2, 0, 3],  
        2: [5, 4, 0, 1],  
        3: [5, 1, 0, 4],  
        4: [5, 3, 0, 2], 
        5: [3, 4, 1, 2], 
    }

    if front not in adjacent_faces:
        print("Invalid face index")
        return

    a, b, c, d = adjacent_faces[front]  # Get adjacent faces

    # Save the original stickers to avoid overwriting
    temp = [cube[b][0], cube[b][1]]

    # Move stickers in a cycle (counterclockwise direction)
    cube[b][0], cube[b][1] = cube[a][0], cube[a][1]  
    cube[a][0], cube[a][1] = cube[d][0], cube[d][1]  
    cube[d][0], cube[d][1] = cube[c][0], cube[c][1]  
    cube[c][0], cube[c][1] = temp[0], temp[1]  


#randomizes the cube by performing a given number of random rotations.
def randomize(cube, moves):
    last_move = None  # store previous move
    
    for _ in range(moves):
        while True:
            face = random.randint(0, 5)  
            direction = random.choice([rotate_right, rotate_left])  # Randomly choose CW or CCW rotation
            
            # Ensure the move is not the direct inverse of the last one
            if last_move is None or not (last_move[0] == face and last_move[1] != direction):
                break  # Valid move found
        
        direction(cube, face)  # Apply the rotation
        last_move = (face, direction)  # Update last move
    
    print("cube randomized")

def main():
    print("this is the current state of the cube.")
    print_cube()
    while True:
        print("input the move you want to use; R = rotate right, L = rotate left, S = scramble, C = check if solved, Q = quit")
        user_input = input("input a move: ")

        if user_input == "Q":
            print("bye!")
            break
        elif user_input == "S":
            moves = int(input("how many random actions do you want to scramble the cube? "))
            randomize(cube, moves)
            print_cube()
        elif user_input == "C":
            if is_solved(cube):
                print("the cube is solved!")
            else:
                print("the cube is not solved.")
        elif user_input == "R" or user_input == "L":
            face = int(input("enter face number (0 to 5): "))
            if user_input == "R":
                rotate_right(cube, face)
            elif user_input == "L":
                rotate_left(cube, face)
            print_cube()

if __name__ == "__main__":
    main()
