import tkinter as tk
from tkinter import messagebox
from .service import login, create_account

BURGUNDY = "#800020"
WHITE = "#FFFFFF"
BLACK = "#000000"
BG = "#F5F5F5"


def show_login(root, success):
    root.configure(bg=BG)

    def clear():
        for w in root.winfo_children():
            w.destroy()

    def label(parent, text, size=11, color=BLACK):
        tk.Label(
            parent,
            text=text,
            font=("Arial", size, "bold" if size > 20 else "normal"),
            bg=parent.cget("bg"),
            fg=color
        ).pack(pady=5)

    def button(parent, text, command):
        tk.Button(
            parent,
            text=text,
            command=command,
            width=20,
            bg=WHITE,
            fg=BLACK,
            activebackground=WHITE,
            activeforeground=BLACK
        ).pack(pady=5)

    def login_page():
        clear()

        box = tk.Frame(
            root,
            bg=WHITE,
            padx=40,
            pady=30
        )
        box.pack(expand=True)

        label(box, "MyBudgetBuddy", 24, BURGUNDY)
        label(box, "Username")

        username = tk.Entry(
            box,
            bg=WHITE,
            fg=BLACK,
            insertbackground=BLACK
        )
        username.pack(pady=5)

        label(box, "Password")

        password = tk.Entry(
            box,
            show="*",
            bg=WHITE,
            fg=BLACK,
            insertbackground=BLACK
        )
        password.pack(pady=5)

        def submit():
            if login(username.get(), password.get()):
                success()
            else:
                messagebox.showerror(
                    "Login",
                    "Invalid username or password."
                )

        button(box, "Login", submit)
        button(box, "Register", register_page)

    def register_page():
        clear()

        box = tk.Frame(
            root,
            bg=WHITE,
            padx=40,
            pady=30
        )
        box.pack(expand=True)

        label(box, "Create Account", 22, BURGUNDY)

        entries = []

        for text in (
            "Username",
            "Password",
            "Confirm Password"
        ):
            label(box, text)

            e = tk.Entry(
                box,
                bg=WHITE,
                fg=BLACK,
                insertbackground=BLACK,
                show="*" if "Password" in text else ""
            )
            e.pack(pady=5)
            entries.append(e)

        def submit():
            username, password, confirm = [
                e.get() for e in entries
            ]

            if not username or not password:
                messagebox.showwarning(
                    "Register",
                    "Please complete all fields."
                )

            elif password != confirm:
                messagebox.showwarning(
                    "Register",
                    "Passwords do not match."
                )

            elif create_account(username, password):
                messagebox.showinfo(
                    "Register",
                    "Account created successfully."
                )
                login_page()

            else:
                messagebox.showerror(
                    "Register",
                    "Username already exists."
                )

        button(box, "Create Account", submit)
        button(box, "Back to Login", login_page)

    login_page()
