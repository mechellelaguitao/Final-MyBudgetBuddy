from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QFrame, QMessageBox, QDialog, QScrollArea, QProgressBar, QGraphicsDropShadowEffect
)
from PyQt6.QtGui import QColor
from PyQt6.QtCore import Qt

from database.database import load_user_data, save_user_data
from features.authentication.view import show_login
from features.budget.model import empty_budget
from features.budget.view import setup_budget
from features.budget.service import remaining, status, all_categories, ensure_categories, usage_ratio
from features.expenses.service import add_expense, total, category_totals
from features.expenses.view import ExpenseFormDialog, ExpenseEditDialog, ExpenseListDialog

BURGUNDY, GOLD, CREAM, BG, WHITE, BLACK = "#900020", "#C9A227", "#FFF9EC", "#F5F5F5", "#FFFFFF", "#000000"
RED, GREEN, ORANGE, GRAY, LINE, EDGE = "#B42318", "#2E7D32", "#E08A00", "#6B6B6B", "#D8D0BE", "#E8DFCB"
FONT = "'Georgia'"
NUMBER_WIDTH = 105
BAR_WIDTH = 90
CENTER = Qt.AlignmentFlag.AlignCenter
RIGHT = Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter


def usage_color(ratio):
    """Green = safe, orange = nearly used up, red = fully used / over."""
    return RED if ratio >= 1 else ORANGE if ratio >= 0.8 else GREEN


def menu_button_style():
    return f"""
        QPushButton {{ background:{WHITE}; color:{BLACK}; border:1px solid {EDGE}; border-left:6px solid {BURGUNDY}; border-radius:12px; font-family:{FONT}; font-size:16px; text-align:left; padding-left:14px; }}
        QPushButton:hover {{ background:{BURGUNDY}; color:{WHITE}; border-left:6px solid {GOLD}; }}
    """


def scrollbar_style():
    return f"""
        QScrollBar:vertical {{ background:#EFE8D8; width:12px; border-radius:6px; margin:0; }}
        QScrollBar::handle:vertical {{ background:{BURGUNDY}; border-radius:6px; min-height:30px; }}
        QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{ height:0; }}
    """


def scroll_style(background=CREAM, border=True):
    return f"""
        QScrollArea {{ border:{f"1px solid {LINE}" if border else "none"}; border-radius:8px; background:{background}; }}
        QWidget#holder {{ background:{background}; }}
        {scrollbar_style()}
    """


def progress_style(color):
    return f"""
        QProgressBar {{ background:#E8E0D0; border:none; border-radius:5px; }}
        QProgressBar::chunk {{ background:{color}; border-radius:5px; }}
    """


def styled(text, css, align=None):
    label = QLabel(text)
    label.setStyleSheet(css)
    if align:
        label.setAlignment(align)
    return label


def strip(height, color):
    frame = QFrame()
    frame.setObjectName("strip")
    frame.setFixedHeight(height)
    frame.setStyleSheet(f"QFrame#strip {{ background:{color}; }}")
    return frame


def shadow(widget, blur=20, offset=4):
    effect = QGraphicsDropShadowEffect()
    effect.setBlurRadius(blur)
    effect.setOffset(0, offset)
    effect.setColor(QColor(0, 0, 0, 45))
    widget.setGraphicsEffect(effect)


def plain_label(text, size=15, bold=False, color=BLACK, align=None):
    """QLabel that ignores the page background (used inside panels)."""
    return styled(text, f"color:{color};font-size:{size}px;font-weight:{'bold' if bold else 'normal'};background:transparent;border:none;", align)


def progress_bar(ratio, height):
    bar = QProgressBar()
    bar.setRange(0, 100)
    bar.setValue(min(100, int(ratio * 100)))
    bar.setTextVisible(False)
    bar.setFixedHeight(height)
    bar.setStyleSheet(progress_style(usage_color(ratio)))
    return bar


class App(QMainWindow):
    def __init__(self):
        super().__init__()
        self.current_user = None
        self.budget = empty_budget()
        self.expenses = []
        self.setWindowTitle("MyBudgetBuddy")
        self.setFixedSize(1000, 700)
        self.login()

    def clear(self):
        old = self.takeCentralWidget()
        if old:
            old.deleteLater()

    def login(self):
        show_login(self, self.after_login)

    def after_login(self, user):
        self.current_user = user["username"]
        self.budget, self.expenses = load_user_data(self.current_user)
        self.dashboard() if self.budget["month"] else self.budget_period()

    def set_budget(self, budget):
        self.budget, self.expenses = budget, []
        ensure_categories(self.budget, self.expenses)
        self.save()
        self.dashboard()

    def cancel_budget(self):
        if self.budget["month"]:
            self.dashboard()
        else:
            self.current_user, self.budget, self.expenses = None, empty_budget(), []
            self.login()

    def save(self):
        if self.current_user:
            save_user_data(self.current_user, self.budget, self.expenses)

    def categories(self):
        return all_categories(self.budget, self.expenses)

    def dashboard(self):
        self.clear()
        page = QWidget()
        page.setObjectName("page")
        page.setStyleSheet(f"QWidget#page {{ background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 {BG}, stop:1 #EFE6D6); }}")
        main = QVBoxLayout(page)
        main.setContentsMargins(0, 0, 0, 0)
        main.setSpacing(8)

        header = strip(115, f"qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 {BURGUNDY}, stop:1 #5E0014)")
        header_layout = QHBoxLayout(header)
        header_layout.setContentsMargins(35, 0, 30, 0)
        header_layout.setSpacing(10)
        header_layout.addWidget(styled("💵", "font-size:30px;"))
        header_layout.addWidget(styled("MyBudgetBuddy", f"color:{WHITE};font-size:22px;font-weight:bold;"))
        header_layout.addStretch()

        logout = QPushButton("Log out")
        logout.setFixedSize(120, 40)
        logout.setStyleSheet(f"QPushButton {{ background:{WHITE}; color:{BURGUNDY}; border:none; border-radius:20px; font-size:15px; font-weight:bold; }} QPushButton:hover {{ background:{CREAM}; color:{BURGUNDY}; }}")
        logout.clicked.connect(self.logout)
        header_layout.addWidget(logout)
        main.addWidget(header)
        main.addWidget(strip(4, GOLD))
        main.addWidget(styled(f"{self.budget['month']} Dashboard", f"color:{BLACK};font-family:'Freight Text Pro','Freight Text',Georgia,serif;font-size:38px;font-weight:600;font-style:italic;padding:8px;", CENTER))

        spent = total(self.expenses)
        left = remaining(self.budget, spent)
        cards = QHBoxLayout()
        cards.setSpacing(25)
        for name, value in (("Budget", self.budget["total"]), ("Expenses", spent), ("Remaining", left)):
            cards.addWidget(self.card(name, value))
        main.addLayout(cards)
        main.addWidget(styled(status(self.budget, spent), f"color:{RED if left < 0 else BURGUNDY};font-size:24px;font-weight:bold;padding:8px;", CENTER))

        body = QHBoxLayout()
        body.setContentsMargins(30, 4, 30, 18)
        body.setSpacing(25)
        body.addWidget(self.menu(), 0, Qt.AlignmentFlag.AlignTop)
        body.addWidget(self.summary_panel(spent, left), 1)
        main.addLayout(body, 1)
        self.setCentralWidget(page)

    def menu(self):
        menu_widget = QWidget()
        menu_widget.setFixedWidth(290)
        menu = QVBoxLayout(menu_widget)
        menu.setContentsMargins(0, 0, 0, 0)
        menu.setSpacing(8)
        for text, command in (("➕  Add Expenses", self.add), ("📋  View Expenses", self.view), ("✏️  Edit Expenses", self.edit),
                              ("🗑️  Delete Expenses", self.delete), ("📅  Budget Period", self.budget_period)):
            button = QPushButton(text)
            button.setFixedSize(290, 46)
            button.setStyleSheet(menu_button_style())
            button.clicked.connect(command)
            shadow(button, 12, 2)
            menu.addWidget(button)
        return menu_widget

    def card(self, title, value):
        box = QFrame()
        box.setFixedSize(230, 95)
        accent = {"Budget": BURGUNDY, "Expenses": GOLD, "Remaining": GREEN}.get(title, BURGUNDY)
        box.setObjectName("stat")
        box.setStyleSheet(f"QFrame#stat {{ background:{WHITE}; border:1px solid {EDGE}; border-top:5px solid {accent}; border-radius:14px; }}")
        shadow(box)
        layout = QVBoxLayout(box)
        layout.addWidget(styled(title, f"color:{GRAY};font-size:16px;", CENTER))
        layout.addWidget(styled(f"₱{value:,.2f}", f"color:{BURGUNDY};font-size:25px;font-weight:bold;", CENTER))
        return box

    def summary_row(self, name, budget_text, spent_text, left_text, bar=None, bold=False, left_color=BLACK, size=14, head=False):
        row = QHBoxLayout()
        row.setSpacing(6)
        row.addWidget(plain_label(name, size, bold), 1)
        for i, (text, color) in enumerate(((budget_text, BLACK), (spent_text, BLACK), (left_text, left_color))):
            label = plain_label(text, size, bold, color, CENTER if i < 2 else RIGHT)
            label.setFixedWidth(NUMBER_WIDTH)
            row.addWidget(label)
        if bar is None:
            row.setContentsMargins(0, 0, 16, 0)
        widget = bar if bar is not None else QWidget()
        widget.setFixedWidth(BAR_WIDTH)
        row.addWidget(widget)
        return row

    def summary_panel(self, spent, left):
        categories = self.categories()
        data = category_totals(self.expenses, categories)

        panel = QFrame()
        panel.setObjectName("summary")
        panel.setStyleSheet(f"QFrame#summary {{ background:{WHITE};border:1px solid {EDGE};border-radius:16px; }}")
        shadow(panel, 24, 5)
        layout = QVBoxLayout(panel)
        layout.setContentsMargins(18, 10, 18, 10)
        layout.setSpacing(5)

        top = QHBoxLayout()
        top.addWidget(plain_label("📊 Monthly Summary", 20, True, BURGUNDY))
        top.addStretch()
        top.addWidget(plain_label(self.budget["month"], 15, False, GRAY))
        layout.addLayout(top)

        ratio = usage_ratio(spent, self.budget["total"])
        used = QHBoxLayout()
        used.setSpacing(10)
        used.addWidget(progress_bar(ratio, 12), 1)
        used.addWidget(plain_label(f"{ratio * 100:.0f}% of budget used", 14, True, usage_color(ratio)))
        layout.addLayout(used)
        layout.addLayout(self.summary_row("Category", "Budget", "Spent", "Left", bold=True, head=True))

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet(scroll_style("transparent", border=False))
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)

        holder = QWidget()
        holder.setObjectName("holder")
        rows = QVBoxLayout(holder)
        rows.setAlignment(Qt.AlignmentFlag.AlignTop)
        rows.setContentsMargins(0, 0, 4, 0)
        rows.setSpacing(6)
        total_budget = 0

        for category in categories:
            budgeted = self.budget["categories"].get(category, 0)
            used_amount = data[category]
            category_left = budgeted - used_amount
            total_budget += budgeted
            rows.addLayout(self.summary_row(
                category, f"₱{budgeted:,.2f}", f"₱{used_amount:,.2f}", f"₱{category_left:,.2f}",
                bar=progress_bar(usage_ratio(used_amount, budgeted), 10), left_color=RED if category_left < 0 else BLACK))

        if not categories:
            rows.addWidget(plain_label("No categories yet. Open Budget Period to add some.", 14, False, GRAY))

        scroll.setWidget(holder)
        layout.addWidget(scroll, 1)
        layout.addLayout(self.summary_row(
            "TOTAL", f"₱{total_budget:,.2f}", f"₱{spent:,.2f}", f"₱{total_budget - spent:,.2f}",
            bold=True, left_color=RED if total_budget - spent < 0 else BLACK))
        return panel

    def has_expenses(self, title):
        if self.expenses:
            return True
        QMessageBox.information(self, title, "You don't have any expenses yet.")
        return False

    def add(self):
        dialog = ExpenseFormDialog(self, self.categories())
        if dialog.exec() == QDialog.DialogCode.Accepted:
            for description, category, amount in dialog.values():
                add_expense(self.expenses, description, category, amount)
            ensure_categories(self.budget, self.expenses)
            self.save()
            self.dashboard()

    def view(self):
        self.open_expense_page("view")

    def edit(self):
        self.open_expense_page("edit")

    def delete(self):
        self.open_expense_page("delete")

    def open_expense_page(self, action, index=None):
        titles = {"view": "View Expenses", "edit": "Edit Expenses", "delete": "Delete Expenses"}
        if not self.has_expenses(titles[action]):
            return

        changed = False
        while action:
            categories = self.categories()
            dialog = (ExpenseEditDialog(self, self.expenses, categories, focus_index=index) if action == "edit"
                      else ExpenseListDialog(self, self.expenses, categories, mode=action, focus_index=index))
            accepted = dialog.exec() == QDialog.DialogCode.Accepted
            if accepted and action in ("edit", "delete"):
                self.expenses = dialog.result_expenses()
                ensure_categories(self.budget, self.expenses)
                self.save()
                changed = True
            action, index = dialog.shortcut or (None, None)

        if changed:
            self.dashboard()

    def budget_period(self):
        setup_budget(self, self.set_budget, self.cancel_budget, self.budget, {expense["category"] for expense in self.expenses})

    def logout(self):
        if QMessageBox.question(self, "Log out", "Do you want to log out?") == QMessageBox.StandardButton.Yes:
            self.save()
            self.current_user, self.budget, self.expenses = None, empty_budget(), []
            self.login()