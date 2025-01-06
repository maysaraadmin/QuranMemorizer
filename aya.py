from PyQt5.QtWidgets import QListWidgetItem
from PyQt5.QtGui import QColor
from quran_data import suras_dict

# Define colors as constants
COLOR1 = "lightgray"
COLOR2 = "white"
BESM_ALAH = "بِسْمِ ٱللَّهِ ٱلرَّحْمَٰنِ ٱلرَّحِيمِ "

class Aya(QListWidgetItem):
    def __init__(self, text, number, color_int, align):
        super().__init__()
        self.text = text
        self.number = number
        self.set_text(text, number)
        self.set_color(color_int)
        self.setTextAlignment(align)

    def set_color(self, color_int):
        if not isinstance(color_int, int):
            print(f"Warning: color_int is not an integer value: {color_int}. Defaulting to lightgray.")
            color_int = 1
        self.setBackground(QColor(COLOR1 if color_int else COLOR2))

    def set_text(self, text, number):
        if not isinstance(text, str) or not isinstance(number, int):
            raise ValueError("text must be a string and number must be an integer.")
        self.setText(f"{text} ({number})" if text != BESM_ALAH else text)