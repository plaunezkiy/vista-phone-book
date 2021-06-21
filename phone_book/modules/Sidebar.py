import datetime

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QDialog, QMessageBox, QSizePolicy

from .Dialogs import RecordFormDialog
from .Celebrants import CelebrantsLayout
from .db import create_record, delete_record, update_record


class Sidebar(QWidget):
    def __init__(self, *args):
        super().__init__(*args)
        self.user_icon = QLabel()
        self.user_icon.setPixmap(QIcon("icons/user.svg").pixmap(32, 32))

        self.user_label = QLabel(f"<a href='#'>{self.parent().user_name}</a>")
        self.user_label.setWordWrap(True)
        self.user_label.setAlignment(Qt.AlignCenter)
        self.user_label.setToolTip("Выйти")
        self.user_label.linkActivated.connect(self.parent().logout)

        self.create_record_button = QPushButton(QIcon("icons/add.svg"), "Добавить", self)
        self.create_record_button.clicked.connect(self.create_record)

        self.update_record_button = QPushButton(QIcon("icons/pen.svg"), "Изменить", self)
        self.update_record_button.clicked.connect(self.update_record)

        self.delete_record_button = QPushButton(QIcon("icons/delete.svg"), "Удалить", self)
        self.delete_record_button.clicked.connect(self.delete_record)

        self.gift_icon = QLabel()
        self.gift_icon.setPixmap(QIcon("icons/gift.svg").pixmap(40, 40))
        self.celebrants = CelebrantsLayout(self)
        self.setupUI()

    def setupUI(self):
        layout = QVBoxLayout(self)
        layout.addWidget(self.user_icon, alignment=Qt.AlignCenter)
        layout.addWidget(self.user_label, alignment=Qt.AlignCenter)
        layout.addSpacing(30)
        layout.addWidget(self.create_record_button)
        layout.addWidget(self.update_record_button)
        layout.addWidget(self.delete_record_button)
        layout.addSpacing(30)
        layout.addWidget(self.gift_icon, alignment=Qt.AlignCenter)
        layout.addWidget(self.celebrants, alignment=Qt.AlignCenter)
        layout.addStretch()
        layout.setContentsMargins(0, 0, 0, 0)

        self.setLayout(layout)

    def create_record(self):
        user_id = self.parent().parent().user_id
        dialog = RecordFormDialog(None, self)
        if dialog.exec() == QDialog.Accepted:
            name, phone, bdate = dialog.data
            bdate = datetime.datetime.strptime(bdate, "%d/%m/%Y")
            created = create_record(user_id, name, phone, bdate.strftime("%Y-%m-%d"))
            if not created:
                QMessageBox.warning(
                    self,
                    "Ошибка",
                    "Такой контакт уже есть в книге",
                    QMessageBox.Ok
                )
                return
            tab = 0
            for n, letterset in enumerate(self.parent().parent().book.tab_labels):
                if name[0].upper() in letterset:
                    tab = n
            self.parent().parent().update_table(tab)
            QMessageBox.information(
                self,
                "Контакт записан",
                "Контакт успешно записан в книгу",
                QMessageBox.Ok
            )

    def delete_record(self):
        user_id = self.parent().parent().user_id
        record = self.parent().parent().get_selected_record()
        if record != -1:
            confirm = QMessageBox.warning(
                self,
                "Внимание",
                f"Вы действительно хотите удалить контакт: {record[0]}?",
                QMessageBox.Ok | QMessageBox.Cancel,
            )

            if confirm == QMessageBox.Ok:
                record[2] = record[2].strftime("%Y-%m-%d")
                delete_record(user_id, *record)
                self.parent().parent().update_table()
        else:
            QMessageBox.warning(
                self,
                "Ошибка",
                "Выберите контакт",
                QMessageBox.Ok,
            )

    def update_record(self):
        user_id = self.parent().parent().user_id
        record = self.parent().parent().get_selected_record()
        if record != -1:
            dialog = RecordFormDialog(record, self)
            if dialog.exec() == QDialog.Accepted:
                name, phone, bdate = dialog.data
                bdate = datetime.datetime.strptime(bdate, "%d/%m/%Y")
                record[2] = record[2].strftime("%Y-%m-%d")
                updated = update_record(
                    user_id,
                    record,
                    [name, phone, bdate.strftime("%Y-%m-%d")]
                )
                if not updated:
                    QMessageBox.warning(
                        self,
                        "Ошибка",
                        "Такой контакт уже есть в книге",
                        QMessageBox.Ok
                    )
                    return
                self.parent().parent().update_table()
                QMessageBox.information(
                    self,
                    "Контакт изменен",
                    "Контакт успешно изменен",
                    QMessageBox.Ok
                )
        else:
            QMessageBox.warning(
                self,
                "Ошибка",
                "Выберите контакт",
                QMessageBox.Ok
            )
