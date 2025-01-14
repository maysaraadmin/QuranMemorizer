from PyQt5.QtWidgets import (
    QMainWindow,
    QPushButton,
    QSlider,
    QComboBox,
    QListWidget,
    QVBoxLayout,
    QHBoxLayout,
    QWidget,
    QLabel,
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QColor
from aya import Aya
from quran_data import suras_names, get_sura, qari_styles
from audio_player import AudioPlayer

font_main = QFont("KFGQPC HAFS Uthmanic Script", 20)
font_second = QFont("Calibri", 14)
font_third = QFont("Calibri", 14)

class QuranMemorizer(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("قاري")
        self.setGeometry(100, 100, 800, 600)

        # Initialize layouts and widgets
        self.init_ui()

        # Initialize qari_style
        self.qari_style = list(qari_styles.keys())[0]

        # Set default sura
        self.current_sura_index = 1  # Start with the first sura (الفاتحة)
        self.default_sura = suras_names[self.current_sura_index]
        self.refresh_sura(self.default_sura)

    def init_ui(self):
        self.root = QWidget(self)
        self.setCentralWidget(self.root)

        self.verticalLayout = QVBoxLayout(self.root)
        self.horizontalLayoutTop = QHBoxLayout()
        self.horizontalLayoutBottom = QHBoxLayout()

        # Label to display the current sura name
        self.lblSuraName = QLabel(self.root)
        self.lblSuraName.setFont(QFont("KFGQPC HAFS Uthmanic Script", 24))
        self.lblSuraName.setAlignment(Qt.AlignCenter)
        self.verticalLayout.addWidget(self.lblSuraName)

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
        self.sld.valueChanged.connect(self.slide_font_size)
        self.horizontalLayoutTop.addWidget(self.sld)

        # Navigation buttons
        self.btnPrev = QPushButton("السورة السابقة", self.root)
        self.btnPrev.setFont(font_second)
        self.btnPrev.clicked.connect(self.prev_sura)
        self.horizontalLayoutTop.addWidget(self.btnPrev)

        self.btnNext = QPushButton("السورة الاحقة", self.root)
        self.btnNext.setFont(font_second)
        self.btnNext.clicked.connect(self.next_sura)
        self.horizontalLayoutTop.addWidget(self.btnNext)

        # Exit button
        self.btnExit = QPushButton("خروج", self.root)
        self.btnExit.setFont(font_second)
        self.btnExit.clicked.connect(self.close)
        self.horizontalLayoutTop.addWidget(self.btnExit)

        self.verticalLayout.addLayout(self.horizontalLayoutTop)

    def refresh_sura(self, sura):
        self.listWidget.clear()
        if sura and sura.strip() and sura in suras_names:
            try:
                # Update the sura name label
                self.lblSuraName.setText(sura)

                # Load the sura content
                sura_list = get_sura(sura)
                for index, aya in enumerate(sura_list, start=1):
                    self.listWidget.addItem(Aya(aya, index, index % 2, Qt.AlignRight))

                # Set the audio player to the current sura
                sura_number = suras_names.index(sura)
                self.audio_player.set_sura(sura_number)
            except Exception as e:
                print(f"Error refreshing sura: {e}")
        else:
            print(f"Sura name '{sura}' not found.")

    def slide_font_size(self):
        self.listWidget.setFont(QFont("KFGQPC HAFS Uthmanic Script", self.sld.value()))

    def set_qari_style(self, qari_style):
        if qari_style in qari_styles:
            self.qari_style = qari_style
            print(f"Qari style set to: {self.qari_style}")
        else:
            print(f"Invalid Qari style: {qari_style}")

    def next_sura(self):
        if self.current_sura_index < len(suras_names) - 1:
            self.current_sura_index += 1
            self.refresh_sura(suras_names[self.current_sura_index])

    def prev_sura(self):
        if self.current_sura_index > 1:
            self.current_sura_index -= 1
            self.refresh_sura(suras_names[self.current_sura_index])