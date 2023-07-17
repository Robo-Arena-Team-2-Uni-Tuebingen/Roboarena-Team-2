import sys
from configparser import ConfigParser
from PyQt5.QtCore import QUrl
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtWidgets import QApplication

class MusicPlayer():

    def __init__(self):
        self.music_player = QMediaPlayer()
        self.volume = 50
        self.load_volume_from_file()
        self.music_player.setVolume(50)
        self.music_player.mediaStatusChanged.connect(self.loop_song)

    def load_song(self, filename):
        song = QMediaContent(QUrl.fromLocalFile(filename))
        self.music_player.setMedia(song)

    def play(self):
        self.music_player.play()

    def pause(self):
        self.music_player.pause()

    def set_volume(self, value):
        self.volume = value
        self.music_player.setVolume(self.volume)
        self.save_volume_to_file()

    def loop_song(self, status):
        if status == QMediaPlayer.EndOfMedia:
            self.music_player.setPosition(0)
            self.music_player.play()

    def load_volume_from_file(self):
        config = ConfigParser()
        config.read("config.ini")
        if "Settings" in config and "Volume" in config["Settings"]:
            self.volume = config.getint("Settings", "Volume")

    def save_volume_to_file(self):
        config = ConfigParser()
        config["Settings"] = {"Volume": str(self.volume)}
        with open("config.ini", "w") as config_file:
            config.write(config_file)

if __name__ == "__main__":
    app = QApplication(sys.argv)

    music_player = MusicPlayer()
    music_player.load_song("backgroundmusic/Discord_Amongst_Operatives.mp3")
    music_player.play

    sys.exit(app.exec_())