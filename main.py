import tkinter as tk

from database.database import load_data, save_data
from features.authentication.view import show_login
from features.budget.view import setup_budget
from features.dashboard.view import App


def start(root):
    users, budget, expenses = load_data()

    def save():
        save_data(
            users,
            budget,
            expenses
        )

    def set_budget(new_budget):
        budget.update(new_budget)
        save()

        App(
            root,
            users,
            budget,
            expenses,
            save,
            show_login_page
        )

    def login_success():
        if budget["month"]:
            App(
                root,
                users,
                budget,
                expenses,
                save,
                show_login_page
            )
        else:
            setup_budget(
                root,
                set_budget,
                [
                    "Food",
                    "Transportation",
                    "School",
                    "Bills",
                    "Personal",
                    "Other"
                ]
            )

    def show_login_page():
        show_login(
            root,
            login_success
        )

    show_login_page()


root = tk.Tk()
root.title("MyBudgetBuddy")
root.geometry("1000x700")

start(root)

root.mainloop()