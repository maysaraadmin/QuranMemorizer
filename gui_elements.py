from PyQt5.QtWidgets import (
    QMainWindow,
    QListWidgetItem,
    QPushButton,
    QSlider,
    QComboBox,
    QListWidget,
    QVBoxLayout,
    QHBoxLayout,
    QWidget,
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from aya import Aya
from quran_data import suras_names, get_sura
from audio_player import AudioPlayer

font_main = QFont("KFGQPC HAFS Uthmanic Script", 20)
font_second = QFont("Calibri", 14)
font_third = QFont("Calibri", 14)


class QuranMemorizer(QMainWindow):
    def __init__(self):
        super().__init__()

        self.resize(800, 600)
        self.setWindowTitle("Quran Memorizer")
        self.root = QWidget(self)

        self.verticalLayout = QVBoxLayout(self.root)
        self.horizontalLayoutTop = QHBoxLayout()
        self.horizontalLayoutBottom = QHBoxLayout()

        self.btnSettings = QPushButton(self.root)
        self.btnSettings.setText("|||")
        self.btnSettings.setFont(font_second)
        self.horizontalLayoutTop.addWidget(self.btnSettings)

        self.sld = QSlider(Qt.Horizontal, self.root)
        self.sld.setValue(20)
        self.sld.setRange(15, 40)
        self.horizontalLayoutTop.addWidget(self.sld)

        self.btnExit = QPushButton(self.root)
        self.btnExit.setText("خروج")
        self.btnExit.setFont(font_second)
        self.horizontalLayoutTop.addWidget(self.btnExit)

        self.verticalLayout.addLayout(self.horizontalLayoutTop)

        self.listWidget = QListWidget(self.root)
        self.listWidget.setWordWrap(True)
        self.listWidget.setFont(font_main)
        self.verticalLayout.addWidget(self.listWidget)

        self.audio_player = AudioPlayer()
        self.verticalLayout.addWidget(self.audio_player)

        self.btnNext = QPushButton(self.root)
        self.btnNext.setText("السورة التالية")
        self.btnNext.setFont(font_second)
        self.horizontalLayoutBottom.addWidget(self.btnNext)

        self.cb = QComboBox(self.root)
        self.cb.setFont(font_third)
        self.cb.addItems(suras_names[1:])
        self.cb.setCurrentIndex(0)
        self.horizontalLayoutBottom.addWidget(self.cb)

        self.btnPrev = QPushButton(self.root)
        self.btnPrev.setText("السورة السابقة")
        self.btnPrev.setFont(font_second)
        self.horizontalLayoutBottom.addWidget(self.btnPrev)

        self.verticalLayout.addLayout(self.horizontalLayoutBottom)

        self.setCentralWidget(self.root)

        self.btnNext.clicked.connect(self.next_sura)
        self.btnPrev.clicked.connect(self.prev_sura)
        self.btnExit.clicked.connect(self.close)
        self.cb.currentTextChanged.connect(self.change_sura)
        self.sld.valueChanged.connect(self.slide_font_size)

        self.refresh_sura(suras_names[1])

    def refresh_sura(self, sura):
        self.listWidget.clear()
        sura_list = get_sura(sura)
        for aya in sura_list:
            self.listWidget.addItem(
                Aya(
                    aya,
                    sura_list.index(aya) + 1,
                    sura_list.index(aya) % 2,
                    Qt.AlignRight,
                )
            )
        sura_number = suras_names.index(sura)
        self.audio_player.set_sura(sura_number)

    def next_sura(self):
        current_index = self.cb.currentIndex()
        if current_index < len(suras_names) - 2:
            self.cb.setCurrentIndex(current_index + 1)
            self.refresh_sura(self.cb.currentText())

    def prev_sura(self):
        current_index = self.cb.currentIndex()
        if current_index > 0:
            self.cb.setCurrentIndex(current_index - 1)
            self.refresh_sura(self.cb.currentText())

    def change_sura(self, text):
        self.refresh_sura(text)

    def slide_font_size(self):
        val = self.sld.value()
        self.listWidget.setFont(QFont("KFGQPC HAFS Uthmanic Script", val))
