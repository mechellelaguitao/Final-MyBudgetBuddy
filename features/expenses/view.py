from PyQt6.QtWidgets import QDialog,QWidget,QVBoxLayout,QHBoxLayout,QLabel,QLineEdit,QPushButton,QMessageBox,QTableWidget,QTableWidgetItem,QHeaderView,QComboBox
from PyQt6.QtCore import Qt
from .service import CATEGORIES

BURGUNDY="#900020"; WHITE="#FFFFFF"; BLACK="#000000"

def input_style():
    return f"""QLineEdit {{ background:{WHITE}; color:{BLACK}; border:2px solid {BLACK}; padding:5px; font-size:15px; }}"""

def button_style():
    return f"""QPushButton {{ background:{WHITE}; color:{BLACK}; border:3px solid {BLACK}; font-size:16px; padding:8px; }} QPushButton:hover {{ background:#EEEEEE; color:{BLACK}; }}"""


class ExpenseFormDialog(QDialog):

    def __init__(self,parent,title):
        super().__init__(parent); self.setWindowTitle(title); self.setFixedSize(750,520); self.setStyleSheet(f"background:{WHITE};color:{BLACK};")
        layout=QVBoxLayout(self)
        heading=QLabel(title); heading.setAlignment(Qt.AlignmentFlag.AlignCenter); heading.setStyleSheet(f"color:{BURGUNDY};font-size:30px;font-weight:bold;"); layout.addWidget(heading)

        box=QWidget(); form=QVBoxLayout(box); headers=QHBoxLayout()
        labels=[QLabel("Category"),QLabel("Description"),QLabel("Amount")]

        for label,width in zip(labels,[170,260,150]):
            label.setFixedWidth(width); label.setStyleSheet(f"color:{BLACK};font-size:16px;font-weight:bold;"); headers.addWidget(label)

        form.addLayout(headers); self.rows=[]

        for category in CATEGORIES:
            row=QHBoxLayout(); category_name=QLabel(category); category_name.setFixedWidth(170); category_name.setStyleSheet(f"color:{BLACK};font-size:15px;")
            description=QLineEdit(); description.setFixedWidth(260); description.setStyleSheet(input_style())
            amount=QLineEdit(); amount.setFixedWidth(150); amount.setStyleSheet(input_style())
            row.addWidget(category_name); row.addWidget(description); row.addWidget(amount); form.addLayout(row); self.rows.append((category,description,amount))

        layout.addWidget(box)
        save=QPushButton("Add Expenses"); save.setFixedSize(280,45); save.setStyleSheet(button_style()); save.clicked.connect(self.submit); layout.addWidget(save,alignment=Qt.AlignmentFlag.AlignCenter)

    def submit(self):
        self._expenses=[]

        for category,description,amount in self.rows:
            desc=description.text().strip(); value=amount.text().strip()
            if not desc and not value: continue
            if not desc or not value: QMessageBox.warning(self,"Add Expenses",f"Please complete the {category} row."); return
            try:
                number=float(value)
                if number<=0: raise ValueError
            except ValueError:
                QMessageBox.warning(self,"Add Expenses",f"Please enter a valid amount for {category}."); return
            self._expenses.append((desc,category,number))

        if not self._expenses: QMessageBox.warning(self,"Add Expenses","Please enter at least one expense."); return
        self.accept()

    def values(self):
        return self._expenses


class ExpenseListDialog(QDialog):

    def __init__(self,parent,expenses,title,mode="view"):
        super().__init__(parent); self.expenses=expenses; self.mode=mode; self.setWindowTitle(title); self.setFixedSize(900,600); self.setStyleSheet(f"background:{WHITE};color:{BLACK};")
        layout=QVBoxLayout(self)
        heading=QLabel(title); heading.setAlignment(Qt.AlignmentFlag.AlignCenter); heading.setStyleSheet(f"color:{BURGUNDY};font-size:30px;font-weight:bold;"); layout.addWidget(heading)

        instruction="Edit the information below, then click SAVE." if mode=="edit" else "Select an expense, click DELETE, then click SAVE." if mode=="delete" else "View your expenses below."
        text=QLabel(instruction); text.setAlignment(Qt.AlignmentFlag.AlignCenter); text.setStyleSheet(f"color:{BLACK};font-size:15px;padding:5px;"); layout.addWidget(text)

        if mode=="edit": self.create_edit_form(layout)
        else: self.create_table(layout)

        buttons=QHBoxLayout()

        if mode=="view":
            close=QPushButton("CLOSE"); close.clicked.connect(self.reject); buttons.addWidget(close)
        elif mode=="edit":
            save=QPushButton("SAVE"); save.clicked.connect(self.save_edit); buttons.addWidget(save)
        else:
            delete=QPushButton("DELETE"); delete.clicked.connect(self.delete_selected); save=QPushButton("SAVE"); save.clicked.connect(self.save_delete); buttons.addWidget(delete); buttons.addWidget(save)

        for button in buttons.findChildren(QPushButton): button.setFixedSize(220,45); button.setStyleSheet(button_style())
        layout.addLayout(buttons)

    def create_edit_form(self,layout):
        self.edit_rows=[]; headers=QHBoxLayout()
        labels=[QLabel("Description"),QLabel("Category"),QLabel("Amount")]

        for label,width in zip(labels,[300,230,180]):
            label.setFixedWidth(width); label.setStyleSheet(f"color:{BLACK};font-size:16px;font-weight:bold;"); headers.addWidget(label)

        layout.addLayout(headers)

        for expense in self.expenses:
            row=QHBoxLayout()
            description=QLineEdit(expense["description"]); description.setFixedWidth(300); description.setStyleSheet(input_style())
            category=QComboBox(); category.addItems(CATEGORIES); category.setCurrentText(expense["category"]); category.setFixedWidth(230); category.setStyleSheet(f"background:{WHITE};color:{BLACK};border:2px solid {BLACK};padding:5px;font-size:15px;")
            amount=QLineEdit(f"{expense['amount']:.2f}"); amount.setFixedWidth(180); amount.setStyleSheet(input_style())
            row.addWidget(description); row.addWidget(category); row.addWidget(amount); layout.addLayout(row); self.edit_rows.append((description,category,amount))

    def create_table(self,layout):
        self.table=QTableWidget(len(self.expenses),3); self.table.setHorizontalHeaderLabels(["Description","Category","Amount"]); self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch); self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows); self.table.setSelectionMode(QTableWidget.SelectionMode.SingleSelection); self.table.setStyleSheet(f"""QTableWidget {{ background:{WHITE}; color:{BLACK}; gridline-color:#AAAAAA; font-size:15px; }} QHeaderView::section {{ background:{BURGUNDY}; color:{WHITE}; font-weight:bold; padding:8px; }} QTableWidget::item:selected {{ background:#557A95; color:{WHITE}; }}"""); self.load_table(); layout.addWidget(self.table)

    def load_table(self):
        for row,expense in enumerate(self.expenses):
            self.table.setItem(row,0,QTableWidgetItem(expense["description"])); self.table.setItem(row,1,QTableWidgetItem(expense["category"])); self.table.setItem(row,2,QTableWidgetItem(f"{expense['amount']:.2f}"))

    def save_edit(self):
        updated=[]

        for description,category,amount in self.edit_rows:
            desc=description.text().strip(); cat=category.currentText(); value=amount.text().strip()

            if not desc: QMessageBox.warning(self,"Edit Expense","Description cannot be empty."); return

            try:
                number=float(value)
                if number<=0: raise ValueError
            except ValueError:
                QMessageBox.warning(self,"Edit Expense",f"Please enter a valid amount for {desc}."); return

            updated.append({"description":desc,"category":cat,"amount":number})

        self._result=updated; self.accept()

    def result_expenses(self):
        return getattr(self,"_result",self.expenses)

    def delete_selected(self):
        row=self.table.currentRow()

        if row<0: QMessageBox.warning(self,"Delete Expense","Please select an expense."); return

        answer=QMessageBox.question(self,"Delete Expense","Do you want to delete the selected expense?")

        if answer==QMessageBox.StandardButton.Yes: self.table.removeRow(row)

    def save_delete(self):
        updated=[]

        for row in range(self.table.rowCount()):
            description=self.table.item(row,0).text().strip(); category=self.table.item(row,1).text().strip(); value=self.table.item(row,2).text().strip()

            try:
                amount=float(value)
                if not description or category not in CATEGORIES or amount<=0: raise ValueError
            except ValueError:
                QMessageBox.warning(self,"Delete Expense","Invalid expense information."); return

            updated.append({"description":description,"category":category,"amount":amount})

        self._result=updated; self.accept()