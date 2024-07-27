from PyQt5.QtWidgets import QListWidgetItem
from PyQt5.QtGui import QColor
from quran_data import suras_dict

color1 = "lightgray"
color2 = "white"
besmAlah = " بِسۡمِ ٱللَّهِ ٱلرَّحۡمَٰنِ ٱلرَّحِيمِ "


class Aya(QListWidgetItem):
    def __init__(self, text, number, colorInt, align):
        super().__init__()
        self.text = text
        self.number = number
        self.set_text(text, number)
        self.set_color(colorInt)
        self.setTextAlignment(align)

    def set_color(self, colorInt):
        self.setBackground(QColor(color1 if colorInt else color2))

    def set_text(self, text, number):
        self.setText(text if text == besmAlah else f"{text} ({number})")
