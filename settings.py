from tkinter import *

import ai
import menu
import game_logic as gl


def menu_page(root, row_count_slider, column_count_slider, difficulty):
    gl.number_of_rows = row_count_slider.get()
    gl.number_of_columns = column_count_slider.get()
    ai.difficulty = difficulty.get()
    root.destroy()
    menu.main()


def switch_ai_playing(switch_button, on, off):
    ai.is_ai_playing = not ai.is_ai_playing
    if ai.is_ai_playing:
        switch_button.config(image=on)
    else:
        switch_button.config(image=off)


def switch_ai_first(switch_button, on, off):
    ai.is_ai_first_player = not ai.is_ai_first_player
    if ai.is_ai_first_player:
        switch_button.config(image=on)
    else:
        switch_button.config(image=off)


def main():
    ws = Tk()
    ws.geometry('300x500')
    ws.title('Settings')

    f = ("Times bold", 14)

    Label(
        ws,
        text="Settings",
        padx=20,
        pady=30,
        font=f
    ).pack(expand=True, fill=BOTH)


    Label(
        ws,
        text="Number of rows",
        font=("Times bold", 10)
    ).pack(expand=True, fill=BOTH)
    row_count_slider = Scale(ws, from_=4, to=12, orient=HORIZONTAL)
    row_count_slider.pack(ipadx=80)
    row_count_slider.set(gl.number_of_rows)



    Label(
        ws,
        text="Number of columns",
        font=("Times bold", 10)
    ).pack(expand=True, fill=BOTH)
    column_count_slider = Scale(ws, from_=4, to=12, orient=HORIZONTAL)
    column_count_slider.set(gl.number_of_columns)
    column_count_slider.pack(ipadx=80)

    Label(
        ws,
        text="A.I. Difficulty",
        font=("Times bold", 10)
    ).pack(expand=True, fill=BOTH)
    difficulty = IntVar()
    difficulty.set(ai.difficulty)

    Radiobutton(ws,
                text="Easy",
                padx=20,
                variable=difficulty,
                value=0).pack()

    Radiobutton(ws,
                text="Medium",
                padx=20,
                variable=difficulty,
                value=1).pack()

    Radiobutton(ws,
                text="Hard",
                padx=20,
                variable=difficulty,
                value=2).pack()

    on = PhotoImage(file="images/on.png")
    off = PhotoImage(file="images/off.png")

    if ai.is_ai_playing:
        switch_button_ai_playing = Button(ws, image=on, bd=0,
                                          command=lambda: switch_ai_playing(switch_button_ai_playing, on, off))
    else:
        switch_button_ai_playing = Button(ws, image=off, bd=0,
                                          command=lambda: switch_ai_playing(switch_button_ai_playing, on, off))

    Label(
        ws,
        text="Playing against A.I.",
        font=("Times bold", 10)
    ).pack(expand=True, fill=BOTH)
    switch_button_ai_playing.pack()

    if ai.is_ai_first_player:
        switch_button_ai_first = Button(ws, image=on, bd=0,
                                        command=lambda: switch_ai_first(switch_button_ai_first, on, off))
    else:
        switch_button_ai_first = Button(ws, image=off, bd=0,
                                        command=lambda: switch_ai_first(switch_button_ai_first, on, off))

    Label(
        ws,
        text="A.I. goes first",
        font=("Times bold", 10)
    ).pack(expand=True, fill=BOTH)
    switch_button_ai_first.pack()

    Button(
        ws,
        text="Back",
        font=f,
        command=lambda: menu_page(ws, row_count_slider, column_count_slider, difficulty)
    ).pack(fill=X, expand=TRUE, side=LEFT)

    ws.mainloop()


if __name__ == '__main__':
    main()
