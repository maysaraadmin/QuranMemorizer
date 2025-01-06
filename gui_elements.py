from PyQt5.QtWidgets import QMainWindow, QPushButton, QSlider, QComboBox, QListWidget, QVBoxLayout, QHBoxLayout, QWidget
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from aya import Aya
from quran_data import suras_names, get_sura, qari_styles
from audio_player import AudioPlayer

font_main = QFont("KFGQPC HAFS Uthmanic Script", 20)
font_second = QFont("Calibri", 14)
font_third = QFont("Calibri", 14)

class QuranMemorizer(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Quran Memorizer")
        self.setGeometry(100, 100, 800, 600)

        # Initialize layouts and widgets
        self.init_ui()

        # Initialize qari_style
        self.qari_style = list(qari_styles.keys())[0]

        # Set default sura
        self.default_sura = suras_names[1]
        self.refresh_sura(self.default_sura)

    def init_ui(self):
        self.root = QWidget(self)
        self.setCentralWidget(self.root)

        self.verticalLayout = QVBoxLayout(self.root)
        self.horizontalLayoutTop = QHBoxLayout()
        self.horizontalLayoutBottom = QHBoxLayout()

        # List widget
        self.listWidget = QListWidget(self.root)
        self.listWidget.setWordWrap(True)
        self.listWidget.setFont(font_main)
        self.verticalLayout.addWidget(self.listWidget)

        # Initialize audio player
        self.audio_player = AudioPlayer()
        self.verticalLayout.addWidget(self.audio_player)

        # Font size slider
        self.sld = QSlider(Qt.Horizontal, self.root)
        self.sld.setValue(20)
        self.sld.setRange(15, 40)
        self.horizontalLayoutTop.addWidget(self.sld)

        # Settings button
        self.btnSettings = QPushButton("|||", self.root)
        self.btnSettings.setFont(font_second)
        self.horizontalLayoutTop.addWidget(self.btnSettings)

        # Exit button
        self.btnExit = QPushButton("خروج", self.root)
        self.btnExit.setFont(font_second)
        self.horizontalLayoutTop.addWidget(self.btnExit)

        self.verticalLayout.addLayout(self.horizontalLayoutTop)

        # Navigation buttons and combobox
        self.btnNext = QPushButton("السورة التالية", self.root)
        self.btnNext.setFont(font_second)
        self.horizontalLayoutBottom.addWidget(self.btnNext)

        self.cb = QComboBox(self.root)
        self.cb.setFont(font_third)
        self.cb.addItems(suras_names)
        self.cb.setCurrentIndex(1)
        self.horizontalLayoutBottom.addWidget(self.cb)

        self.btnPrev = QPushButton("السورة السابقة", self.root)
        self.btnPrev.setFont(font_second)
        self.horizontalLayoutBottom.addWidget(self.btnPrev)

        # Connect signals and slots
        self.btnNext.clicked.connect(self.next_sura)
        self.btnPrev.clicked.connect(self.prev_sura)
        self.btnExit.clicked.connect(self.close)
        self.cb.currentTextChanged.connect(self.change_sura)
        self.sld.valueChanged.connect(self.slide_font_size)

    def refresh_sura(self, sura):
        self.listWidget.clear()
        if sura and sura.strip() and sura in suras_names:
            try:
                sura_list = get_sura(sura)
                for index, aya in enumerate(sura_list, start=1):
                    self.listWidget.addItem(Aya(aya, index, index % 2, Qt.AlignRight))
                sura_number = suras_names.index(sura)
                self.audio_player.set_sura(sura_number)
            except Exception as e:
                print(f"Error refreshing sura: {e}")
        else:
            print(f"Sura name '{sura}' not found.")

    def next_sura(self):
        current_index = self.cb.currentIndex()
        if current_index < len(suras_names) - 1:
            self.cb.setCurrentIndex(current_index + 1)
            self.refresh_sura(self.cb.currentText())

    def prev_sura(self):
        current_index = self.cb.currentIndex()
        if current_index > 0:
            self.cb.setCurrentIndex(current_index - 1)
            self.refresh_sura(self.cb.currentText())

    def change_sura(self, text):
        if text and text.strip():
            self.refresh_sura(text)

    def slide_font_size(self):
        self.listWidget.setFont(QFont("KFGQPC HAFS Uthmanic Script", self.sld.value()))

    def set_qari_style(self, qari_style):
        if qari_style in qari_styles:
            self.qari_style = qari_style
            print(f"Qari style set to: {self.qari_style}")
        else:
            print(f"Invalid Qari style: {qari_style}")