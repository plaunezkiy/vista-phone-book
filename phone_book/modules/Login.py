import json
import re
from datetime import datetime

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import (QWidget, QDialog, QLabel, QPushButton, QLineEdit,
                             QMessageBox, QFormLayout, QVBoxLayout,
                             QHBoxLayout, QCheckBox, QDateEdit)

from .db import create_user, authenticate


class LoginDialog(QWidget):
    _password_shown = False
    _creds_file = "files/login.json"

    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.setFixedSize(400, 300)
        self.setWindowTitle("Войти в книгу")

        self.login_name_entry = QLineEdit()
        self.login_name_entry.setMinimumWidth(250)
        self.login_name_entry.setPlaceholderText("Имя")

        self.login_password_entry = QLineEdit()
        self.login_password_entry.setMinimumWidth(250)
        self.login_password_entry.setEchoMode(QLineEdit.Password)
        self.login_password_entry.setPlaceholderText("Пароль")
        self.remember_checkbox = QCheckBox("Запомнить меня")

        self.load_creds()
        self.setupUI()

    def setupUI(self):
        """Set up the widgets for the login GUI."""
        header_label = QLabel("Авторизация")
        header_label.setFont(QFont("Arial", 20))
        header_label.setAlignment(Qt.AlignCenter)

        login_form = QFormLayout()
        login_form.setLabelAlignment(Qt.AlignLeft)
        login_form.addRow(self.login_name_entry)
        login_form.addRow(self.login_password_entry)

        connect_button = QPushButton("Войти")
        connect_button.setProperty("class", "green")
        connect_button.clicked.connect(self.login)

        register_button = QPushButton("Регистрация")
        register_button.clicked.connect(self.create_new_user)

        cancel_button = QPushButton("Отмена")
        cancel_button.setProperty("class", "red")
        cancel_button.clicked.connect(exit)

        buttons = QHBoxLayout()
        buttons.addWidget(connect_button)
        buttons.addWidget(register_button)
        buttons.addWidget(cancel_button)

        show_password_checkbox = QCheckBox("Показать пароль")
        show_password_checkbox.toggled.connect(self.show_password)

        forgot_password = QLabel("<a href='#'>Забыли пароль?</a>")
        forgot_password.linkActivated.connect(self.reset_password)

        controls_layout = QVBoxLayout()
        controls_layout.setAlignment(Qt.AlignCenter)
        controls_layout.addWidget(self.remember_checkbox)
        controls_layout.addWidget(show_password_checkbox)
        controls_layout.addWidget(forgot_password)

        main_v_box = QVBoxLayout()
        main_v_box.setAlignment(Qt.AlignTop)

        main_v_box.addWidget(header_label)
        main_v_box.addSpacing(10)
        main_v_box.addLayout(login_form)

        main_v_box.addLayout(buttons)
        main_v_box.addLayout(controls_layout)

        self.setLayout(main_v_box)

    def load_creds(self):
        """loads credentials from a json file"""
        with open(self._creds_file, "r", encoding="utf-8") as json_file:
            data = json.load(json_file)
            name = data["name"]
            password = data["password"]
            if name and password:
                self.login_name_entry.setText(name)
                self.login_password_entry.setText(password)
            self.remember_checkbox.setChecked(True)

    def save_creds(self):
        """stores valid credentials in a json file"""
        with open(self._creds_file, "w", encoding="utf-8") as json_file:
            data = {
                "name": self.login_name_entry.text(),
                "password": self.login_password_entry.text()
            }
            json.dump(data, json_file)

    def show_password(self):
        if self._password_shown:
            self.login_password_entry.setEchoMode(QLineEdit.Password)
        else:
            self.login_password_entry.setEchoMode(QLineEdit.Normal)
        self._password_shown = not self._password_shown

    def reset_entries(self):
        self.login_name_entry.setText("")
        self.login_password_entry.setText("")
        self.remember_checkbox.setChecked(False)

    def reset_password(self):
        reset_dialog = QDialog(self)
        reset_dialog.setWindowTitle("Сбросить пароль")

        header_label = QLabel("Сброс пароля")
        header_label.setFont(QFont("Arial", 20))
        header_label.setAlignment(Qt.AlignCenter)

        email_entry = QLineEdit()
        email_entry.setPlaceholderText("Email")
        dialog_form = QFormLayout()
        dialog_form.addRow(email_entry)

        reset_button = QPushButton("Сбросить")
        # replace for reset functionality
        reset_button.clicked.connect(lambda: self.validate_email(email_entry.text()))

        cancel_button = QPushButton("Отмена")
        cancel_button.setProperty("class", "red")
        cancel_button.clicked.connect(reset_dialog.close)

        buttons_layout = QHBoxLayout()
        buttons_layout.addWidget(reset_button)
        buttons_layout.addWidget(cancel_button)

        dialog_v_box = QVBoxLayout()
        dialog_v_box.setAlignment(Qt.AlignTop)

        dialog_v_box.addWidget(header_label)
        dialog_v_box.addSpacing(10)
        dialog_v_box.addLayout(dialog_form, 1)
        dialog_v_box.addLayout(buttons_layout)
        reset_dialog.setLayout(dialog_v_box)
        reset_dialog.show()

    def login(self):
        name = self.login_name_entry.text()
        password = self.login_password_entry.text()
        user = authenticate(name, password)
        if user:
            self.parent.login(user)
            if self.remember_checkbox.isChecked():
                self.save_creds()
            self.reset_entries()
            self.close()
        else:
            QMessageBox.warning(
                self,
                "Ошибка",
                "Пользователь не найден"
            )

    def create_new_user(self):
        """set up the dialog box for the user to create a new user account."""
        self.new_user_dialog = QDialog(self)
        self.new_user_dialog.setWindowTitle("Регистрация")
        header_label = QLabel("Регистрация")
        header_label.setFont(QFont("Arial", 20))
        header_label.setAlignment(Qt.AlignCenter)

        # entries
        self.new_name_entry = QLineEdit()
        self.new_name_entry.setPlaceholderText("Имя")
        self.new_email_entry = QLineEdit()
        self.new_email_entry.setPlaceholderText("Email")

        self.new_password_entry = QLineEdit()
        self.new_password_entry.setEchoMode(QLineEdit.Password)
        self.new_password_entry.setPlaceholderText("Пароль")
        self.new_confirm_password_entry = QLineEdit()
        self.new_confirm_password_entry.setEchoMode(QLineEdit.Password)
        self.new_confirm_password_entry.setPlaceholderText("Пароль еще раз")

        self.birthdate_picker = QDateEdit(calendarPopup=True)

        # form
        dialog_form = QFormLayout()
        dialog_form.addRow(self.new_name_entry)
        dialog_form.addRow(self.new_email_entry)
        dialog_form.addRow("Дата рождения:", self.birthdate_picker)
        dialog_form.addRow(self.new_password_entry)
        dialog_form.addRow(self.new_confirm_password_entry)

        create_acct_button = QPushButton("Зарегестрироваться")
        create_acct_button.setProperty("class", "green")
        create_acct_button.clicked.connect(self.accept_user_info)
        cancel_button = QPushButton("Отмена")
        cancel_button.setProperty("class", "red")
        cancel_button.clicked.connect(self.new_user_dialog.close)
        buttons_layout = QHBoxLayout()
        buttons_layout.addWidget(create_acct_button)
        buttons_layout.addWidget(cancel_button)

        dialog_v_box = QVBoxLayout()
        dialog_v_box.setAlignment(Qt.AlignTop)

        dialog_v_box.addWidget(header_label)
        dialog_v_box.addSpacing(10)
        dialog_v_box.addLayout(dialog_form, 1)
        dialog_v_box.addLayout(buttons_layout)

        self.new_user_dialog.setLayout(dialog_v_box)
        self.new_user_dialog.show()

    def accept_user_info(self):
        """verify that the user's passwords match and the email is valid. If so, create an account"""
        # gather data
        name = self.new_name_entry.text()
        email = self.new_email_entry.text()
        bdate = self.birthdate_picker.text()
        bdate = self.reformat_date(bdate)
        password = self.new_password_entry.text()
        confirm_password = self.new_confirm_password_entry.text()

        # validate email
        self.validate_email(email)
        if password != confirm_password:
            # password do not match
            QMessageBox.warning(
                self,
                "Ошибка",
                "Пароли не совпадают, попробуйте еще раз",
                QMessageBox.Close
            )
        else:
            # if passwords match, create user
            exists = create_user(name, email, bdate, password)
            # if the entry already exists, inform the user
            if exists:
                QMessageBox.warning(
                    self,
                    "Ошибка",
                    "Пользователь уже существует",
                    QMessageBox.Close
                )
            else:
                # successful reg
                QMessageBox.information(
                    self,
                    "Регистрация успешна",
                    "Пользователь зарегестрирован",
                    QMessageBox.Close
                )
                self.new_user_dialog.close()
            self.show()

    def validate_email(self, email):
        # simple regex to validate the email
        regex = r'^[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,}'
        if re.search(regex, email):
            return
        else:
            QMessageBox.warning(
                self,
                "Ошибка",
                "Проверьте введенный email.",
                QMessageBox.Close
            )

    def reformat_date(self, date):
        """convert date to db compatible format"""
        f = "%Y-%m-%d"
        date = datetime.strptime(date, "%d/%m/%Y")
        return date.strftime(f)
