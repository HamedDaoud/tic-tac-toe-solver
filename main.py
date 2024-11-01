import tkinter as tk
import tkinter.messagebox as messagebox
from solver import dfs, bfs, ids, ucs

class TicTacToe:
    def __init__(self, root):
        self.root = root
        self.root.title("Tic Tac Toe")
        self.root.configure(bg="#2c2c2c")
        self.board = [[" " for _ in range(3)] for _ in range(3)]
        self.current_algorithm = None
        self.buttons = []

        self.create_widgets()

    def create_widgets(self):
        for row in range(3):
            button_row = []
            for col in range(3):
                button = tk.Button(self.root, text=" ", width=10, height=4, command=lambda r=row, c=col: self.player_move(r, c),
                                   bg="#ffffff", fg="#000000", activebackground="#add8e6", font=("Helvetica", 16, "bold"))
                button.grid(row=row, column=col, sticky="nsew", padx=10, pady=10)
                button_row.append(button)
            self.buttons.append(button_row)

        control_frame = tk.Frame(self.root, bg="#2c2c2c")
        control_frame.grid(row=3, column=0, columnspan=3, pady=(20, 10))

        new_game_button = tk.Button(control_frame, text="New Game", command=self.new_game, 
                                    bg="#ffd700", fg="#000000", activebackground="#ffea70", font=("Helvetica", 14, "bold"))
        new_game_button.pack(side=tk.LEFT, padx=10)

        self.algorithm_buttons = {
            "DFS": tk.Button(control_frame, text="DFS", command=lambda: self.select_algorithm("DFS"), 
                              bg="#ffd700", fg="#000000", activebackground="#ffea70", font=("Helvetica", 12, "bold")),
            "BFS": tk.Button(control_frame, text="BFS", command=lambda: self.select_algorithm("BFS"), 
                              bg="#ffd700", fg="#000000", activebackground="#ffea70", font=("Helvetica", 12, "bold")),
            "IDS": tk.Button(control_frame, text="IDS", command=lambda: self.select_algorithm("IDS"), 
                              bg="#ffd700", fg="#000000", activebackground="#ffea70", font=("Helvetica", 12, "bold")),
            "UCS": tk.Button(control_frame, text="UCS", command=lambda: self.select_algorithm("UCS"), 
                              bg="#ffd700", fg="#000000", activebackground="#ffea70", font=("Helvetica", 12, "bold"))
        }
        for button in self.algorithm_buttons.values():
            button.pack(side=tk.LEFT, padx=5)

        for i in range(3):
            self.root.grid_columnconfigure(i, weight=1)
        for i in range(4):
            self.root.grid_rowconfigure(i, weight=1)

    def new_game(self):
        self.board = [[" " for _ in range(3)] for _ in range(3)]
        self.current_algorithm = None
        for row in self.buttons:
            for button in row:
                button.config(text=" ", state=tk.NORMAL, bg="#ffffff")
        for button in self.algorithm_buttons.values():
            button.config(state=tk.NORMAL, relief=tk.RAISED)

    def select_algorithm(self, algorithm):
        if not self.current_algorithm:
            self.current_algorithm = algorithm
            for name, button in self.algorithm_buttons.items():
                if name == algorithm:
                    button.config(relief=tk.SUNKEN)
                else:
                    button.config(state=tk.DISABLED)

    def player_move(self, row, col):
        if self.board[row][col] == " " and self.current_algorithm:
            self.board[row][col] = "X"
            self.buttons[row][col].config(text="X", state=tk.DISABLED, bg="#add8e6")
            if self.check_win("X"):
                self.end_game("Player wins!")
                return
            self.computer_move()

    def computer_move(self):
        if self.current_algorithm == "DFS":
            move = dfs(self.board)
        elif self.current_algorithm == "BFS":
            move = bfs(self.board)
        elif self.current_algorithm == "IDS":
            move = ids(self.board)
        elif self.current_algorithm == "UCS":
            move = ucs(self.board)
        else:
            return

        if move:
            row, col = move[0]
            self.board[row][col] = "O"
            self.buttons[row][col].config(text="O", state=tk.DISABLED, bg="#ffd700")
            if self.check_win("O"):
                self.end_game("Computer wins!")
            elif self.check_draw():
                self.end_game("It's a draw!")

    def check_win(self, player):
        for row in self.board:
            if all(cell == player for cell in row):
                return True
        for col in range(3):
            if all(self.board[row][col] == player for row in range(3)):
                return True
        if all(self.board[i][i] == player for i in range(3)) or all(self.board[i][2 - i] == player for i in range(3)):
            return True
        return False

    def check_draw(self):
        return all(cell != " " for row in self.board for cell in row)

    def end_game(self, message):
        for row in self.buttons:
            for button in row:
                button.config(state=tk.DISABLED)
        messagebox.showinfo("Game Over", message)

if __name__ == "__main__":
    root = tk.Tk()
    game = TicTacToe(root)
    root.mainloop()