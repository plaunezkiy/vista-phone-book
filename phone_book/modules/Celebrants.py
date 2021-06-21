from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel
from .db import get_celebrants


class CelebrantsLayout(QWidget):
    def __init__(self, *args):
        super().__init__(*args)
        self.setFont(QFont("Arial", 10))
        self.layout = QVBoxLayout()
        self.setupUI()

    def setupUI(self):
        # get celebrants(именинники) for the next 7 days
        celebrants = self.get_celebrants()
        for person in celebrants:
            label = QLabel(f"<a href='#'>{person[0]}</a>")
            # tooltip to let the user know when the birthday is
            label.setToolTip(person[1].strftime("%d %B"))
            self.layout.addWidget(label)
        self.setLayout(self.layout)

    def get_celebrants(self):
        # fetch celebrants from the db
        user_id = self.parent().parent().user_id
        return get_celebrants(user_id)
