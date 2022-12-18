import game_page as g

number_of_rows = 6  # 6
number_of_columns = 7  # 7
number_of_played_pieces = 0
is_first_player_turn = True
table = [[0 for j in range(0, number_of_columns)] for i in range(0, number_of_rows)]


def get_current_player_index():
    """
    Gives the index of the current player
    :return: 1 if it is the turn of the first player and 2 if it is the turn of the second player
    """
    if is_first_player_turn:
        return 1
    else:
        return 2


def is_game_in_draw_state():
    """
    Check if the game is in draw state
    :return: True if the game is in draw state, false otherwise
    """
    return number_of_played_pieces == number_of_columns * number_of_rows


def is_move_valid(row, column):
    """
    Checks if a move is valid
    :param row: row to make move in
    :param column: column to make move in
    :return: True if the move is valid, False otherwise
    """
    if table[row][column] != 0:
        return False

    if row == (len(table) - 1) or table[row + 1][column] != 0:
        return True


def reset_game():
    """
    Resets the internal state of the game
    """
    global table
    global is_first_player_turn
    global number_of_played_pieces
    is_first_player_turn = True
    number_of_played_pieces = 0
    table = [[0 for _ in range(0, number_of_columns)] for _ in range(0, number_of_rows)]


def check_main_diagonal(row, column, some_table):
    """
    Checks if a piece placed at specified row and column connects to other consecutive pieces on main diagonal
    :param row: specified row for placed piece
    :param column: specified column for placed piece
    :param some_table: table to check win on main diagonal condition in
    :return: True, and coordinates necessary to draw line on the 4 connected pieces if move results in win,
    False, None otherwise
    """
    # main diagonal
    superior_limit = max(max(-3, -row), -column)
    inferior_limit = min(min(3, number_of_rows - row - 1), number_of_columns - column - 1)

    if abs(inferior_limit) + abs(superior_limit) + 1 >= 4:
        offset = superior_limit
        if some_table[row + offset][column + offset] == some_table[row + offset + 1][column + offset + 1] == \
                some_table[row + offset + 2][column + offset + 2] == some_table[row + offset + 3][column + offset + 3]:
            return True, ((row + offset, column + offset), (row + offset + 3, column + offset + 3))
        while offset <= inferior_limit - 4:
            offset += 1
            if some_table[row + offset][column + offset] == some_table[row + offset + 1][column + offset + 1] == \
                    some_table[row + offset + 2][column + offset + 2] == some_table[row + offset + 3][
                column + offset + 3]:
                return True, ((row + offset, column + offset), (row + offset + 3, column + offset + 3))

    return False, None


def check_secondary_diagonal(row, column, some_table):
    """
    Checks if a piece placed at specified row and column connects to other consecutive pieces on secondary diagonal
    :param row: specified row for placed piece
    :param column: specified column for placed piece
    :param some_table: table to check win on secondary diagonal condition in
    :return: True, and coordinates necessary to draw line on the 4 connected pieces if move results in win,
    False, None otherwise
    """
    # secondary diagonal
    superior_limit = max(max(-3, -row), -(number_of_columns - column - 1))
    inferior_limit = min(min(3, number_of_rows - row - 1), column)

    if abs(inferior_limit) + abs(superior_limit) + 1 >= 4:
        offset = superior_limit
        if some_table[row + offset][column - offset] == some_table[row + offset + 1][column - offset - 1] == \
                some_table[row + offset + 2][column - offset - 2] == some_table[row + offset + 3][column - offset - 3]:
            return True, ((row + offset, column - offset), (row + offset + 3, column - offset - 3))
        while offset <= inferior_limit - 4:
            offset += 1
            if some_table[row + offset][column - offset] == some_table[row + offset + 1][column - offset - 1] == \
                    some_table[row + offset + 2][column - offset - 2] == some_table[row + offset + 3][
                column - offset - 3]:
                return True, ((row + offset, column - offset), (row + offset + 3, column - offset - 3))

    return False, None


def check_horizontal_line(row, column, some_table):
    """
    Checks if a piece placed at specified row and column connects to other consecutive pieces on horizontal line
    :param row: specified row for placed piece
    :param column: specified column for placed piece
    :param some_table: table to check win on horizontal condition in
    :return: True, and coordinates necessary to draw line on the 4 connected pieces if move results in win,
    False, None otherwise
    """
    left_limit = max(-3, -column)
    right_limit = min(3, number_of_columns - column - 1)
    if abs(left_limit) + abs(right_limit) + 1 >= 4:
        offset = left_limit
        if some_table[row][column + offset] == some_table[row][column + offset + 1] == some_table[row][
            column + offset + 2] == \
                some_table[row][column + offset + 3]:
            return True, ((row, column + offset), (row, column + offset + 3))
        while offset <= right_limit - 4:
            offset += 1
            if some_table[row][column + offset] == some_table[row][column + offset + 1] == some_table[row][
                column + offset + 2] == \
                    some_table[row][column + offset + 3]:
                return True, ((row, column + offset), (row, column + offset + 3))

    return False, None


def is_move_winner(row, column, some_table):
    """
    Checks if a piece placed at specified row and column connects to other consecutive pieces on any direction
    :param row: specified row for placed piece
    :param column: specified column for placed piece
    :param some_table: table to check win conditions in
    :return: True, and coordinates necessary to draw line on the 4 connected pieces if move results in win,
    False, None otherwise
    """
    if row is None or column is None:
        return False, None

    player_piece = some_table[row][column]

    # vertical line
    if row + 3 < number_of_rows and player_piece == some_table[row + 1][column] == some_table[row + 2][column] == \
            some_table[row + 3][column]:

        return True, ((row, column), (row + 3, column))

    check_horizontal_line_output = check_horizontal_line(row, column, some_table)
    if check_horizontal_line_output[0]:

        return check_horizontal_line_output

    check_main_diagonal_output = check_main_diagonal(row, column, some_table)
    if check_main_diagonal_output[0]:

        return check_main_diagonal_output

    check_secondary_diagonal_output = check_secondary_diagonal(row, column, some_table)
    if check_secondary_diagonal_output[0]:

        return check_secondary_diagonal_output

    return False, None


if __name__ == '__main__':
    g.main()
