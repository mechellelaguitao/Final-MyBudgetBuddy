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