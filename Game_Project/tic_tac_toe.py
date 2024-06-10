import tkinter as tk
from tkinter import messagebox

class TicTacToe(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.master.title("Tic Tac Toe")
        self.grid()
        self.create_widgets()
        self.reset_game()
        
    def create_widgets(self):
        # create buttons for each cell in the grid
        self.cells = []
        for i in range(3):
            row = []
            for j in range(3):
                button = tk.Button(self, text=" ", bg="black", fg="white", font=("Helvetica", 24), width=4, height=2,
                                   command=lambda i=i, j=j: self.play_move(i, j))
                button.grid(row=i+1, column=j+1)
                row.append(button)
            self.cells.append(row)
        
        # create reset button
        self.reset_button = tk.Button(self, text="Reset", font=("Helvetica", 16),
                                      command=self.reset_game)
        self.reset_button.grid(row=4, column=2)
        
        # create scoreboard labels
        self.score_label = tk.Label(self, text="Score:", font=("Helvetica", 16))
        self.score_label.grid(row=0, column=0)
        self.player1_label = tk.Label(self, text="Player 1: 0", bg="blue", fg="white", font=("Helvetica", 16))
        self.player1_label.grid(row=1, column=0)
        self.player2_label = tk.Label(self, text="Player 2: 0", bg="blue", fg="white", font=("Helvetica", 16))
        self.player2_label.grid(row=2, column=0)
        
    def reset_game(self):
        # clear the grid and reset the player turn
        self.grid_state = [[' ']*3 for _ in range(3)]
        self.player_turn = 1
        for i in range(3):
            for j in range(3):
                self.cells[i][j].configure(text=" ", state="normal")
        
    def play_move(self, i, j):
        # check if cell is empty and update the grid state
        if self.grid_state[i][j] == ' ':
            if self.player_turn == 1:
                self.cells[i][j].configure(text="X", fg="blue")
                self.grid_state[i][j] = 'X'
                self.player_turn = 2
            else:
                self.cells[i][j].configure(text="O", fg="red")
                self.grid_state[i][j] = 'O'
                self.player_turn = 1
        
        # check if game is won or tied
        if self.check_win():
            self.game_over(True)
        elif self.check_tie():
            self.game_over(False)
            
    def check_win(self):
        # check rows
        for i in range(3):
            if self.grid_state[i][0] == self.grid_state[i][1] == self.grid_state[i][2] != ' ':
                self.update_score(self.grid_state[i][0])
                return True
        # check columns
        for j in range(3):
            if self.grid_state[0][j] == self.grid_state[1][j] == self.grid_state[2][j] != ' ':
                self.update_score(self.grid_state[0][j])
                return True
        # check diagonals
        if self.grid_state[0][0] == self.grid_state[1][1] == self.grid_state[2][2] != ' ':
            self.update_score(self.grid_state[0][0])
            return True
        if self.grid_state[0][2] == self.grid_state[1][1] == self.grid_state[2][0] != ' ':
            self.update_score(self.grid_state[0][2])
            return True
        return False
        
    def check_tie(self):
        for i in range(3):
            for j in range(3):
                if self.grid_state[i][j] == ' ':
                    return False
        return True
    
    def game_over(self, won):
        for i in range(3):
            for j in range(3):
                self.cells[i][j].configure(state="disabled")
        if won:
            winner = "Player 1" if self.player_turn == 2 else "Player 2"
            messagebox.showinfo("Game Over", f"{winner} has won the game!")
        else:
            messagebox.showinfo("Game Over", "The game is tied!")
        
    def update_score(self, player):
        if player == 'X':
            player_label = self.player1_label
        else:
            player_label = self.player2_label
        score = int(player_label.cget("text").split()[-1]) + 1
        player_label.configure(text=f"{player_label.cget('text').split(':')[0]}: {score}")
    
if __name__ == '__main__':
    root = tk.Tk()
    game = TicTacToe(root)
    game.mainloop()
