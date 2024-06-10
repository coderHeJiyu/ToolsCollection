import os
from typing import Optional
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtGui import QDragEnterEvent, QDropEvent
from PyQt5.QtCore import QUrl, pyqtSignal
from vlc import MediaPlayer


class VideoPlayWidget(QVideoWidget):
    video_accepted = pyqtSignal(QUrl)

    def __init__(self, parent=None):
        super(QVideoWidget, self).__init__(parent)
        self.player: Optional[MediaPlayer] = None

    def set_player(self, player: MediaPlayer):
        self.player = player
        self.player.set_hwnd(self.winId())

    def dragEnterEvent(self, a0: QDragEnterEvent):
        super().dragEnterEvent(a0)
        if not a0.mimeData().hasUrls():
            return
        file_path = a0.mimeData().urls()[0]
        if not file_path.isLocalFile():
            return
        file_path = file_path.toLocalFile()
        if os.path.isfile(file_path):
            a0.acceptProposedAction()

    def dropEvent(self, a0: QDropEvent):
        super().dropEvent(a0)
        file_url = a0.mimeData().urls()[0]
        self.video_accepted.emit(file_url)
