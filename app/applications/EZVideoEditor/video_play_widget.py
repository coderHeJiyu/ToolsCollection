import os
from typing import Optional
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtGui import (
    QDragEnterEvent,
    QDropEvent,
    QResizeEvent,
    QShowEvent,
    QHideEvent,
)
from PyQt5.QtCore import QUrl, pyqtSignal, Qt, QTimer
from PyQt5.QtWidgets import QWidget
from vlc import MediaPlayer


class VideoPlayWidget(QWidget):
    video_accepted = pyqtSignal(QUrl)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.player: Optional[MediaPlayer] = None
        self.video_widget = OverlayWidget()
        self.video_widget.video_accepted.connect(self.video_accepted.emit)
        # 每100毫秒检查一次位置
        self.old_pos = self.pos()
        self.timer = QTimer()
        self.timer.timeout.connect(self.check_position)

    def set_player(self, player: MediaPlayer):
        self.player = player
        self.player.set_hwnd(self.video_widget.winId())

    def check_position(self):
        new_pos = self.mapToGlobal(self.pos())
        if new_pos != self.old_pos:
            self.old_pos = new_pos
            self.on_position_changed()

    def on_position_changed(self):
        global_pos = self.mapToGlobal(self.pos())
        x, y = global_pos.x() - 11, global_pos.y() - 11
        self.video_widget.move(x, y)

    def resizeEvent(self, a0: QResizeEvent):
        super().resizeEvent(a0)
        self.video_widget.resize(self.size())

    def showEvent(self, a0: QShowEvent):
        super().showEvent(a0)
        self.timer.start(100)
        self.video_widget.show()

    def hideEvent(self, a0: QHideEvent):
        super().hideEvent(a0)
        self.timer.stop()
        self.video_widget.hide()


class OverlayWidget(QVideoWidget):
    video_accepted = pyqtSignal(QUrl)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAcceptDrops(True)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setStyleSheet("background-color: Black;")

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
