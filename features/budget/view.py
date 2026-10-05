import tkinter as tk
from tkinter import messagebox
from .model import create_budget

BURGUNDY = "#800020"
BG = "#F5F5F5"
WHITE = "#FFFFFF"
DARK = "#222222"


def setup_budget(root, save, categories):
    for w in root.winfo_children():
        w.destroy()

    root.configure(bg=BG)

    box = tk.Frame(root, bg=WHITE, padx=30, pady=20)
    box.pack(expand=True)

    tk.Label(
        box,
        text="Monthly Budget Setup",
        font=("Arial", 22, "bold"),
        bg=WHITE,
        fg=BURGUNDY
    ).pack(pady=10)

    tk.Label(
        box, text="Month",
        bg=WHITE, fg=DARK
    ).pack()

    month = tk.Entry(box)
    month.pack(pady=5)

    tk.Label(
        box, text="Total Monthly Budget",
        bg=WHITE, fg=DARK
    ).pack()

    total = tk.Entry(box)
    total.pack(pady=5)

    entries = {}

    for category in categories:
        row = tk.Frame(box, bg=WHITE)
        row.pack(pady=2)

        tk.Label(
            row, text=category,
            width=18, anchor="w",
            bg=WHITE, fg=DARK
        ).pack(side="left")

        e = tk.Entry(row, width=15)
        e.pack(side="left")
        entries[category] = e

    def submit():
        try:
            total_amount = float(total.get())

            if not month.get() or total_amount <= 0:
                raise ValueError

            category_amounts = {}

            for category, entry in entries.items():
                amount = float(entry.get() or 0)

                if amount < 0:
                    raise ValueError

                category_amounts[category] = amount

            save(create_budget(
                month.get(),
                total_amount,
                category_amounts
            ))

        except ValueError:
            messagebox.showwarning(
                "Budget",
                "Please enter valid amounts."
            )

    tk.Button(
        box,
        text="Save Budget",
        command=submit,
        bg=BURGUNDY,
        fg=WHITE,
        width=20
    ).pack(pady=15)