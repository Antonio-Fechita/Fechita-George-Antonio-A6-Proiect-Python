import ai
import graphics as g

number_of_rows = 6  # 6
number_of_columns = 7  # 7
is_first_player_turn = True
table = [[0 for j in range(0, number_of_columns)] for i in range(0, number_of_rows)]


def get_current_player_index():
    if is_first_player_turn:
        return 1
    else:
        return 2


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


def check_main_diagonal(row, column, some_table):
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
    if row is None or column is None:
        return False, None

    player_piece = some_table[row][column]

    # vertical line
    if row + 3 < number_of_rows and player_piece == some_table[row + 1][column] == some_table[row + 2][column] == \
            some_table[row + 3][column]:
        # print("VERTICAL")
        return True, ((row, column), (row + 3, column))

    check_horizontal_line_output = check_horizontal_line(row, column, some_table)
    if check_horizontal_line_output[0]:
        # print("HORIZONTAL")
        return check_horizontal_line_output

    check_main_diagonal_output = check_main_diagonal(row, column, some_table)
    if check_main_diagonal_output[0]:
        # print("MAIN DIAGONAL")
        return check_main_diagonal_output

    check_secondary_diagonal_output = check_secondary_diagonal(row, column, some_table)
    if check_secondary_diagonal_output[0]:
        # print("SECONDARY DIAGONAL")
        return check_secondary_diagonal_output

    return False, None


if __name__ == '__main__':
    g.main()
