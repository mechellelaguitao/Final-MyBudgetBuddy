from .model import create_expense
from .repository import add, update, delete

CATEGORIES = [
    "Food", "Transportation", "School",
    "Bills", "Personal", "Other"
]


def add_expense(expenses, description, category, amount):
    add(expenses, create_expense(description, category, amount))


def add_multiple_expenses(expenses, expense_list):
    for description, category, amount in expense_list:
        add_expense(expenses, description, category, amount)


def edit_expense(expenses, index, description, category, amount):
    update(
        expenses, index,
        create_expense(description, category, amount)
    )


def delete_expense(expenses, index):
    delete(expenses, index)


def total(expenses):
    return sum(e["amount"] for e in expenses)


def category_totals(expenses):
    return {
        c: sum(e["amount"] for e in expenses if e["category"] == c)
        for c in CATEGORIES
    }