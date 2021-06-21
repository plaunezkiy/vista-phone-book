from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMessageBox, QDialogButtonBox, QFormLayout, QLineEdit, QVBoxLayout, QDialog, QDateEdit, QPushButton


class RecordFormDialog(QDialog):
    def __init__(self, data=None, *args):
        super().__init__(*args)
        self.setWindowTitle("Контакт")
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.data = data

        self.setupUI()

    def setupUI(self):
        # Create line edits for data fields
        self.name_entry = QLineEdit()
        self.phone_entry = QLineEdit()
        self.birthdate_picker = QDateEdit(calendarPopup=True)

        if self.data:
            self.name_entry.setText(self.data[0])
            self.phone_entry.setText(self.data[1])
            self.birthdate_picker.setDate(self.data[2])

        # Lay out the data fields
        dialog_form = QFormLayout()
        dialog_form.addRow("Имя:", self.name_entry)
        dialog_form.addRow("Телефон:", self.phone_entry)
        dialog_form.addRow("Дата рождения:", self.birthdate_picker)

        # Add standard buttons to the dialog and connect them
        self.buttons_box = QDialogButtonBox(self)
        self.buttons_box.setOrientation(Qt.Horizontal)

        self.buttons_box.addButton(QPushButton("Сохранить"), QDialogButtonBox.ButtonRole.AcceptRole)
        self.buttons_box.accepted.connect(self.accept)
        self.buttons_box.addButton(QPushButton("Отмена"), QDialogButtonBox.ButtonRole.RejectRole)
        self.buttons_box.rejected.connect(self.reject)

        self.layout.addLayout(dialog_form)
        self.layout.addWidget(self.buttons_box)

    def accept(self):
        self.data = []
        for field in (self.name_entry, self.phone_entry, self.birthdate_picker):
            if not field.text():
                QMessageBox.critical(
                    self,
                    "Ошибка",
                    "Поля не должны быть пустыми",
                )
                self.data = None
                return

            self.data.append(field.text())

        if not self.data:
            return

        super().accept()
