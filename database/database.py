FILE = "monthly_expenses.txt"


def load_data():
    users, expenses = [], []
    budget = {"month": "", "total": 0, "categories": {}}
    section = ""

    try:
        with open(FILE) as f:
            for line in f:
                line = line.strip()

                if line.startswith("["):
                    section = line[1:-1].lower()
                    continue

                if "|" not in line:
                    continue

                x = line.split("|")

                if section == "users" and len(x) == 2:
                    users.append({"username": x[0], "password": x[1]})

                elif section == "budget":
                    if x[0] == "month":
                        budget["month"] = x[1]
                    elif x[0] == "total":
                        budget["total"] = float(x[1])
                    elif x[0] == "category":
                        budget["categories"][x[1]] = float(x[2])

                elif section == "expenses" and len(x) == 3:
                    expenses.append({
                        "description": x[0],
                        "category": x[1],
                        "amount": float(x[2])
                    })

    except FileNotFoundError:
        pass

    if not users:
        users.append({"username": "admin", "password": "admin123"})

    return users, budget, expenses


def save_data(users, budget, expenses):
    with open(FILE, "w") as f:
        f.write("[USERS]\n")

        for u in users:
            f.write(f"{u['username']}|{u['password']}\n")

        f.write("\n[BUDGET]\n")
        f.write(f"month|{budget['month']}\n")
        f.write(f"total|{budget['total']}\n")

        for c, amount in budget["categories"].items():
            f.write(f"category|{c}|{amount}\n")

        f.write("\n[EXPENSES]\n")

        for e in expenses:
            f.write(
                f"{e['description']}|{e['category']}|{e['amount']}\n"
            )