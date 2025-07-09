import tkinter as tk
from tkinter import messagebox

BOARD_SIZE = 5
NUM_SHIPS = 3

class BattleshipGame:
    def __init__(self, master):
        self.master = master
        master.title("Battleship - Multiplayer GUI")

        self.turn = 0  # 0 for Player 1, 1 for Player 2
        self.phase = "setup"  # setup or play

        self.player_boards = [[["~"] * BOARD_SIZE for _ in range(BOARD_SIZE)] for _ in range(2)]
        self.ship_counts = [0, 0]
        self.ship_buttons = [[[], []] for _ in range(2)]  # For controlling GUI updates
        self.shots_taken = [[[], []] for _ in range(2)]

        self.status = tk.Label(master, text="Player 1: Place your 3 ships")
        self.status.pack()

        self.frame = tk.Frame(master)
        self.frame.pack()

        self.grid_buttons = [[], []]
        for p in range(2):
            board_frame = tk.Frame(self.frame)
            board_frame.grid(row=0, column=p, padx=50)

            tk.Label(board_frame, text=f"Player {p + 1}'s Board").grid(row=0, column=0, columnspan=BOARD_SIZE)

            for i in range(BOARD_SIZE):
                row = []
                for j in range(BOARD_SIZE):
                    btn = tk.Button(board_frame, text="~", width=10, height=5,
                                    command=lambda x=i, y=j, player=p: self.cell_clicked(player, x, y),background= "red")
                    btn.grid(row=i + 1, column=j)
                    row.append(btn)
                self.grid_buttons[p].append(row)

        self.reset_btn = tk.Button(master, text="Reset The Game", command=self.reset_game)
        self.reset_btn.pack(pady=5)

    def cell_clicked(self, player, row, col):
        if self.phase == "setup":
            if player != self.turn:
                messagebox.showinfo("Wait!", f"Player {self.turn + 1}, it's your turn to place ships.")
                return

            if self.player_boards[player][row][col] == "S":
                messagebox.showwarning("Already placed", "You already placed a ship here.")
                return

            self.player_boards[player][row][col] = "S"
            self.grid_buttons[player][row][col].config(text="S", bg="gray")
            self.ship_counts[player] += 1

            if self.ship_counts[player] == NUM_SHIPS:
                if self.turn == 0:
                    self.turn = 1
                    self.status.config(text="Player 2: Place your 3 ships")
                else:
                    self.phase = "play"
                    self.turn = 0
                    self.status.config(text="Player 1's turn to fire")

        elif self.phase == "play":
            target_player = 1 - self.turn
            if player != target_player:
                messagebox.showwarning("Wrong board", f"Player {self.turn + 1}, fire on Player {target_player + 1}'s board.")
                return

            if self.player_boards[player][row][col] in ["X", "O"]:
                messagebox.showinfo("Already tried", "You've already fired here.")
                return

            if self.player_boards[player][row][col] == "S":
                self.grid_buttons[player][row][col].config(text="X", bg="red")
                self.player_boards[player][row][col] = "X"
                self.status.config(text=f"🔥 Hit! Player {self.turn + 1} go again!")
            else:
                self.grid_buttons[player][row][col].config(text="O", bg="blue")
                self.player_boards[player][row][col] = "O"
                self.turn = target_player
                self.status.config(text=f"💨 Miss! Player {self.turn + 1}'s turn")

            if self.check_win(player):
                messagebox.showinfo("🏆 Game Over", f"Player {self.turn + 1} wins!")
                self.phase = "done"
                self.status.config(text="Game Over")

    def check_win(self, player):
        for row in self.player_boards[player]:
            if "S" in row:
                return False
        return True

    def reset_game(self):
        self.turn = 0
        self.phase = "setup"
        self.ship_counts = [0, 0]
        self.status.config(text="Player 1: Place your 3 ships")
        self.player_boards = [[["~"] * BOARD_SIZE for _ in range(BOARD_SIZE)] for _ in range(2)]

        for p in range(2):
            for i in range(BOARD_SIZE):
                for j in range(BOARD_SIZE):
                    self.grid_buttons[p][i][j].config(text="~", bg="SystemButtonFace")


# Run the GUI
if __name__ == "__main__":
    root = tk.Tk()
    game = BattleshipGame(root)
    root.mainloop()
