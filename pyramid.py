from games import *

class Pyramid(Game):
    """Play Pyramid version of Tic-Tac-Toe with first player 'MAX'.
    A state has the player to move, a cached utility, a list of moves in
    the form of a list of (x, y) positions, and a board, in the form of
    a list with number of objects in each row."""

    def __init__(self, columns=[1, 2, 3, 2, 1]):
        self.rows = max(columns)
        self.columns = columns
        moves = [(1,1), (1,2), (1,3), (1,4), (1,5), (2,2), (2,3), (2,4), (3,3)] # (row, column)
        self.initial = GameState(to_move='X', utility=0, board={}, moves=moves)

    def actions(self, state):
        """Legal moves are at least one object, all from the same row."""
        return state.moves

    def result(self, state, move):
        if move not in state.moves:
            return state
        board = state.board.copy()
        board[move] = state.to_move
        moves = list(state.moves)
        moves.remove(move)
        return GameState(to_move=('O' if state.to_move == 'X' else 'X'),
                         utility=self.compute_utility(board, move, state.to_move),
                         board=board, moves=moves)

    def utility(self, state, player):
        """Return the value to player; 1 for win, -1 for loss, 0 otherwise."""
        return state.utility if player == 'X' else -state.utility

    def terminal_test(self, state):
        """A state is terminal if there are no objects left"""
        return state.utility != 0 or len(state.moves) == 0

    def display(self, state):
        columns1 = self.columns.copy()
        for x in reversed(range(1, self.rows + 1)):
            row_ = ""
            for key, value in enumerate(columns1):
                if value == x:
                    row_ += state.board.get((x, key + 1), ".") + " "
                    columns1[key] -= 1
                else:
                    row_ += "  "
            print(row_, end="\n")

    def compute_utility(self, board, move, player):
        """If 'X' wins this move return 1; if 'O' wins return -1; else return 0."""
        if (self.three_in_row(board, move, player, (0, 1)) or
                self.three_in_row(board, move, player, (1, 0)) or
                self.three_in_row(board, move, player, (1, -1)) or
                self.three_in_row(board, move, player, (1, 1))):
            return +1 if player == 'X' else -1
        else:
            return 0
    
    def three_in_row(self, board, move, player, delta_x_y):
        """Return true if there is aline through move on board for player."""
        (delta_x, delta_y) = delta_x_y
        x, y = move
        n = 0 # n is number of moves in row
        while board.get((x, y)) == player:
            n += 1
            x, y = x + delta_x, y + delta_y
        x, y = move
        while board.get((x, y)) == player:
            n += 1
            x, y = x - delta_x, y - delta_y
        n -= 1 # Because we counted move itself twice
        return n >= 3


if __name__ == "__main__":
    pyramid = Pyramid() # Creating the game instance
    # nim1 = TicTacToe()
    #nim = GameOfNim(board=[7, 5, 3, 1]) # a much larger tree to search
    print(pyramid.initial.board) # must be [0, 5, 3, 1]
    print(pyramid.initial.moves) # must be [(1, 1), (1, 2), (1, 3), (1, 4), (1, 5), (2, 1), (2, 2), (2, 3), (3, 1)]
    print(pyramid.display(pyramid.initial))
    print(pyramid.result(pyramid.initial, (1, 1)))
    utility = pyramid.play_game(alpha_beta_player, query_player) # computer moves first

    if (utility == -1):
        print("MIN won the game")
    elif (utility == 1):
        print("MAX won the game")
    else:
        print("Game ends in Draw")
