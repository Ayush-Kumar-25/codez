import tkinter as tk
from random import randint

def rock_paper_window(main):
    # Initialize scores
    user_score = 0
    computer_score = 0
    tie_score = 0

    def play(player_choice):
        nonlocal user_score, computer_score, tie_score

        options = ["rock", "paper", "scissor"]
        computer_choice = options[randint(0, 2)]
        computer_label.config(text=f"🤖 Computer chose: {computer_choice.capitalize()}")

        if player_choice == computer_choice:
            result = "😐 It's a TIE!"
            tie_score += 1
        elif player_choice == "rock":
            if computer_choice == "scissor":
                result = "🏆 You Win!"
                user_score += 1
            else:
                result = "💻 Computer Wins"
                computer_score += 1
        elif player_choice == "paper":
            if computer_choice == "rock":
                result = "🏆 You Win!"
                user_score += 1
            else:
                result = "💻 Computer Wins"
                computer_score += 1
        elif player_choice == "scissor":
            if computer_choice == "paper":
                result = "🏆 You Win!"
                user_score += 1
            else:
                result = "💻 Computer Wins"
                computer_score += 1

        result_label.config(text=result)
        update_scores()

    def update_scores():
        score_label.config(text=f"😎 You: {user_score}    💻 Computer: {computer_score}    🤝 Ties: {tie_score}")

    def reset_game():
        nonlocal user_score, computer_score, tie_score
        user_score = computer_score = tie_score = 0
        result_label.config(text="")
        computer_label.config(text="🤖 Computer chose: ")
        update_scores()

    def quit_game():
        root.destroy()

    # Setup Tkinter window
    root = tk.Toplevel(main)
    root.title("🪨📄✂️ Rock Paper Scissors")
    root.geometry("460x480")
    root.configure(bg="#282c34")

    # Title
    title = tk.Label(root, text="Rock 🪨  Paper 📄  Scissor ✂️",
                     font=("Segoe UI", 22, "bold"), bg="#282c34", fg="#61dafb")
    title.pack(pady=20)

    # Instruction label
    instruction = tk.Label(root, text="Make your choice:",
                           font=("Segoe UI", 16), bg="#282c34", fg="#abb2bf")
    instruction.pack(pady=5)

    # Frame for choice buttons
    button_frame = tk.Frame(root, bg="#282c34")
    button_frame.pack(pady=25)

    # Style for big emoji buttons
    def on_enter(e):
        e.widget['background'] = '#61dafb'
        e.widget['foreground'] = '#282c34'

    def on_leave(e):
        e.widget['background'] = '#444c56'
        e.widget['foreground'] = 'white'

    btn_style = {"font": ("Segoe UI Emoji", 36, "bold"), "width": 4, "height": 2,
                 "bg": "#444c56", "fg": "white", "relief": "raised", "bd": 3, "activebackground": "#61dafb"}

    btn_rock = tk.Button(button_frame, text="🪨", command=lambda: play("rock"), **btn_style)
    btn_rock.grid(row=0, column=0, padx=15)
    btn_rock.bind("<Enter>", on_enter)
    btn_rock.bind("<Leave>", on_leave)

    btn_paper = tk.Button(button_frame, text="📄", command=lambda: play("paper"), **btn_style)
    btn_paper.grid(row=0, column=1, padx=15)
    btn_paper.bind("<Enter>", on_enter)
    btn_paper.bind("<Leave>", on_leave)

    btn_scissor = tk.Button(button_frame, text="✂️", command=lambda: play("scissor"), **btn_style)
    btn_scissor.grid(row=0, column=2, padx=15)
    btn_scissor.bind("<Enter>", on_enter)
    btn_scissor.bind("<Leave>", on_leave)

    # Labels for computer choice and result
    computer_label = tk.Label(root, text="🤖 Computer chose: ", font=("Segoe UI", 14), bg="#282c34", fg="#e06c75")
    computer_label.pack(pady=12)

    result_label = tk.Label(root, text="", font=("Segoe UI", 20, "bold"), bg="#282c34", fg="#98c379")
    result_label.pack(pady=8)

    # Score label
    score_label = tk.Label(root, text="😎 You: 0    💻 Computer: 0    🤝 Ties: 0",
                           font=("Segoe UI", 14, "bold"), bg="#282c34", fg="#56b6c2")
    score_label.pack(pady=12)

    # Frame for reset and quit
    control_frame = tk.Frame(root, bg="#282c34")
    control_frame.pack(pady=20)

    reset_btn = tk.Button(control_frame, text="🔄 Restart", command=reset_game,
                          font=("Segoe UI", 14), width=12, bg="#61dafb", fg="#282c34", relief="flat")
    reset_btn.grid(row=0, column=0, padx=20)
    quit_btn = tk.Button(control_frame, text="❌ Quit", command=quit_game,
                         font=("Segoe UI", 14), width=12, bg="#e06c75", fg="white", relief="flat")
    quit_btn.grid(row=0, column=1, padx=20)

    # Center window on screen
    root.update_idletasks()
    width = root.winfo_width()
    height = root.winfo_height()
    x = (root.winfo_screenwidth() // 2) - (width // 2)
    y = (root.winfo_screenheight() // 2) - (height // 2)
    root.geometry(f"{width}x{height}+{x}+{y}")

# Example usage:
if __name__ == "__main__":
    main_win = tk.Tk()
    main_win.withdraw()  # Hide main window
    rock_paper_window(main_win)
    main_win.mainloop()
