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
from quran_data import suras_names, get_sura, qari_styles
from audio_player import AudioPlayer
import os

font_main = QFont("KFGQPC HAFS Uthmanic Script", 20)
font_second = QFont("Calibri", 14)
font_third = QFont("Calibri", 14)


class QuranMemorizer(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Quran Memorizer")
        self.setGeometry(100, 100, 800, 600)  # Set initial window size

        # Initialize layouts and widgets
        self.init_ui()

        # Initialize qari_style
        self.qari_style = list(qari_styles.keys())[0]  # Default to the first Qari style

        # Set default sura
        self.default_sura = suras_names[1]  # Correctly set default sura to the second
        self.refresh_sura(self.default_sura)

    def init_ui(self):
        """Initialize the UI components."""
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
        self.cb.setCurrentIndex(1)  # Set default selection to the second sura
        self.horizontalLayoutBottom.addWidget(self.cb)

        self.btnPrev = QPushButton("السورة السابقة", self.root)
        self.btnPrev.setFont(font_second)
        self.horizontalLayoutBottom.addWidget(self.btnPrev)

        self.btnCompare = QPushButton("Compare Recitation", self.root)
        self.btnCompare.setFont(font_second)
        self.horizontalLayoutBottom.addWidget(self.btnCompare)

        self.verticalLayout.addLayout(self.horizontalLayoutBottom)

        # Connect signals and slots
        self.btnNext.clicked.connect(self.next_sura)
        self.btnPrev.clicked.connect(self.prev_sura)
        self.btnExit.clicked.connect(self.close)
        self.cb.currentTextChanged.connect(self.change_sura)
        self.sld.valueChanged.connect(self.slide_font_size)
        self.btnCompare.clicked.connect(self.compare_recitation)

    def refresh_sura(self, sura):
        """Refresh the sura displayed in the list widget."""
        self.listWidget.clear()
        print(f"Refreshing sura: '{sura}'")  # Debug print
        try:
            if not sura or sura.strip() == "" or sura not in suras_names:
                print(f"Sura name '{sura}' not found.")
                return

            sura_list = get_sura(sura)
            if not sura_list:
                print(f"No verses found for sura: {sura}")
                return

            for index, aya in enumerate(sura_list, start=1):
                self.listWidget.addItem(
                    Aya(
                        aya,
                        index,
                        index % 2,
                        Qt.AlignRight,
                    )
                )
            sura_number = suras_names.index(sura)
            self.audio_player.set_sura(sura_number)
        except Exception as e:
            print(f"Error refreshing sura: {e}")

    def next_sura(self):
        """Navigate to the next sura."""
        current_index = self.cb.currentIndex()
        if current_index < len(suras_names) - 1:
            self.cb.setCurrentIndex(current_index + 1)
            self.refresh_sura(self.cb.currentText())

    def prev_sura(self):
        """Navigate to the previous sura."""
        current_index = self.cb.currentIndex()
        if current_index > 0:
            self.cb.setCurrentIndex(current_index - 1)
            self.refresh_sura(self.cb.currentText())

    def change_sura(self, text):
        """Change the displayed sura based on combobox selection."""
        if text and text.strip():
            print(f"Selected sura: '{text}'")  # Debug print
            self.refresh_sura(text)
        else:
            print("Selected sura is empty or invalid.")

    def slide_font_size(self):
        """Adjust the font size of the list widget."""
        val = self.sld.value()
        self.listWidget.setFont(QFont("KFGQPC HAFS Uthmanic Script", val))

    def compare_recitation(self):
        """Compare the user's recitation with the reference recitation."""
        current_sura_name = self.cb.currentText()

        if not current_sura_name or current_sura_name not in suras_names:
            print("Invalid sura selected.")
            return

        sura_index = suras_names.index(current_sura_name)

        # Determine the Qari style and the corresponding audio file
        audio_files = qari_styles.get(self.qari_style, {})
        reference_file = audio_files.get(sura_index)

        if not reference_file:
            print("Reference audio file not found for the selected Qari and Sura.")
            return

        recorded_file = "recorded_audio.wav"

        # Check if the recorded file exists
        if not os.path.exists(recorded_file):
            print(f"Recorded audio file '{recorded_file}' not found.")
            return

        try:
            self.audio_player.compare_audio(recorded_file, reference_file)
        except Exception as e:
            print(f"Error comparing recitation: {e}")

    def set_qari_style(self, qari_style):
        """Set the Qari style."""
        if qari_style in qari_styles:
            self.qari_style = qari_style
            print(f"Qari style set to: {self.qari_style}")
        else:
            print(f"Invalid Qari style: {qari_style}")
