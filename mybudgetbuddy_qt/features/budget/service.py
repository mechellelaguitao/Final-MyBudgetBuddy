import math

# Starting suggestions for a brand-new budget. Users can rename, remove,
# or add as many categories as they want on the Budget Period page.
DEFAULT_CATEGORIES = [
    "Food", "Transportation", "School",
    "Bills", "Personal", "Other"
]


def remaining(budget, total):
    return budget["total"] - total


def status(budget, total):
    left = remaining(budget, total)

    if left < 0:
        return "OVER BUDGET"
    if left == 0:
        return "BUDGET FULLY USED"
    if total >= budget["total"] * 0.8:
        return "WARNING: 80% OF BUDGET USED"

    return "WITHIN BUDGET"


def usage_ratio(spent, limit):
    """Fraction of a limit that has been spent (1.0 = fully used)."""
    if limit > 0:
        return spent / limit

    return 0.0 if spent <= 0 else 1.0


def allocated(category_amounts):
    """Total of all category budgets."""
    return sum(category_amounts.values())


def all_categories(budget, expenses):
    """Budget categories first, then any category only found in expenses."""
    names = list(budget["categories"])

    for expense in expenses:
        if expense["category"] not in names:
            names.append(expense["category"])

    return names


def ensure_categories(budget, expenses):
    """Give every category used by an expense a (zero) budget entry."""
    for expense in expenses:
        if expense["category"] not in budget["categories"]:
            budget["categories"][expense["category"]] = 0


# ----- Helpers for category names and amounts -----

def clean_name(text):
    """Trim a name and collapse repeated spaces: '  Eating   Out ' -> 'Eating Out'."""
    return " ".join(text.split())


def match_name(names, name):
    """Return the existing name that equals `name` ignoring case, or None."""
    key = name.casefold()

    for existing in names:
        if existing.casefold() == key:
            return existing

    return None


def parse_amount(text, allow_zero=False):
    """Turn text such as '1,250.50' into a float, or None if it is invalid."""
    try:
        value = float(text.replace(",", "").replace("₱", "").strip())
    except ValueError:
        return None

    if not math.isfinite(value):
        return None

    if value < 0 or (value == 0 and not allow_zero):
        return None

    return round(value, 2)
