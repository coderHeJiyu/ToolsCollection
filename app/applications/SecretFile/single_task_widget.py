from PyQt5.QtWidgets import QWidget, QListWidgetItem
from PyQt5.QtCore import pyqtSignal, QObject
from qfluentwidgets import FluentIcon
from secret_file_threads import CipherSignals
from ui_single_task_widget import Ui_SingleTaskWidget


class Translator(QObject):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.state_dict = {
            CipherSignals.ENCODE_PROCESS: self.tr("encoding..."),
            CipherSignals.DECODE_PROCESS: self.tr("decoding..."),
            CipherSignals.FINISHED: self.tr("finished"),
            CipherSignals.PW_ERROR: self.tr("wrong password"),
            CipherSignals.FILE_EXIST: self.tr("file already exists"),
            CipherSignals.FILE_BROKEN: self.tr("file is broken"),
        }


class SingleTaskListWidgetItem(QListWidgetItem):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.widget = SingleTaskWidget()
        self.setSizeHint(self.widget.sizeHint())
        self.__translate = Translator()

    def set_src(self, src: str):
        """
        设置源文件路径
        """
        self.widget.label_src.setText(src)

    def set_progress(self, progress: int):
        """
        设置进度条
        """
        self.widget.progressBar.setValue(progress)

    def set_state(self, state: int):
        """
        设置状态
        """
        self.widget.label_state.setText(self.__translate.state_dict[state])
        if state > 1:
            self.widget.pushButton.setEnabled(False)
            self.widget.pushButton_2.setEnabled(True)


class SingleTaskWidget(Ui_SingleTaskWidget, QWidget):
    pause_sig = pyqtSignal()
    remove_sig = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.pushButton.setIcon(FluentIcon.PAUSE)
        self.pushButton_2.setIcon(FluentIcon.CLOSE)
        self.is_paused = False
        self.row = 0

    def pause_toggled(self):
        """
        暂停/继续
        """
        if self.is_paused:
            self.pushButton.setIcon(FluentIcon.PAUSE)
            self.pushButton.setToolTip(self.tr("pause"))
            self.is_paused = False
            self.pushButton_2.setEnabled(False)
        else:
            self.pushButton.setIcon(FluentIcon.PLAY)
            self.pushButton.setToolTip(self.tr("continue"))
            self.is_paused = True
            self.pushButton_2.setEnabled(True)
        self.pause_sig.emit()

    def remove(self):
        """
        移除
        """
        self.remove_sig.emit()
