from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox, QFormLayout, QFrame, QGraphicsDropShadowEffect
from PyQt6.QtGui import QColor
from PyQt6.QtCore import Qt
from .service import login, create_account

BURGUNDY, DARK_BURGUNDY, GOLD, CREAM, WHITE, BLACK, GRAY = "#900020", "#700018", "#C9A227", "#FFF9EC", "#FFFFFF", "#000000", "#6B6B6B"
FONT = "'Georgia'"
CENTER = Qt.AlignmentFlag.AlignCenter


def add_shadow(widget, blur=18, offset=4):
    effect = QGraphicsDropShadowEffect()
    effect.setBlurRadius(blur)
    effect.setOffset(0, offset)
    effect.setColor(QColor(0, 0, 0, 60))
    widget.setGraphicsEffect(effect)


def button_style(kind="primary"):
    bg, fg, border, hover = {"primary": (f"qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #B01030, stop:1 {BURGUNDY})", WHITE, BURGUNDY, DARK_BURGUNDY), "secondary": (WHITE, BURGUNDY, BURGUNDY, CREAM)}[kind]
    return f"""
        QPushButton {{ background:{bg}; color:{fg}; border:2px solid {border}; border-radius:22px; font-family:{FONT}; font-size:15px; font-weight:bold; padding:6px 14px; }}
        QPushButton:hover {{ background:{hover}; color:{fg}; }}
        QPushButton:disabled {{ background:#E4E0D6; color:#9A9A9A; border:2px solid #CFC9BA; }}
    """


def input_style(size=15):
    return f"""
        QLineEdit {{ background:{CREAM}; color:{BLACK}; border:2px solid #E3D3A0; border-radius:10px; padding:4px 10px; font-family:{FONT}; font-size:{size}px; }}
        QLineEdit:focus {{ border:2px solid {BURGUNDY}; background:{WHITE}; }}
        QLineEdit:read-only {{ background:#F1ECE1; color:#444444; }}
    """


def make_label(text, css, align=CENTER):
    label = QLabel(text)
    label.setAlignment(align)
    label.setStyleSheet(f"{css} background: transparent; border: none;")
    return label


def field_label(text, width):
    label = make_label(text, f"color: {BURGUNDY}; font-family: {FONT}; font-size: 18px; font-weight: bold;", Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
    label.setFixedWidth(width)
    return label


def line_edit(hidden=False):
    entry = QLineEdit()
    entry.setFixedHeight(42)
    entry.setStyleSheet(input_style(18))
    if hidden:
        entry.setEchoMode(QLineEdit.EchoMode.Password)
    return entry


def make_button(text, width, kind, command):
    button = QPushButton(text)
    button.setFixedSize(width, 44)
    button.setStyleSheet(button_style(kind))
    button.clicked.connect(command)
    return button


def show_login(root, success):

    def clear():
        old = root.takeCentralWidget()
        if old:
            old.deleteLater()

    def build_card(width, height, title_text, title_size):
        page = QWidget()
        page.setObjectName("page")
        page.setStyleSheet(f"QWidget#page {{ background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 {BURGUNDY}, stop:0.6 #5E0014, stop:1 #2B000A); }}")
        layout = QVBoxLayout(page)
        layout.setAlignment(CENTER)

        box = QFrame()
        box.setObjectName("card")
        box.setFixedSize(width, height)
        box.setStyleSheet(f"QFrame#card {{ background-color: {WHITE}; border: 3px solid {GOLD}; border-radius: 20px; }}")
        add_shadow(box, 40, 10)

        form = QVBoxLayout(box)
        form.setContentsMargins(55, 28, 55, 28)
        form.setSpacing(10)
        coin = QLabel("💵")
        coin.setAlignment(CENTER)
        coin.setFixedSize(76, 76)
        coin.setStyleSheet(f"background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #C2183F, stop:1 {DARK_BURGUNDY}); border: 3px solid {GOLD}; border-radius: 22px; font-size: 36px;")
        add_shadow(coin, 20, 6)
        form.addWidget(coin, alignment=CENTER)
        form.addWidget(make_label(title_text, f"color: {BURGUNDY}; font-family: {FONT}; font-size: {title_size}px; font-weight: bold;"))
        form.addWidget(make_label("Plan it. Track it. Save it.", f"color: #9A7B1C; font-family: {FONT}; font-size: 15px; font-style: italic;"))
        form.addSpacing(8)
        layout.addWidget(box)
        return page, form

    def login_page():
        clear()
        page, form = build_card(600, 520, "MyBudgetBuddy", 32)
        fields = QFormLayout()
        fields.setHorizontalSpacing(15)
        fields.setVerticalSpacing(12)
        fields.setLabelAlignment(Qt.AlignmentFlag.AlignLeft)

        username, password = line_edit(), line_edit(True)
        for text, entry in (("Username:", username), ("Password:", password)):
            entry.setMinimumWidth(350)
            fields.addRow(field_label(text, 120), entry)

        form.addLayout(fields)
        form.addSpacing(14)

        def submit():
            user = login(username.text().strip(), password.text())
            if user:
                success(user)
            else:
                QMessageBox.warning(root, "Login", "Invalid username or password.")

        for entry in (username, password):
            entry.returnPressed.connect(submit)

        buttons = QVBoxLayout()
        buttons.setSpacing(8)
        buttons.setAlignment(CENTER)
        buttons.addWidget(make_button("Log in", 160, "primary", submit), alignment=CENTER)
        buttons.addWidget(make_button("Register", 160, "secondary", register_page), alignment=CENTER)
        form.addLayout(buttons)
        form.addStretch()
        root.setCentralWidget(page)

    def register_page():
        clear()
        page, form = build_card(600, 600, "Create Account", 30)
        fields = QFormLayout()
        fields.setHorizontalSpacing(10)
        fields.setVerticalSpacing(12)
        fields.setLabelAlignment(Qt.AlignmentFlag.AlignLeft)
        fields.setFormAlignment(Qt.AlignmentFlag.AlignHCenter)

        username, password, confirm = line_edit(), line_edit(True), line_edit(True)
        for text, entry in (("Username:", username), ("Password:", password), ("Confirm Password:", confirm)):
            entry.setFixedWidth(285)
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
        for text, kind, command in (("Create Account", "primary", submit), ("Back to Login", "secondary", login_page)):
            form.addWidget(make_button(text, 190, kind, command), alignment=CENTER)
        form.addStretch()
        root.setCentralWidget(page)

    login_page()