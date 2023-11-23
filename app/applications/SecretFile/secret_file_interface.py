import os
from PyQt5.QtCore import QThreadPool
from PyQt5.QtGui import QDragEnterEvent, QDropEvent
from PyQt5.QtWidgets import QFileDialog, QWidget
from qfluentwidgets import FluentIcon
from ui_secret_file_interface import Ui_SecretFileInterface
from single_task_widget import SingleTaskListWidgetItem
from secret_file_threads import EncodeThread, DecodeThread


class SecretFileInterface(Ui_SecretFileInterface, QWidget):
    def __init__(self, parent=None, src: str = None, password: str = None):
        super().__init__(parent)
        self.setupUi(self)
        self.button_open_file.setIcon(FluentIcon.FOLDER)
        self.src: str = src
        self.password: str = password
        self.threadpool = QThreadPool()
        self.__button_lock()
        self.__check_file()
        if self.password:
            self.edit_password.setText(self.password)

    def __button_lock(self):
        """
        锁定“加密”和“解密”按钮
        """
        self.button_encode.setEnabled(False)
        self.button_decode.setEnabled(False)

    def __check_file(self):
        if not self.src:
            self.edit_file.clear()
            return
        self.edit_file.setPlainText(self.src)
        file_type = os.path.splitext(self.src)[-1]
        if file_type != ".hlx":
            self.button_encode.setEnabled(True)
        else:
            self.button_encode.setEnabled(True)
            self.button_decode.setEnabled(True)

    def __start_task(self, mode: int):
        """
        开始任务
        """
        item = SingleTaskListWidgetItem(self.list_widget)
        self.list_widget.addItem(item)
        self.list_widget.setItemWidget(item, item.widget)
        item.set_src(os.path.basename(self.src))
        item.set_progress(0)
        if mode == 0:
            _task = EncodeThread(self.src, self.password)
        else:
            _task = DecodeThread(self.src, self.password)
        _task.signals.status_sig.connect(item.set_state)
        _task.signals.process_sig.connect(item.set_progress)
        item.widget.pause_sig.connect(_task.pause_trigger)
        item.widget.remove_sig.connect(_task.quit)
        item.widget.remove_sig.connect(
            lambda: self.list_widget.takeItem(self.list_widget.row(item))
        )
        self.threadpool.start(_task)

    def open_file(self):
        """
        “打开”按钮的事件
        """
        # 界面更新
        self.__button_lock()
        # 数据更新(依托于文件选择器)
        self.src, _ = QFileDialog.getOpenFileName(None, "打开文件", "./", "全部文件(*.*)")
        # 界面更新
        self.__check_file()

    def encode(self):
        """
        “加密”按钮的事件
        """
        self.password = self.edit_password.text()
        self.__start_task(0)

    def decode(self):
        """
        “解密”按钮的事件
        """
        self.password = self.edit_password.text()
        self.__start_task(1)

    def dragEnterEvent(self, a0: QDragEnterEvent):
        super().dragEnterEvent(a0)
        if not a0.mimeData().hasUrls():
            return
        folder_path = a0.mimeData().urls()[0]
        if not folder_path.isLocalFile():
            return
        folder_path = folder_path.toLocalFile()
        if os.path.isfile(folder_path):
            a0.acceptProposedAction()

    def dropEvent(self, a0: QDropEvent):
        # 界面更新
        self.__button_lock()
        # 数据更新
        self.src = a0.mimeData().urls()[0].toLocalFile()
        # 界面更新
        self.__check_file()
