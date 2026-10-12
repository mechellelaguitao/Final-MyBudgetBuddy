import sys
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QApplication
from database.database import create_tables
from features.dashboard.view import App


def main():
    app = QApplication(sys.argv)

    # Georgia everywhere (labels, buttons, tables, message boxes, tooltips).
    app.setFont(QFont("Georgia", 10))
    app.setStyleSheet("* { font-family: 'Georgia'; }")

    create_tables()

    window = App()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
