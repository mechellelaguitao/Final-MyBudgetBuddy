from PyQt6.QtWidgets import QMainWindow,QWidget,QVBoxLayout,QHBoxLayout,QGridLayout,QLabel,QPushButton,QFrame,QMessageBox,QDialog
from PyQt6.QtCore import Qt
from database.database import save_data
from features.authentication.view import show_login
from features.budget.view import setup_budget
from features.budget.service import remaining,status
from features.expenses.service import CATEGORIES,add_expense,total,category_totals
from features.expenses.view import ExpenseFormDialog,ExpenseListDialog

BURGUNDY="#900020"; BG="#F5F5F5"; WHITE="#FFFFFF"; BLACK="#000000"; RED="#B42318"


class App(QMainWindow):

    def __init__(self,users,budget,expenses):
        super().__init__()
        self.users=users; self.budget=budget; self.expenses=expenses
        self.setWindowTitle("MyBudgetBuddy"); self.setFixedSize(1000,700)
        self.login()

    def clear(self):
        old=self.takeCentralWidget()
        if old: old.deleteLater()

    def login(self):
        show_login(self,self.after_login)

    def after_login(self):
        if self.budget["month"]:
            self.dashboard()
        else:
            setup_budget(self,self.set_budget,CATEGORIES)

    def set_budget(self,budget):
        self.budget=budget; self.save(); self.dashboard()

    def save(self):
        save_data(self.users,self.budget,self.expenses)

    def dashboard(self):

        self.clear()

        page=QWidget(); page.setStyleSheet(f"background:{BG};color:{BLACK};")
        main=QVBoxLayout(page); main.setContentsMargins(0,0,0,0); main.setSpacing(8)

        header=QFrame(); header.setFixedHeight(115); header.setStyleSheet(f"background:{BURGUNDY};")
        header_layout=QHBoxLayout(header); header_layout.setContentsMargins(35,0,30,0)

        title=QLabel("MyBudgetBuddy"); title.setStyleSheet(f"color:{WHITE};font-size:32px;font-weight:bold;")
        header_layout.addWidget(title); header_layout.addStretch()

        logout=QPushButton("Log out"); logout.setFixedSize(250,55)
        logout.setStyleSheet(f"""
        QPushButton {{
            background:{WHITE};
            color:{BLACK};
            border:3px solid {BLACK};
            font-size:16px;
        }}
        QPushButton:hover {{ background:#EEEEEE;color:{BLACK}; }}
        """)
        logout.clicked.connect(self.logout); header_layout.addWidget(logout); main.addWidget(header)

        heading=QLabel(f"{self.budget['month']} Dashboard"); heading.setAlignment(Qt.AlignmentFlag.AlignCenter)
        heading.setStyleSheet(f"color:{BLACK};font-size:38px;font-weight:bold;padding:8px;"); main.addWidget(heading)

        spent=total(self.expenses); left=remaining(self.budget,spent)

        cards=QHBoxLayout(); cards.setSpacing(25)
        cards.addWidget(self.card("Budget",self.budget["total"]))
        cards.addWidget(self.card("Expenses",spent))
        cards.addWidget(self.card("Remaining",left))
        main.addLayout(cards)

        stat=QLabel(status(self.budget,spent)); stat.setAlignment(Qt.AlignmentFlag.AlignCenter)
        stat.setStyleSheet(f"color:{RED if left<0 else BURGUNDY};font-size:24px;font-weight:bold;padding:8px;"); main.addWidget(stat)

        menu=QGridLayout(); menu.setHorizontalSpacing(18); menu.setVerticalSpacing(12)

        buttons=[
            ("Add Expenses",self.add),
            ("View Expenses",self.view),
            ("Edit Expense",self.edit),
            ("Delete Expense",self.delete),
            ("Budget Period",self.budget_period),
            ("Monthly Summary",self.summary)
        ]

        for i,(text,command) in enumerate(buttons):
            button=QPushButton(text); button.setFixedSize(320,55)
            button.setStyleSheet(f"""
            QPushButton {{
                background:{WHITE};
                color:{BLACK};
                border:3px solid {BLACK};
                font-size:16px;
            }}
            QPushButton:hover {{ background:#EEEEEE;color:{BLACK}; }}
            """)
            button.clicked.connect(command); menu.addWidget(button,i//2,i%2)

        menu_widget=QWidget(); menu_widget.setLayout(menu)
        main.addWidget(menu_widget,alignment=Qt.AlignmentFlag.AlignCenter); main.addStretch()
        self.setCentralWidget(page)

    def card(self,title,value):

        box=QFrame(); box.setFixedSize(270,115)
        box.setStyleSheet(f"background:{WHITE};color:{BLACK};border:1px solid {BLACK};")
        layout=QVBoxLayout(box)

        label=QLabel(title); label.setAlignment(Qt.AlignmentFlag.AlignCenter); label.setStyleSheet(f"color:{BLACK};font-size:17px;"); layout.addWidget(label)

        amount=QLabel(f"₱{value:,.2f}"); amount.setAlignment(Qt.AlignmentFlag.AlignCenter)
        amount.setStyleSheet(f"color:{BURGUNDY};font-size:25px;font-weight:bold;"); layout.addWidget(amount)

        return box

    def add(self):

        dialog=ExpenseFormDialog(self,"Add Expenses")

        if dialog.exec()==QDialog.DialogCode.Accepted:

            for description,category,amount in dialog.values():
                add_expense(self.expenses,description,category,amount)

            self.save(); self.dashboard()

    def view(self):

        dialog=ExpenseListDialog(self,self.expenses,"View Expenses",mode="view")
        dialog.exec()

    def edit(self):

        dialog=ExpenseListDialog(self,self.expenses,"Edit Expense",mode="edit")

        if dialog.exec()==QDialog.DialogCode.Accepted:
            self.expenses=dialog.result_expenses()
            self.save(); self.dashboard()

    def delete(self):

        dialog=ExpenseListDialog(self,self.expenses,"Delete Expense",mode="delete")

        if dialog.exec()==QDialog.DialogCode.Accepted:
            self.expenses=dialog.result_expenses()
            self.save(); self.dashboard()

    def budget_period(self):
        setup_budget(self,self.set_budget,CATEGORIES,self.budget)

    def summary(self):

        spent=total(self.expenses); left=remaining(self.budget,spent); data=category_totals(self.expenses)

        dialog=QDialog(self); dialog.setWindowTitle("Monthly Summary"); dialog.setFixedSize(700,650)
        dialog.setStyleSheet(f"background:{WHITE};color:{BLACK};")

        layout=QVBoxLayout(dialog); layout.setContentsMargins(40,25,40,25); layout.setSpacing(8)

        title=QLabel("Monthly Summary"); title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet(f"color:{BURGUNDY};font-size:30px;font-weight:bold;"); layout.addWidget(title)

        info=QLabel(
            f"Month: {self.budget['month']}\n"
            f"Total Budget: ₱{self.budget['total']:,.2f}\n"
            f"Total Expenses: ₱{spent:,.2f}\n"
            f"Remaining: ₱{left:,.2f}"
        )

        info.setAlignment(Qt.AlignmentFlag.AlignCenter)
        info.setStyleSheet(f"color:{BLACK};font-size:17px;padding:10px;")
        layout.addWidget(info)

        table=QGridLayout(); table.setHorizontalSpacing(70); table.setVerticalSpacing(12)

        for column,text in enumerate(["Category","Budget","Spent"]):
            label=QLabel(text); label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            label.setStyleSheet(f"color:{BLACK};font-size:17px;font-weight:bold;")
            table.addWidget(label,0,column)

        for row,category in enumerate(CATEGORIES,1):

            category_label=QLabel(category)
            budget_label=QLabel(f"₱{self.budget['categories'].get(category,0):,.2f}")
            spent_label=QLabel(f"₱{data[category]:,.2f}")

            for label in [category_label,budget_label,spent_label]:
                label.setAlignment(Qt.AlignmentFlag.AlignCenter)
                label.setStyleSheet(f"color:{BLACK};font-size:16px;")

            table.addWidget(category_label,row,0)
            table.addWidget(budget_label,row,1)
            table.addWidget(spent_label,row,2)

        layout.addLayout(table); layout.addStretch()

        text=status(self.budget,spent)
        color=RED if left<0 else BURGUNDY

        status_label=QLabel(text); status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        status_label.setStyleSheet(f"color:{color};font-size:24px;font-weight:bold;padding:10px;")
        layout.addWidget(status_label)

        close=QPushButton("Close"); close.setFixedSize(200,42)
        close.setStyleSheet(f"""
        QPushButton {{
            background:{WHITE};
            color:{BLACK};
            border:3px solid {BLACK};
            font-size:16px;
        }}
        QPushButton:hover {{ background:#EEEEEE;color:{BLACK}; }}
        """)
        close.clicked.connect(dialog.close)
        layout.addWidget(close,alignment=Qt.AlignmentFlag.AlignCenter)

        dialog.exec()

    def logout(self):

        answer=QMessageBox.question(self,"Logout","Do you want to log out?")

        if answer==QMessageBox.StandardButton.Yes:
            self.save(); self.login()