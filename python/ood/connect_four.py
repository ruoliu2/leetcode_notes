"""
High-level

We will need a Grid class to maintain the state of the 2-D board
The board cell can be empty, yellow (occupied by Player 1) or red (occupied by Player 2)
The grid will also be responsible for checking for a win condition
We can have a Player class to represent the player's piece color
This isn't super important, but encapsulating information is generally a good practice
The Game class will be composed of the Grid and Players
The Game class will be responsible for the game loop and keeping track of the score

"""

import enum


class GridPosition(enum.Enum):

    EMPTY = 0
    YELLOW = 1
    RED = 2


# The Grid will maintain the state of the board and all of the pieces. It will also check for a win condition
# Perhaps it would be more appropriate to name the checkWin method to checkNConnected, since the Grid itself shouldn't need to know what the rules of the game are.
class Grid:

    def __init__(self, rows, columns):
        self._rows = rows
        self._columns = columns
        self._grid = None
        self.init_grid()

    def init_grid(self):
        self._grid = [
            [GridPosition.EMPTY for _ in range(self._columns)]
            for _ in range(self._rows)
        ]

    def get_grid(self):
        return self._grid

    def get_column_count(self):
        return self._columns

    def place_piece(self, column, piece):
        if column < 0 or column >= self._columns:
            raise ValueError("Invalid column")
        if piece == GridPosition.EMPTY:
            raise ValueError("Invalid piece")
        for row in range(self._rows - 1, -1, -1):
            if self._grid[row][column] == GridPosition.EMPTY:
                self._grid[row][column] = piece
                return row

    def check_win(self, connect_n, row, col, piece):
        count = 0
        # Check horizontal
        for c in range(self._columns):
            if self._grid[row][c] == piece:
                count += 1
            else:
                count = 0
            if count == connect_n:
                return True

        # Check vertical
        count = 0
        for r in range(self._rows):
            if self._grid[r][col] == piece:
                count += 1
            else:
                count = 0
            if count == connect_n:
                return True

        # Check diagonal
        count = 0
        for r in range(self._rows):
            c = row + col - r
            if c >= 0 and c < self._columns and self._grid[r][c] == piece:
                count += 1
            else:
                count = 0
            if count == connect_n:
                return True

        # Check anti-diagonal
        count = 0
        for r in range(self._rows):
            c = col - row + r
            if c >= 0 and c < self._columns and self._grid[r][c] == piece:
                count += 1
            else:
                count = 0
            if count == connect_n:
                return True

        return False


# A Player is only meant to encapsulate the player's information, more importantly the player's piece color.
class Player:

    def __init__(self, name, piece_color):
        self._name = name
        self._piece_color = piece_color

    def get_name(self):
        return self._name

    def get_piece_color(self):
        return self._piece_color


# The Game class will be used to play the game. It will keep track of the players, the score, and the grid. It will also be responsible for the game loop.
# The game parameters passed in via the constructor give us flexibility to play the game with slightly different rules and dimensions.
# While we could instantiate the board within the Game class, it's preferred to pass it in via the constructor. This means the Game class does not need to know how to instantiate the board.
# Even though we are only playing with two players, we can still use a list to store the players. This is not necessary, but it's easy enough and gives us flexibility to add more players in the future.
class Game:
    def __init__(self, grid, connect_n, target_score):
        self._grid = grid
        self._connect_n = connect_n
        self._target_score = target_score

        self._players = [
            Player("Player 1", GridPosition.YELLOW),
            Player("Player 2", GridPosition.RED),
        ]

        self._score = {}
        for player in self._players:
            self._score[player.get_name()] = 0

    def print_board(self):
        print("Board:\n")
        grid = self._grid.get_grid()
        for i, row_cells in enumerate(grid):
            row = ""
            for piece in row_cells:
                if piece == GridPosition.EMPTY:
                    row += "0 "
                elif piece == GridPosition.YELLOW:
                    row += "Y "
                elif piece == GridPosition.RED:
                    row += "R "
            print(row)
        print("")

    def play_move(self, player):
        self.print_board()
        print(f"{player.get_name()}'s turn")
        col_cnt = self._grid.get_column_count()
        move_column = int(
            input(f"Enter column between {0} and {col_cnt - 1} to add piece: ")
        )
        move_row = self._grid.place_piece(move_column, player.get_piece_color())
        return (move_row, move_column)

    def play_round(self):
        while True:
            for player in self._players:
                row, col = self.play_move(player)
                piece_color = player.get_piece_color()
                if self._grid.check_win(self._connect_n, row, col, piece_color):
                    self._score[player.get_name()] += 1
                    return player

    def play(self):
        max_score = 0
        winner = None
        while max_score < self._target_score:
            winner = self.play_round()
            print(f"{winner.get_name()} won the round")
            max_score = max(self._score[winner.get_name()], max_score)

            self._grid.init_grid()  # reset grid
        print(f"{winner.get_name()} won the game")


grid = Grid(6, 7)
game = Game(grid, 4, 2)
game.play()
