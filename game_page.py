from tkinter import *

import ai
import game_logic as gl
import menu

# width and height of the window in pixels
width = 900
height = 900
table_exterior_offset_x = 20  # space in pixels between window edge and table edge on X axis
table_exterior_offset_y = 20  # space in pixels between window edge and table edge on Y axis

table_interior_offset_x = 20  # space in pixels between table edge and first or last circle in a row
table_interior_offset_y = 20  # space in pixels between table edge and first or last circle in a column

space_between_circles_x = None  # space between circles on X axis
space_between_circles_y = None  # space between circles on Y axis
minim_space_between_circles_x = 20  # space_between_circles_x must be a minimum of this value, but it can also be a bigger value
minim_space_between_circles_y = 20  # space_between_circles_y must be a minimum of this value, but it can also be a bigger value

clickable = True

background_color = "#323232"  # hex color code for the background
table_color = "#34AFDE"  # hex color code for the table
first_player_tile_color = "#EB2316"  # hex color code for first player's pieces (red)
second_player_tile_color = "#F5EE05"  # hex color code for second player's pieces (yellow)

first_player_unselected_tile_color = "#8F2B24"  # hex color code for first player's pieces position preview on table
second_player_unselected_tile_color = "#94901C"  # hex color code for second player's pieces position preview on table

cursor_position_x = None  # position of the cursor during the game
hovered_column = None  # currently hovered column in table


def initialize_game():
    """
    Resets the game state, initializes table and empty circles and applies first AI move if necessary
    """
    gl.reset_game()
    round_rectangle(table_exterior_offset_x, table_exterior_offset_y, width - table_exterior_offset_x,
                    height - table_exterior_offset_y, 25,
                    fill=table_color)
    initialize_circles()
    if ai.is_ai_playing and ai.is_ai_first_player:
        row, column = ai.make_a_move()
        gl.number_of_played_pieces = gl.number_of_played_pieces + 1
        circle_center_x, circle_center_y = convert_rows_and_columns_to_coordinates(row, column)

        canvas.create_oval(circle_center_x - circle_radius, circle_center_y - circle_radius,
                           circle_center_x + circle_radius, circle_center_y + circle_radius,
                           fill=get_color_for_player_turn())
        gl.table[row][column] = gl.get_current_player_index()

        gl.is_first_player_turn = not gl.is_first_player_turn

    global clickable
    clickable = True


def menu_page():
    """
    changes the game page with the main menu page
    """
    root.destroy()
    menu.main()


def get_column_from_coordinates(x):
    """
    Returns the column at coordinate x if there is one, otherwise returns None
    :param x: the x coordinate on table
    :return: Column index if x coordinate is above a column, None otherwise
    """
    if x < table_exterior_offset_x or x > width - table_exterior_offset_x:
        return None
    elif x > table_exterior_offset_x and x < table_exterior_offset_x + table_interior_offset_x + 2 * circle_radius + space_between_circles_x // 2:
        return 0
    else:
        column = (x - table_exterior_offset_x - table_interior_offset_x + space_between_circles_x // 2) // (
                circle_radius * 2 + space_between_circles_x)
        if column == -1 or column == gl.number_of_columns:
            return None
        else:
            return int(column)


def get_color_for_player_turn():
    """
    Returns the color code for the player at turn
    :return: hex color code for red for the first player and hex color code for yellow for the second player
    """
    if gl.is_first_player_turn:
        return first_player_tile_color
    else:
        return second_player_tile_color


def round_rectangle(x1, y1, x2, y2, radius=25, **kwargs):
    """
    Draws a rectangle with rounded corners of selected radius on screen from the upper left and lower right point coordinates
    :param x1: x coordinate of upper left point
    :param y1: y coordinate of upper left point
    :param x2: x coordinate of lower right point
    :param y2: y coordinate of lower right point
    :param radius: radius for the rounded corners
    :param kwargs: key word arguments to be passed to create_polygon function of canvas
    """
    points = [x1 + radius, y1,
              x1 + radius, y1,
              x2 - radius, y1,
              x2 - radius, y1,
              x2, y1,
              x2, y1 + radius,
              x2, y1 + radius,
              x2, y2 - radius,
              x2, y2 - radius,
              x2, y2,
              x2 - radius, y2,
              x2 - radius, y2,
              x1 + radius, y2,
              x1 + radius, y2,
              x1, y2,
              x1, y2 - radius,
              x1, y2 - radius,
              x1, y1 + radius,
              x1, y1 + radius,
              x1, y1]

    canvas.create_polygon(points, **kwargs, smooth=True)


def get_closest_circle_center_coordinates(x, y):
    """
    Returns the closest coordinates of a circle center on the table for the given coordinates
    :param x: x coordinate
    :param y: y coordinate
    :return: a tuple with coordinates of the center of a circle on the table
    """
    global space_between_circles_x
    global space_between_circles_y
    circle_center_x = table_exterior_offset_x + table_interior_offset_x + (
            (x - table_exterior_offset_x - table_interior_offset_x) //
            (2 * circle_radius + space_between_circles_x) + 1) * (2 * circle_radius + space_between_circles_x) \
                      - space_between_circles_x - circle_radius

    circle_center_y = table_exterior_offset_y + table_interior_offset_y + (
            (y - table_exterior_offset_y - table_interior_offset_y) //
            (2 * circle_radius + space_between_circles_y) + 1) * (2 * circle_radius + space_between_circles_y) \
                      - space_between_circles_y - circle_radius

    return circle_center_x, circle_center_y


def convert_coordinates_to_rows_and_columns(x, y):
    """
    Converts x and y coordinates of a circle center to the row and column in the table of that circle
    :param x: x coordinate of circle center
    :param y: y coordinate of circle center
    :return: a tuple with the row and column of the circle with center at coordinates x and y in the table
    """
    global space_between_circles_x
    global space_between_circles_y
    row = int(abs((table_exterior_offset_y + table_interior_offset_y + circle_radius - y) / (
            circle_radius * 2 + space_between_circles_y)))
    column = int(abs((table_exterior_offset_x + table_interior_offset_x + circle_radius - x) / (
            circle_radius * 2 + space_between_circles_x)))
    return row, column


def convert_rows_and_columns_to_coordinates(row, column):
    """
    Converts row and column of a circle in the table to the coordinates of it's center on that table
    :param row: row that the circle is on
    :param column: column that the circle is on
    :return: a tuple with the x and y coordinates for the circle's center on the screen
    """
    x_coordinate = table_exterior_offset_x + table_interior_offset_x + (
            2 * circle_radius + space_between_circles_x) * column + circle_radius
    y_coordinate = table_exterior_offset_y + table_interior_offset_y + (
            2 * circle_radius + space_between_circles_y) * row + circle_radius
    return x_coordinate, y_coordinate


def draw_line(row1, column1, row2, column2):
    """
    Draws a line connecting 4 pieces of the same color for determining how the game was won
    :param row1: row where the first circle in the configuration of 4 circles is placed
    :param column1: column where the first circle in the configuration of 4 circles is placed
    :param row2: row where the last circle in the configuration of 4 circles is placed
    :param column2: column where the last circle in the configuration of 4 circles is placed
    """
    x1, y1 = convert_rows_and_columns_to_coordinates(row1, column1)
    x2, y2 = convert_rows_and_columns_to_coordinates(row2, column2)
    canvas.create_line(x1, y1, x2, y2, fill="green", width=5)


def initialize_circles():
    """
    Draws all the empty spaces for circles at the start of the game based on the number of rows and columns
    """
    global minim_space_between_circles_x
    global minim_space_between_circles_y
    circle_cell_width = ((width - 2 * table_exterior_offset_x - 2 * table_interior_offset_x) - (
            gl.number_of_columns - 1) * minim_space_between_circles_x) / gl.number_of_columns
    circle_cell_height = ((height - 2 * table_exterior_offset_y - 2 * table_interior_offset_y) - (
            gl.number_of_rows - 1) * minim_space_between_circles_y) / gl.number_of_rows
    global circle_radius
    circle_radius = min(circle_cell_height, circle_cell_width) / 2

    global space_between_circles_x
    global space_between_circles_y
    space_between_circles_x = minim_space_between_circles_x + circle_cell_width - 2 * circle_radius
    space_between_circles_y = minim_space_between_circles_y + circle_cell_height - 2 * circle_radius

    global canvas
    for row in range(0, gl.number_of_rows):
        for column in range(0, gl.number_of_columns):
            circle_center_x = table_exterior_offset_x + table_interior_offset_x + column * (
                    circle_radius * 2 + space_between_circles_x) + circle_radius
            circle_center_y = table_exterior_offset_y + table_interior_offset_y + row * (
                    circle_radius * 2 + space_between_circles_y) + circle_radius
            canvas.create_oval(circle_center_x - circle_radius, circle_center_y - circle_radius,
                               circle_center_x + circle_radius, circle_center_y + circle_radius, fill=background_color,
                               tags="empty_circle")


def mouse_tracking(event):
    """
    Keeps track of cursor position on window.

    Updates the hovered column so that it can display a preview of the position a certain piece is going to land in
    depending on the hovered column
    :param event: tkinter event useful for monitoring the position of the cursor on the X axis
    """
    global cursor_position_x
    global hovered_column
    cursor_position_x = event.x
    column = get_column_from_coordinates(cursor_position_x)

    if column is not None:

        if column != hovered_column:

            if hovered_column is not None:
                row = ai.get_available_row_for_column(gl.table, hovered_column)

                if row is not None:
                    coordinate_of_column, coordinate_of_row = convert_rows_and_columns_to_coordinates(row,
                                                                                                      hovered_column)
                    circle_center_x, circle_center_y = get_closest_circle_center_coordinates(coordinate_of_column,
                                                                                             coordinate_of_row)

                    canvas.create_oval(circle_center_x - circle_radius, circle_center_y - circle_radius,
                                       circle_center_x + circle_radius, circle_center_y + circle_radius,
                                       fill=background_color)

            hovered_column = column

            row = ai.get_available_row_for_column(gl.table, column)
            if row is not None:
                coordinate_of_column, coordinate_of_row = convert_rows_and_columns_to_coordinates(row, column)
                circle_center_x, circle_center_y = get_closest_circle_center_coordinates(coordinate_of_column,
                                                                                         coordinate_of_row)

                if gl.is_first_player_turn:
                    canvas.create_oval(circle_center_x - circle_radius, circle_center_y - circle_radius,
                                       circle_center_x + circle_radius, circle_center_y + circle_radius,
                                       fill=first_player_unselected_tile_color)
                else:
                    canvas.create_oval(circle_center_x - circle_radius, circle_center_y - circle_radius,
                                       circle_center_x + circle_radius, circle_center_y + circle_radius,
                                       fill=second_player_unselected_tile_color)


def canvas_clicked(event):
    """
    Handles the event in which a user clicks on the table to select a move.

    It can draw the selected move on screen and respond with a move generated by the AI if necessary or simply change
    the player's turn in case of a human adversary
    :param event: tkinter event not particularly useful, but required to exist for successfully binding the function to
    the canvas
    """
    global clickable
    global hovered_column

    if clickable:
        row = ai.get_available_row_for_column(gl.table, hovered_column)

        if row is not None:
            gl.number_of_played_pieces = gl.number_of_played_pieces + 1
            column = hovered_column

            coordinate_of_column, coordinate_of_row = convert_rows_and_columns_to_coordinates(
                ai.get_available_row_for_column(gl.table, hovered_column), hovered_column)
            circle_center_x, circle_center_y = get_closest_circle_center_coordinates(coordinate_of_column,
                                                                                     coordinate_of_row)

            canvas.create_oval(circle_center_x - circle_radius, circle_center_y - circle_radius,
                               circle_center_x + circle_radius, circle_center_y + circle_radius,
                               fill=get_color_for_player_turn())

            gl.table[row][column] = gl.get_current_player_index()

            is_move_winner_output = gl.is_move_winner(row, column, gl.table)
            if is_move_winner_output[0]:
                print("Player", gl.get_current_player_index(), "won!")
                draw_line(is_move_winner_output[1][0][0], is_move_winner_output[1][0][1],
                          is_move_winner_output[1][1][0],
                          is_move_winner_output[1][1][1])

                clickable = False
                canvas.after(3000, menu_page)

            elif gl.is_game_in_draw_state():
                clickable = False
                canvas.after(3000, menu_page)

            else:
                gl.is_first_player_turn = not gl.is_first_player_turn
                if ai.is_ai_playing:
                    row, column = ai.make_a_move()
                    gl.number_of_played_pieces = gl.number_of_played_pieces + 1
                    circle_center_x, circle_center_y = convert_rows_and_columns_to_coordinates(row, column)

                    canvas.create_oval(circle_center_x - circle_radius, circle_center_y - circle_radius,
                                       circle_center_x + circle_radius, circle_center_y + circle_radius,
                                       fill=get_color_for_player_turn())
                    gl.table[row][column] = gl.get_current_player_index()

                    is_move_winner_output = gl.is_move_winner(row, column, gl.table)
                    if is_move_winner_output[0]:
                        print("Player", gl.get_current_player_index(), "won!")
                        draw_line(is_move_winner_output[1][0][0], is_move_winner_output[1][0][1],
                                  is_move_winner_output[1][1][0], is_move_winner_output[1][1][1])

                        clickable = False
                        canvas.after(3000, menu_page)

                    elif gl.is_game_in_draw_state():
                        clickable = False
                        canvas.after(3000, menu_page)

                    else:
                        gl.is_first_player_turn = not gl.is_first_player_turn


def main():
    """
    Main starting point for the game page.
    """
    global root
    root = Tk()
    root.title("4 in a row")
    global canvas
    canvas = Canvas(root, width=width, height=height, bg=background_color)

    canvas.bind("<Button-1>", canvas_clicked)
    canvas.pack()
    initialize_game()

    root.bind('<Motion>', mouse_tracking)
    root.mainloop()


if __name__ == '__main__':
    main()
