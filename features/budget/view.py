from PyQt6.QtWidgets import QWidget,QVBoxLayout,QHBoxLayout,QLabel,QLineEdit,QPushButton,QComboBox,QMessageBox
from PyQt6.QtCore import Qt
from .model import create_budget

BURGUNDY="#900020"; BG="#F5F5F5"; WHITE="#FFFFFF"; BLACK="#000000"
MONTHS=["January","February","March","April","May","June","July","August","September","October","November","December"]


def field_style():
    return f"""QLineEdit {{ background:{WHITE}; color:{BLACK}; border:3px solid {BLACK}; padding:4px; font-size:15px; }}"""


def setup_budget(root,save,categories,budget=None):

    page=QWidget(); page.setStyleSheet(f"background:{BG};color:{BLACK};")
    layout=QVBoxLayout(page); layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

    box=QWidget(); box.setFixedSize(540,610); box.setStyleSheet(f"background:{WHITE};color:{BLACK};")
    form=QVBoxLayout(box); form.setContentsMargins(40,25,40,25); form.setSpacing(5)

    title=QLabel("Budget Period"); title.setAlignment(Qt.AlignmentFlag.AlignCenter); title.setStyleSheet(f"color:{BURGUNDY};font-size:30px;font-weight:bold;"); form.addWidget(title)

    month_label=QLabel("Month"); month_label.setAlignment(Qt.AlignmentFlag.AlignCenter); month_label.setStyleSheet(f"color:{BLACK};font-size:16px;"); form.addWidget(month_label)

    month=QComboBox(); month.addItems(MONTHS); month.setCurrentIndex(0); month.setFixedHeight(38)
    month.setStyleSheet(f"""QComboBox {{ background:{WHITE}; color:{BLACK}; border:3px solid {BLACK}; padding:4px; font-size:15px; }} QComboBox QAbstractItemView {{ background:{WHITE}; color:{BLACK}; selection-background-color:{BURGUNDY}; selection-color:{WHITE}; }}""")
    month.view().setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded); form.addWidget(month)

    year_label=QLabel("Year"); year_label.setAlignment(Qt.AlignmentFlag.AlignCenter); year_label.setStyleSheet(f"color:{BLACK};font-size:16px;"); form.addWidget(year_label)

    year=QLineEdit(); year.setFixedHeight(38); year.setPlaceholderText("Enter year"); year.setStyleSheet(field_style()); form.addWidget(year)

    total_label=QLabel("Total Monthly Budget"); total_label.setAlignment(Qt.AlignmentFlag.AlignCenter); total_label.setStyleSheet(f"color:{BLACK};font-size:16px;"); form.addWidget(total_label)

    total=QLineEdit(); total.setFixedHeight(38); total.setPlaceholderText("Enter total budget"); total.setStyleSheet(field_style()); form.addWidget(total)

    entries={}

    for category in categories:
        row=QHBoxLayout(); row.setSpacing(15)
        label=QLabel(category); label.setFixedWidth(210); label.setStyleSheet(f"color:{BLACK};font-size:15px;")
        entry=QLineEdit(); entry.setFixedHeight(36); entry.setPlaceholderText("Amount"); entry.setStyleSheet(field_style())
        entries[category]=entry; row.addWidget(label); row.addWidget(entry); form.addLayout(row)

    def submit():

        if not year.text().strip():
            QMessageBox.warning(root,"Budget Period","Please enter a year."); return

        try:
            total_amount=float(total.text().strip())
            if total_amount<=0: raise ValueError
        except ValueError:
            QMessageBox.warning(root,"Budget Period","Please enter a valid total monthly budget."); return

        category_amounts={}

        for category,entry in entries.items():
            value=entry.text().strip()

            if not value:
                QMessageBox.warning(root,"Budget Period",f"Please enter an amount for {category}."); return

            try:
                amount=float(value)
                if amount<0: raise ValueError
            except ValueError:
                QMessageBox.warning(root,"Budget Period",f"Please enter a valid amount for {category}."); return

            category_amounts[category]=amount

        save(create_budget(f"{month.currentText()} {year.text().strip()}",total_amount,category_amounts))

    button=QPushButton("Save Budget"); button.setFixedSize(310,42); button.setStyleSheet(f"""QPushButton {{ background:{WHITE}; color:{BLACK}; border:3px solid {BLACK}; font-size:16px; }} QPushButton:hover {{ background:#EEEEEE; color:{BLACK}; }}""")
    button.clicked.connect(submit); form.addWidget(button,alignment=Qt.AlignmentFlag.AlignCenter)

    layout.addWidget(box); root.setCentralWidget(page)