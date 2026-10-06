import tkinter as tk
from tkinter import ttk, messagebox
from .model import create_budget

BURGUNDY = "#800020"
WHITE = "#FFFFFF"
BLACK = "#000000"
BG = "#F5F5F5"


def setup_budget(root, save, categories):
    for w in root.winfo_children():
        w.destroy()

    root.configure(bg=BG)

    box = tk.Frame(
        root,
        bg=WHITE,
        padx=30,
        pady=20
    )
    box.pack(expand=True)

    tk.Label(
        box,
        text="Budget Period",
        font=("Arial", 22, "bold"),
        bg=WHITE,
        fg=BURGUNDY
    ).pack(pady=10)

    # Month
    tk.Label(
        box,
        text="Month",
        bg=WHITE,
        fg=BLACK
    ).pack()

    month = tk.StringVar(value="January")

    ttk.Combobox(
        box,
        textvariable=month,
        values=[
            "January", "February", "March",
            "April", "May", "June",
            "July", "August", "September",
            "October", "November", "December"
        ],
        state="readonly",
        width=25
    ).pack(pady=5)

    # Year
    tk.Label(
        box,
        text="Year",
        bg=WHITE,
        fg=BLACK
    ).pack()

    year = tk.Entry(
        box,
        bg=WHITE,
        fg=BLACK,
        insertbackground=BLACK,
        width=28
    )
    year.pack(pady=5)

    # Total budget
    tk.Label(
        box,
        text="Total Monthly Budget",
        bg=WHITE,
        fg=BLACK
    ).pack()

    total = tk.Entry(
        box,
        bg=WHITE,
        fg=BLACK,
        insertbackground=BLACK,
        width=28
    )
    total.pack(pady=5)

    # Category budgets
    entries = {}

    for category in categories:
        row = tk.Frame(
            box,
            bg=WHITE
        )
        row.pack(pady=2)

        tk.Label(
            row,
            text=category,
            width=18,
            anchor="w",
            bg=WHITE,
            fg=BLACK
        ).pack(side="left")

        entries[category] = tk.Entry(
            row,
            width=15,
            bg=WHITE,
            fg=BLACK,
            insertbackground=BLACK
        )
        entries[category].pack(side="left")

    def submit():
        try:
            year_value = year.get().strip()
            total_amount = float(total.get())

            if (
                len(year_value) != 4
                or not year_value.isdigit()
                or total_amount <= 0
            ):
                raise ValueError

            amounts = {}

            for category, entry in entries.items():
                amount = float(entry.get() or 0)

                if amount < 0:
                    raise ValueError

                amounts[category] = amount

            save(
                create_budget(
                    f"{month.get()} {year_value}",
                    total_amount,
                    amounts
                )
            )

        except ValueError:
            messagebox.showwarning(
                "Budget",
                "Please enter a valid year and budget amount."
            )

    tk.Button(
        box,
        text="Save Budget",
        command=submit,
        bg=WHITE,
        fg=BLACK,
        activebackground=WHITE,
        activeforeground=BLACK,
        width=20
    ).pack(pady=10)