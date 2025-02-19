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


#set a certain face on the front (void)
#input the face you want on the front
def set_front(cube, face):

    # Cube face mappings:
    # [Front, Top, Bottom, Left, Right, Back]
    rotations = {
        0: [0, 1, 5, 3, 4, 2],  # White to front
        1: [1, 5, 0, 3, 2, 4],  # Green to front
        2: [2, 5, 0, 1, 4, 3],  # Blue to front
        3: [3, 5, 0, 2, 1, 4],  # Orange to front
        4: [4, 5, 0, 3, 2, 1],  # Red to front
        5: [5, 2, 1, 3, 4, 0],  # Yellow to front
    }

    if face not in rotations:
        print("Invalid face index. Use values 0-5.")
        return

    new_order = rotations[face]
    
    # Reorder the cube based on the rotation mapping
    cube[:] = [cube[i] for i in new_order]


#helper functions to rotate face
def rotate_face_clockwise(face):
    #Rotates a 2x2 face clockwise in-place.
    face[0], face[1], face[2], face[3] = face[2], face[0], face[3], face[1]

def rotate_face_counterclockwise(face):
    #Rotates a 2x2 face counterclockwise in-place.
    face[0], face[1], face[2], face[3] = face[1], face[3], face[0], face[2]


#rotates the specified front face clockwise and shifts adjacent edges.
def rotate_right(cube, front):
    rotate_face_clockwise(cube[front])

    # Define adjacent face mappings based on the front face being rotated
    adjacent_faces = {
        0: [1, 2, 4, 3],  # White front: affects Green, Blue, Red, Orange
        1: [5, 2, 0, 3],  # Green front: affects Yellow, Blue, White, Orange
        2: [5, 4, 0, 1],  # Blue front: affects Yellow, Red, White, Green
        3: [5, 1, 0, 4],  # Orange front: affects Yellow, Green, White, Red
        4: [5, 3, 0, 2],  # Red front: affects Yellow, Orange, White, Blue
        5: [3, 4, 1, 2],  # Yellow front: affects Orange, Red, Green, Blue
    }

    if front not in adjacent_faces:
        print("Invalid face index")
        return

    a, b, c, d = adjacent_faces[front]  # Get adjacent faces

    # Rotate edges of adjacent faces
    cube[a][2], cube[a][3], cube[b][0], cube[b][2], cube[c][0], cube[c][1], cube[d][1], cube[d][3] = \
        cube[d][1], cube[d][3], cube[a][2], cube[a][3], cube[b][0], cube[b][2], cube[c][0], cube[c][1]

#rotates the specified front face counterclockwise and shifts adjacent edges.
def rotate_left(cube, front):
    rotate_face_counterclockwise(cube[front])

    # Define adjacent face mappings (same as clockwise)
    adjacent_faces = {
        0: [1, 2, 4, 3],
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

    # Reverse rotation of edges
    cube[d][1], cube[d][3], cube[c][0], cube[c][1], cube[b][0], cube[b][2], cube[a][2], cube[a][3] = \
        cube[a][2], cube[a][3], cube[d][1], cube[d][3], cube[c][0], cube[c][1], cube[b][0], cube[b][2]

#randomizes the cube by performing a given number of random rotations.
def randomize(cube, moves):
    for _ in range(moves):
        face = random.randint(0, 5)  # Select a random face (0-5)
        direction = random.choice([rotate_right, rotate_left])  # Randomly choose CW or CCW rotation
        direction(cube, face)  # Apply the rotation

