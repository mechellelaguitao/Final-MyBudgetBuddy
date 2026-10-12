from .model import create_expense
from .repository import add, update, delete


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
    """Delete one expense. Returns True if it was deleted, False if the
    index does not exist (so a wrong index can never remove another item)."""
    if not 0 <= index < len(expenses):
        return False

    delete(expenses, index)
    return True


def delete_expenses(expenses, indexes):
    """Delete several expenses at once, highest index first.

    Duplicate and out-of-range indexes are ignored.
    Returns how many expenses were actually deleted.
    """
    valid = sorted(
        {i for i in indexes if 0 <= i < len(expenses)},
        reverse=True
    )

    for index in valid:
        delete(expenses, index)

    return len(valid)


def copy_expenses(expenses):
    """Independent copy, so dialogs can be cancelled without side effects."""
    return [dict(expense) for expense in expenses]


def filter_by_category(expenses, category=None):
    """Return (index, expense) pairs, optionally for one category only."""
    return [
        (index, expense)
        for index, expense in enumerate(expenses)
        if not category or expense["category"] == category
    ]


def total(expenses):
    return sum(e["amount"] for e in expenses)


def category_totals(expenses, categories=None):
    """Spent per category. Works with any (dynamic) list of categories and
    also includes categories that only appear in the expenses."""
    names = list(categories or [])

    for expense in expenses:
        if expense["category"] not in names:
            names.append(expense["category"])

    return {
        name: sum(e["amount"] for e in expenses if e["category"] == name)
        for name in names
    }