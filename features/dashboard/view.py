import tkinter as tk
from tkinter import messagebox

from features.budget.service import remaining, status
from features.budget.view import setup_budget
from features.expenses.service import CATEGORIES, add_multiple_expenses, edit_expense, delete_expense, total
from features.expenses.view import bulk_expense_form, expense_form, expense_list

BURGUNDY = "#800020"
WHITE = "#FFFFFF"
BLACK = "#000000"
BG = "#F5F5F5"
RED = "#B42318"


class App:

    def __init__(self, root, users, budget, expenses, save, login):
        self.root = root
        self.users = users
        self.budget = budget
        self.expenses = expenses
        self.save_data = save
        self.login = login
        self.dashboard()

    def clear(self):
        for widget in self.root.winfo_children(): widget.destroy()

    def save(self):
        self.save_data()

    def button(self, parent, text, command, width=20, pady=5):
        return tk.Button(parent, text=text, command=command, bg=WHITE, fg=BLACK,
                         activebackground=WHITE, activeforeground=BLACK,
                         width=width, pady=pady)

    def label(self, parent, text, size=11, color=BLACK):
        tk.Label(parent, text=text, font=("Arial", size, "bold" if size > 15 else "normal"),
                 bg=parent.cget("bg"), fg=color).pack(pady=5)

    def dashboard(self):
        self.clear()
        self.root.configure(bg=BG)

        header = tk.Frame(self.root, bg=BURGUNDY)
        header.pack(fill="x")

        tk.Label(header, text="MyBudgetBuddy", font=("Arial", 24, "bold"),
                 bg=BURGUNDY, fg=WHITE).pack(side="left", padx=25, pady=18)

        self.button(header, "Logout", self.logout).pack(side="right", padx=20)

        spent = total(self.expenses)
        left = remaining(self.budget, spent)

        self.label(self.root, f"{self.budget['month']} Dashboard", 22)

        cards = tk.Frame(self.root, bg=BG)
        cards.pack()

        for i, (name, value) in enumerate([("Budget", self.budget["total"]), ("Expenses", spent), ("Remaining", left)]):
            self.card(cards, name, value, i)

        tk.Label(self.root, text=status(self.budget, spent), font=("Arial", 14, "bold"),
                 bg=BG, fg=RED if left < 0 else BURGUNDY).pack(pady=15)

        menu = tk.Frame(self.root, bg=BG)
        menu.pack()

        buttons = [
            ("Add Expenses", self.add),
            ("View Expenses", self.view),
            ("Edit Expense", self.edit),
            ("Delete Expense", self.delete),
            ("Budget Period", self.set_period),
            ("Monthly Summary", self.summary)
        ]

        for i, (text, command) in enumerate(buttons): self.button(menu, text, command, width=22, pady=7).grid(row=i // 2, column=i % 2, padx=6, pady=5)

    def card(self, parent, title, value, column):
        box = tk.Frame(parent, bg=WHITE, width=200, height=90, relief="solid", bd=1)
        box.grid(row=0, column=column, padx=10)
        box.pack_propagate(False)

        tk.Label(box, text=title, bg=WHITE, fg=BLACK).pack(pady=10)
        tk.Label(box, text=f"₱{value:,.2f}", font=("Arial", 15, "bold"),
                 bg=WHITE, fg=BURGUNDY).pack()

    def add(self):
        bulk_expense_form(self.root, self.add_save)

    def add_save(self, expenses):
        add_multiple_expenses(self.expenses, expenses)
        self.save()
        self.dashboard()

    def view(self):
        expense_list(self.root, self.expenses, "View Expenses")

    def edit(self):
        expense_list(self.root, self.expenses, "Edit Expense", self.edit_selected)

    def edit_selected(self, index):
        expense_form(self.root, "Edit Expense",
                     lambda d, c, a: self.edit_save(index, d, c, a),
                     self.expenses[index])

    def edit_save(self, index, description, category, amount):
        edit_expense(self.expenses, index, description, category, amount)
        self.save()
        self.dashboard()

    def delete(self):
        expense_list(self.root, self.expenses, "Delete Expense", self.delete_selected)

    def delete_selected(self, index):
        if messagebox.askyesno("Delete", "Do you want to delete this expense?"):
            delete_expense(self.expenses, index)
            self.save()
            self.dashboard()

    def set_period(self):
        setup_budget(self.root, self.set_budget, CATEGORIES)

    def set_budget(self, budget):
        self.budget.clear()
        self.budget.update(budget)
        self.save()
        self.dashboard()

    def summary(self):
        spent = total(self.expenses)
        budget = self.budget["total"]
        left = budget - spent

        win = tk.Toplevel(self.root)
        win.title("Monthly Summary")
        win.geometry("600x550")
        win.configure(bg=WHITE)

        tk.Label(win, text="Monthly Summary", font=("Arial", 20, "bold"),
                 bg=WHITE, fg=BURGUNDY).pack(pady=15)

        tk.Label(win, text=f"Month: {self.budget['month']}\n"
                           f"Total Budget: ₱{budget:,.2f}\n"
                           f"Total Expenses: ₱{spent:,.2f}\n"
                           f"Remaining: ₱{left:,.2f}",
                 font=("Arial", 12), bg=WHITE, fg=BLACK).pack(pady=10)

        box = tk.Frame(win, bg=WHITE)
        box.pack(pady=10)

        for col, text in enumerate(["Category", "Budget", "Spent"]):
            tk.Label(box, text=text, font=("Arial", 11, "bold"),
                     bg=WHITE, fg=BLACK, width=18).grid(row=0, column=col, pady=5)

        for row, category in enumerate(CATEGORIES, 1):
            category_budget = self.budget["categories"].get(category, 0)
            category_spent = sum(e["amount"] for e in self.expenses if e["category"] == category)

            for col, value in enumerate([
                category,
                f"₱{category_budget:,.2f}",
                f"₱{category_spent:,.2f}"
            ]):
                tk.Label(box, text=value, bg=WHITE, fg=BLACK,
                         width=18).grid(row=row, column=col, pady=5)

        overall = "Over Budget" if spent > budget else "Within Budget"

        tk.Label(win, text=overall, font=("Arial", 18, "bold"),
                 bg=WHITE, fg=RED if spent > budget else BURGUNDY).pack(pady=20)

    def logout(self):
        if messagebox.askyesno("Logout", "Do you want to logout?"):
            self.save()
            self.login()