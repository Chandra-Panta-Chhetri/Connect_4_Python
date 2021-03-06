import numpy as np
import pygame
import sys
import math
from typing import List, Tuple

NUM_ROWS = 6
NUM_COLS = 7
PIXEL_SIZE = 90
RADIUS = int(PIXEL_SIZE / 2 - 4)
LIGHT_BLUE = (102, 178, 255)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)


def find_available_row(column: int, board: List[list]) -> int:
    """Return the first available row  (board[row][column] == 0) relative to the bottom. If no row is available
    in the specified column, -1 returned.

    The following assumes the board is 4 by 5. However, works for any sized board.
    >>> board = [[0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 2], [0, 1, 2, 0, 1]]
    >>> find_available_row(4, board)
    1
    >>> board == [[0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 2], [0, 1, 2, 0, 1]]
    True
    >>> board = [[0, 0, 0, 2, 0], [0, 0, 0, 1, 0], [0, 0, 0, 2, 2], [0, 1, 2, 1, 1]]
    >>> find_available_row(3, board)
    -1
    >>> board == [[0, 0, 0, 2, 0], [0, 0, 0, 1, 0], [0, 0, 0, 2, 2], [0, 1, 2, 1, 1]]
    True
    """

    for row in range(len(board) - 1, -1, -1):
        if board[row][column] == 0:
            return row
    return -1


def turn(player: int, board: List[list], x_pos: int) -> Tuple[bool, bool]:
    """Return a tuple consisting of 2 bool values: game_over, row_found, respectively. game_over is
    determined using player, x_pos, and board.

    The following assumes the board is 4 by 5. However, works for any sized board.
    >>> board = [[0, 0, 0, 0, 0], [0, 0, 0, 0, 1], [0, 0, 0, 0, 2], [0, 1, 2, 0, 1]]
    >>> turn(2, board, 406)
    (False, True)
    >>> board == [[0, 0, 0, 0, 2], [0, 0, 0, 0, 1], [0, 0, 0, 0, 2], [0, 1, 2, 0, 1]]
    True
    """

    column = int(math.floor(x_pos / PIXEL_SIZE))
    game_over, row_found = False, False
    if column >= 0 & column <= NUM_COLS - 1:
        empty_row_index = find_available_row(column, board)
        if empty_row_index != -1:
            board[empty_row_index][column] = player
            game_over = check_wins(player, board, empty_row_index, column)
            row_found = True
    return game_over, row_found


def check_horizontal(player: int, row_num: int, board: List[list]) -> bool:
    """Return true if there are 4 consecutive occurrence of player in the row, row_num in board.
    Return false otherwise.

    The following assumes the board is 4 by 5. However, works for any sized board.
    >>> board = [[0, 0, 0, 0, 2], [0, 1, 1, 1, 1], [2, 2, 1, 2, 2], [2, 1, 2, 1, 1]]
    >>> check_horizontal(1, 1, board)
    True
    >>> board == [[0, 0, 0, 0, 2], [0, 1, 1, 1, 1], [2, 2, 1, 2, 2], [2, 1, 2, 1, 1]]
    True
    >>> board = [[0, 0, 0, 0, 2], [0, 0, 2, 0, 1], [0, 2, 1, 2, 2], [1, 1, 2, 1, 1]]
    >>> check_horizontal(2, 2, board)
    False
    >>> board == [[0, 0, 0, 0, 2], [0, 0, 2, 0, 1], [0, 2, 1, 2, 2], [1, 1, 2, 1, 1]]
    True
    """

    num_same = 0  # number of consecutive occurrence of player
    for col in range(0, NUM_COLS):
        if board[row_num][col] == player:
            num_same += 1
        else:
            num_same = 0
        if num_same == 4:
            return True
    return False


def check_vertical(player: int, col_num: int, board: List[list]) -> bool:
    """Return true if there are 4 consecutive occurrence of player in the column, col_num in board.
    Return false otherwise.

    The following assumes the board is 4 by 5. However, works for any sized board.
    >>> board = [[0, 1, 0, 0, 2], [2, 1, 2, 1, 1], [2, 1, 1, 2, 2], [2, 1, 2, 1, 1]]
    >>> check_vertical(1, 1, board)
    True
    >>> board == [[0, 1, 0, 0, 2], [2, 1, 2, 1, 1], [2, 1, 1, 2, 2], [2, 1, 2, 1, 1]]
    True
    >>> board = [[2, 0, 0, 2, 2], [1, 1, 2, 1, 1], [2, 1, 1, 2, 2], [2, 1, 2, 1, 1]]
    >>> check_vertical(2, 0, board)
    False
    >>> board == [[2, 0, 0, 2, 2], [1, 1, 2, 1, 1], [2, 1, 1, 2, 2], [2, 1, 2, 1, 1]]
    True
    """

    num_same = 0  # number of consecutive occurrence of player
    for row in range(0, NUM_ROWS):
        if board[row][col_num] == player:
            num_same += 1
        else:
            num_same = 0
        if num_same == 4:
            return True
    return False


def pos_slope_diagonal(row_index: int, col_index: int) -> Tuple[int, int]:
    """Return a tuple consisting of the start index(row_index, col_index) of the positive sloped diagonal
    relative to the index specified by row_index and col_index.

    The following assumes the board is 4 by 5. However, works for any sized board.
    >>> pos_slope_diagonal(1, 1)
    (2, 0)
    >>> pos_slope_diagonal(2, 2)
    (4, 1)
    """

    while ((col_index >= 1) & (col_index <= NUM_COLS)) & ((row_index >= -1) & (row_index <= NUM_ROWS - 2)):
        col_index -= 1
        row_index += 1
    return row_index, col_index


def neg_slope_diagonal(row_num: int, column_num: int) -> Tuple[int, int]:
    """Return a tuple consisting of the start index(row_index, col_index) of the negative sloped diagonal
    relative to the index specified by row_index and col_index.

    The following assumes the board is 4 by 5. However, works for any sized board.
    >>> neg_slope_diagonal(1, 1)
    (0, 0)
    >>> neg_slope_diagonal(2, 2)
    (0, 0)
    """

    while ((column_num >= 1) & (column_num <= NUM_COLS)) & ((row_num >= 1) & (row_num <= NUM_ROWS)):
        column_num -= 1
        row_num -= 1
    return row_num, column_num


def check_diagonal(player: int, start_row: int, start_col: int, board: List[list], row_increment: int) -> bool:
    """Return true when there are 4 consecutive occurrence of player in the diagonal starting at index specified
    by start_row and start_col. Each index on the diagonal is calculated based on row_increment. Return
    false otherwise.

    The following assumes the board is 4 by 5. However, works for any sized board.
    >>> board = [[1, 0, 1, 2, 2], [1, 0, 2, 1, 1], [2, 2, 1, 2, 2], [2, 1, 2, 1, 1]]
    >>> check_diagonal(2, 3, 0, board, -1)
    True
    >>> board == [[1, 0, 1, 2, 2], [1, 0, 2, 1, 1], [2, 2, 1, 2, 2], [2, 1, 2, 1, 1]]
    True
    >>> board = [[0, 0, 1, 2, 2], [1, 1, 2, 1, 1], [2, 2, 1, 2, 2], [2, 1, 2, 1, 1]]
    >>> check_diagonal(1, 0, 0, board, 1)
    False
    >>> board == [[0, 0, 1, 2, 2], [1, 1, 2, 1, 1], [2, 2, 1, 2, 2], [2, 1, 2, 1, 1]]
    True
    """

    num_same = 0  # number of consecutive occurrence of player
    # Checking every element on the diagonal indicated by start_row and start_col
    while ((start_col >= 0) & (start_col <= NUM_COLS - 1)) & ((start_row >= 0) & (start_row <= NUM_ROWS - 1)):
        if board[start_row][start_col] == player:
            num_same += 1
        else:
            num_same = 0
        if num_same == 4:
            return True
        start_col += 1
        start_row += row_increment
    return False


def win_diagonal(player: int, row_num: int, col_num: int, board: List[list]) -> bool:
    """Return true if there are 4 consecutive occurrence of player in either the positive sloped diagonal or
    negative sloped diagonal relative to row_num and col_num. Return false otherwise.

    The following assumes the board is 4 by 5. However, works for any sized board.
    >>> board = [[0, 0, 1, 2, 2], [1, 1, 2, 1, 1], [2, 2, 1, 2, 2], [2, 1, 2, 1, 1]]
    >>> win_diagonal(2, 2, 1, board)
    True
    >>> board == [[0, 0, 1, 2, 2], [1, 1, 2, 1, 1], [2, 2, 1, 2, 2], [2, 1, 2, 1, 1]]
    True
    >>> board = [[2, 0, 1, 0, 2], [1, 1, 2, 1, 1], [2, 2, 1, 2, 2], [2, 1, 2, 1, 1]]
    >>> win_diagonal(1, 1, 1, board)
    False
    >>> board == [[2, 0, 1, 0, 2], [1, 1, 2, 1, 1], [2, 2, 1, 2, 2], [2, 1, 2, 1, 1]]
    True
    """

    # Finding start index of positive sloped diagonal relative to row_num and column_num
    pos_start_row, pos_start_col = pos_slope_diagonal(row_num, col_num)
    # Finding start index of negative sloped diagonal relative to row_num and column_num
    neg_start_row, neg_start_col = neg_slope_diagonal(row_num, col_num)
    # checking negative sloped diagonal relative to row_num and column_num
    winner = check_diagonal(player, neg_start_row, neg_start_col, board, 1)
    if winner:
        return True
    # checking positive sloped diagonal relative to row_num and column_num
    winner = check_diagonal(player, pos_start_row, pos_start_col, board, -1)
    if winner:
        return True
    return False


def check_wins(player: int, board: int, row_num: int, col_num: int) -> bool:
    """Return true if there are 4 consecutive occurrence of player once player has been placed at
    board[row_num][col_num] in any of the three possible directions: vertically, horizontally or diagonally. Return
    false otherwise.

    The following assumes the board is 4 by 5. However, works for any sized board.
    >>> board = [[0, 0, 1, 2, 2], [1, 1, 2, 1, 1], [2, 2, 1, 2, 2], [2, 1, 2, 1, 1]]
    >>> check_wins(2, board, 0, 3)
    True
    >>> board == [[0, 0, 1, 2, 2], [1, 1, 2, 1, 1], [2, 2, 1, 2, 2], [2, 1, 2, 1, 1]]
    True
    >>> board = [[2, 0, 1, 1, 2], [1, 1, 2, 1, 1], [2, 2, 1, 2, 2], [2, 1, 2, 1, 1]]
    >>> check_wins(1, board, 0, 2)
    False
    >>> board == [[2, 0, 1, 1, 2], [1, 1, 2, 1, 1], [2, 2, 1, 2, 2], [2, 1, 2, 1, 1]]
    True
    """

    return check_horizontal(player, row_num, board) | check_vertical(player, col_num, board) \
           | win_diagonal(player, row_num, col_num, board)


def main(board: List[list], screen: pygame.Surface) -> None:
    """Let users play connect_4 game.
    """

    game_over = False
    total_pieces = 0  # Indicates the number of pieces currently on board
    text_font = pygame.font.SysFont("monospace", 35)
    # Game runs as long as there are no winners and total number of pieces currently on the board is less than
    # the number of pieces board can have
    while (not game_over) & (total_pieces < NUM_ROWS * NUM_COLS):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            # Shows player the column in which they are about to drop their piece
            if event.type == pygame.MOUSEMOTION:
                pygame.draw.rect(screen, LIGHT_BLUE, (0, 0, NUM_COLS * PIXEL_SIZE, PIXEL_SIZE))
                x_pos = event.pos[0]
                # Player 1 plays on every odd total number  of pieces currently on the board + 1
                if (total_pieces + 1) % 2 != 0:
                    pygame.draw.circle(screen, RED, (x_pos, int(PIXEL_SIZE/2)), RADIUS)
                else:
                    pygame.draw.circle(screen, YELLOW, (x_pos, int(PIXEL_SIZE / 2)), RADIUS)
                pygame.display.update()

            # Detects the column the player chooses to drop their piece
            if event.type == pygame.MOUSEBUTTONDOWN:
                # x_pos is location on the x-axis at which player clicks the mouse. Helps determine the column where
                # player wants to drop their piece
                x_pos = event.pos[0]
                if (total_pieces + 1) % 2 != 0:
                    # Places piece at location determined by x_pos
                    game_over, piece_placed = turn(1, board, x_pos)
                    draw_board(screen, board)
                    if game_over:   # Checks if player 1 won
                        winner = 1  # Indicates the player who has won
                        break
                else:
                    game_over, placed = turn(2, board, x_pos)
                    winner = 2
                    draw_board(screen, board)
                # Increments total number of pieces on board only if piece has been successfully placed
                if piece_placed:
                    total_pieces += 1

    # Prints an appropriate message on game window depending on outcome of the game
    if game_over:
        if winner == 1:
            output_text = text_font.render("Player 1 Wins!", 1, WHITE)
        else:
            output_text = text_font.render("Player 2 Wins!", 1, WHITE)
    elif total_pieces == NUM_ROWS * NUM_COLS:
        output_text = text_font.render("Tie!", 1, WHITE)

    pygame.draw.rect(screen, LIGHT_BLUE, (0, 0, NUM_COLS * PIXEL_SIZE, PIXEL_SIZE))
    screen.blit(output_text, (10, 10))
    pygame.display.update()
    pygame.time.wait(3500)

# Used https://github.com/KeithGalli/Connect4-Python for GUI
def draw_board(screen: pygame.Surface, board: List[list]) -> None:
    """Draw connect_4 board onto output window using screen.
    """

    # Draws a light blue colored rectangle with a white circle inside for each row and column onto screen
    # Empty spots on board are represented by white circles
    # Red spots represent player 1's moves. Yellow spots represent player 2's moves
    for col in range(NUM_COLS):
        for row in range(NUM_ROWS):
            pygame.draw.rect(screen, LIGHT_BLUE,
                             (col * PIXEL_SIZE, row * PIXEL_SIZE + PIXEL_SIZE, PIXEL_SIZE, PIXEL_SIZE))
            if board[row][col] == 0:
                pygame.draw.circle(screen, WHITE, (int(col * PIXEL_SIZE + PIXEL_SIZE / 2),
                                                   int(row * PIXEL_SIZE + PIXEL_SIZE + PIXEL_SIZE / 2)), RADIUS)
            elif board[row][col] == 1:
                pygame.draw.circle(screen, RED, (int(col * PIXEL_SIZE + PIXEL_SIZE / 2),
                                                 int(row * PIXEL_SIZE + PIXEL_SIZE + PIXEL_SIZE / 2)), RADIUS)
            else:
                pygame.draw.circle(screen, YELLOW, (int(col * PIXEL_SIZE + PIXEL_SIZE / 2),
                                                    int(row * PIXEL_SIZE + PIXEL_SIZE + PIXEL_SIZE / 2)), RADIUS)
    pygame.display.update()


def initialize_screen(board: List[list]) -> pygame.Surface:
    """Create window to display connect_4 board.
    """

    pygame.init()
    width = NUM_COLS * PIXEL_SIZE
    height = (NUM_ROWS + 1) * PIXEL_SIZE
    screen = pygame.display.set_mode((width, height))
    draw_board(screen, board)
    pygame.display.update()
    return screen


if __name__ == "__main__":
    board = np.zeros((NUM_ROWS, NUM_COLS))
    display = initialize_screen(board)
    main(board, display)