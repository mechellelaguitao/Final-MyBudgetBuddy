from PyQt6.QtWidgets import QWidget,QVBoxLayout,QLabel,QLineEdit,QPushButton,QMessageBox
from PyQt6.QtCore import Qt
from .service import login,create_account

BURGUNDY="#900020"; BG="#F5F5F5"; WHITE="#FFFFFF"; BLACK="#000000"


def input_style():
    return f"""
    QLineEdit {{
        background:{WHITE};
        color:{BLACK};
        border:3px solid {BLACK};
        font-size:18px;
        padding:5px;
    }}
    """


def button_style():
    return f"""
    QPushButton {{
        background:{BURGUNDY};
        color:{WHITE};
        border:3px solid {BURGUNDY};
        font-size:18px;
    }}
    QPushButton:hover {{
        background:#700018;
        color:{WHITE};
    }}
    """


def show_login(root,success):

    def clear():
        old=root.takeCentralWidget()
        if old: old.deleteLater()

    def login_page():

        clear()

        page=QWidget(); page.setStyleSheet(f"background:{BG};")
        layout=QVBoxLayout(page); layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        box=QWidget(); box.setFixedSize(500,480); box.setStyleSheet(f"background:{WHITE};")
        form=QVBoxLayout(box); form.setContentsMargins(60,40,60,40); form.setSpacing(12)

        title=QLabel("MyBudgetBuddy"); title.setAlignment(Qt.AlignmentFlag.AlignCenter); title.setStyleSheet(f"color:{BURGUNDY};font-size:32px;font-weight:bold;"); form.addWidget(title)

        username_label=QLabel("Username"); username_label.setAlignment(Qt.AlignmentFlag.AlignCenter); username_label.setStyleSheet(f"color:{BLACK};font-size:20px;"); form.addWidget(username_label)

        username=QLineEdit(); username.setFixedHeight(42); username.setStyleSheet(input_style()); form.addWidget(username)

        password_label=QLabel("Password"); password_label.setAlignment(Qt.AlignmentFlag.AlignCenter); password_label.setStyleSheet(f"color:{BLACK};font-size:20px;"); form.addWidget(password_label)

        password=QLineEdit(); password.setFixedHeight(42); password.setEchoMode(QLineEdit.EchoMode.Password); password.setStyleSheet(input_style()); form.addWidget(password)

        form.addSpacing(15)

        def submit():
            if login(username.text(),password.text()):
                success()
            else:
                QMessageBox.warning(root,"Login","Invalid username or password.")

        login_button=QPushButton("Login"); login_button.setFixedHeight(42); login_button.setStyleSheet(button_style()); login_button.clicked.connect(submit); form.addWidget(login_button)

        register_button=QPushButton("Register"); register_button.setFixedHeight(42); register_button.setStyleSheet(button_style()); register_button.clicked.connect(register_page); form.addWidget(register_button)

        layout.addWidget(box); root.setCentralWidget(page)

    def register_page():

        clear()

        page=QWidget(); page.setStyleSheet(f"background:{BG};")
        layout=QVBoxLayout(page); layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        box=QWidget(); box.setFixedSize(500,540); box.setStyleSheet(f"background:{WHITE};")
        form=QVBoxLayout(box); form.setContentsMargins(60,40,60,40); form.setSpacing(12)

        title=QLabel("Create Account"); title.setAlignment(Qt.AlignmentFlag.AlignCenter); title.setStyleSheet(f"color:{BURGUNDY};font-size:30px;font-weight:bold;"); form.addWidget(title)

        username=QLineEdit(); password=QLineEdit(); confirm=QLineEdit()

        fields=[
            ("Username",username),
            ("Password",password),
            ("Confirm Password",confirm)
        ]

        for text,entry in fields:

            label=QLabel(text); label.setAlignment(Qt.AlignmentFlag.AlignCenter); label.setStyleSheet(f"color:{BLACK};font-size:20px;"); form.addWidget(label)

            entry.setFixedHeight(42); entry.setStyleSheet(input_style())

            if text!="Username":
                entry.setEchoMode(QLineEdit.EchoMode.Password)

            form.addWidget(entry)

        form.addSpacing(15)

        def submit():

            user=username.text().strip(); pw=password.text(); conf=confirm.text()

            if not user or not pw:
                QMessageBox.warning(root,"Register","Please complete all fields.")

            elif pw!=conf:
                QMessageBox.warning(root,"Register","Passwords do not match.")

            elif create_account(user,pw):
                QMessageBox.information(root,"Register","Account created successfully.")
                login_page()

            else:
                QMessageBox.warning(root,"Register","Username already exists.")

        create=QPushButton("Create Account"); create.setFixedHeight(42); create.setStyleSheet(button_style()); create.clicked.connect(submit); form.addWidget(create)

        back=QPushButton("Back to Login"); back.setFixedHeight(42); back.setStyleSheet(button_style()); back.clicked.connect(login_page); form.addWidget(back)

        layout.addWidget(box); root.setCentralWidget(page)

    login_page()