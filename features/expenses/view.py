import tkinter as tk
from tkinter import ttk, messagebox
from .service import CATEGORIES

BURGUNDY = "#800020"
WHITE = "#FFFFFF"
BLACK = "#000000"
BG = "#F5F5F5"


def button(parent, text, command, width=20):
    tk.Button(
        parent,
        text=text,
        command=command,
        bg=WHITE,
        fg=BLACK,
        activebackground=WHITE,
        activeforeground=BLACK,
        width=width
    ).pack(pady=10)


def setup_style():
    style = ttk.Style()

    try:
        style.theme_use("clam")
    except tk.TclError:
        pass

    style.configure(
        "Treeview",
        background=WHITE,
        foreground=BLACK,
        fieldbackground=WHITE
    )

    style.configure(
        "Treeview.Heading",
        background=BURGUNDY,
        foreground=WHITE
    )


def bulk_expense_form(root, save):
    win = tk.Toplevel(root)
    win.title("Add Expenses")
    win.geometry("750x500")
    win.configure(bg=BG)

    tk.Label(
        win,
        text="Add Expenses",
        font=("Arial", 22, "bold"),
        bg=BG,
        fg=BURGUNDY
    ).pack(pady=15)

    tk.Label(
        win,
        text="Enter one or more expenses below.",
        bg=BG,
        fg=BLACK
    ).pack()

    box = tk.Frame(
        win,
        bg=WHITE,
        padx=15,
        pady=15
    )
    box.pack(
        fill="both",
        expand=True,
        padx=20,
        pady=10
    )

    headers = [
        ("Category", 18),
        ("Description", 25),
        ("Amount", 15)
    ]

    for col, (text, width) in enumerate(headers):
        tk.Label(
            box,
            text=text,
            font=("Arial", 11, "bold"),
            bg=WHITE,
            fg=BLACK,
            width=width
        ).grid(
            row=0,
            column=col,
            padx=5,
            pady=5
        )

    entries = {}

    for row, category in enumerate(CATEGORIES, 1):
        tk.Label(
            box,
            text=category,
            bg=WHITE,
            fg=BLACK,
            width=18,
            anchor="w"
        ).grid(
            row=row,
            column=0,
            padx=5,
            pady=5
        )

        desc = tk.Entry(
            box,
            width=25,
            bg=WHITE,
            fg=BLACK,
            insertbackground=BLACK
        )
        desc.grid(
            row=row,
            column=1,
            padx=5,
            pady=5
        )

        amount = tk.Entry(
            box,
            width=15,
            bg=WHITE,
            fg=BLACK,
            insertbackground=BLACK
        )
        amount.grid(
            row=row,
            column=2,
            padx=5,
            pady=5
        )

        entries[category] = (desc, amount)

    def submit():
        data = []

        try:
            for category in CATEGORIES:
                desc, amount = entries[category]

                description = desc.get().strip()
                value = amount.get().strip()

                if not description and not value:
                    continue

                if not description or not value:
                    raise ValueError(
                        f"Please complete the {category} information."
                    )

                value = float(value)

                if value <= 0:
                    raise ValueError(
                        f"Amount for {category} must be greater than zero."
                    )

                data.append(
                    (description, category, value)
                )

            if not data:
                raise ValueError(
                    "Please enter at least one expense."
                )

            save(data)
            win.destroy()

        except ValueError as e:
            messagebox.showwarning(
                "Expense",
                str(e)
            )

    button(
        win,
        "Save All Expenses",
        submit,
        25
    )


def expense_form(root, title, save, expense=None):
    win = tk.Toplevel(root)
    win.title(title)
    win.geometry("400x350")
    win.configure(bg=WHITE)

    tk.Label(
        win,
        text=title,
        font=("Arial", 20, "bold"),
        bg=WHITE,
        fg=BURGUNDY
    ).pack(pady=15)

    def field(text):
        tk.Label(
            win,
            text=text,
            bg=WHITE,
            fg=BLACK
        ).pack()

        e = tk.Entry(
            win,
            width=30,
            bg=WHITE,
            fg=BLACK,
            insertbackground=BLACK
        )
        e.pack(pady=5)

        return e

    description = field("Description")

    tk.Label(
        win,
        text="Category",
        bg=WHITE,
        fg=BLACK
    ).pack()

    category = tk.StringVar(
        value=expense["category"]
        if expense
        else CATEGORIES[0]
    )

    ttk.OptionMenu(
        win,
        category,
        category.get(),
        *CATEGORIES
    ).pack(pady=5)

    amount = field("Amount")

    if expense:
        description.insert(
            0,
            expense["description"]
        )

        amount.insert(
            0,
            expense["amount"]
        )

    def submit():
        try:
            value = float(amount.get())

            if not description.get().strip() or value <= 0:
                raise ValueError

            save(
                description.get().strip(),
                category.get(),
                value
            )

            win.destroy()

        except ValueError:
            messagebox.showwarning(
                "Expense",
                "Please enter valid information."
            )

    button(
        win,
        "Save",
        submit
    )


def expense_list(root, expenses, title, action=None):
    if not expenses:
        messagebox.showinfo(
            "Expenses",
            "No expenses recorded."
        )
        return

    setup_style()

    win = tk.Toplevel(root)
    win.title(title)
    win.geometry("650x450")
    win.configure(bg=WHITE)

    tree = ttk.Treeview(
        win,
        columns=(
            "No",
            "Description",
            "Category",
            "Amount"
        ),
        show="headings"
    )

    for col in (
        "No",
        "Description",
        "Category",
        "Amount"
    ):
        tree.heading(
            col,
            text=col
        )

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

            index = tree.index(
                selected[0]
            )

            win.destroy()
            action(index)

        button(
            win,
            "SELECT",
            select
        )