style_sheet = """
QPushButton {
    border-style: outset;
    border-width: 2px;
    border-radius: 10px;
    border-color: gray;
    padding: 6px;
}

QPushButton:hover {
    background-color: darkgray;
}

QPushButton:pressed {
    background-color: dimgray;
}

QPushButton[class="green"] {
    background-color: GreenYellow;
}
QPushButton[class="green"]:hover {
    background-color: YellowGreen;
}
QPushButton[class="green"]:pressed {
    background-color: OliveDrab;
}

QPushButton[class="red"] {
    background-color: LightCoral;
}
QPushButton[class="red"]:hover {
    background-color: IndianRed;
}
QPushButton[class="red"]:pressed {
    background-color: Brown;
}

QLineEdit {
    border-style: outset;
    border-width: 2px;
    border-radius: 10px;
    border-color: gray;
    padding: 6px;
}

QDateEdit {
    border-style: outset;
    border-width: 2px;
    border-radius: 10px;
    border-color: gray;
    padding: 6px;
}

QDateEdit::drop-down {    
    image: url(icons/down-arrow.svg);
    height: 30px;
    width: 20px;
    subcontrol-origin: content;
    subcontrol-position: right center;
    background-color: white;
    border-radius: 10px;
}
"""