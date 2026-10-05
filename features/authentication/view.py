import tkinter as tk
from tkinter import messagebox

from .service import login, create_account


BURGUNDY = "#800020"
BG = "#F5F5F5"
WHITE = "#FFFFFF"
DARK = "#000000"


def show_login(root, success):

    root.configure(bg=BG)
    root.title("MyBudgetBuddy")

    def clear():
        for w in root.winfo_children():
            w.destroy()

    def login_page():
        clear()

        box = tk.Frame(
            root,
            bg=WHITE,
            padx=40,
            pady=30
        )
        box.pack(expand=True)

        tk.Label(
            box,
            text="MyBudgetBuddy",
            font=("Arial", 24, "bold"),
            bg=WHITE,
            fg=BURGUNDY
        ).pack(pady=10)

        tk.Label(
            box,
            text="Username",
            bg=WHITE,
            fg=DARK
        ).pack()

        username = tk.Entry(
            box,
            fg=DARK,
            bg=WHITE
        )
        username.pack(pady=5)

        tk.Label(
            box,
            text="Password",
            bg=WHITE,
            fg=DARK
        ).pack()

        password = tk.Entry(
            box,
            show="*",
            fg=DARK,
            bg=WHITE
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

        tk.Button(
            box,
            text="Login",
            command=submit,
            bg=BURGUNDY,
            fg=WHITE,
            width=20
        ).pack(pady=10)

        tk.Button(
            box,
            text="Register",
            command=register_page,
            bg=WHITE,
            fg=BURGUNDY,
            width=20
        ).pack()

    def register_page():
        clear()

        box = tk.Frame(
            root,
            bg=WHITE,
            padx=40,
            pady=30
        )
        box.pack(expand=True)

        tk.Label(
            box,
            text="Create Account",
            font=("Arial", 22, "bold"),
            bg=WHITE,
            fg=BURGUNDY
        ).pack(pady=10)

        entries = []

        for text in (
            "Username",
            "Password",
            "Confirm Password"
        ):
            tk.Label(
                box,
                text=text,
                bg=WHITE,
                fg=DARK
            ).pack()

            entry = tk.Entry(
                box,
                fg=DARK,
                bg=WHITE,
                show="*" if "Password" in text else ""
            )
            entry.pack(pady=5)

            entries.append(entry)

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

        tk.Button(
            box,
            text="Create Account",
            command=submit,
            bg=BURGUNDY,
            fg=WHITE,
            width=20
        ).pack(pady=10)

        tk.Button(
            box,
            text="Back to Login",
            command=login_page,
            bg=WHITE,
            fg=BURGUNDY,
            width=20
        ).pack()

    login_page()





