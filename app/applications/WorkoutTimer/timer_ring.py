import winsound
from PyQt5.QtCore import QTimer, pyqtSignal, QRunnable, QThreadPool
from qfluentwidgets import ProgressRing

BEEP_FREQUENCY = 1500
BEEP_DURATION = 1000


class BeepThread(QRunnable):
    def __init__(self):
        super().__init__()

    def run(self):
        winsound.Beep(BEEP_FREQUENCY, BEEP_DURATION)


class TimerRing(ProgressRing):
    time_up = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(200, 200)
        self.setTextVisible(True)
        self.valueChanged.connect(self.__value2text)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.__decrement)
        self.timer.setInterval(1000)
        self.thread_pool = QThreadPool()

    def __beep(self):
        self.thread_pool.start(BeepThread())

    def __decrement(self):
        self.setValue(self.value() - 1)

    def __value2text(self, value: int):
        if value >= 3600:
            self.setFormat(
                f"{value // 3600:02d}:{value % 3600 // 60:02d}:{value % 60:02d}"
            )
        else:
            self.setFormat(f"{value // 60:02d}:{value % 60:02d}")
        if value == 0:
            self.timer.stop()
            self.time_up.emit()
            self.__beep()

    def start(self):
        """
        开始计时
        """
        if self.value() != self.maximum():
            return False
        self.timer.start()
        return True

    def stop(self):
        """
        停止计时
        """
        if self.timer.isActive():
            self.timer.stop()

    def reset_secs(self, seconds: int):
        """
        重置秒数
        :param seconds: 秒数
        """
        if seconds < 0:
            return
        self.stop()
        if seconds == 0:
            self.setMaximum(1)
            self.setValue(1)
            self.setFormat("∞")
            return
        self.setMaximum(seconds)
        self.setValue(seconds)
