import tkinter as tk
from tkinter import messagebox

from database.database import load_data, save_data
from features.authentication.view import show_login
from features.budget.view import setup_budget
from features.budget.service import remaining, status
from features.expenses.service import (
    CATEGORIES, add_expense, edit_expense,
    delete_expense, total, category_totals
)
from features.expenses.view import expense_form, expense_list


BURGUNDY = "#800020"
BG = "#F5F5F5"
WHITE = "#FFFFFF"
BLACK = "#000000"
RED = "#B42318"


class App:

    def __init__(self, root):
        self.root = root
        self.root.title("MyBudgetBuddy")
        self.root.geometry("1000x700")
        self.users, self.budget, self.expenses = load_data()
        self.login()

    def clear(self):
        for w in self.root.winfo_children():
            w.destroy()

    def login(self):
        show_login(self.root, self.after_login)

    def after_login(self):
        if self.budget["month"]:
            self.dashboard()
        else:
            setup_budget(
                self.root,
                self.set_budget,
                CATEGORIES
            )

    def set_budget(self, budget):
        self.budget = budget
        self.save()
        self.dashboard()

    def save(self):
        save_data(
            self.users,
            self.budget,
            self.expenses
        )

    def dashboard(self):
        self.clear()
        self.root.configure(bg=BG)

        header = tk.Frame(
            self.root,
            bg=BURGUNDY
        )
        header.pack(fill="x")

        tk.Label(
            header,
            text="MyBudgetBuddy",
            font=("Arial", 24, "bold"),
            bg=BURGUNDY,
            fg=WHITE
        ).pack(
            side="left",
            padx=25,
            pady=18
        )

        tk.Button(
            header,
            text="Logout",
            command=self.logout,
            bg=WHITE,
            fg=BURGUNDY,
            activebackground=WHITE,
            activeforeground=BURGUNDY
        ).pack(
            side="right",
            padx=20
        )

        spent = total(self.expenses)
        left = remaining(
            self.budget,
            spent
        )

        tk.Label(
            self.root,
            text=f"{self.budget['month']} Dashboard",
            font=("Arial", 22, "bold"),
            bg=BG,
            fg=BLACK
        ).pack(pady=20)

        cards = tk.Frame(
            self.root,
            bg=BG
        )
        cards.pack()

        for i, (name, value) in enumerate([
            ("Budget", self.budget["total"]),
            ("Expenses", spent),
            ("Remaining", left)
        ]):
            self.card(
                cards,
                name,
                value,
                i
            )

        tk.Label(
            self.root,
            text=status(
                self.budget,
                spent
            ),
            font=("Arial", 14, "bold"),
            bg=BG,
            fg=RED if left < 0 else BURGUNDY
        ).pack(pady=15)

        menu = tk.Frame(
            self.root,
            bg=BG
        )
        menu.pack()

        buttons = [
            ("Add Expense", self.add),
            ("View Expenses", self.view),
            ("Edit Expense", self.edit),
            ("Delete Expense", self.delete),
            ("Expense Categories", self.categories),
            ("Budget Warning", self.warning),
            ("Monthly Summary", self.summary)
        ]

        for i, (text, command) in enumerate(buttons):
            tk.Button(
                menu,
                text=text,
                command=command,
                bg=BURGUNDY,
                fg=BLACK,
                activebackground=BURGUNDY,
                activeforeground=BLACK,
                width=22,
                pady=7
            ).grid(
                row=i // 2,
                column=i % 2,
                padx=6,
                pady=5
            )

    def card(self, parent, title, value, column):
        box = tk.Frame(
            parent,
            bg=WHITE,
            width=200,
            height=90,
            relief="solid",
            bd=1
        )
        box.grid(
            row=0,
            column=column,
            padx=10
        )
        box.pack_propagate(False)

        tk.Label(
            box,
            text=title,
            bg=WHITE,
            fg=BLACK
        ).pack(pady=10)

        tk.Label(
            box,
            text=f"₱{value:,.2f}",
            font=("Arial", 15, "bold"),
            bg=WHITE,
            fg=BURGUNDY
        ).pack()

    def add(self):
        expense_form(
            self.root,
            "Add Expense",
            self.add_save
        )

    def add_save(
        self,
        description,
        category,
        amount
    ):
        add_expense(
            self.expenses,
            description,
            category,
            amount
        )
        self.save()
        self.dashboard()

    def view(self):
        expense_list(
            self.root,
            self.expenses,
            "View Expenses"
        )

    def edit(self):
        expense_list(
            self.root,
            self.expenses,
            "Edit Expense",
            self.edit_selected
        )

    def delete(self):
        expense_list(
            self.root,
            self.expenses,
            "Delete Expense",
            self.delete_selected
        )

    def edit_selected(self, index):
        expense_form(
            self.root,
            "Edit Expense",
            lambda d, c, a:
                self.edit_save(
                    index,
                    d,
                    c,
                    a
                ),
            self.expenses[index]
        )

    def edit_save(
        self,
        index,
        description,
        category,
        amount
    ):
        edit_expense(
            self.expenses,
            index,
            description,
            category,
            amount
        )
        self.save()
        self.dashboard()

    def delete_selected(self, index):
        if messagebox.askyesno(
            "Delete",
            "Delete this expense?"
        ):
            delete_expense(
                self.expenses,
                index
            )
            self.save()
            self.dashboard()

    def categories(self):
        data = category_totals(
            self.expenses
        )

        text = "\n".join(
            f"{c}: ₱{data[c]:,.2f} / "
            f"₱{self.budget['categories'].get(c, 0):,.2f}"
            for c in CATEGORIES
        )

        messagebox.showinfo(
            "Expense Categories",
            text
        )

    def warning(self):
        messagebox.showwarning(
            "Budget Warning",
            status(
                self.budget,
                total(self.expenses)
            )
        )

    def summary(self):
        spent = total(
            self.expenses
        )
        left = remaining(
            self.budget,
            spent
        )
        data = category_totals(
            self.expenses
        )

        text = (
            f"Month: {self.budget['month']}\n"
            f"Budget: ₱{self.budget['total']:,.2f}\n"
            f"Expenses: ₱{spent:,.2f}\n"
            f"Remaining: ₱{left:,.2f}\n\n"
            "Category Summary\n\n"
        )

        text += "\n".join(
            f"{c}: ₱{data[c]:,.2f} / "
            f"₱{self.budget['categories'].get(c, 0):,.2f}"
            for c in CATEGORIES
        )

        win = tk.Toplevel(self.root)
        win.title("Monthly Summary")
        win.geometry("500x450")
        win.configure(bg=WHITE)

        tk.Label(
            win,
            text=text,
            font=("Arial", 12),
            justify="left",
            bg=WHITE,
            fg=BLACK,
            padx=30,
            pady=30
        ).pack(
            fill="both",
            expand=True
        )

    def logout(self):
        if messagebox.askyesno(
            "Logout",
            "Do you want to logout?"
        ):
            self.save()
            self.login()


root = tk.Tk()
App(root)
root.mainloop()

