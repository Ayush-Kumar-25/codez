import tkinter as tk
from tkinter import messagebox, Menu
import random

def tic_tac_toe_window(main):
    win = tk.Toplevel(main)
    win.title("Tic Tac Toe - Neon Style")
    win.geometry("400x450")
    win.config(bg="#0D0D1A")

    count = 0
    click = True
    won = False
    game_mode = tk.StringVar(value="Two Player")  # Default mode
    starter = tk.StringVar(value="Human")

    PlayerX = tk.IntVar()
    PlayerO = tk.IntVar()
    PlayerX.set(0)
    PlayerO.set(0)

    playerX_text = tk.StringVar(value=f"Player X: {PlayerX.get()}")
    playerO_text = tk.StringVar(value=f"Player O: {PlayerO.get()}")

    neon_pink = "#FF00FF"
    neon_yellow = "#FFFF00"
    dark_bg = "#0D0D1A"
    grid_line_color = "#FF00FF"

    def disable():
        for b in buttons:
            b.config(state=tk.DISABLED)

    def update_score(symbol):
        if symbol == '✖':
            PlayerX.set(PlayerX.get() + 1)
            playerX_text.set(f"Player X: {PlayerX.get()}")
        elif symbol == '⭕':
            PlayerO.set(PlayerO.get() + 1)
            playerO_text.set(f"Player O: {PlayerO.get()}")

    def check_winner(symbol):
        nonlocal won
        combos = [
            (0, 1, 2), (3, 4, 5), (6, 7, 8),
            (0, 3, 6), (1, 4, 7), (2, 5, 8),
            (0, 4, 8), (2, 4, 6)
        ]
        for i, j, k in combos:
            if buttons[i]["text"] == symbol and buttons[j]["text"] == symbol and buttons[k]["text"] == symbol:
                buttons[i].config(bg="red")
                buttons[j].config(bg="red")
                buttons[k].config(bg="red")
                messagebox.showinfo("Neon Tic Tac Toe", f"{symbol} wins!")
                update_score(symbol)
                disable()
                won = True
                return
        if count == 9 and not won:
            messagebox.showinfo("Neon Tic Tac Toe", "It's a tie!")
            disable()

    def computer_move():
        nonlocal count, click, won
        best_score = float('-inf')
        best_move = None
        board_state = [b["text"] for b in buttons]
        for i in range(9):
            if board_state[i] == "":
                board_state[i] = "⭕"
                score = minimax(board_state, 0, False)
                board_state[i] = ""
                if score > best_score:
                    best_score = score
                    best_move = i

        if best_move is not None:
            buttons[best_move].config(text="⭕", fg=neon_pink)
            count += 1
            check_winner("⭕")
            click = True
    
    def minimax(board, depth, is_maximizing):
        winner = get_winner(board)
        if winner == "⭕":
            return 1
        elif winner == "✖":
            return -1
        elif "" not in board:
            return 0

        if is_maximizing:
            best = float('-inf')
            for i in range(9):
                if board[i] == "":
                    board[i] = "⭕"
                    score = minimax(board, depth + 1, False)
                    board[i] = ""
                    best = max(score, best)
            return best
        else:
            best = float('inf')
            for i in range(9):
                if board[i] == "":
                    board[i] = "✖"
                    score = minimax(board, depth + 1, True)
                    board[i] = ""
                    best = min(score, best)
            return best
    
    def get_winner(board):
        win_combos = [
        (0, 1, 2), (3, 4, 5), (6, 7, 8),
        (0, 3, 6), (1, 4, 7), (2, 5, 8),
        (0, 4, 8), (2, 4, 6)
        ]
        for i, j, k in win_combos:
            if board[i] == board[j] == board[k] != "":
                return board[i]
        return None


    def clicked(b):
        nonlocal count, click
        if b["text"] != "" or won:
            messagebox.showwarning("Invalid", "Box already selected!")
            return

        if click:
            b.config(text="✖", fg=neon_yellow)
            count += 1
            check_winner("✖")
            click = False
            if game_mode.get() == "Computer" and not won and count < 9:
                win.after(300, computer_move)
        else:
            b.config(text="⭕", fg=neon_pink)
            count += 1
            check_winner("⭕")
            click = True

    def reset():
        nonlocal count, click, won, buttons
        count = 0
        won = False
        for b in buttons:
            b.config(text="", bg=dark_bg, fg="white", state=tk.NORMAL)
        if game_mode.get() == "Two Player":
            click = True  # Player X always starts
        else:
                # Set based on who is selected to start
            if starter.get() == "Computer":
                click = False
                win.after(300, computer_move)
            else:
                click = True

    # Score Display
    top = tk.Frame(win, bg=dark_bg)
    top.pack(fill="both")
    tk.Label(top, textvariable=playerX_text, bg=dark_bg, fg=neon_yellow, font=("Arial", 14, "bold")).pack(side="left", expand=True)
    tk.Label(top, textvariable=playerO_text, bg=dark_bg, fg=neon_pink, font=("Arial", 14, "bold")).pack(side="right", expand=True)

    # Game Grid
    board = tk.Frame(win, bg=grid_line_color, padx=2, pady=2)
    board.pack(expand=True, fill="both")
    buttons = []

    for r in range(3):
        for c in range(3):
            b = tk.Button(
                board, text="", font=("Arial", 24, "bold"),
                bg=dark_bg, fg="white", width=5, height=2,
                bd=2, relief="ridge", activebackground="#2B2B40"
            )
            b.config(command=lambda btn=b: clicked(btn))
            b.grid(row=r, column=c, padx=3, pady=3, sticky="nsew")
            buttons.append(b)

    for i in range(3):
        board.grid_rowconfigure(i, weight=1)
        board.grid_columnconfigure(i, weight=1)

    # Menu
    menu = Menu(win)
    opt = Menu(menu, tearoff=0)
    opt.add_command(label="Reset", command=reset)
    opt.add_command(label="Quit", command=win.destroy)
    menu.add_cascade(label="Options", menu=opt)

    mode = Menu(menu, tearoff=0)
    mode.add_radiobutton(label="Two Player", variable=game_mode, value="Two Player", command=reset)
    mode.add_radiobutton(label="Play vs Computer", variable=game_mode, value="Computer", command=reset)
    menu.add_cascade(label="Mode", menu=mode)
    
    start_menu = Menu(menu, tearoff=0)
    start_menu.add_radiobutton(label="Human", variable=starter, value="Human", command=reset)
    start_menu.add_radiobutton(label="Computer", variable=starter, value="Computer", command=reset)
    menu.add_cascade(label="Who Starts", menu=start_menu)
    
    win.config(menu=menu)
