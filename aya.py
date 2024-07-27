from PyQt5.QtWidgets import QListWidgetItem
from PyQt5.QtGui import QColor
from quran_data import suras_dict

# Define colors as constants
COLOR1 = "lightgray"
COLOR2 = "white"
BESM_ALAH = "بِسْمِ ٱللَّهِ ٱلرَّحْمَٰنِ ٱلرَّحِيمِ "


class Aya(QListWidgetItem):
    def __init__(self, text, number, color_int, align):
        """
        Initialize an Aya item for the QListWidget.

        Args:
            text (str): The text to display.
            number (int): The verse number to display.
            color_int (int): Determines the background color (0 or 1).
            align (int): The text alignment.
        """
        super().__init__()
        self.text = text
        self.number = number
        self.set_text(text, number)
        self.set_color(color_int)
        self.setTextAlignment(align)

    def set_color(self, color_int):
        """
        Set the background color of the item based on color_int.

        Args:
            color_int (int): Determines the background color (0 or 1).
        """
        if not isinstance(color_int, int):
            print(
                f"Warning: color_int is not an integer value: {color_int}. Defaulting to lightgray."
            )
            color_int = 1  # Default to 1 or handle it as needed

        # Convert integer to boolean
        color_int = bool(color_int)
        self.setBackground(QColor(COLOR1 if color_int else COLOR2))

    def set_text(self, text, number):
        """
        Set the text of the item. Append the verse number if it's not BESM_ALAH.

        Args:
            text (str): The text to display.
            number (int): The verse number to append.
        """
        if not isinstance(text, str) or not isinstance(number, int):
            raise ValueError("text must be a string and number must be an integer.")

        if text == BESM_ALAH:
            self.setText(text)
        else:
            self.setText(f"{text} ({number})")
