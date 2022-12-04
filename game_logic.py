number_of_rows = 6  # 6
number_of_columns = 7  # 7
is_first_player_turn = True
table = [[0 for j in range(0, number_of_columns)] for i in range(0, number_of_rows)]


def is_move_valid(row, column):
    if table[row][column] != 0:
        return False

    if row == (len(table) - 1) or table[row + 1][column] != 0:
        return True


def reset_game():
    global table
    global is_first_player_turn
    is_first_player_turn = True
    table = [[0 for _ in range(0, number_of_columns)] for _ in range(0, number_of_rows)]


def check_main_diagonal(row, column):
    # main diagonal
    superior_limit = max(max(-3, -row), -column)
    inferior_limit = min(min(3, number_of_rows - row - 1), number_of_columns - column - 1)
    # print("main diagonal: ", superior_limit, inferior_limit)

    if abs(inferior_limit) + abs(superior_limit) + 1 >= 4:
        offset = superior_limit
        if table[row + offset][column + offset] == table[row + offset + 1][column + offset + 1] == \
                table[row + offset + 2][column + offset + 2] == table[row + offset + 3][column + offset + 3]:
            return True
        while offset <= inferior_limit - 4:
            offset += 1
            if table[row + offset][column + offset] == table[row + offset + 1][column + offset + 1] == \
                    table[row + offset + 2][column + offset + 2] == table[row + offset + 3][column + offset + 3]:
                return True


def check_secondary_diagonal(row, column):
    # secondary diagonal
    superior_limit = max(max(-3, -row), -(number_of_columns - column - 1))
    inferior_limit = min(min(3, number_of_rows - row - 1), column)
    # print("secondary diagonal: ", superior_limit, inferior_limit)

    if abs(inferior_limit) + abs(superior_limit) + 1 >= 4:
        offset = superior_limit
        if table[row + offset][column - offset] == table[row + offset + 1][column - offset - 1] == \
                table[row + offset + 2][column - offset - 2] == table[row + offset + 3][column - offset - 3]:
            return True
        while offset <= inferior_limit - 4:
            offset += 1
            if table[row + offset][column - offset] == table[row + offset + 1][column - offset - 1] == \
                    table[row + offset + 2][column - offset - 2] == table[row + offset + 3][column - offset - 3]:
                return True


def check_horizontal_line(row, column):
    left_limit = max(-3, -column)
    right_limit = min(3, number_of_columns - column - 1)
    if abs(left_limit) + abs(right_limit) + 1 >= 4:
        offset = left_limit
        if table[row][column + offset] == table[row][column + offset + 1] == table[row][column + offset + 2] == \
                table[row][column + offset + 3]:
            return True
        while offset <= right_limit - 4:
            offset += 1
            if table[row][column + offset] == table[row][column + offset + 1] == table[row][column + offset + 2] == \
                    table[row][column + offset + 3]:
                return True


def is_move_winner(row, column):
    player_piece = table[row][column]

    # vertical line
    if row + 3 < number_of_rows and player_piece == table[row + 1][column] == table[row + 2][column] == \
            table[row + 3][column]:
        return True

    if check_horizontal_line(row, column):
        return True

    if check_main_diagonal(row, column):
        return True

    if check_secondary_diagonal(row, column):
        return True

    return False