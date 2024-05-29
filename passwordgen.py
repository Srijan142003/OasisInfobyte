import tkinter as tk
from tkinter import messagebox
import random
import string
import pyperclip

class PasswordGeneratorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Advanced Password Generator")
        
        tk.Label(root, text="Password Length:").grid(row=0, column=0, sticky="w")
        self.length_var = tk.IntVar(value=12)
        tk.Entry(root, textvariable=self.length_var).grid(row=0, column=1, pady=5)
        
        self.include_uppercase = tk.BooleanVar(value=True)
        self.include_lowercase = tk.BooleanVar(value=True)
        self.include_digits = tk.BooleanVar(value=True)
        self.include_symbols = tk.BooleanVar(value=True)
        
        tk.Checkbutton(root, text="Include Uppercase Letters", variable=self.include_uppercase).grid(row=1, column=0, columnspan=2, sticky="w")
        tk.Checkbutton(root, text="Include Lowercase Letters", variable=self.include_lowercase).grid(row=2, column=0, columnspan=2, sticky="w")
        tk.Checkbutton(root, text="Include Digits", variable=self.include_digits).grid(row=3, column=0, columnspan=2, sticky="w")
        tk.Checkbutton(root, text="Include Symbols", variable=self.include_symbols).grid(row=4, column=0, columnspan=2, sticky="w")
        
        tk.Label(root, text="Exclude Characters:").grid(row=5, column=0, sticky="w")
        self.exclude_var = tk.StringVar()
        tk.Entry(root, textvariable=self.exclude_var).grid(row=5, column=1, pady=5)
        
        tk.Button(root, text="Generate Password", command=self.generate_password).grid(row=6, column=0, columnspan=2, pady=10)
        
        self.password_var = tk.StringVar()
        tk.Entry(root, textvariable=self.password_var, state="readonly", width=50).grid(row=7, column=0, columnspan=2, pady=5)
        
        tk.Button(root, text="Copy to Clipboard", command=self.copy_to_clipboard).grid(row=8, column=0, columnspan=2, pady=5)
        
    def generate_password(self):
        length = self.length_var.get()
        exclude_chars = set(self.exclude_var.get())
        
        if length < 1:
            messagebox.showerror("Error", "Password length must be at least 1.")
            return
        
        char_sets = []
        if self.include_uppercase.get():
            char_sets.append(set(string.ascii_uppercase) - exclude_chars)
        if self.include_lowercase.get():
            char_sets.append(set(string.ascii_lowercase) - exclude_chars)
        if self.include_digits.get():
            char_sets.append(set(string.digits) - exclude_chars)
        if self.include_symbols.get():
            char_sets.append(set(string.punctuation) - exclude_chars)
        
        if not char_sets:
            messagebox.showerror("Error", "At least one character set must be selected.")
            return
        
        all_chars = [char for char_set in char_sets for char in char_set]
        
        if len(all_chars) < length:
            messagebox.showerror("Error", "Not enough unique characters to generate the password of the desired length.")
            return
        
        password = ''.join(random.sample(all_chars, length))
        self.password_var.set(password)
        
    def copy_to_clipboard(self):
        password = self.password_var.get()
        if password:
            pyperclip.copy(password)
            messagebox.showinfo("Copied", "Password copied to clipboard.")
        else:
            messagebox.showwarning("Warning", "No password to copy.")

if __name__ == "__main__":
    root = tk.Tk()
    app = PasswordGeneratorApp(root)
    root.mainloop()
