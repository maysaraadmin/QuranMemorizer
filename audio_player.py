from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QComboBox
from PyQt5.QtCore import QUrl
from quran_data import qari_styles  # Import qari_styles from quran_data


class AudioPlayer(QWidget):
    def __init__(self):
        super().__init__()
        self.player = QMediaPlayer()

        self.layout = QVBoxLayout(self)

        self.qari_selector = QComboBox(self)
        self.qari_selector.addItems(qari_styles.keys())  # Use keys from qari_styles
        self.qari_selector.currentTextChanged.connect(self.change_qari)
        self.layout.addWidget(self.qari_selector)

        self.play_button = QPushButton("Play", self)
        self.play_button.clicked.connect(self.play_audio)
        self.layout.addWidget(self.play_button)

        self.stop_button = QPushButton("Stop", self)
        self.stop_button.clicked.connect(self.stop_audio)
        self.layout.addWidget(self.stop_button)

        self.current_qari = self.qari_selector.currentText()

    def change_qari(self, qari):
        self.current_qari = qari

    def set_audio(self, sura_number):
        audio_path = qari_styles[self.current_qari][sura_number]
        self.player.setMedia(QMediaContent(QUrl.fromLocalFile(audio_path)))

    def play_audio(self):
        self.player.play()

    def stop_audio(self):
        self.player.stop()
