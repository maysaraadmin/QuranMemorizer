from PyQt5.QtWidgets import (
    QWidget,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QSlider,
    QComboBox,
)
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtCore import Qt, QUrl
from quran_data import qari_styles
import os


class AudioPlayer(QWidget):
    def __init__(self):
        super().__init__()

        self.verticalLayout = QVBoxLayout(self)
        self.horizontalLayout = QHBoxLayout()

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

        self.mediaPlayer = QMediaPlayer(None, QMediaPlayer.StreamPlayback)
        self.sldVolume.valueChanged.connect(self.update_volume)

        self.btnPlay.clicked.connect(self.play)
        self.btnStop.clicked.connect(self.stop)
        self.comboQari.currentTextChanged.connect(self.set_audio)

        self.current_sura = None

    def update_volume(self):
        volume = self.sldVolume.value()
        self.mediaPlayer.setVolume(volume)

    def set_audio(self):
        if self.current_sura:
            qari = self.comboQari.currentText()
            audio_file = qari_styles.get(qari, {}).get(self.current_sura, None)
            if audio_file:
                normalized_path = os.path.normpath(audio_file)
                if os.path.exists(normalized_path):
                    self.mediaPlayer.setMedia(
                        QMediaContent(QUrl.fromLocalFile(normalized_path))
                    )
                    print(f"Setting audio file: {normalized_path}")
                else:
                    print(f"Audio file not found: {normalized_path}")
            else:
                print(
                    f"No audio file found for sura: {self.current_sura} with qari: {qari}"
                )

    def play(self):
        if (
            self.current_sura
            and self.mediaPlayer.mediaStatus() == QMediaPlayer.LoadedMedia
        ):
            self.mediaPlayer.play()
            print("Playing audio...")
        else:
            self.set_audio()
            if self.mediaPlayer.mediaStatus() == QMediaPlayer.LoadedMedia:
                self.mediaPlayer.play()
                print("Playing audio...")
            else:
                print("Media not loaded")

    def stop(self):
        self.mediaPlayer.stop()
        print("Stopping audio...")

    def set_sura(self, sura_number):
        self.current_sura = sura_number
        self.set_audio()


# Assuming the other classes remain the same, here is the modified main script:
if __name__ == "__main__":
    import sys
    from PyQt5.QtWidgets import QApplication
    from gui_elements import QuranMemorizer

    app = QApplication(sys.argv)
    quran_memorizer = QuranMemorizer()
    quran_memorizer.show()
    sys.exit(app.exec_())
