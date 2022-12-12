from tkinter import *
import re
import game_logic as gl
import ai
import time

width = 900
height = 900
table_exterior_offset_x = 20
table_exterior_offset_y = 20

table_interior_offset_x = 20
table_interior_offset_y = 20

space_between_circles_x = None
space_between_circles_y = None
minim_space_between_circles_x = 20
minim_space_between_circles_y = 20

circle_clickable = True

background_color = "#323232"
table_color = "#34AFDE"
first_player_tile_color = "#EB2316"  # red
second_player_tile_color = "#F5EE05"  # yellow


def reset():
    gl.reset_game()
    round_rectangle(table_exterior_offset_x, table_exterior_offset_y, width - table_exterior_offset_x,
                    height - table_exterior_offset_y, 25,
                    fill=table_color)
    initialize_circles()
    if ai.is_ai_playing and ai.is_ai_first_player:
        row, column = ai.predict_best_move()
        circle_center_x, circle_center_y = convert_rows_and_columns_to_coordinates(row, column)

        canvas.create_oval(circle_center_x - circle_radius, circle_center_y - circle_radius,
                           circle_center_x + circle_radius, circle_center_y + circle_radius,
                           fill=get_color_for_player_turn())
        gl.table[row][column] = gl.get_current_player_index()

        gl.is_first_player_turn = not gl.is_first_player_turn

    global circle_clickable
    circle_clickable = True
    print("Inside reset:", circle_clickable)


def get_color_for_player_turn():
    if gl.is_first_player_turn:
        return first_player_tile_color
    else:
        return second_player_tile_color


def round_rectangle(x1, y1, x2, y2, radius=25, **kwargs):
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
    global space_between_circles_x
    global space_between_circles_y
    row = int(abs((table_exterior_offset_y + table_interior_offset_y + circle_radius - y) / (
            circle_radius * 2 + space_between_circles_y)))
    column = int(abs((table_exterior_offset_x + table_interior_offset_x + circle_radius - x) / (
            circle_radius * 2 + space_between_circles_x)))
    return row, column


def convert_rows_and_columns_to_coordinates(row, column):
    x_coordinate = table_exterior_offset_x + table_interior_offset_x + (
            2 * circle_radius + space_between_circles_x) * column + circle_radius
    y_coordinate = table_exterior_offset_y + table_interior_offset_y + (
            2 * circle_radius + space_between_circles_y) * row + circle_radius
    return x_coordinate, y_coordinate


def draw_line(row1, column1, row2, column2):
    x1, y1 = convert_rows_and_columns_to_coordinates(row1, column1)
    x2, y2 = convert_rows_and_columns_to_coordinates(row2, column2)
    canvas.create_line(x1, y1, x2, y2, fill="green", width=5)


def clicked(*args):
    global circle_clickable
    if circle_clickable:
        x, y = re.findall("x=(\d+) y=(\d+)>", str(args))[0]
        x = int(x)
        y = int(y)
        circle_center_x, circle_center_y = get_closest_circle_center_coordinates(x, y)
        row, column = convert_coordinates_to_rows_and_columns(circle_center_x, circle_center_y)

        if gl.is_move_valid(row, column):
            canvas.create_oval(circle_center_x - circle_radius, circle_center_y - circle_radius,
                               circle_center_x + circle_radius, circle_center_y + circle_radius,
                               fill=get_color_for_player_turn())
            gl.table[row][column] = gl.get_current_player_index()

            is_move_winner_output = gl.is_move_winner(row, column, gl.table)
            if is_move_winner_output[0]:
                print("Player", gl.get_current_player_index(), "won!")
                draw_line(is_move_winner_output[1][0][0], is_move_winner_output[1][0][1], is_move_winner_output[1][1][0],
                          is_move_winner_output[1][1][1])

                circle_clickable = False
                canvas.after(3000, reset)
            else:
                gl.is_first_player_turn = not gl.is_first_player_turn
                if ai.is_ai_playing:
                    row, column = ai.predict_best_move()
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

                        circle_clickable = False
                        canvas.after(3000, reset)
                    else:
                        gl.is_first_player_turn = not gl.is_first_player_turn
    else:
        print(circle_clickable)

def initialize_circles():
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
    canvas.tag_bind("empty_circle", "<Button-1>", clicked)


def main():
    root = Tk()
    root.title("4 in a row")
    global canvas
    canvas = Canvas(root, width=width, height=height, bg=background_color)
    canvas.pack()
    reset()

    root.mainloop()


if __name__ == '__main__':
    main()
