import sys
from PyQt6.QtWidgets import QApplication
from database.database import load_data
from features.dashboard.view import App


def main():
    users,budget,expenses=load_data()
    app=QApplication(sys.argv)
    window=App(users,budget,expenses)
    window.show()
    sys.exit(app.exec())


if __name__=="__main__":
    main()