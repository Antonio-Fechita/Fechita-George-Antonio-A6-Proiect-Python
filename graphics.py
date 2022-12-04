from tkinter import *
import re
import game_logic as gl

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

background_color = "#323232"
table_color = "#34AFDE"
first_player_tile_color = "#EB2316"
second_player_tile_color = "#F5EE05"


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


def clicked(*args):
    x, y = re.findall("x=(\d+) y=(\d+)>", str(args))[0]
    x = int(x)
    y = int(y)
    circle_center_x, circle_center_y = get_closest_circle_center_coordinates(x, y)
    row, column = convert_coordinates_to_rows_and_columns(circle_center_x, circle_center_y)

    if gl.is_move_valid(row, column):
        if gl.is_first_player_turn:
            canvas.create_oval(circle_center_x - circle_radius, circle_center_y - circle_radius,
                               circle_center_x + circle_radius, circle_center_y + circle_radius,
                               fill=first_player_tile_color)
            gl.table[row][column] = 1
        else:
            canvas.create_oval(circle_center_x - circle_radius, circle_center_y - circle_radius,
                               circle_center_x + circle_radius, circle_center_y + circle_radius,
                               fill=second_player_tile_color)
            gl.table[row][column] = 2

        if gl.is_move_winner(row, column):
            if gl.is_first_player_turn:
                print("First player won!")
            else:
                print("Second player won!")
            initialize_circles()
            gl.reset_game()
        gl.is_first_player_turn = not gl.is_first_player_turn
        # print(gl.table)


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
    round_rectangle(table_exterior_offset_x, table_exterior_offset_y, width - table_exterior_offset_x,
                    height - table_exterior_offset_y, 25,
                    fill=table_color)
    initialize_circles()
    root.mainloop()


if __name__ == '__main__':
    main()
