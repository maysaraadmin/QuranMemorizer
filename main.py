import sys
from PyQt5.QtWidgets import QApplication
from gui_elements import QuranMemorizer

if __name__ == "__main__":
    app = QApplication(sys.argv)
    quran_memorizer = QuranMemorizer()
    quran_memorizer.show()
    sys.exit(app.exec_())