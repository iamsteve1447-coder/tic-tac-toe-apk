from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivy.uix.spinner import Spinner
from kivy.uix.label import Label
from kivy.core.window import Window
from kivy.uix.anchorlayout import AnchorLayout

import random

# ---------- THEMES ----------

THEMES = {
    "Default": (0.95, 0.95, 0.95, 1),
    "Dark": (0.1, 0.1, 0.1, 1),
    "Light": (1, 1, 1, 1),
    "Red": (0.5, 0.1, 0.1, 1),
    "Dark Green": (0.1, 0.3, 0.1, 1),
    "Dark Blue": (0.1, 0.1, 0.4, 1),
    "Dark Purple": (0.2, 0.1, 0.3, 1),
    "Gold": (0.6, 0.5, 0.1, 1),
}

# ---------- AI ----------

def check_winner(board):
    wins = [
        (0,1,2),(3,4,5),(6,7,8),
        (0,3,6),(1,4,7),(2,5,8),
        (0,4,8),(2,4,6)
    ]

    for a,b,c in wins:
        if board[a] == board[b] == board[c] != "":
            return board[a]

    if "" not in board:
        return "Draw"

    return None


def random_ai(board):
    empty = [i for i in range(9) if board[i] == ""]
    return random.choice(empty)


def smart_ai(board):
    # simple smart
    for i in range(9):
        if board[i] == "":
            board[i] = "O"
            if check_winner(board) == "O":
                board[i] = ""
                return i
            board[i] = ""

    for i in range(9):
        if board[i] == "":
            board[i] = "X"
            if check_winner(board) == "X":
                board[i] = ""
                return i
            board[i] = ""

    return random_ai(board)


def minimax(board, is_max):
    result = check_winner(board)

    if result == "O":
        return 1
    elif result == "X":
        return -1
    elif result == "Draw":
        return 0

    if is_max:
        best = -999
        for i in range(9):
            if board[i] == "":
                board[i] = "O"
                score = minimax(board, False)
                board[i] = ""
                best = max(best, score)
        return best

    else:
        best = 999
        for i in range(9):
            if board[i] == "":
                board[i] = "X"
                score = minimax(board, True)
                board[i] = ""
                best = min(best, score)
        return best


def pro_ai(board):
    best_score = -999
    move = None

    for i in range(9):
        if board[i] == "":
            board[i] = "O"
            score = minimax(board, False)
            board[i] = ""

            if score > best_score:
                best_score = score
                move = i

    return move


# ---------- GAME ----------

class TicTacToe(GridLayout):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.cols = 1

        self.mode = "Self"
        self.difficulty = "Dumb"

        self.board = [""] * 9

        # TOP BAR

        top = BoxLayout(size_hint=(1, 0.1))

        gear = Button(
            text="⚙",
            font_size=28,
            size_hint=(0.2, 1)
        )

        gear.bind(on_press=self.open_settings)

        top.add_widget(gear)

        self.add_widget(top)

        # GRID

        self.grid = GridLayout(cols=3)

        self.buttons = []

        for i in range(9):
            btn = Button(
                text="",
                font_size=40
            )

            btn.bind(on_press=self.on_press)

            self.buttons.append(btn)
            self.grid.add_widget(btn)

        self.add_widget(self.grid)

    # ---------- SETTINGS ----------

    def open_settings(self, instance):

        layout = BoxLayout(
            orientation="vertical",
            spacing=10,
            padding=10
        )

        # MODE

        mode_spinner = Spinner(
            text=self.mode,
            values=["Self", "Bot"]
        )

        layout.add_widget(Label(text="Mode"))
        layout.add_widget(mode_spinner)

        # DIFFICULTY

        diff_spinner = Spinner(
            text=self.difficulty,
            values=["Dumb", "Smart", "Pro"]
        )

        layout.add_widget(Label(text="Difficulty"))
        layout.add_widget(diff_spinner)

        # THEME

        theme_spinner = Spinner(
            text="Default",
            values=list(THEMES.keys())
        )

        layout.add_widget(Label(text="Theme"))
        layout.add_widget(theme_spinner)

        save_btn = Button(
            text="Save",
            size_hint=(1, 0.3)
        )

        layout.add_widget(save_btn)

        popup = Popup(
            title="Settings",
            content=layout,
            size_hint=(0.8, 0.8)
        )

        def save_settings(instance):

            self.mode = mode_spinner.text
            self.difficulty = diff_spinner.text

            Window.clearcolor = THEMES[
                theme_spinner.text
            ]

            popup.dismiss()

        save_btn.bind(on_press=save_settings)

        popup.open()

    # ---------- GAME ----------

    def on_press(self, btn):

        index = self.buttons.index(btn)

        if self.board[index] != "":
            return

        btn.text = "X"
        self.board[index] = "X"

        winner = check_winner(self.board)

        if winner:
            self.show_result(winner)
            return

        if self.mode == "Bot":
            self.bot_move()

    def bot_move(self):

        if self.difficulty == "Dumb":
            move = random_ai(self.board)

        elif self.difficulty == "Smart":
            move = smart_ai(self.board)

        else:
            move = pro_ai(self.board)

        self.buttons[move].text = "O"
        self.board[move] = "O"

        winner = check_winner(self.board)

        if winner:
            self.show_result(winner)

    def show_result(self, result):

        text = result

        layout = BoxLayout(
            orientation="vertical"
        )

        layout.add_widget(
            Label(text=text)
        )

        btn = Button(text="Restart")

        layout.add_widget(btn)

        popup = Popup(
            title="Game Over",
            content=layout,
            size_hint=(0.6, 0.6)
        )

        def restart(instance):

            self.board = [""] * 9

            for b in self.buttons:
                b.text = ""

            popup.dismiss()

        btn.bind(on_press=restart)

        popup.open()


class TicTacToeApp(App):

    def build(self):

        Window.clearcolor = THEMES["Default"]

        return TicTacToe()


if __name__ == "__main__":
    TicTacToeApp().run()