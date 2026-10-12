
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox, QFormLayout, QFrame, QGraphicsDropShadowEffect
from PyQt6.QtGui import QColor
from PyQt6.QtCore import Qt
from .service import login, create_account

BURGUNDY = "#900020"
DARK_BURGUNDY = "#700018"
BG = "#F5F5F5"
WHITE = "#FFFFFF"
BLACK = "#000000"
GRAY = "#6B6B6B"
LIGHT = "#EEEEEE"
FONT = "'Georgia'"


def add_shadow(widget, blur=18, offset=4):
    effect = QGraphicsDropShadowEffect()
    effect.setBlurRadius(blur)
    effect.setOffset(0, offset)
    effect.setColor(QColor(0, 0, 0, 60))
    widget.setGraphicsEffect(effect)


def button_style(kind="primary"):
    colors = {"primary": (BURGUNDY, WHITE, BURGUNDY, DARK_BURGUNDY), "secondary": (WHITE, BLACK, BLACK, LIGHT)}
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


def show_login(root, success):

    def clear():
        old = root.takeCentralWidget()
        if old:
            old.deleteLater()

    def build_card(width, height, title_text, title_size):
        page = QWidget()
        page.setObjectName("page")
        page.setStyleSheet(f"QWidget#page {{ background-color: {BG}; }}")
        layout = QVBoxLayout(page)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        box = QFrame()
        box.setObjectName("card")
        box.setFixedSize(width, height)
        box.setStyleSheet(f"QFrame#card {{ background-color: {WHITE}; border: 2px solid {BURGUNDY}; border-radius: 14px; }}")
        add_shadow(box)

        form = QVBoxLayout(box)
        form.setContentsMargins(55, 28, 55, 28)
        form.setSpacing(10)

        coin = QLabel("💰")
        coin.setAlignment(Qt.AlignmentFlag.AlignCenter)
        coin.setStyleSheet("font-size: 40px; background: transparent; border: none;")
        form.addWidget(coin)

        title = QLabel(title_text)
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet(f"color: {BURGUNDY}; font-family: {FONT}; font-size: {title_size}px; font-weight: bold; background: transparent; border: none;")
        form.addWidget(title)

        tagline = QLabel("Plan it. Track it. Save it.")
        tagline.setAlignment(Qt.AlignmentFlag.AlignCenter)
        tagline.setStyleSheet(f"color: {GRAY}; font-family: {FONT}; font-size: 15px; font-style: italic; background: transparent; border: none;")
        form.addWidget(tagline)
        form.addSpacing(8)
        layout.addWidget(box)
        return page, form

    def field_label(text, width=None):
        label = QLabel(text)
        label.setStyleSheet(f"color: {BLACK}; font-family: {FONT}; font-size: 18px; background: transparent; border: none;")
        if width:
            label.setFixedWidth(width)
            label.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        return label

    def login_page():
        clear()
        page, form = build_card(600, 520, "MyBudgetBuddy", 32)
        fields = QFormLayout()
        fields.setHorizontalSpacing(15)
        fields.setVerticalSpacing(12)

        username = QLineEdit()
        username.setMinimumWidth(350)
        username.setFixedHeight(42)
        username.setStyleSheet(input_style(18))
        fields.addRow(field_label("Username:"), username)

        password = QLineEdit()
        password.setMinimumWidth(350)
        password.setFixedHeight(42)
        password.setEchoMode(QLineEdit.EchoMode.Password)
        password.setStyleSheet(input_style(18))
        fields.addRow(field_label("Password:"), password)

        form.addLayout(fields)
        form.addSpacing(14)

        def submit():
            user = login(username.text().strip(), password.text())
            if user:
                success(user)
            else:
                QMessageBox.warning(root, "Login", "Invalid username or password.")

        password.returnPressed.connect(submit)
        username.returnPressed.connect(submit)

        buttons = QVBoxLayout()
        buttons.setSpacing(8)
        buttons.setAlignment(Qt.AlignmentFlag.AlignCenter)

        login_button = QPushButton("Log in")
        login_button.setFixedSize(160, 44)
        login_button.setStyleSheet(button_style("primary"))
        login_button.clicked.connect(submit)
        buttons.addWidget(login_button, alignment=Qt.AlignmentFlag.AlignCenter)

        register_button = QPushButton("Register")
        register_button.setFixedSize(160, 44)
        register_button.setStyleSheet(button_style("secondary"))
        register_button.clicked.connect(register_page)
        buttons.addWidget(register_button, alignment=Qt.AlignmentFlag.AlignCenter)

        form.addLayout(buttons)
        form.addStretch()
        root.setCentralWidget(page)

    def register_page():
        clear()
        page, form = build_card(600, 600, "Create Account", 30)

        fields = QFormLayout()
        fields.setHorizontalSpacing(10)
        fields.setVerticalSpacing(12)
        fields.setLabelAlignment(Qt.AlignmentFlag.AlignRight)
        fields.setFormAlignment(Qt.AlignmentFlag.AlignHCenter)

        username, password, confirm = QLineEdit(), QLineEdit(), QLineEdit()
        entries = [("Username:", username, False), ("Password:", password, True), ("Confirm Password:", confirm, True)]

        for text, entry, hidden in entries:
            entry.setFixedWidth(285)
            entry.setFixedHeight(42)
            entry.setStyleSheet(input_style(18))
            if hidden:
                entry.setEchoMode(QLineEdit.EchoMode.Password)
            fields.addRow(field_label(text, 180), entry)

        form.addLayout(fields)
        form.addSpacing(10)

        def submit():
            user, pw, conf = username.text().strip(), password.text(), confirm.text()
            if not user or not pw or not conf:
                QMessageBox.warning(root, "Register", "Please complete all fields.")
            elif pw != conf:
                QMessageBox.warning(root, "Register", "Passwords do not match.")
            elif create_account(user, pw):
                QMessageBox.information(root, "Register", "Account created successfully.")
                login_page()
            else:
                QMessageBox.warning(root, "Register", "Username already exists.")

        confirm.returnPressed.connect(submit)

        create = QPushButton("Create Account")
        create.setFixedSize(190, 44)
        create.setStyleSheet(button_style("primary"))
        create.clicked.connect(submit)
        form.addWidget(create, alignment=Qt.AlignmentFlag.AlignCenter)

        back = QPushButton("Back to Login")
        back.setFixedSize(190, 44)
        back.setStyleSheet(button_style("secondary"))
        back.clicked.connect(login_page)
        form.addWidget(back, alignment=Qt.AlignmentFlag.AlignCenter)

        form.addStretch()
        root.setCentralWidget(page)

    login_page()
