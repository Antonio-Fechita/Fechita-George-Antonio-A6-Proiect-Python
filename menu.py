from tkinter import *
import game_page as gp
import settings as st


def game_page(ws):
    """
    Changes the menu page with the game page
    :param ws: the current window
    """
    ws.destroy()
    gp.main()


def settings_page(ws):
    """
    Changes the menu page with the settings page
    :param ws: the current window
    """
    ws.destroy()
    st.main()


def quit(ws):
    """
    Quits the application
    :param ws: the current window
    """
    ws.destroy()


def main():
    """
    Main starting point for the menu page
    """
    ws = Tk()
    ws.geometry('300x300')
    ws.title('Main Menu')

    f = ("Times bold", 14)

    Label(
        ws,
        text="Main menu",
        padx=20,
        pady=20,
        font=f
    ).pack()

    Button(
        ws,
        text="Start",
        font=f,
        command=lambda: game_page(ws)
    ).pack(pady=10)

    Button(
        ws,
        text="Settings",
        font=f,
        command=lambda: settings_page(ws)
    ).pack(pady=10)

    Button(
        ws,
        text="Quit",
        font=f,
        command=lambda: quit(ws)
    ).pack(pady=10)

    ws.mainloop()


if __name__ == '__main__':
    main()
