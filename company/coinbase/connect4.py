class Connect4:
    def __init__(self, rows=6, cols=7):
        self.rows = rows
        self.cols = cols
        self.board = [[" " for _ in range(cols)] for _ in range(rows)]
        self.moves = 0
        self.current_player = "X"
        self.game_over = False
        self.winner = None
        # Keep track of the number of pieces in each column for O(1) placement
        self.heights = [0] * cols

    def make_move(self, col):
        """Place a piece in the specified column."""
        if self.game_over:
            raise ValueError("Game is already over")

        if col < 0 or col >= self.cols:
            raise ValueError(f"Column must be between 0 and {self.cols-1}")

        if self.heights[col] >= self.rows:
            raise ValueError("Column is full")

        # Place the piece at the top of the column
        row = self.rows - 1 - self.heights[col]
        self.board[row][col] = self.current_player
        self.heights[col] += 1
        self.moves += 1

        # Check for win
        if self._check_win(row, col):
            self.game_over = True
            self.winner = self.current_player
            return True

        # Check for draw
        if self.moves == self.rows * self.cols:
            self.game_over = True
            return False

        # Switch player
        self.current_player = "O" if self.current_player == "X" else "X"
        return False

    def _check_win(self, row, col):
        """Check if the current move results in a win."""
        player = self.board[row][col]
        directions = [
            [(0, 1), (0, -1)],  # horizontal
            [(1, 0), (-1, 0)],  # vertical
            [(1, 1), (-1, -1)],  # diagonal /
            [(1, -1), (-1, 1)],  # diagonal \
        ]

        for dir_pair in directions:
            count = 1  # Count the piece just placed

            # Check both directions
            for dr, dc in dir_pair:
                r, c = row, col

                # Count consecutive pieces in this direction
                for _ in range(3):  # Need 3 more to get 4 in a row
                    r, c = r + dr, c + dc
                    if (
                        0 <= r < self.rows
                        and 0 <= c < self.cols
                        and self.board[r][c] == player
                    ):
                        count += 1
                    else:
                        break

            if count >= 4:
                return True

        return False

    def get_board(self):
        """Return a copy of the current board state."""
        return [row[:] for row in self.board]

    def is_game_over(self):
        """Return whether the game is over."""
        return self.game_over

    def get_winner(self):
        """Return the winner of the game, or None if there is no winner."""
        return self.winner

    def get_current_player(self):
        """Return the current player."""
        return self.current_player


# Example usage:
def play_game():
    game = Connect4()
    while not game.is_game_over():
        try:
            col = int(
                input(f"Player {game.get_current_player()}, choose a column (0-6): ")
            )
            game.make_move(col)
            # Display board if needed
        except ValueError as e:
            print(f"Error: {e}")

    if game.get_winner():
        print(f"Player {game.get_winner()} wins!")
    else:
        print("It's a draw!")


# This will execute play_game() when the script is run directly
if __name__ == "__main__":
    play_game()
