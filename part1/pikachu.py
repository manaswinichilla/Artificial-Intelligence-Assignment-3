#
# pikachu.py : Play the game of Pikachu
#
# admysore-hdeshpa-machilla
#
# Based on skeleton code by D. Crandall, March 2021
#
import copy

import sys
import time



def board_to_string(board, N):
    return "\n".join(board[i:i + N] for i in range(0, len(board), N))

# Gives opponent of the player
def get_opponent(player):
    player_in_game = ['w', 'b']
    player_in_game.remove(player)
    opponent = player_in_game[0]
    return opponent


# Checks if a board has reached goal state,
# which is when all the pieces of any one of the player are taken by the other player
def goal_state(board, N, player, opponent):
    is_goal = False
    count_player_pichu, count_player_pikachu, count_opponent_pichu, count_opponent_pikachu = 0, 0, 0, 0

    for rows in board:
        count_player_pichu += rows.count(player)
        count_player_pikachu += rows.count(player.upper())
        count_opponent_pichu += rows.count(opponent)
        count_opponent_pikachu += rows.count(opponent.upper())

    count_player = count_player_pichu + count_player_pikachu
    count_opponent = count_opponent_pichu + count_opponent_pikachu

    if count_player == 0 and count_opponent > 0:
        is_goal = True
    elif count_opponent == 0 and count_player > 0:
        is_goal = True
    elif count_opponent == count_player:
        is_goal = False


    return is_goal


# http://www.cs.columbia.edu/~devans/TIC/AB.html

# The evaluation function written below takes into consideration the Material score
# Material score is the weighted difference of number of pieces between white and black pieces.


def evaluation(board, N, player):
    if player in ('w'):
        player_weight = 1
    else:
        player_weight = -1

    count_player_pichu, count_player_pikachu, count_opponent_pichu, count_opponent_pikachu = 0, 0, 0, 0
    opponent = get_opponent(player)

    for rows in board:
        count_player_pichu += rows.count(player)

        count_player_pikachu += rows.count(player.upper())

        count_opponent_pichu += rows.count(opponent)

        count_opponent_pikachu += rows.count(opponent.upper())

    pichus = (count_player_pichu) - (count_opponent_pichu )
    pikachu = (count_player_pikachu ) - (count_opponent_pikachu )
    # mobility = len(successors(board, player, N)) -(len(successors(board, opponent, N)))

    # piece_and_board =  piece_and_board(board, N, player, opponent)
    weight = (100 * pikachu) + ( pichus)
    # weight = weight * (-1)
    # weight = (((100 * count_player_pikachu) + count_player_pichu) *player_weight)- ((100 * count_opponent_pikachu) + count_opponent_pichu)

    return weight


def max_value(depth_limit, depth, N, player, timelimit, succ_board, alpha_value, beta_value, end_time):
    # global depth
    depth = depth + 1

    local_alpha_value = -1000000000000

    if depth == depth_limit or goal_state(succ_board, N, player, get_opponent(player)):
        # if goal_state(succ_board, N, player, get_opponent(player)):
        return evaluation(succ_board, N, player)
    else:
        # depth = depth + 1
        for new_boards in successors(succ_board, player, N):
            # alpha_value = max( alpha_value, min_value( depth_limit,depth, N, player, timelimit, new_boards[0], alpha_value, beta_value, end_time))
            # if alpha_value >= beta_value:
            #     return alpha_value

            new_value = min_value(depth_limit, depth, N, player, timelimit, new_boards[0], alpha_value, beta_value,
                                  end_time)
            if new_value > local_alpha_value:
                local_alpha_value = new_value
            if new_value > alpha_value:
                alpha_value = new_value
            if new_value >= beta_value:
                return new_value

    return local_alpha_value


def min_value(depth_limit, depth, N, player, timelimit, succ_board, alpha_value, beta_value, end_time):
    # global depth
    depth = depth + 1
    opponent = get_opponent(player)

    local_beta_value = 1000000000000
    if depth == depth_limit or goal_state(succ_board, N, player, opponent):
        return evaluation(succ_board, N, opponent)
    else:

        for new_boards in successors(succ_board, opponent, N):
            # beta_value = min(beta_value,
            #                         max_value( depth_limit,depth, N, player, timelimit, new_boards[0], alpha_value, beta_value, end_time))
            # if alpha_value >= beta_value:
            #     return beta_value
            new_value = max_value(depth_limit, depth, N, player, timelimit, new_boards[0], alpha_value, beta_value,
                                  end_time)
            if new_value < local_beta_value:
                local_beta_value = new_value
            if new_value < beta_value:
                beta_value = new_value
            if alpha_value >= new_value:
                return local_beta_value

    return local_beta_value

# From the successors of the board, Min-Max will choose the maximum value state of board.
# In the Initial call we will go to Min function for the successors of each successor
# of the initial state of board.
# And that Min function will call Max function and so on.
# This is done with Alpha beta pruning
def min_max_decision(board, N, player, timelimit, start_time, end_time, depth_limit):
    opponent = get_opponent(player)
    final_board = []
    alpha_value = -1000000000000
    beta_value =  +1000000000000

    depth = 0

    for succ_board in successors(board, player, N):
        final_score = min_value(depth_limit, depth, N, opponent, timelimit, succ_board[0], alpha_value, beta_value,
                                end_time)
        if final_score > alpha_value:
            alpha_value = final_score
            final_board = [final_score, succ_board]

    return final_board



def find_best_move(board, N, player, timelimit):
    # This sample code just returns the same board over and over again (which
    # isn't a valid move anyway.) Replace this with your code!
    #
    start_time = time.time()
    end_time = start_time + float(timelimit)

    board_list = []
    board_list[:0] = board
    board_2d = []
    # Creating 2D Board
    for row in range(0, N * N, N):
        board_2d.append(board_list[row:row + N])


    for depth_limit in range(1, 100, 2):

        [score, final_board_tuple] = min_max_decision(board_2d, N, player, timelimit, start_time, end_time, depth_limit)
        final_board = final_board_tuple[0]
        print("Hmm, Id recommend moving the Pichu at row", final_board_tuple[1], "column ", final_board_tuple[2],
              " to row ", final_board_tuple[3], " column ", final_board_tuple[4])
        print("new Board")
        str = ''

        final_board_1d_list = [s for S in final_board for s in S]
        for char in final_board_1d_list:
            str += char
        yield str



# Adding pikachu in the board that we have given
def add_pikachu(pikachu, board_2d, player_row, player_col, increment, opponent_loc, after_opponent_last_dots_loc, flag):
    board_front_list = []
    if flag == "R":
        for rows in range(opponent_loc, after_opponent_last_dots_loc, increment):
            board_front = copy.deepcopy(board_2d)
            board_front[player_row][player_col], board_front[opponent_loc - increment][player_col], \
            board_front[rows][player_col] = '.', '.', board_front[player_row][player_col]
            board_front_list.append((board_front, player_row, player_col, rows, player_col))
    elif flag == "C":
        for cols in range(opponent_loc, after_opponent_last_dots_loc, increment):
            board_front = copy.deepcopy(board_2d)
            board_front[player_row][player_col], board_front[player_row][opponent_loc - increment], \
            board_front[player_row][cols] = '.', '.', board_front[player_row][player_col]
            board_front_list.append((board_front, player_row, player_col, player_row, cols))

    return board_front_list

# Checking if there is anything other than dots or empty squares after the opponent.
# If we find anything other than dot then we return  True and the last dot's location that we encountered previously
# If the next location after the opponent is not dot then we return False
def check_after_opponent(board_2d, player_row, player_col, increment, opponent_location, end, flag):


    last_dots_poistion = [False, -100]

    if opponent_location != N - 1 or opponent_location != 0:  # If opponent loc is N-1 then its at last opistion and then we cant jump over it

        if flag == "R":
            # if opponent_location != N - 1  or opponent_location != 0: #If opponent row is N-1 then its at last opistion and then we cant jump over it
            for rows in range(opponent_location, end, increment):
                if board_2d[rows][player_col] in ('.'):
                    # can_add= True
                    last_dots_poistion = [True, rows]
                else:
                    # last_dots_poistion[0] = False I dont need to update to False Need to return only the last dot poistion
                    return last_dots_poistion
                    # First Non Dot poisition i get I return and dont loop bcuz i want
                    # last Dot's poistion
        # else:
        #     last_dots_poistion = [False, -100]
        elif flag == "C":
            # if opponent_location != N - 1  or opponent_location != 0: #If opponent row is N-1 then its at last opistion and then we cant jump over it
            for cols in range(opponent_location, end, increment):
                if board_2d[player_row][cols] in ('.'):
                    # can_add= True
                    last_dots_poistion = [True, cols]
                else:
                    # last_dots_poistion[0] = False I dont need to update to False Need to return only the last dot poistion
                    return last_dots_poistion
                    # First Non Dot poisition i get I return and dont loop bcuz i want
                    # last Dot's poistion
        # else:
        #     last_dots_poistion = [False, -100]
    else:
        last_dots_poistion = [False, -100]
    return last_dots_poistion

# Checking if there are anything other than dots in between the player and the opponent.
# If we find anything other than dot then we return False and we cannot add. Otherwise we can add
def check_between_player_opponent(board_2d, player_row, player_col, increment, opponent_location, flag):
    # we can add
    can_add = True  # True bcuz even if in the next col or row the opponent is present then we need to go ahead
    # if opponent_row != N -1: #Even if the opponent is at last row and the between points are dots then the player can move
    if flag == 'R':
        for rows in range(player_row, opponent_location,
                          increment):  # We can put opponent_row +1 as it can take maximum value till N-1
            if board_2d[rows][player_col] not in ('.'):  # if we find dots then we can add
                can_add = False
        # This below condition wont work bcuz if (player, player_pichu, dot, opponent) then it will give True As dot is the last.
        # So it will overwrite the previous False
        # else:
        #     can_add = False # if we find anything other than dots then we cant add
    elif flag == 'C':
        for cols in range(player_col, opponent_location,
                          increment):  # We can put opponent_col +1 as it can take maximum value till N-1
            if board_2d[player_row][cols] not in ('.'):  # if we find dots then we can add
                can_add = False

    return can_add

# We check if opponent exist in the row and return the first opponents position
# We check the same column but different rows
def check_opponent_in_rows(board_2d, start, end, increment, player_col, opponent, opponent_pikachu):
    # We are returning the first opponent we ever find
    for rows in range(start, end, increment):
        if board_2d[rows][player_col] in (opponent_pikachu, opponent):
            return [True, rows]  # We return the first opponent we encounter and its position

    return [False, 0]

# getting successor of pikachu if an empty square exits in front of the black pikachu
# if or an empty square exits at the back of the front pikachu
def check_front_of_black_back_of_white_pikachu(pickachu, board_2d, row, col):
    successor_pikachu_list_front = []

    pikachu_row = row
    board_2d_front = copy.deepcopy(board_2d)

    if pickachu == board_2d[row][col]:
        for rows in range(row + 1, N):
            board_2d_front = copy.deepcopy(board_2d_front)

            if board_2d_front[rows][col] == "." and pickachu == board_2d_front[rows - 1][
                col] and pikachu_row == rows - 1:
                # board_2d_front = copy.deepcopy(board_2d_front)
                board_2d_front[rows][col], board_2d_front[rows - 1][col] = board_2d_front[rows - 1][col], \
                                                                           board_2d_front[rows][col]

                # print(board_2d_left)
                pikachu_row = rows

                successor_pikachu_list_front.append((board_2d_front, row, col, pikachu_row, col))


    return successor_pikachu_list_front

# getting successor of pikachu if the player can jump over the opponent which exits in front of the black pikachu
# if or an opponent exits at the back of the white pikachu
def check_front_of_black_back_of_white_pikachu_opponent(pickachu, board_2d, row, col, opponent, opponent_pikachu):
    successor_pikachu_front_opponent = []
    # Gives position of first opponent
    result = check_opponent_in_rows(board_2d, row + 1, N, 1, col, opponent, opponent_pikachu)
    if result[0]:
        opponent_row = result[1]  # first opponents Location

        if check_between_player_opponent(board_2d, row + 1, col, 1, opponent_row, "R"):
            # If nothing between the opponent and the player then we go ahead and check if after the opponent we can add

            after_opponent_result = check_after_opponent(board_2d, row, col, 1, opponent_row + 1, N, "R")
            if after_opponent_result[0]:
                after_opponent_last_dots_row = after_opponent_result[1]  # We get the last dots position
                successor_pikachu_front_opponent = add_pikachu(pickachu, board_2d, row, col, 1, opponent_row + 1,
                                                               after_opponent_last_dots_row + 1, "R")
    return successor_pikachu_front_opponent

# getting successor of pikachu if an empty square exits in frontof the white pikachu
# if or an empty square exits at the back of the black pikachu
def check_front_of_white_back_of_black_pikachu(pickachu, board_2d, row, col):
    successor_pikachu_list_front = []

    board_2d_front = copy.deepcopy(board_2d)
    pickachu_row = row
    if pickachu == board_2d[row][col]:
        for rows in range(row - 1, -1, -1):

            if board_2d_front[rows][col] == "." and pickachu == board_2d_front[rows + 1][
                col] and pickachu_row == rows + 1:
                board_2d_front = copy.deepcopy(board_2d_front)
                board_2d_front[rows][col], board_2d_front[rows + 1][col] = board_2d_front[rows + 1][col], \
                                                                           board_2d_front[rows][col]
                pickachu_row = rows  # without this if there are more than 2 pikachu then the new boarch gives duplicate boards
                # so I keep track of the original pikachu I am working at the moment and its updated locations

                successor_pikachu_list_front.append((board_2d_front, row, col, pickachu_row, col))


    return successor_pikachu_list_front

# getting successor of pikachu if an empty square exists at the left of the pikachu
def check_left_of_pickachu(pickachu, board_2d, row, col):
    successor_pikachu_list_left = []

    board_2d_left = copy.deepcopy(board_2d)
    pikachu_col = col
    if pickachu == board_2d[row][col]:
        for column in range(col - 1, -1, -1):

            if board_2d_left[row][column] == "." and board_2d_left[row][
                column + 1] == pickachu and pikachu_col == column + 1:
                board_2d_left = copy.deepcopy(board_2d_left)
                board_2d_left[row][column + 1], board_2d_left[row][column] = board_2d_left[row][column], \
                                                                             board_2d_left[row][column + 1]

                # print(board_2d_left)
                pikachu_col = column

                successor_pikachu_list_left.append((board_2d_left, row, col, row, column + 1))


    return successor_pikachu_list_left

# getting successor of pikachu if an empty square exists at the right of the pikachu
def check_right_of_pickachu(pickachu, board_2d, row, col):
    successor_pikachu_list_right = []

    board_2d_right = copy.deepcopy(board_2d)
    pikachu_col = col

    if pickachu == board_2d[row][col]:
        for column in range(col + 1, N):

            if board_2d_right[row][column] == "." and board_2d_right[row][
                column - 1] == pickachu and pikachu_col == column - 1:
                board_2d_right = copy.deepcopy(board_2d_right)
                board_2d_right[row][column - 1], board_2d_right[row][column] = board_2d_right[row][column], \
                                                                               board_2d_right[row][column - 1]

                # print(board_2d_right)
                pikachu_col = column
                successor_pikachu_list_right.append((board_2d_right, row, col, row, column))


    return successor_pikachu_list_right


# Checking if the player can jump over its opponent which exists in front of the black pikachu
# Checking if the white pikachu can jump over the opponent behind him
def check_front_of_white_back_of_black_pickachu_opponent(pickachu, board_2d, row, col, opponent, opponent_pikachu):
    successor_pikachu_front_opponent = []
    result = check_opponent_in_rows(board_2d, row - 1, -1, -1, col, opponent, opponent_pikachu)
    if result[0]:
        opponent_row = result[1]  # opponents Location
        # between_player_and_opponent = check_between_player_opponent(pickachu, board_2d, row, col,  opponent_row,
        #                                                             opponent, opponent_pikachu)

        if check_between_player_opponent(board_2d, row - 1, col, -1, opponent_row, "R"):
            # If nothing between the opponent and the player then we go ahead and check if after the opponent we can add

            after_opponent_result = check_after_opponent(board_2d, row, col, -1, opponent_row - 1, -1, "R")
            if after_opponent_result[0]:
                after_opponent_last_dots_row = after_opponent_result[1]  # We get the last dots position
                successor_pikachu_front_opponent = add_pikachu(pickachu, board_2d, row, col, -1, opponent_row - 1,
                                                               after_opponent_last_dots_row - 1, "R")
    return successor_pikachu_front_opponent

# Checking if the player can jump over its opponent which exists in front of the white pikachu
# Checking if the black pikachu can jump over the opponent behind him
def check_front_of_white_back_of_black_pickachu_opponent(pickachu, board_2d, row, col, opponent, opponent_pikachu):
    successor_pikachu_front_opponent = []
    result = check_opponent_in_rows(board_2d, row - 1, -1, -1, col, opponent, opponent_pikachu)
    if result[0]:
        opponent_row = result[1]  # opponents Location

        if check_between_player_opponent(board_2d, row - 1, col, -1, opponent_row, "R"):
            # If nothing between the opponent and the player then we go ahead and check if after the opponent we can add

            after_opponent_result = check_after_opponent(board_2d, row, col, -1, opponent_row - 1, -1, "R")
            if after_opponent_result[0]:
                after_opponent_last_dots_row = after_opponent_result[1]  # We get the last dots position
                successor_pikachu_front_opponent = add_pikachu(pickachu, board_2d, row, col, -1, opponent_row - 1,
                                                               after_opponent_last_dots_row - 1, "R")
    return successor_pikachu_front_opponent

# We check if opponent exist in the columns and return the first opponents position.
# We check the same row but different columns of that row
def check_opponent_in_col(board_2d, player_row, end, increment, player_col, opponent, opponent_pikachu):
    result = [False, 0]
    for cols in range(player_col, end, increment):
        if board_2d[player_row][cols] in (opponent, opponent_pikachu):
            return [True, cols]

    return result

# Checking if the pikachu can jump over the opponent to the right
def check_right_of_pikachu_opponent(pickachu, board_2d, row, col, opponent, opponent_pikachu):
    successor_pikachu_right_opponent = []
    # Gives position of first opponent
    result = check_opponent_in_col(board_2d, row, N, 1, col + 1, opponent, opponent_pikachu)
    if result[0]:
        opponent_col = result[1]  # first opponents Location


        if check_between_player_opponent(board_2d, row, col + 1, 1, opponent_col, "C"):
            # If nothing between the opponent and the player then we go ahead and check if after the opponent we can add

            after_opponent_result = check_after_opponent(board_2d, row, col, 1, opponent_col + 1, N, "C")
            if after_opponent_result[0]:
                after_opponent_last_dots_row = after_opponent_result[1]  # We get the last dots position
                successor_pikachu_right_opponent = add_pikachu(pickachu, board_2d, row, col, 1, opponent_col + 1,
                                                               after_opponent_last_dots_row + 1, "C")
    return successor_pikachu_right_opponent

# Checking if the pikachu can jump over the opponent to the left
def check_left_of_pikachu_opponent(pickachu, board_2d, row, col, opponent, opponent_pikachu):
    successor_pikachu_left_opponent = []
    # Gives position of first opponent
    result = check_opponent_in_col(board_2d, row, -1, -1, col - 1, opponent, opponent_pikachu)
    if result[0]:
        opponent_col = result[1]  # first opponents Location

        if check_between_player_opponent(board_2d, row, col - 1, -1, opponent_col, "C"):
            # If nothing between the opponent and the player then we go ahead and check if after the opponent we can add

            after_opponent_result = check_after_opponent(board_2d, row, col, -1, opponent_col - 1, -1, "C")
            if after_opponent_result[0]:
                after_opponent_last_dots_row = after_opponent_result[1]  # We get the last dots position
                successor_pikachu_left_opponent = add_pikachu(pickachu, board_2d, row, col, -1, opponent_col - 1,
                                                              after_opponent_last_dots_row - 1, "C")
    return successor_pikachu_left_opponent

# Getting successors for pikachu
def get_pikachu_successor(board_2d, pikachu, N):

    opponent = get_opponent(player)

    successor_pikachu_list = []

    for row in range(N):
        for col in range(N):
            if board_2d[row][col] == pikachu:

                board_2d_right = copy.deepcopy(board_2d)
                board_2d_left = copy.deepcopy(board_2d)
                board_2d_front = copy.deepcopy(board_2d)

                board_2d_right_oppo = copy.deepcopy(board_2d)
                board_2d_left_oppo = copy.deepcopy(board_2d)
                board_2d_front_oppo = copy.deepcopy(board_2d)

                # # Opponents
                # #
                # Check front with opponents
                # if pickachu == 'W' :
                # Getting successors for jumping over and opponent for black piece (Backward Motion) and
                # Getting successors for jumping over and opponent for white piece ( Forward Motion)
                successor_white_pikachu_list_from_front = check_front_of_white_back_of_black_pickachu_opponent(pikachu,
                                                                                                               board_2d,
                                                                                                               row, col,
                                                                                                               opponent,
                                                                                                               opponent.upper())
                #
                # Getting successors for jumping over and opponent for white piece (Backward Motion) and
                # Getting successors for jumping over and opponent for black piece ( Forward Motion)

                successor_black_pikachu_list_from_front = check_front_of_black_back_of_white_pikachu_opponent(pikachu,
                                                                                                              board_2d,
                                                                                                              row, col,
                                                                                                              opponent,
                                                                                                              opponent.upper())
                # adding every board from the above list in our original list
                for board in successor_white_pikachu_list_from_front:
                    successor_pikachu_list.append(board)

                for board in successor_black_pikachu_list_from_front:
                    successor_pikachu_list.append(board)

                # # Check right of Opponent
                # Getting successors for player jumping over an opponent at the right side of the player
                successor_pikachu_list_from_right_opponent = check_right_of_pikachu_opponent(pikachu, board_2d,
                                                                                             row, col, opponent,
                                                                                             opponent.upper())
                for board in successor_pikachu_list_from_right_opponent:
                    successor_pikachu_list.append(board)
                #
                # # Check left of Opponent
                # Getting successors for player jumping over an opponent at the left side of the player
                successor_pikachu_list_from_left_opponent = check_left_of_pikachu_opponent(pikachu,
                                                                                           board_2d, row,
                                                                                           col, opponent,
                                                                                           opponent.upper())
                for board in successor_pikachu_list_from_left_opponent:
                    successor_pikachu_list.append(board)

                # No Opponent just empty dot position
                # Checking if . at right
                # Getting successor in which the player moves in the right if the next squares are empty
                successor_pikachu_list_from_right = check_right_of_pickachu(pikachu, board_2d, row, col)
                for board in successor_pikachu_list_from_right:
                    successor_pikachu_list.append(board)

                # # Checking if at left
                # Getting successor in which the player moves in the left if the next squares are empty
                successor_pikachu_list_from_left = check_left_of_pickachu(pikachu, board_2d, row, col)
                for board in successor_pikachu_list_from_left:
                    successor_pikachu_list.append(board)
                #

                # #Checking in the back and front of the pikachu
                # # if pickachu == 'W':
                # Getting successors for moving to an empty space in front of white piece (Forward Motion) and
                # Getting successors for moving to an empty space behind of black piece ( Backward Motion)

                successor_white_pikachu_list_from_front = check_front_of_white_back_of_black_pikachu(pikachu, board_2d,
                                                                                                     row, col)
                # Getting successors for moving to an empty space in front of black piece (Forward Motion) and
                # Getting successors for moving to an empty space behind of white piece ( Backward Motion)
                successor_black_pikachu_list_from_front = check_front_of_black_back_of_white_pikachu(pikachu, board_2d,
                                                                                                     row, col)

                for board in successor_white_pikachu_list_from_front:
                    successor_pikachu_list.append(board)

                for board in successor_black_pikachu_list_from_front:
                    successor_pikachu_list.append(board)
                # Backward Movement Use above Only
    return successor_pikachu_list

# Getting successors of pichus
def get_pichu_successor(board_2d, player, N):
    opponent = get_opponent(player)
    successlor_list_2d = []
    for row in range(N):

        for col in range(N):
            if board_2d[row][col] == player:
                board_2d_right = copy.deepcopy(board_2d)
                board_2d_left = copy.deepcopy(board_2d)
                board_2d_front = copy.deepcopy(board_2d)

                board_2d_right_oppo = copy.deepcopy(board_2d)
                board_2d_left_oppo = copy.deepcopy(board_2d)
                board_2d_front_oppo = copy.deepcopy(board_2d)

                # Opponent
                # Right
                # Checking if the pichu can jump over opponent to its right
                if col < N - 2 and board_2d[row][col + 1] == opponent and board_2d[row][col + 2] == '.':
                    # Swap
                    board_2d_right_oppo[row][col], board_2d_right_oppo[row][col + 2], board_2d_right_oppo[row][
                        col + 1] = board_2d_right_oppo[row][col + 2], board_2d_right_oppo[row][col], '.'
                    successlor_list_2d.append((board_2d_right_oppo, row, col, row, col + 2))
                    # print(successlor_list_2d)
                # Checking if . at left
                # Checking if the pichu can jump over opponent to its left
                if col - 2 in range(0, N) and board_2d[row][col - 2] == '.' and board_2d[row][
                    col - 1] == opponent:  # col-2 gives -1 and goes at the end of the row
                    # Swap
                    board_2d_left_oppo[row][col], board_2d_left_oppo[row][col - 2], board_2d_left_oppo[row][col - 1] = \
                        board_2d_left_oppo[row][col - 2], board_2d_left_oppo[row][col], '.'
                    successlor_list_2d.append((board_2d_left_oppo, row, col, row, col - 2))

                # Checking for front of the player
                # Checking if the pichu can jump over opponent in front of it
                if row != N - 1 and board_2d[row + 1][col] == opponent and board_2d[row + 2][
                    col] == '.' and player == 'w':
                    if row + 2 != N - 1:
                        board_2d_front_oppo[row][col], board_2d_front_oppo[row + 2][col], board_2d_front_oppo[row + 1][
                            col] = \
                            board_2d_front_oppo[row + 2][col], board_2d_front_oppo[row][col], '.'
                        # If goes to the last row then converts into pickachu
                    elif row + 2 == N - 1:
                        board_2d_front_oppo[row][col], board_2d_front_oppo[row + 2][col], board_2d_front_oppo[row + 1][
                            col] = \
                            board_2d_front_oppo[row + 2][col], player.upper(), '.'
                    successlor_list_2d.append((board_2d_front_oppo, row, col, row + 2, col))

                # Checking if the pichu can jump over opponent in front of it ( for black player)
                if row - 1 in range(0, N) and board_2d[row - 1][col] == opponent and board_2d[row - 2][
                    col] == '.' and player == 'b':
                    if row - 2 != 0:
                        board_2d_front_oppo[row][col], board_2d_front_oppo[row - 2][col], board_2d_front_oppo[row - 1][
                            col] = board_2d_front_oppo[row - 2][col], \
                                   board_2d_front_oppo[row][col], '.'
                        # If goes to the first row then converts into pickachu
                    elif row - 2 == 0:
                        board_2d_front_oppo[row][col], board_2d_front_oppo[row - 2][col], board_2d_front_oppo[row - 1][
                            col] = \
                            board_2d_front_oppo[row - 2][col], player.upper(), '.'
                    successlor_list_2d.append((board_2d_front_oppo, row, col, row - 2, col))

                # No Opponent just empty or dot squares
                # Moving to right if the next square is empty
                if col != N - 1 and board_2d[row][col + 1] == '.':
                    # Swap
                    board_2d_right[row][col], board_2d_right[row][col + 1] = board_2d_right[row][col + 1], \
                                                                             board_2d_right[row][col]
                    successlor_list_2d.append((board_2d_right, row, col, row, col + 1))
                    # print(successlor_list_2d)
                # Checking if . at left
                # Moving to left if the next square is empty
                if col - 1 in range(0, N) and board_2d[row][col - 1] == '.':
                    # Swap
                    board_2d_left[row][col], board_2d_left[row][col - 1] = board_2d_left[row][col - 1], \
                                                                           board_2d_left[row][col]
                    successlor_list_2d.append((board_2d_left, row, col, row, col - 1))

                # # Checking for front of the player
                # Moving to front if the next square is empty ( for player is white)
                if row != N - 1 and board_2d[row + 1][col] == '.' and player == 'w':
                    if row + 1 != N - 1:
                        board_2d_front[row][col], board_2d_front[row + 1][col] = board_2d_front[row + 1][col], \
                                                                                 board_2d_front[row][col]
                        # converts into pikachu
                    elif row + 1 == N - 1:
                        board_2d_front[row][col], board_2d_front[row + 1][col] = board_2d_front[row + 1][col], \
                                                                                 player.upper()
                    successlor_list_2d.append((board_2d_front, row, col, row + 1, col))

                # Moving to front if the next square is empty ( for player is black)
                if row - 1 in range(0, N) and board_2d[row - 1][col] == '.' and player == 'b':
                    if row - 1 != 0:
                        board_2d_front[row][col], board_2d_front[row - 1][col] = board_2d_front[row - 1][col], \
                                                                                 board_2d_front[row][col]
                    # converts into pikachu
                    elif row - 1 == 0:
                        board_2d_front[row][col], board_2d_front[row - 1][col] = board_2d_front[row - 1][col], \
                                                                                 player.upper()
                    successlor_list_2d.append((board_2d_front, row, col, row - 1, col))

    return successlor_list_2d


# Checking if the pikachu exists in the board
def check_pikachu_exists(board, player, N, pikachu):
    exists = False
    for rows in board:
        if pikachu in rows:
            exists = True
            return exists
    return exists


# Getting successors of the board
def successors(board, player, N):
    pikachu = player.upper()
    successor_list = []
    pikachu_successors = []
    # getting successors of pikachu id it exists in board
    if check_pikachu_exists(board, player, N, pikachu):
        pikachu_successors = get_pikachu_successor(board, pikachu, N)

    for boards in pikachu_successors:
        successor_list.append(boards)
    # getting successors of pichus
    pichu_successors = get_pichu_successor(board, player, N)
    for boards in pichu_successors:
        successor_list.append(boards)



    return successor_list




#
#
if __name__ == "__main__":
    if len(sys.argv) != 5:
        raise Exception("Usage: pikachu.py N player board timelimit")

    (_, N, player, board, timelimit) = sys.argv
    N = int(N)
    timelimit = int(timelimit)
    if player not in "wb":
        raise Exception("Invalid player.")

    if len(board) != N * N or 0 in [c in "wb.WB" for c in board]:
        raise Exception("Bad board string.")



    print("Searching for best move for " + player + " from board state: \n" + board_to_string(board, N))
    print("Here's what I decided:")



    for new_board in find_best_move(board, N, player, timelimit):
        print(new_board)




########## Different Evaluation functions I tried
# https://www.cs.huji.ac.il/~ai/projects/old/English-Draughts.pdf
# #
# def evaluation_adv(board, N, player):
#     opponent = get_opponent(player)
#     count_of_player = piece_and_board(board, N, player)
#     count_of_opponent = piece_and_board(board, N, opponent)
#     eval_weight = count_of_player - count_of_opponent
#
#     return eval_weight
#
#
# def evaluation_new_adv(board, N, player):
#     opponent = get_opponent(player)
#     count_of_player = piece_and_row(board, N, player)
#     count_of_opponent = piece_and_row(board, N, opponent)
#     eval_weight = count_of_player - count_of_opponent
#
#     return eval_weight
#
#
# def piece_and_row(board, N, player):
#     count_of_player_pichus = count_of_pichus_in_a_row(board, N, player)
#     count_of_player_pikachus = count_of_pichus_in_a_row(board, N, player.upper())
#
#     weight = count_of_player_pichus + (100 * count_of_player_pikachus)
#     return weight
#
#
# def count_of_pikachus_in_a_row(board, N, player):
#     count_of_pikachus = 0
#     number_of_rows = 0
#     for rows in board:
#         if player in rows:
#             number_of_rows += 1
#         count_of_pikachus += rows.count(player)
#
#     count_of_pikachus += rows
#     return count_of_pikachus
#
#
# def count_of_pichus_in_a_row(board, N, player):
#     count_of_pichus = 0
#     row_number = 0
#     for rows in board:
#         row_number += 1
#         count_of_pichus += rows.count(player) + row_number
#
#     return count_of_pichus
#
#
# def count_of_birds(board, N, player, start, end, increment):
#     count_of_bird = 0
#
#     for rows in range(start, end, increment):
#         row_of_board = board[rows]
#         count_of_bird += row_of_board.count(player)
#     return count_of_bird
#
#
# def piece_and_board(board, N, player):
#     count_of_player_pichu_in_players_half, count_of_player_pichu_in_opponent_half = 0, 0
#     count_of_player_pikachu, count_of_player_in_middle_row = 0, 0
#
#     count_of_player = 0
#     if N % 2 == 0:  # eg 4
#         if player == 'w':
#             players_half = N // 2  # 2  [0,2)
#             opponent_half = N - players_half  # 2  [2,3]
#             count_of_player_pichu_in_players_half = count_of_birds(board, N, player, 0, players_half, 1)
#             count_of_player_pichu_in_opponent_half = count_of_birds(board, N, player, opponent_half, N, 1)
#             count_of_player_pikachu = count_of_birds(board, N, player.upper(), 0, N, 1)
#             # count_of_player = 50 * count_of_player_pichu_in_players_half +
#             #                   100 * count_of_player_pichu_in_opponent_half +
#             #                   200 * count_of_player_pikachu
#         if player == 'b':
#             opponent_half = N // 2  # 2 [0,2)
#             players_half = N - opponent_half  # 2  [2,3]
#             count_of_player_pichu_in_players_half = count_of_birds(board, N, player, N - 1, players_half - 1, -1)
#             count_of_player_pichu_in_opponent_half = count_of_birds(board, N, player, 0, opponent_half, 1)
#             count_of_player_pikachu = count_of_birds(board, N, player.upper(), 0, N, 1)
#
#     if N % 2 == 1:  # eg 5
#         if player == 'w':
#             players_half = (N // 2) - 1  # 1 [0, 1]
#             opponent_half = players_half + 2  # 3 [3,4]
#             count_of_player_pichu_in_players_half = count_of_birds(board, N, player, 0, players_half + 1, 1)
#             count_of_player_pichu_in_opponent_half = count_of_birds(board, N, player, opponent_half, N, 1)
#             count_of_player_pikachu = count_of_birds(board, N, player, 0, N, 1)
#             count_of_player_in_middle_row = count_of_birds(board, N, player, players_half + 1, opponent_half,
#                                                            1)  # row 2
#         if player == 'b':
#             opponent_half = (N // 2) - 1  # 1 [0, 1]
#             players_half = opponent_half + 2  # 3 [3,4]
#             count_of_player_pichu_in_players_half = count_of_birds(board, N, player, N - 1, players_half - 1, -1)
#             count_of_player_pichu_in_opponent_half = count_of_birds(board, N, player, 0, opponent_half + 1, 1)
#             count_of_player_pikachu = count_of_birds(board, N, player, 0, N, 1)
#             count_of_player_in_middle_row = count_of_birds(board, N, player, players_half - 1, opponent_half, -1)
#
#     count_of_player = (50 * count_of_player_pichu_in_players_half) + (75 * count_of_player_in_middle_row) + (
#                 100 * count_of_player_pichu_in_opponent_half) + (200 * count_of_player_pikachu)
#
#     return count_of_player
