import sys

from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QHBoxLayout, QWidget, QLabel, QToolTip
from PyQt5.QtCore import Qt
from modules.Login import LoginDialog
from modules.Book import Book
from modules.Sidebar import Sidebar
from modules.db import get_records
from modules.StyleSheet import style_sheet


class PhoneBook(QMainWindow):
    user_name = None
    user_email = None
    user_id = None

    def __init__(self):
        super().__init__()
        self.setMinimumSize(1100, 800)
        self.move(QApplication.desktop().screen().rect().center() - self.rect().center())
        self.setWindowTitle("Телефонная книга")

        self.centralWidget = QWidget()
        self.setCentralWidget(self.centralWidget)
        self.layout = QHBoxLayout()
        self.centralWidget.setLayout(self.layout)

        self.login_dialog = LoginDialog(self)
        self.login_dialog.show()

    def setupUI(self):
        self.book = Book(self)
        self.sidebar = Sidebar(self)

        self.layout.addWidget(self.book)
        self.layout.addWidget(self.sidebar)

    def login(self, user_dict):
        self.user_name = user_dict['name']
        self.user_email = user_dict['email']
        self.user_id = user_dict['user_id']

        self.setupUI()
        self.show()

    def logout(self):
        self.user_name = None
        self.user_email = None
        self.user_id = None
        self.reset()
        self.login_dialog.show()

    def reset(self):
        while self.layout.count():
            child = self.layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
        self.close()

    def fetch_records(self, letterset):
        return get_records(self.user_id, letterset)

    def get_selected_record(self):
        return self.book.get_seleted_record()

    def update_table(self, tab=None):
        self.book.update_table(tab)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.processEvents()
    app.setStyleSheet(style_sheet)
    app.setFont(QFont("Arial", 11))

    book = PhoneBook()

    sys.exit(app.exec_())
