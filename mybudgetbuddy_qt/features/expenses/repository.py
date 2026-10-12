def add(expenses, expense):
    expenses.append(expense)


def update(expenses, index, expense):
    expenses[index] = expense


def delete(expenses, index):
    expenses.pop(index)