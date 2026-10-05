import tkinter as tk
from tkinter import ttk, messagebox
from .service import CATEGORIES

BURGUNDY = "#800020"
WHITE = "#FFFFFF"
BLACK = "#000000"


def add_expenses(root, save):
    win = tk.Toplevel(root)
    win.title("Add Expenses")
    win.geometry("450x500")
    win.configure(bg=WHITE)

    tk.Label(
        win, text="Add Expenses",
        font=("Arial", 22, "bold"),
        bg=WHITE, fg=BURGUNDY
    ).pack(pady=20)

    entries = {}

    for category in CATEGORIES:
        row = tk.Frame(win, bg=WHITE)
        row.pack(pady=5)

        tk.Label(
            row, text=category,
            width=20, anchor="w",
            bg=WHITE, fg=BLACK
        ).pack(side="left")

        entry = tk.Entry(
            row, width=15,
            bg=WHITE, fg=BLACK
        )
        entry.pack(side="left")
        entries[category] = entry

    def submit():
        expenses = []

        try:
            for category, entry in entries.items():
                amount = float(entry.get() or 0)

                if amount < 0:
                    raise ValueError

                if amount > 0:
                    expenses.append((category, amount))

            if not expenses:
                raise ValueError

            save(expenses)
            win.destroy()

        except ValueError:
            messagebox.showwarning(
                "Expense",
                "Please enter valid amounts."
            )

    tk.Button(
        win,
        text="Save Expenses",
        command=submit,
        bg=BURGUNDY,
        fg=WHITE,
        activebackground=BURGUNDY,
        activeforeground=WHITE,
        width=20,
        relief="flat",
        bd=0
    ).pack(pady=20)


def expense_form(root, title, save, expense=None):
    win = tk.Toplevel(root)
    win.title(title)
    win.geometry("400x350")
    win.configure(bg=WHITE)

    tk.Label(
        win, text=title,
        font=("Arial", 20, "bold"),
        bg=WHITE, fg=BURGUNDY
    ).pack(pady=15)

    tk.Label(
        win, text="Description",
        bg=WHITE, fg=BLACK
    ).pack()

    description = tk.Entry(
        win, width=30,
        bg=WHITE, fg=BLACK
    )
    description.pack(pady=5)

    tk.Label(
        win, text="Category",
        bg=WHITE, fg=BLACK
    ).pack()

    category = tk.StringVar(
        value=expense["category"] if expense else CATEGORIES[0]
    )

    ttk.OptionMenu(
        win, category, category.get(), *CATEGORIES
    ).pack(pady=5)

    tk.Label(
        win, text="Amount",
        bg=WHITE, fg=BLACK
    ).pack()

    amount = tk.Entry(
        win, width=30,
        bg=WHITE, fg=BLACK
    )
    amount.pack(pady=5)

    if expense:
        description.insert(0, expense["description"])
        amount.insert(0, expense["amount"])

    def submit():
        try:
            value = float(amount.get())

            if not description.get() or value <= 0:
                raise ValueError

            save(
                description.get(),
                category.get(),
                value
            )
            win.destroy()

        except ValueError:
            messagebox.showwarning(
                "Expense",
                "Please enter valid information."
            )

    tk.Button(
        win,
        text="Save",
        command=submit,
        bg=BURGUNDY,
        fg=WHITE,
        activebackground=BURGUNDY,
        activeforeground=WHITE,
        width=20,
        relief="flat",
        bd=0
    ).pack(pady=15)


def expense_list(root, expenses, title, action=None):
    if not expenses:
        messagebox.showinfo(
            "Expenses",
            "No expenses recorded."
        )
        return

    win = tk.Toplevel(root)
    win.title(title)
    win.geometry("650x450")
    win.configure(bg=WHITE)

    tree = ttk.Treeview(
        win,
        columns=("No", "Description", "Category", "Amount"),
        show="headings"
    )

    for col in ("No", "Description", "Category", "Amount"):
        tree.heading(col, text=col)

    for i, e in enumerate(expenses, 1):
        tree.insert(
            "",
            "end",
            values=(
                i,
                e["description"],
                e["category"],
                f"₱{e['amount']:.2f}"
            )
        )

    tree.pack(
        fill="both",
        expand=True,
        padx=15,
        pady=15
    )

    if action:
        def select():
            selected = tree.selection()

            if not selected:
                messagebox.showwarning(
                    "Select",
                    "Please select an expense."
                )
                return

            index = tree.index(selected[0])
            win.destroy()
            action(index)

        tk.Button(
            win,
            text="SELECT",
            command=select,
            bg=BURGUNDY,
            fg=WHITE,
            activebackground=BURGUNDY,
            activeforeground=WHITE,
            width=20,
            relief="flat",
            bd=0
        ).pack(pady=10)
