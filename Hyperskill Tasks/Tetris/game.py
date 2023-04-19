import copy
import random
import math
n_rows = 24
n_cols = 10

def generate_empty_matrix(n_rows, n_cols):
    matrix = []
    for i in range(n_rows):
        matrix.append(['-']*n_cols)
    return matrix

def print_matrix(matrix):
    for i in range(len(matrix)):
        print(' '.join(matrix[i]))
    print()


def insert_piece(matrix, piece):

    local_matrix = list(copy.deepcopy(matrix))
    size = len(local_matrix[0])
    for index in piece:
        row = math.floor(index/size)
        col = index%size
        local_matrix[row][col] = '0'
    return local_matrix

# old move piece
# def move_piece(matrix, direction, empty_matrix, piece_position):
#     # matrix - current game state
#     # direction - move
#     # empty matrix - empty matrix to be input to avoid generating it every time
#
#     n_rows = len(matrix)
#     n_cols = len(matrix[0])
#     output_matrix = list(copy.deepcopy(empty_matrix))
#
#     if direction == 'right':
#         for i in reversed(range(n_rows)):
#             for j in reversed(range(n_cols)):
#                 if matrix[i][j] == '0 ':
#                     if j!=n_cols-1:
#                         output_matrix[i][j+1] = '0 '
#                     else:
#                         output_matrix[i][0] = '0 '  # moving through border
#
#                     # output_matrix[i][j] = '- '  # leaving the crate empty after moving symbol
#     piece_position[0] += 1
#
#     if direction == 'left':
#         for i in range(n_rows):
#             for j in range(n_cols):
#                 if matrix[i][j] == '0 ':
#                     if j!=0:
#                         output_matrix[i][j-1] = '0 '
#                     else:
#                         output_matrix[i][n_cols-1] = '0 '
#                     # output_matrix[i][j] = '- '
#     piece_position[0] -= 1
#
#     if direction == "down":
#         for i in reversed(range(n_rows)):
#             for j in range(n_cols):
#                 if matrix[i][j] == '0 ':
#                     if i!=n_rows-1:
#                         output_matrix[i+1][j] = '0 '
#                     else:
#                         output_matrix[0][j] = '0 '
#                     # output_matrix[i][j] = '- '
#     piece_position[1] +=1
#     return output_matrix, piece_position

def check_complete_row(matrix):
    n_rows = len(matrix)
    n_cols = len(matrix[0])
    for i in range(n_rows):
        single_row = matrix[i]
        if single_row.count('0') == n_cols:
            for j in range(i-1):
                matrix[i-j] = copy.deepcopy(matrix[i-j-1])
            matrix[0] = ['-'] * n_cols
    return matrix



def check_complete_col(matrix):
    n_rows = len(matrix)
    n_cols = len(matrix[0])
    for i in range(n_cols):
        single_col = [elem[i] for elem in matrix]
        if single_col.count('0') == n_rows:
            return True
    return False


def move_piece(matrix, direction, empty_matrix, piece_position, chosen_piece):
    # matrix - current game state
    # direction - move
    # empty matrix - empty matrix to be input to avoid generating it every time


    next_trigger = 0
    n_rows = len(matrix)
    n_cols = len(matrix[0])
    output_matrix = list(copy.deepcopy(empty_matrix))
    local_piece = list(copy.deepcopy(chosen_piece[piece_position[2]]))

    # prevents piece from moving when its touching the bottom
    if any([element + piece_position[1] * n_cols > n_cols * (n_rows-1) for element in local_piece]):
        empty_matrix = matrix
        next_trigger = 1
        return matrix, piece_position, next_trigger

    if any([element + piece_position[1] * n_cols > n_cols * (n_rows-1) for element in local_piece]):
        empty_matrix = matrix
        next_trigger = 1
        return matrix, piece_position, next_trigger

    if direction == 'right':
        piece_position[0] += 1


    if direction == 'left':
        piece_position[0] -= 1

    if direction == "down":
        # size = len(local_piece)
        for element in local_piece:
            element = element + piece_position[0] + piece_position[1] * n_cols
            row = math.floor(element / n_cols)
            col = element % n_cols
            if empty_matrix[row+1][col] == '0':
                empty_matrix = matrix
                next_trigger = 1
                return matrix, piece_position, next_trigger
        piece_position[1] +=1

    # stop pieces from moving between borders
    if any([element%n_cols + piece_position[0] > n_cols - 1  for element in local_piece]):
        piece_position[0] -= 1
    if any([element%n_cols + piece_position[0] < 0  for element in local_piece]):
        piece_position[0] += 1
    if any([element > n_cols * n_rows for element in local_piece]):
        piece_position[1] -= 1


    # for element in local_piece:
        # element += piece_position[0] + piece_position[1] * n_cols
    local_piece_shifted = []

    # taking into account moving pieces through walls ( propably prevented higher in this fcn)
    for element in local_piece:
        if element%n_cols + piece_position[0] > n_cols - 1:
            element_shifted = element + piece_position[0] + piece_position[1] * n_cols - n_cols
        elif element%n_cols + piece_position[0] < 0:
            element_shifted = element + piece_position[0] + piece_position[1] * n_cols + n_cols
        else:
            element_shifted = element + piece_position[0] + piece_position[1] * n_cols

        # moving piece through bottom to up of screen (propably prevented blocked higher in this fcn)
        if element_shifted> n_cols * n_rows:
            element_shifted -= n_cols * n_rows
        local_piece_shifted.append(element_shifted)



    output_matrix = insert_piece(output_matrix, local_piece_shifted)
    return output_matrix, piece_position, next_trigger

def rotate_piece(matrix, empty_matrix, piece_position, chosen_piece):
    # output_matrix = list(copy.deepcopy(empty_matrix))
    # # current_piece = copy.deepcopy(chosen_piece)
    # current_piece = []
    # n_rows = len(matrix)
    # n_cols = len(matrix[0])
    #
    # for rows in chosen_piece:
    #     new_row = []
    #     for cols in rows:
    #         new_row.append(cols + piece_position[0] +  piece_position[1] * n_cols)
    #     current_piece.append(new_row)

    n_rows = len(matrix)
    n_cols = len(matrix[0])
    output_matrix = list(copy.deepcopy(empty_matrix))

    #     state = i%len(chosen_piece)
    #     rotation_state = chosen_piece[i%len(chosen_piece)]
    local_piece = list(copy.deepcopy(chosen_piece[piece_position[2]]))
    if any([element + piece_position[1] * n_cols > n_cols * (n_rows-1) for element in local_piece]):
        return matrix, piece_position

    piece_position[2] += 1
    if piece_position[2] > len(chosen_piece) - 1:
        piece_position[2] -= len(chosen_piece)

    local_piece = list(copy.deepcopy(chosen_piece[piece_position[2]]))



    # for element in local_piece:
        # element += piece_position[0] + piece_position[1] * n_cols
    local_piece_shifted = []
    for element in local_piece:
        if element%n_cols + piece_position[0] > n_cols - 1:
            element_shifted = element + piece_position[0] + piece_position[1] * n_cols - n_cols
        elif element%n_cols + piece_position[0] < 0:
            element_shifted = element + piece_position[0] + piece_position[1] * n_cols + n_cols
        else:
            element_shifted = element + piece_position[0] + piece_position[1] * n_cols

        if element_shifted> n_cols * n_rows:
            element_shifted -= n_cols * n_rows
        local_piece_shifted.append(element_shifted)

    output_matrix = insert_piece(output_matrix, local_piece_shifted)

    return output_matrix, piece_position



O = [[4, 14, 15, 5]]
I = [[4, 14, 24, 34], [3, 4, 5, 6]]
S = [[5, 4, 14, 13], [4, 14, 15, 25]]
Z = [[4, 5, 15, 16], [5, 15, 14, 24]]
L = [[4, 14, 24, 25], [5, 15, 14, 13], [4, 5, 15, 25], [6, 5, 4, 14]]
J = [[5, 15, 25, 24], [15, 5, 4, 3], [5, 4, 14, 24], [4, 14, 15, 16]]
T = [[4, 14, 24, 15], [4, 13, 14, 15], [5, 15, 25, 14], [4, 5, 6, 15]]


# user_chosen_shape = input()
# chosen_piece = globals()[user_chosen_shape]
#
# empty_matrix = generate_empty_matrix(n_rows, n_cols)
# print_matrix(empty_matrix)
#
# printing user input piece in every rotation
# for i in range(5):
#     state = i%len(chosen_piece)
#     rotation_state = chosen_piece[i%len(chosen_piece)]
#     #empty_matrix = generate_empty_matrix(n_rows, n_cols)
#     piece_matrix = insert_piece(empty_matrix, rotation_state).copy()
#     print_matrix(piece_matrix)

if __name__ == '__main__':

    n_cols, n_rows = [int(x) for  x in input().split()]


    # printing empty starting screen
    empty_matrix = generate_empty_matrix(n_rows, n_cols)
    print_matrix(empty_matrix)

    # printing starting screen with piece on it

    piece_position = [0, 0, 0]
    # print_matrix(game_screen)
    # game_screen = []
    trigger = 1
    game_screen = empty_matrix
    endgame = 0
    while 1:

        if endgame == 1:
            break

        user_move = input()

        if trigger == 1:
            empty_matrix = game_screen
            if user_move == 'exit':
                endgame = 1
                break

            if user_move == 'piece':
                chosen_piece = globals()[input()]
                piece_position = [0 for i in piece_position]
                game_screen = insert_piece(empty_matrix, chosen_piece[0])
                trigger = 0
                print_matrix(game_screen)

            if user_move == 'break':
                game_screen = check_complete_row(game_screen)

                print_matrix(game_screen)


        else:
            if user_move == 'exit':
                endgame = 1
                break
            if user_move in ('left', 'right'):
                game_screen, piece_position, trigger = move_piece(game_screen, user_move, empty_matrix, piece_position, chosen_piece)
                game_screen, piece_position, trigger = move_piece(game_screen, 'down', empty_matrix, piece_position,chosen_piece)
            if user_move in 'rotate':
                game_screen, piece_position = rotate_piece(game_screen, empty_matrix, piece_position, chosen_piece)
                game_screen, piece_position, trigger = move_piece(game_screen, 'down', empty_matrix, piece_position, chosen_piece)
            if user_move == 'down':
                game_screen, piece_position, trigger = move_piece(game_screen, 'down', empty_matrix, piece_position, chosen_piece)

            if user_move == 'break':
                game_screen = check_complete_row(game_screen)

            print_matrix(game_screen)
            if check_complete_col(game_screen):
                print('Game Over!')
                endgame = 1
                break
            # after every move, move the piece one row down
            # game_screen, piece_position, trigger = move_piece(game_screen, 'down', empty_matrix, piece_position, chosen_piece)


        # if trigger == 1:
        #     game_screen = check_complete_row(game_screen)
        #
        #     print("piece")
        #     chosen_piece = globals()[input()]
        #     piece_position = [0 for i in piece_position]
        #     empty_matrix = game_screen
        #     game_screen = insert_piece(game_screen, chosen_piece[0])
        #     print_matrix(game_screen)



