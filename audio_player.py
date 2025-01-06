from PyQt5.QtWidgets import QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QSlider, QComboBox
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtCore import Qt, QUrl
import os

from quran_data import qari_styles

class AudioPlayer(QWidget):
    def __init__(self):
        super().__init__()

        # Initialize layout
        self.verticalLayout = QVBoxLayout(self)
        self.horizontalLayout = QHBoxLayout()

        # Create UI components
        self.btnPlay = QPushButton("Play", self)
        self.horizontalLayout.addWidget(self.btnPlay)

        self.btnStop = QPushButton("Stop", self)
        self.horizontalLayout.addWidget(self.btnStop)

        self.comboQari = QComboBox(self)
        self.comboQari.addItems(qari_styles.keys())
        self.horizontalLayout.addWidget(self.comboQari)

        self.sldVolume = QSlider(Qt.Horizontal, self)
        self.sldVolume.setValue(50)
        self.sldVolume.setRange(0, 100)
        self.horizontalLayout.addWidget(self.sldVolume)

        self.verticalLayout.addLayout(self.horizontalLayout)

        # Initialize media player
        self.mediaPlayer = QMediaPlayer(None, QMediaPlayer.StreamPlayback)
        self.sldVolume.valueChanged.connect(self.update_volume)

        self.btnPlay.clicked.connect(self.play)
        self.btnStop.clicked.connect(self.stop)
        self.comboQari.currentTextChanged.connect(self.set_audio)

        self.current_sura = None

    def set_sura(self, sura_number):
        self.current_sura = sura_number
        self.set_audio()

    def update_volume(self):
        self.mediaPlayer.setVolume(self.sldVolume.value())

    def set_audio(self):
        if self.current_sura:
            qari = self.comboQari.currentText()
            audio_file = qari_styles.get(qari, {}).get(self.current_sura, None)
            if audio_file and os.path.exists(audio_file):
                self.mediaPlayer.setMedia(QMediaContent(QUrl.fromLocalFile(audio_file)))
                print(f"Setting audio file: {audio_file}")
            else:
                print(f"Audio file not found: {audio_file}")

    def play(self):
        if self.mediaPlayer.mediaStatus() != QMediaPlayer.LoadedMedia:
            self.set_audio()
        if self.mediaPlayer.mediaStatus() == QMediaPlayer.LoadedMedia:
            self.mediaPlayer.play()
            print("Playing audio...")
        else:
            print("Media not loaded")

    def stop(self):
        self.mediaPlayer.stop()
        print("Stopping audio...")