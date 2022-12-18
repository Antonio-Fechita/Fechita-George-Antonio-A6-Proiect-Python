import game_logic as gl
import game_page as g
import random

is_ai_first_player = False
is_ai_playing = False
infinity = 10000
original_depth = 4
difficulty = 2


def print_table(table):
    for row in table:
        print(row)


def get_available_row_for_column(table, column):
    for row in range(len(table) - 1, -1, -1):
        if table[row][column] == 0:
            return row
    return None


def get_table_with_added_move(table, row, column, maximizing_player):
    new_table = [row[:] for row in table]  # copies the original table in the new table

    if (maximizing_player and is_ai_first_player) or (not maximizing_player and not is_ai_first_player):
        player_piece = 1
    else:
        player_piece = 2

    new_table[row][column] = player_piece

    return new_table


def get_available_moves_from_current_table(table):
    moves_list = []

    if gl.number_of_columns % 2 == 1:
        column = gl.number_of_columns // 2
        row = get_available_row_for_column(table, column)

        if row is not None:
            moves_list.append((row, column))
        for offset in range(1, gl.number_of_columns // 2 + 1):
            column = gl.number_of_columns // 2 + offset
            row = get_available_row_for_column(table, column)

            if row is not None:
                moves_list.append((row, column))

            column = gl.number_of_columns // 2 - offset
            row = get_available_row_for_column(table, column)

            if row is not None:
                moves_list.append((row, column))
    else:
        for offset in range(0, gl.number_of_columns // 2):
            column = gl.number_of_columns // 2 - offset - 1
            row = get_available_row_for_column(table, column)

            if row is not None:
                moves_list.append((row, column))

            column = gl.number_of_columns // 2 + offset
            row = get_available_row_for_column(table, column)

            if row is not None:
                moves_list.append((row, column))

    return moves_list


def is_table_filled(table):
    for row in table:
        if 0 in row:
            return False
    return True


def analyze_selected_pieces(analyzed_pieces):
    if 1 in analyzed_pieces and 2 in analyzed_pieces:
        return 0

    if is_ai_first_player:
        number_of_ai_pieces = analyzed_pieces.count(1)
        number_of_player_pieces = analyzed_pieces.count(2)
    else:
        number_of_ai_pieces = analyzed_pieces.count(2)
        number_of_player_pieces = analyzed_pieces.count(1)

    if number_of_ai_pieces == 4:
        return 10000
    elif number_of_ai_pieces == 3:
        return 500
    elif number_of_ai_pieces == 2:
        return 100
    elif number_of_ai_pieces == 1:
        return 10

    elif number_of_player_pieces == 4:
        return -10000
    elif number_of_player_pieces == 3:
        return -500
    elif number_of_player_pieces == 2:
        return -100
    elif number_of_player_pieces == 1:
        return -10

    return 0


def evaluate_table(table, is_table_in_winning_position, maximizing_player, depth):
    if is_table_in_winning_position:
        if maximizing_player:
            return -10 * infinity
        else:
            return 10 * infinity

    if is_table_filled(table):
        return 0

    score = 0

    #  vertical
    for row in range(0, gl.number_of_rows - 3):
        for column in range(0, gl.number_of_columns):
            analyzed_pieces = [table[row][column], table[row + 1][column], table[row + 2][column],
                               table[row + 3][column]]
            score += analyze_selected_pieces(analyzed_pieces)

    #  horizontal
    for row in range(0, gl.number_of_rows):
        for column in range(0, gl.number_of_columns - 3):
            analyzed_pieces = [table[row][column], table[row][column + 1], table[row][column + 2],
                               table[row][column + 3]]
            score += analyze_selected_pieces(analyzed_pieces)

    #  main diagonal
    for row in range(0, gl.number_of_rows - 3):
        for column in range(0, gl.number_of_columns - 3):
            analyzed_pieces = [table[row][column], table[row + 1][column + 1], table[row + 2][column + 2],
                               table[row + 3][column + 3]]
            score += analyze_selected_pieces(analyzed_pieces)

    #  secondary diagonal
    for row in range(0, gl.number_of_rows - 3):
        for column in range(3, gl.number_of_columns):
            analyzed_pieces = [table[row][column], table[row + 1][column - 1], table[row + 2][column - 2],
                               table[row + 3][column - 3]]
            score += analyze_selected_pieces(analyzed_pieces)

    return score


def scan_for_instant_win(table):
    available_moves = get_available_moves_from_current_table(table)
    for move in available_moves:
        new_table = get_table_with_added_move(table, move[0], move[1], True)
        if gl.is_move_winner(move[0], move[1], new_table)[0]:
            return True, move
    return False, None


def minimax(table, depth, alpha, beta, maximizing_player, last_row, last_column):
    is_table_in_winning_position = gl.is_move_winner(last_row, last_column, table)[0]

    # print(get_available_moves_from_current_table(table))
    if is_table_filled(table) and is_table_in_winning_position == False:
        return 0, None

    best_move = get_available_moves_from_current_table(table)[0]
    if depth == 0 or is_table_in_winning_position:
        output = evaluate_table(table, is_table_in_winning_position, maximizing_player, depth), best_move
        return output

    if maximizing_player:  # AI player

        if depth == original_depth:
            is_winnable_in_one_move = scan_for_instant_win(table)
            if is_winnable_in_one_move[0]:
                return infinity, is_winnable_in_one_move[1]

        max_eval = -infinity

        for move in get_available_moves_from_current_table(table):
            new_table = get_table_with_added_move(table, move[0], move[1], maximizing_player)

            eval = minimax(new_table, depth - 1, alpha, beta, False, move[0], move[1])[0]

            if eval > max_eval:
                max_eval = eval
                best_move = move

            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        return max_eval, best_move

    else:
        min_eval = +infinity
        for move in get_available_moves_from_current_table(table):
            new_table = get_table_with_added_move(table, move[0], move[1], maximizing_player)

            eval = minimax(new_table, depth - 1, alpha, beta, True, move[0], move[1])[0]

            if eval < min_eval:
                min_eval = eval
                best_move = move
            beta = min(beta, eval)
            if beta <= alpha:
                break
        return min_eval, best_move


def pick_random_available_move():
    moves = get_available_moves_from_current_table(gl.table)
    return random.choice(moves)


def make_a_move():
    print(difficulty)
    if difficulty == 0:
        return pick_random_available_move()
    elif difficulty == 1:
        if random.choice([0, 1]) == 0:
            return pick_random_available_move()
    return minimax(gl.table, original_depth, -infinity, +infinity, True, None, None)[1]


def tables_equal(table1, table2):
    for row in range(0, len(table1)):
        for column in range(0, len(table1[0])):
            if table1[row][column] != table2[row][column]:
                return False
    return True


if __name__ == '__main__':
    g.main()
