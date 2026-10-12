def empty_budget():
    return {
        "month": "",
        "total": 0,
        "categories": {}
    }


def create_budget(month, total, categories):
    return {
        "month": month,
        "total": total,
        "categories": categories
    }