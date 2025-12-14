import random
import string
import os
from datetime import datetime
import pyperclip
import tkinter as tk
from tkinter import messagebox, simpledialog, scrolledtext
import csv

# Global set to avoid duplicate passwords
generated_passwords = set()

# Load words from file
def load_words(filename="file.txt"):
    wordlist = []
    try:
        with open(filename, "r") as file:
            for line in file:
                for word in line.split():
                    if len(word) > 5:
                        wordlist.append(word.capitalize())
        if not wordlist:
            raise ValueError("Wordlist is empty. Please check your file.")
        return wordlist
    except FileNotFoundError:
        messagebox.showerror("Error", f"{filename} not found.")
        return []
    except Exception as e:
        messagebox.showerror("Error", f"Error loading words: {e}")
        return []

# Generate password
def generate_password(wordlist, length=12, strength="strong"):
    if not wordlist:
        return None

    word = random.choice(wordlist)
    symbols = '!@#$%^&*'
    digits = string.digits
    letters = string.ascii_letters
    password_chars = list(word)

    if strength.lower() == "weak":
        while len(password_chars) < length:
            password_chars.append(random.choice(letters))
    elif strength.lower() == "medium":
        while len(password_chars) < length:
            password_chars.append(random.choice(letters + digits))
    else:  # strong
        while len(password_chars) < length:
            password_chars.append(random.choice(letters + digits + symbols))

    random.shuffle(password_chars)
    password = ''.join(password_chars)

    if password in generated_passwords:
        return generate_password(wordlist, length, strength)
    generated_passwords.add(password)
    return password

# Save password
def save_password(password, filename="generated_passwords.txt"):
    try:
        with open(filename, "a") as file:
            file.write(f"{datetime.now()} - {password}\n")
    except Exception as e:
        messagebox.showerror("Error", f"Error saving password: {e}")

# Save multiple passwords to CSV
def save_passwords_csv(password_list, filename="generated_passwords.csv"):
    try:
        with open(filename, "a", newline='') as csvfile:
            writer = csv.writer(csvfile)
            for pwd in password_list:
                writer.writerow([datetime.now(), pwd])
    except Exception as e:
        messagebox.showerror("Error", f"Error saving to CSV: {e}")

# Password strength checker
def check_strength(password):
    length = len(password)
    has_upper = any(c.isupper() for c in password)
    has_lower = any(c.islower() for c in password)
    has_digit = any(c.isdigit() for c in password)
    has_symbol = any(c in '!@#$%^&*' for c in password)

    score = 0
    if length >= 8: score += 1
    if has_upper: score += 1
    if has_lower: score += 1
    if has_digit: score += 1
    if has_symbol: score += 1

    if score <= 2:
        return "Weak"
    elif score == 3 or score == 4:
        return "Medium"
    else:
        return "Strong"

# GUI Application
class PasswordApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Password Generator")
        self.wordlist = load_words()
        self.create_widgets()

    def create_widgets(self):
        tk.Label(self.master, text="Password Length:").grid(row=0, column=0, padx=5, pady=5)
        self.length_entry = tk.Entry(self.master)
        self.length_entry.insert(0, "12")
        self.length_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(self.master, text="Strength:").grid(row=1, column=0, padx=5, pady=5)
        self.strength_var = tk.StringVar(value="strong")
        tk.OptionMenu(self.master, self.strength_var, "weak", "medium", "strong").grid(row=1, column=1, padx=5, pady=5)

        tk.Label(self.master, text="Number of Passwords:").grid(row=2, column=0, padx=5, pady=5)
        self.count_entry = tk.Entry(self.master)
        self.count_entry.insert(0, "1")
        self.count_entry.grid(row=2, column=1, padx=5, pady=5)

        tk.Button(self.master, text="Generate Password(s)", command=self.generate_button).grid(row=3, column=0, columnspan=2, pady=10)

        self.password_display = scrolledtext.ScrolledText(self.master, width=50, height=10)
        self.password_display.grid(row=4, column=0, columnspan=2, padx=5, pady=5)

        tk.Button(self.master, text="Copy Last Password", command=self.copy_password).grid(row=5, column=0, columnspan=2, pady=5)
        tk.Button(self.master, text="View Saved Passwords", command=self.view_saved).grid(row=6, column=0, columnspan=2, pady=5)

    def generate_button(self):
        try:
            length = int(self.length_entry.get())
        except ValueError:
            messagebox.showwarning("Warning", "Invalid length. Using default 12.")
            length = 12

        try:
            count = int(self.count_entry.get())
            if count < 1:
                count = 1
        except ValueError:
            count = 1

        strength = self.strength_var.get()
        passwords = []

        for _ in range(count):
            pwd = generate_password(self.wordlist, length, strength)
            if pwd:
                passwords.append(pwd)
                save_password(pwd)

        if passwords:
            self.password_display.delete('1.0', tk.END)
            for pwd in passwords:
                self.password_display.insert(tk.END, f"{pwd}  ({check_strength(pwd)})\n")
            pyperclip.copy(passwords[-1])
            save_passwords_csv(passwords)
            messagebox.showinfo("Success", f"{len(passwords)} password(s) generated and last one copied to clipboard!")

    def copy_password(self):
        content = self.password_display.get('1.0', tk.END).strip().split('\n')
        if content:
            last_password = content[-1].split()[0]
            pyperclip.copy(last_password)
            messagebox.showinfo("Copied", "Last password copied to clipboard!")
        else:
            messagebox.showwarning("Warning", "No password to copy!")

    def view_saved(self):
        if os.path.exists("generated_passwords.txt"):
            top = tk.Toplevel(self.master)
            top.title("Saved Passwords")
            text_area = scrolledtext.ScrolledText(top, width=50, height=20)
            text_area.pack(padx=5, pady=5)
            with open("generated_passwords.txt", "r") as file:
                text_area.insert(tk.END, file.read())
            text_area.config(state='disabled')
        else:
            messagebox.showinfo("Info", "No saved passwords found.")

if __name__ == "__main__":
    root = tk.Tk()
    app = PasswordApp(root)
    root.mainloop()
