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
import os
import sounddevice as sd
import numpy as np
import wavio
import librosa
import librosa.display
import matplotlib.pyplot as plt
import soundfile as sf

from quran_data import qari_styles


class AudioPlayer(QWidget):

    def __init__(self):
        super().__init__()

        # Initialize layout
        self.verticalLayout = QVBoxLayout(self)
        self.horizontalLayout = QHBoxLayout()

        # Initialize recording variables
        self.recording = False
        self.recorded_audio = None

        # Create UI components
        self.record_button = QPushButton("Record", self)
        self.record_button.clicked.connect(self.record_audio)
        self.horizontalLayout.addWidget(self.record_button)

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

    def compare_audio(self, recorded_file, reference_file):
        try:
            # Read the recorded and reference audio files
            recorded_audio, recorded_sr = sf.read(recorded_file)
            reference_audio, reference_sr = sf.read(reference_file)

            # Check if the sample rates match
            if recorded_sr != reference_sr:
                print(
                    f"Sample rates do not match. Resampling from {recorded_sr} to {reference_sr}."
                )
                recorded_audio = librosa.resample(
                    y=recorded_audio, orig_sr=recorded_sr, target_sr=reference_sr
                )
                recorded_sr = reference_sr

            # Convert to mono if necessary
            if recorded_audio.ndim > 1:
                recorded_audio = np.mean(recorded_audio, axis=1)
            if reference_audio.ndim > 1:
                reference_audio = np.mean(reference_audio, axis=1)

            # Adjust lengths to match
            min_length = min(len(recorded_audio), len(reference_audio))
            recorded_audio = recorded_audio[:min_length]
            reference_audio = reference_audio[:min_length]

            # Calculate the correlation between the recorded and reference audio
            correlation = np.corrcoef(recorded_audio, reference_audio)[0, 1]
            print(f"Audio correlation: {correlation:.2f}")

            if correlation > 0.8:
                print("The recitation matches well with the reference.")
            else:
                print("The recitation does not match well with the reference.")

        except Exception as e:
            print(f"Error comparing audio: {e}")

    def record_audio(self):
        """Start or stop recording audio."""
        if not self.recording:
            self.recording = True
            self.record_button.setText("Stop Recording")
            self.recorded_audio = None  # Reset recorded audio
            try:
                device_info = sd.query_devices()
                input_device = (
                    None  # Replace with the index of your desired input device
                )

                # Find the first available input device if input_device is not set
                if input_device is None:
                    for i, dev in enumerate(device_info):
                        if dev["max_input_channels"] > 0:
                            input_device = i
                            break

                self.record_thread = sd.InputStream(
                    callback=self.audio_callback, device=input_device
                )
                self.record_thread.start()
            except sd.PortAudioError as e:
                self.recording = False
                self.record_button.setText("Record")
                print(f"PortAudioError: {e}")
            except Exception as e:
                self.recording = False
                self.record_button.setText("Record")
                print(f"Error: {e}")
        else:
            self.recording = False
            self.record_button.setText("Record")
            if self.record_thread:
                self.record_thread.stop()
                self.record_thread.close()

            if self.recorded_audio is not None:
                wavio.write(
                    "recorded_audio.wav", self.recorded_audio, 44100, sampwidth=2
                )
                print("Recording saved as recorded_audio.wav")
            else:
                print("No audio recorded")

    def audio_callback(self, indata, frames, time, status):
        """Callback function to handle audio recording."""
        if status:
            print(status)
        if self.recorded_audio is None:
            self.recorded_audio = np.array(indata)
        else:
            self.recorded_audio = np.append(self.recorded_audio, indata, axis=0)

    def plot_waveform(self, audio_file):
        try:
            audio, sr = librosa.load(audio_file)
            plt.figure(figsize=(10, 4))
            librosa.display.waveshow(audio, sr=sr)
            plt.title("Waveform")
            plt.show()
        except Exception as e:
            print(f"Error plotting waveform: {e}")

    def plot_pitch(self, audio_file):
        try:
            audio, sr = librosa.load(audio_file)
            pitches, magnitudes = librosa.piptrack(y=audio, sr=sr)
            plt.figure(figsize=(10, 4))
            plt.plot(pitches)
            plt.title("Pitch")
            plt.show()
        except Exception as e:
            print(f"Error plotting pitch: {e}")

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
        if self.mediaPlayer.mediaStatus() == QMediaPlayer.LoadedMedia:
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


# Ensure the quran_data module and audio files are correctly placed for the code to run properly.
