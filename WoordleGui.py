import tkinter as tk
from tkinter import messagebox
import random

# Sample word list (you can expand it with a full list)
WORD_LIST = ['apple', 'grape', 'brick', 'smile', 'flame', 'field', 'moral', 'blush', 'crane', 'drink', 'tiger', 'glory', 'major']


# Choose a random word
TARGET_WORD = random.choice(WORD_LIST).lower()
# Constants
WORD_LENGTH = 5
MAX_ATTEMPTS = 6
BOX_SIZE = 60

# Colors
COLOR_CORRECT = "#6aaa64"  # Green
COLOR_PRESENT = "#c9b458"  # Yellow
COLOR_ABSENT = "#787c7e"   # Gray
COLOR_EMPTY = "#d3d6da"    # Light gray

class WordleGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Wordle Game - GUI")
        self.master.resizable(False, True)
        self.attempt = 0
        self.entries = [[None]*WORD_LENGTH for _ in range(MAX_ATTEMPTS)]
        self.current_guess = ""

        self.create_grid()
        self.create_keyboard()

    def create_grid(self):
        self.canvas = tk.Canvas(self.master, width=BOX_SIZE*WORD_LENGTH, height=BOX_SIZE*MAX_ATTEMPTS)
        self.canvas.grid(row=0, column=0, columnspan=10, padx=10, pady=10)

        for i in range(MAX_ATTEMPTS):
            for j in range(WORD_LENGTH):
                x1 = j * BOX_SIZE
                y1 = i * BOX_SIZE
                x2 = x1 + BOX_SIZE
                y2 = y1 + BOX_SIZE
                rect = self.canvas.create_rectangle(x1, y1, x2, y2, fill=COLOR_EMPTY, outline="black")
                text = self.canvas.create_text(x1 + BOX_SIZE//2, y1 + BOX_SIZE//2, text="", font=("Helvetica", 20, "bold"))
                self.entries[i][j] = (rect, text)
    
    def create_keyboard(self):
        keys = [
            "QWERTYUIOP",
            "ASDFGHJKL",
            "ZXCVBNM"
        ]
        self.master.bind("<Key>", self.handle_keypress)

        self.keyboard_buttons = {}
        for r, row in enumerate(keys):
            frame = tk.Frame(self.master)
            frame.grid(row=r+1, column=0, columnspan=10)
            for c, char in enumerate(row):
                btn = tk.Button(frame, text=char, width=4, height=2, font=("Helvetica", 12, "bold"),
                                command=lambda ch=char: self.add_letter(ch.lower()))
                btn.grid(row=0, column=c, padx=2, pady=2)
                self.keyboard_buttons[char.lower()] = btn

        # Add Enter and Delete
        control_frame = tk.Frame(self.master)
        control_frame.grid(row=4, column=0, columnspan=10)
        tk.Button(control_frame, text="Enter", width=8, height=2, command=self.check_guess).grid(row=0, column=0, padx=5)
        tk.Button(control_frame, text="Del", width=8, height=2, command=self.delete_letter).grid(row=0, column=1, padx=5)
        self.master.bind('<Return>', lambda event: self.check_guess())
        self.master.bind('<BackSpace>', lambda event: self.delete_letter())
    def handle_keypress(self, event):
        if event.char.isalpha() and len(event.char) == 1:
            self.add_letter(event.char.lower())

    def add_letter(self, letter):
        if len(self.current_guess) < WORD_LENGTH:
            i = len(self.current_guess)
            self.canvas.itemconfig(self.entries[self.attempt][i][1], text=letter.upper())
            self.current_guess += letter

    def delete_letter(self):
        if len(self.current_guess) > 0:
            i = len(self.current_guess) - 1
            self.canvas.itemconfig(self.entries[self.attempt][i][1], text="")
            self.current_guess = self.current_guess[:-1]

    def check_guess(self):
        guess = self.current_guess.lower()
        if len(guess) != WORD_LENGTH:
            messagebox.showinfo("Error", "Not enough letters.")
            return
        
    # this lines could be added if we want to display the user if the choosen word is in our word list or not 
        # if guess not in WORD_LIST:
        #     messagebox.showinfo("Error", "Not a valid word.")
        #     return

        # Evaluate guess
        target = list(TARGET_WORD)
        guess_list = list(guess)
        result = ["absent"] * WORD_LENGTH

        # Check correct position
        for i in range(WORD_LENGTH):
            if guess_list[i] == target[i]:
                result[i] = "correct"
            elif guess_list[i] in target:
                result[i] = "present"
                target[target.index(guess_list[i])] = None

        # Apply colors
        for i in range(WORD_LENGTH):
            btn = self.keyboard_buttons.get(guess_list[i])
            if result[i] == "correct":
                color = COLOR_CORRECT
                btn.config(bg=COLOR_CORRECT)
            elif result[i] == "present":
                color = COLOR_PRESENT
                btn.config(bg=COLOR_PRESENT)
            else:
                color = COLOR_ABSENT
                btn.config(bg=COLOR_ABSENT)

            self.canvas.itemconfig(self.entries[self.attempt][i][0], fill=color)

        # Check win
        if guess == TARGET_WORD:
            messagebox.showinfo("Congratulations!", f"You guessed it!\nWord: {TARGET_WORD.upper()}")
            self.master.destroy()
        else:
            self.attempt += 1
            self.current_guess = ""
            if self.attempt == MAX_ATTEMPTS:
                messagebox.showinfo("Game Over", f"Better luck next time!\nWord was: {TARGET_WORD.upper()}")
                self.master.destroy()


# Run the Game
if __name__ == "__main__":
    root = tk.Tk()
    game = WordleGUI(root)
    root.mainloop()