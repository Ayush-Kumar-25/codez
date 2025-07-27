import tkinter as tk
from tic_tac_toe import tic_tac_toe_window
from rock_paper import rock_paper_window

def open_launcher():
    root = tk.Tk()
    root.title("🎮 Game Launcher")
    root.geometry("360x300")
    root.configure(bg="#e6f2ff")  # Light sky blue background

    # Title label
    title = tk.Label(
        root, 
        text="🎮 Choose a Game", 
        font=("Comic Sans MS", 18, "bold"), 
        bg="#e6f2ff", 
        fg="#003366"
    )
    title.pack(pady=20)

    # Button styles
    btn_style = {
        "font": ("Arial", 16, "bold"),
        "width": 30,
        "height": 6,
        "bg": "#4da6ff",
        "fg": "white",
        "relief": "raised",
        "bd": 3,
        "highlightbackground": "#003366",
        "activebackground": "#3399ff",
        "cursor": "hand2"
    }

    # Buttons
    tk.Button(
        root, 
        text="❌ Play Tic Tac Toe", 
        command=lambda: tic_tac_toe_window(root),
        **btn_style
    ).pack(pady=10)

    tk.Button(
        root, 
        text="🪨📄✂️ Rock Paper Scissors", 
        command=lambda: rock_paper_window(root),
        **btn_style
    ).pack(pady=10)

    tk.Button(
        root, 
        text="🚪 Quit", 
        command=root.destroy,
        **btn_style
    ).pack(pady=10)

    root.mainloop()

open_launcher()
