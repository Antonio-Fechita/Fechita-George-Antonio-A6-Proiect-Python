import game_logic as gl
import game_page as g
import random

is_ai_first_player = False  # if it is False the human player will be the first player
is_ai_playing = False  # if it is false the adversary will be another human player
infinity = 10000
max_depth = 4  # the maximum depth of recursive calls for the minimax algorithm
difficulty = 2  # the difficulty selected for the AI


def get_available_row_for_column(table, column):
    """
    Finds the playable row position for a specific column in a specific table configuration if the column is not already
     filled
    :param table: table to search row position for
    :param column: column in specified table to search row position for
    :return: row index if the column is not filled with pieces, None otherwise
    """
    for row in range(len(table) - 1, -1, -1):
        if table[row][column] == 0:
            return row
    return None


def get_table_with_added_move(table, row, column, maximizing_player):
    """
    Receives a table and returns that table with a new piece added to it at specified row and column
    :param table: table to add piece to
    :param row: row to add piece in
    :param column: column to add piece in
    :param maximizing_player: whether the current playing is the AI or the human
    :return: table with added piece at specified location
    """
    new_table = [row[:] for row in table]  # copies the original table in the new table

    if (maximizing_player and is_ai_first_player) or (not maximizing_player and not is_ai_first_player):
        player_piece = 1
    else:
        player_piece = 2

    new_table[row][column] = player_piece

    return new_table


def get_available_moves_from_current_table(table):
    """
    Computes a list of all the available moves in a specified table sorted by how close their position are to the center
    column(s) as those positions are usually better than others
    :param table: table to look for available moves in
    :return: a list of all the available moves sorted by their distance to the center column(s)
    """
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
    """
    Checks if a specified table has been fully filled
    :param table: table to check if has been filled
    :return: True if the table if filled, False otherwise
    """
    for row in table:
        if 0 in row:
            return False
    return True


def analyze_selected_pieces(analyzed_pieces):
    """
    Gives a score for a combination of 4 consecutive locations in the table.

    The score is higher for more AI pieces in the collection, lower for more player pieces in the collection and 0 if
    both AI pieces and player pieces are found as it becomes impossible for those 4 to became winning positions for
    either player
    :param analyzed_pieces: 4 consecutive locations in the current game table that may contain pieces from either
    players or both
    :return: a score depending on how good or bad those 4 positions are for the AI's chances of winning
    """
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


def evaluate_table(table, is_table_in_winning_position, maximizing_player):
    """
    Gives a score for a specified table based on how it impacts AI's chances of winning the game

    It takes into account every possible combination of 4 consecutive positions on the board and each of those get an
    individual score and the final score is the sum of all scores for the individual sets of 4 consecutive positions
    If the board is already in a finished state like won ar draw a score cam immediately be returned
    :param table: specified table to analyze and compute score for
    :param is_table_in_winning_position: whether the game was won
    :param maximizing_player: whether it is the turn of the AI
    :return: a score based on the AI's chances of winning on the specified table
    """
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
    """
    Checks if there is an available win in one move
    :param table: specified table to search winning move in
    :return: a tuple (True, move) where move is the winning move if there exists one, (False, None) otherwise
    """
    available_moves = get_available_moves_from_current_table(table)
    for move in available_moves:
        new_table = get_table_with_added_move(table, move[0], move[1], True)
        if gl.is_move_winner(move[0], move[1], new_table)[0]:
            return True, move
    return False, None


def minimax(table, depth, alpha, beta, maximizing_player, last_row, last_column):
    """
    Minimax algorithm for determining what could be the best currently available move.

    :param table: specified table to look for the best available move
    :param depth: number of recursive calls left available
    :param alpha: alpha minimax specific parameter for pruning the tree of possibilities and optimizing the algorithm
    :param beta:  beta minimax specific parameter for pruning the tree of possibilities and optimizing the algorithm
    :param maximizing_player: whether it is AI's turn or not
    :param last_row: the row where the last piece was played in before this function call
    :param last_column: the column where the last piece was played in before this function call
    :return: tuple consisting of the best evaluation of explored tables and move required to get from the current table
    to the best evaluated table
    """
    is_table_in_winning_position = gl.is_move_winner(last_row, last_column, table)[0]

    if is_table_filled(table) and is_table_in_winning_position == False:
        return 0, None

    best_move = get_available_moves_from_current_table(table)[0]
    if depth == 0 or is_table_in_winning_position:
        output = evaluate_table(table, is_table_in_winning_position, maximizing_player), best_move
        return output

    if maximizing_player:  # AI player

        if depth == max_depth:
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
    """
    Selects a random available move
    :return: some valid move in the current game
    """
    moves = get_available_moves_from_current_table(gl.table)
    return random.choice(moves)


def make_a_move():
    """
    Makes a move depending on the selected difficulty for the AI.

    If the selected difficulty is easy the AI will always pick a random available valid move
    If the selected difficulty is medium the AI will either pick a random available valid move or pick what it considers
    to be the best available move currently, both with a chance of 1/2
    If the selected difficulty is hard the AI will always pick what it considers to be the best available move currently
    :return:
    """
    print(difficulty)
    if difficulty == 0:
        return pick_random_available_move()
    elif difficulty == 1:
        if random.choice([0, 1]) == 0:
            return pick_random_available_move()
    return minimax(gl.table, max_depth, -infinity, +infinity, True, None, None)[1]



if __name__ == '__main__':
    g.main()
