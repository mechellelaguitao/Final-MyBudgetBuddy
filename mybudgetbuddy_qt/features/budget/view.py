
from datetime import date
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QComboBox, QMessageBox, QFrame, QScrollArea, QGraphicsDropShadowEffect
from PyQt6.QtGui import QColor
from PyQt6.QtCore import Qt, QTimer
from .model import create_budget, empty_budget
from .service import DEFAULT_CATEGORIES, allocated, clean_name, match_name, parse_amount

BURGUNDY = "#900020"
DARK_BURGUNDY = "#700018"
GOLD = "#C9A227"
CREAM = "#FFF9EC"
BG = "#F5F5F5"
WHITE = "#FFFFFF"
BLACK = "#000000"
RED = "#B42318"
GREEN = "#2E7D32"
GRAY = "#6B6B6B"
LIGHT = "#EEEEEE"
LINE = "#D8D0BE"
FONT = "'Georgia'"
MONTHS = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]


def add_shadow(widget, blur=18, offset=4):
    effect = QGraphicsDropShadowEffect()
    effect.setBlurRadius(blur)
    effect.setOffset(0, offset)
    effect.setColor(QColor(0, 0, 0, 60))
    widget.setGraphicsEffect(effect)


def button_style(kind="primary"):
    colors = {"primary": (BURGUNDY, WHITE, BURGUNDY, DARK_BURGUNDY), "secondary": (WHITE, BLACK, BLACK, LIGHT), "danger": (RED, WHITE, RED, "#8F1B12"), "gold": (GOLD, BLACK, GOLD, "#B08D1E")}
    bg, fg, border, hover = colors[kind]
    return f"""
        QPushButton {{ background:{bg}; color:{fg}; border:2px solid {border}; border-radius:8px; font-family:{FONT}; font-size:15px; font-weight:bold; padding:6px 14px; }}
        QPushButton:hover {{ background:{hover}; color:{fg}; }}
        QPushButton:disabled {{ background:#E4E0D6; color:#9A9A9A; border:2px solid #CFC9BA; }}
    """


def input_style(size=15):
    return f"""
        QLineEdit {{ background:{WHITE}; color:{BLACK}; border:2px solid #B9B2A3; border-radius:6px; padding:4px 8px; font-family:{FONT}; font-size:{size}px; }}
        QLineEdit:focus {{ border:2px solid {BURGUNDY}; }}
        QLineEdit:read-only {{ background:#F1ECE1; color:#444444; }}
    """


def combo_style():
    return f"""
        QComboBox {{ background:{WHITE}; color:{BLACK}; border:2px solid #B9B2A3; border-radius:6px; padding:4px 8px; font-family:{FONT}; font-size:15px; }}
        QComboBox:focus {{ border:2px solid {BURGUNDY}; }}
        QComboBox QAbstractItemView {{ background:{WHITE}; color:{BLACK}; selection-background-color:{BURGUNDY}; selection-color:{WHITE}; }}
    """


def scrollbar_style():
    return f"""
        QScrollBar:vertical {{ background:#EFE8D8; width:12px; border-radius:6px; margin:0; }}
        QScrollBar::handle:vertical {{ background:{BURGUNDY}; border-radius:6px; min-height:30px; }}
        QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{ height:0; }}
    """


def scroll_style(background=CREAM, border=True):
    frame = f"1px solid {LINE}" if border else "none"
    return f"""
        QScrollArea {{ border:{frame}; border-radius:8px; background:{background}; }}
        QWidget#holder {{ background:{background}; }}
        {scrollbar_style()}
    """


class CategoryRow(QFrame):
    """One editable category: name, budget amount and a remove button."""

    def __init__(self, name="", amount="", locked_name=False, removable=True, on_change=None, on_remove=None):
        super().__init__()
        self.on_change, self.on_remove = on_change, on_remove
        self.setObjectName("categoryRow")
        self.setStyleSheet(f"QFrame#categoryRow {{ background:{WHITE}; border:1px solid {LINE}; border-radius:8px; }}")

        layout = QHBoxLayout(self)
        layout.setContentsMargins(10, 6, 10, 6)
        layout.setSpacing(10)

        self.name = QLineEdit(name)
        self.name.setPlaceholderText("Category name")
        self.name.setFixedHeight(36)
        self.name.setStyleSheet(input_style())
        self.name.setReadOnly(locked_name)
        self.name.textChanged.connect(self.notify)
        layout.addWidget(self.name, 1)

        self.amount = QLineEdit(amount)
        self.amount.setPlaceholderText("Amount (₱)")
        self.amount.setFixedSize(160, 36)
        self.amount.setStyleSheet(input_style())
        self.amount.textChanged.connect(self.notify)
        layout.addWidget(self.amount)

        self.remove_button = QPushButton("✕")
        self.remove_button.setFixedSize(36, 36)
        self.remove_button.setStyleSheet(button_style("danger"))
        self.remove_button.clicked.connect(self.remove)
        self.remove_button.setEnabled(removable)
        if not removable:
            self.remove_button.setToolTip("This category has expenses, so it can't be removed.")
        layout.addWidget(self.remove_button)

    def notify(self, *_):
        if self.on_change:
            self.on_change()

    def remove(self):
        if self.on_remove:
            self.on_remove(self)


def column(label_text, widget):
    box = QVBoxLayout()
    box.setSpacing(4)
    label = QLabel(label_text)
    label.setStyleSheet(f"color:{BLACK};font-size:15px;font-weight:bold;background:transparent;border:none;")
    box.addWidget(label)
    box.addWidget(widget)
    return box


def setup_budget(root, save, cancel, budget=None, used_categories=()):
    """Show the Budget Period page."""
    budget = budget or empty_budget()
    used = set(used_categories)

    page = QWidget()
    page.setObjectName("page")
    page.setStyleSheet(f"QWidget#page {{ background:{BG}; }}")
    layout = QVBoxLayout(page)
    layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

    box = QFrame()
    box.setObjectName("card")
    box.setFixedSize(760, 650)
    box.setStyleSheet(f"QFrame#card {{ background:{WHITE}; border:2px solid {BURGUNDY}; border-radius:14px; }}")
    add_shadow(box)

    form = QVBoxLayout(box)
    form.setContentsMargins(35, 22, 35, 22)
    form.setSpacing(10)

    title = QLabel("💰 Budget Period")
    title.setAlignment(Qt.AlignmentFlag.AlignCenter)
    title.setStyleSheet(f"color:{BURGUNDY};font-family:{FONT};font-size:30px;font-weight:bold;background:transparent;border:none;")
    form.addWidget(title)

    subtitle = QLabel("Set your monthly budget, then split it into your own categories.")
    subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
    subtitle.setStyleSheet(f"color:{GRAY};font-size:14px;background:transparent;border:none;")
    form.addWidget(subtitle)

    today = date.today()
    month_name, _, year_text = budget["month"].partition(" ")

    month = QComboBox()
    month.addItems(MONTHS)
    month.setFixedHeight(38)
    month.setStyleSheet(combo_style())
    month.setCurrentIndex(MONTHS.index(month_name) if month_name in MONTHS else today.month - 1)

    year = QLineEdit(year_text.strip() or str(today.year))
    year.setFixedHeight(38)
    year.setPlaceholderText("Enter year")
    year.setStyleSheet(input_style())

    total = QLineEdit(f"{budget['total']:.2f}" if budget["total"] else "")
    total.setFixedHeight(38)
    total.setPlaceholderText("Enter total budget")
    total.setStyleSheet(input_style())

    top = QHBoxLayout()
    top.setSpacing(14)
    month.setFixedWidth(190)
    year.setFixedWidth(110)
    top.addLayout(column("Month", month))
    top.addLayout(column("Year", year))
    top.addLayout(column("Total Monthly Budget (₱)", total), 1)
    form.addLayout(top)

    category_header = QHBoxLayout()
    category_title = QLabel("Category Budgets")
    category_title.setStyleSheet(f"color:{BLACK};font-size:17px;font-weight:bold;background:transparent;border:none;")
    category_header.addWidget(category_title)
    category_header.addStretch()

    add_button = QPushButton("＋ Add Category")
    add_button.setFixedSize(170, 36)
    add_button.setStyleSheet(button_style("gold"))
    category_header.addWidget(add_button)
    form.addLayout(category_header)

    scroll = QScrollArea()
    scroll.setWidgetResizable(True)
    scroll.setStyleSheet(scroll_style())
    scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

    holder = QWidget()
    holder.setObjectName("holder")
    rows_layout = QVBoxLayout(holder)
    rows_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
    rows_layout.setContentsMargins(10, 10, 10, 10)
    rows_layout.setSpacing(8)
    scroll.setWidget(holder)
    form.addWidget(scroll, 1)

    allocation = QLabel("")
    allocation.setAlignment(Qt.AlignmentFlag.AlignCenter)
    form.addWidget(allocation)
    rows = []

    def update_allocation(*_):
        planned = sum(parse_amount(row.amount.text(), allow_zero=True) or 0 for row in rows)
        limit = parse_amount(total.text())

        if limit is None:
            text, color = f"Allocated to categories: ₱{planned:,.2f}", GRAY
        elif planned > limit:
            text, color = f"Allocated ₱{planned:,.2f} of ₱{limit:,.2f} — ₱{planned - limit:,.2f} OVER your total budget", RED
        else:
            text, color = f"Allocated ₱{planned:,.2f} of ₱{limit:,.2f} — ₱{limit - planned:,.2f} unallocated", GREEN

        allocation.setText(text)
        allocation.setStyleSheet(f"color:{color};font-size:14px;font-weight:bold;background:transparent;border:none;")

    def remove_row(row):
        rows.remove(row)
        rows_layout.removeWidget(row)
        row.deleteLater()
        update_allocation()

    def add_row(name="", amount="", existing=False):
        row = CategoryRow(name, amount, locked_name=existing, removable=not (existing and name in used), on_change=update_allocation, on_remove=remove_row)
        rows.append(row)
        rows_layout.addWidget(row)
        update_allocation()
        return row

    def new_category():
        row = add_row()
        row.name.setFocus()
        QTimer.singleShot(0, lambda: scroll.verticalScrollBar().setValue(scroll.verticalScrollBar().maximum()))

    total.textChanged.connect(update_allocation)
    add_button.clicked.connect(new_category)

    if budget["categories"]:
        for name, amount in budget["categories"].items():
            add_row(name, f"{amount:.2f}", existing=True)
    else:
        for name in DEFAULT_CATEGORIES:
            add_row(name)

    def warn(text):
        QMessageBox.warning(root, "Budget Period", text)

    def submit():
        year_value = year.text().strip()
        if not (year_value.isdigit() and len(year_value) == 4):
            warn("Please enter a valid 4-digit year.")
            return

        total_amount = parse_amount(total.text())
        if total_amount is None:
            warn("Please enter a valid total monthly budget.")
            return
        if not rows:
            warn("Please add at least one category.")
            return

        categories = {}
        for row in rows:
            name = clean_name(row.name.text())
            if not name:
                warn("Please enter a name for every category, or remove the empty row.")
                return
            if match_name(list(categories), name):
                warn(f"The category '{name}' is listed more than once.")
                return

            amount = parse_amount(row.amount.text(), allow_zero=True)
            if amount is None:
                warn(f"Please enter a valid amount for {name} (use 0 if you don't need one).")
                return
            categories[name] = amount

        if allocated(categories) > total_amount:
            answer = QMessageBox.question(root, "Budget Period", "Your category budgets add up to more than your total monthly budget.\n\nSave anyway?")
            if answer != QMessageBox.StandardButton.Yes:
                return

        save(create_budget(f"{month.currentText()} {year_value}", total_amount, categories))

    buttons = QHBoxLayout()
    buttons.setSpacing(14)
    buttons.addStretch()

    cancel_button = QPushButton("Cancel")
    cancel_button.setFixedSize(170, 44)
    cancel_button.setStyleSheet(button_style("secondary"))
    cancel_button.clicked.connect(cancel)
    buttons.addWidget(cancel_button)

    save_button = QPushButton("Save")
    save_button.setFixedSize(170, 44)
    save_button.setStyleSheet(button_style("primary"))
    save_button.clicked.connect(submit)
    buttons.addWidget(save_button)

    buttons.addStretch()
    form.addLayout(buttons)
    layout.addWidget(box)
    root.setCentralWidget(page)
