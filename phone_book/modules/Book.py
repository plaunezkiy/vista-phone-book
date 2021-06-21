from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem, QApplication, QHBoxLayout, QVBoxLayout, QPushButton, \
    QHeaderView, QTabWidget, QWidget, QTableView, QAbstractItemView


class Table(QTableWidget):
    data = None

    def __init__(self, letterset, app, *args):
        super(Table, self).__init__(1, 3, *args)
        self.app = app
        self.letterset = letterset
        self.load_data()
        self.setRowCount(len(self.data))

        self.setFont(QFont("Arial", 14))
        self.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.setHorizontalHeaderLabels(["Имя", "Телефон", "Дата рождения"])
        header = self.horizontalHeader()
        self.verticalHeader().setVisible(False)

        header.setSectionResizeMode(0, QHeaderView.Stretch)
        header.setSectionResizeMode(1, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.Stretch)

        self.set_data()

    def update_data(self):
        # update data in the table
        self.load_data()
        self.setRowCount(len(self.data))
        self.set_data()

    def load_data(self):
        # proxies to the app to get data from the db
        self.data = self.app.fetch_records(self.letterset)

    def set_data(self):
        # set data
        for n, row in enumerate(self.data):
            for m, item in enumerate(row):
                if m == 2:
                    item = item.strftime("%d %B %Y")
                record = QTableWidgetItem(item)
                record.setTextAlignment(Qt.AlignCenter)
                self.setItem(n, m, record)


class Book(QWidget):
    def __init__(self, *args):
        super().__init__(*args)
        self.tab_labels = [
            "АБ", "ВГ", "ДЕЁ", "ЖЗИЙ", "КЛ", "МН", "ОП",
            "РС", "ТУ", "ФХ", "ЦЧШЩ", "ЬЫЪЭ", "ЮЯ"
        ]
        self.setupUI()

    def setupUI(self):
        layout = QHBoxLayout()
        self.tabs = QTabWidget()
        #: Uncomment to place tabs on the left
        # tabs.setTabPosition(QTabWidget.West)

        for letterset in self.tab_labels:
            self.tabs.addTab(Table(letterset, self.parent(), self), letterset)

        layout.addWidget(self.tabs)
        self.setLayout(layout)

    def get_seleted_record(self):
        # returns data of the currently selected row
        table = self.tabs.currentWidget()
        record = table.currentIndex()
        row = record.row()
        if row < 0:
            return -1

        return list(table.data[row])

    def update_table(self, tab=None):
        # updates the current tab
        if tab:
            self.tabs.setCurrentIndex(tab)
        table = self.tabs.currentWidget()
        table.update_data()
