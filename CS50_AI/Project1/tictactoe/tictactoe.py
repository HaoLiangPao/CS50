"""
Tic Tac Toe Player
"""

import math
from copy import deepcopy
from collections import deque

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    X_count = 0
    O_count = 0
    # Check #moves for each player
    for row in board:
        for column in row:
            if column == X:
                X_count += 1
            elif column == O:
                O_count += 1
    # print(f"X_count is {X_count}\nO_count is {O_count}")
    # Return the player with less moves
    return O if O_count < X_count else X


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    result = set()
    for row in range(len(board)):
        for column in range(len(board[0])):
            if board[row][column] == EMPTY:
                result.add((row, column))
    return result


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    # Get current player
    current_player = player(board)
    result_board = deepcopy(board)
    target_cell = result_board[action[0]][action[1]]
    # Raise an error when trying to move on cells already occupied
    if target_cell != EMPTY:
        raise ValueError("Invalid move...")
    # Take an action as the current player
    else:
        result_board[action[0]][action[1]] = current_player
    return result_board


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    result = utility(board)
    if result == 1:
        return X
    elif result == -1:
        return O
    else:
        return None


def winner_dfs(board):
    """
    Returns the winner of the game, if there is one.
    """
    # DFS
    frontier = deque()
    # Starting point
    frontier.append((0,0,0,0))
    explored = set()

    while frontier:
        c_row, c_column, X_count, O_count = frontier.pop()
        explored.add((c_row, c_column))
        print(c_row)
        print(c_column)
        if board[c_row][c_column] == X:
            X_count += 1
        elif board[c_row][c_column] == O:
            O_count += 1
        else:
            break # check next cell in frontier, not possible to win
        # if winning
        if X_count == 3:
            return X
        if O_count == 3:
            return O
        # Add neighbors into the frontier
        if (c_row, c_column + 1) not in explored:
            horizontal  = (c_row, c_column + 1, X_count, O_count)
            frontier.append(horizontal)
        if (c_row + 1, c_column) not in explored:
            vertical  = (c_row + 1, c_column, X_count, O_count)
            frontier.append(vertical)
        if (c_row + 1, c_column + 1) not in explored:
            diagonal  = (c_row + 1, c_column + 1, X_count, O_count)
            frontier.append(diagonal)
    # No one wins the game
    return None

def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    # Game is terminated if there is a winner
    if winner(board):
        return True
    # If there is no winner yet, check if the whole board is occupied
    else:
        for row in range(len(board)):
            for column in range(len(board[0])):
                if board[row][column] == EMPTY:
                    return False
        # All cells are occupied, game is terminated
        return True



def winner_one_spot(board, row, column):
    """
    Check only from the given starting point, returns 1 if X has won
    the game, -1 if O has won, 0 otherwise.
    """
    rules = [(0,1), (1,0), (1,1), (1,-1)]
    for rule in rules:
        start = (row, column)
        # print(f"Starting from {start}")
        # Try three times with the same winning logic
        X_count = 1 if board[start[0]][start[1]] == X else 0
        O_count = 1 if board[start[0]][start[1]] == O else 0
        for i in range(2):
            next = (start[0] + rule[0], start[1] + rule[1])
            # print(f"next is {next}")
            # Only check for valid winning combinations
            if 0 <= next[0] <= 2 and 0 <= next[1] <= 2:
                if board[next[0]][next[1]] == "X":
                    X_count += 1
                elif board[next[0]][next[1]] == "O":
                    O_count += 1
                # print(f"X_count is {X_count}, O_count is {O_count}")
                # Wining Test
                if X_count == 3:
                    return 1
                if O_count == 3:
                    return -1
                start = next
    # When no player wins the game
    return 0


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    # Start from every spot in the board, check if they match a line
    for row in range(len(board)):
        for column in range(len(board[0])):
            # print(f"\nChecking {(row, column)} ...")
            check = winner_one_spot(board, row, column)
            if check != 0:
               return check
    # If no winner been detect after checkin all spots
    return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    index = minimax_action_index(board)[1]
    # print(f"index is {index}")
    possible_moves = list(actions(board))
    # print(f"possible_moves is {possible_moves}")
    return possible_moves[index]


# Helper function
def minimax_action_index(board):
    """
    Returns the optimal action_index for the current player on the board.
    """
    # Resursive algorithum
    # Base Case: the board is terminated, return the final utility score
    if terminal(board):
        return (utility(board), -1)
    # Normal Case: recursively making moves and sum the utility scores
    else:
        # Get current player (X is max player, O is min player)
        current_player = player(board)
        # print(f"current player is {current_player}")
        # Get all possible actions from this state
        moves = list(actions(board))
        # print(f"list of moves is: {moves}")
        scores = [0] * len(moves)
        for move_index in range(len(moves)):
            next_board = result(board, moves[move_index])
            scores[move_index] = minimax_action_index(next_board)[0]
        if current_player == X:
            optimal_score = max(scores)
            # print(f"Max Score is {scores}")
            return (optimal_score, scores.index(optimal_score))
        else:
            optimal_score = min(scores)
            # print(f"Min Score is {scores}")
            return (optimal_score, scores.index(optimal_score))


# Testing boards
# a = [[EMPTY, X, O], [O, X, EMPTY], [X, EMPTY, O]]
# b = [[EMPTY, X, O], [O, X, X], [X, EMPTY, O]]
# c = [[X, X, O], [X, O, EMPTY], [EMPTY, EMPTY, EMPTY]]
d = [[X, X, O], [X, O, EMPTY], [EMPTY, EMPTY, EMPTY]]
e = [[X, X, O], [X, O, EMPTY], [O, EMPTY, EMPTY]]

