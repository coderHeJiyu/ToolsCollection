import os
import sys
from pathlib import Path
from PyQt5.QtGui import QDragEnterEvent, QDropEvent
from PyQt5.QtWidgets import QStackedWidget, QFileDialog
from qfluentwidgets import InfoBar
root_path = Path(__file__).resolve().parents[3]
sys.path.append(str(root_path))
from app.common.more_icon import MoreIcon
from ui_input_widget import Ui_InputWidget


class InputWidget(Ui_InputWidget, QStackedWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.__init_components()

    def __init_components(self):
        self.button_filepath.setIcon(MoreIcon.FILE)

    def read(self):
        _data = {
            "page": self.currentIndex(),
            "text": self.edit_text.toPlainText(),
            "filepath": self.label_filepath.text(),
        }
        return _data

    def write(self, data: dict):
        _tip = self.tr("Drop the file here")
        self.edit_text.setPlainText(data.get("text", ""))
        self.label_filepath.setText(data.get("filepath", _tip))
        if self.label_filepath.text() == "":
            self.label_filepath.setText(_tip)
        self.setCurrentIndex(data.get("page", 0))

    def open_file(self):
        _file, _ = QFileDialog.getOpenFileName(
            self,
            self.tr("Open file"),
            "",
            self.tr("All Files") + " (*)",
        )
        if os.path.isfile(_file):
            self.label_filepath.setText(_file)

    def dragEnterEvent(self, a0: QDragEnterEvent):
        if self.currentIndex() == 0:
            a0.ignore()
            return
        tmp = a0.mimeData().urls()
        if len(tmp) > 1:
            # self.textEdit.setText("请拽入单个文件")
            InfoBar.error(
                title=self.tr("error"),
                content=self.tr("Please drag in a single file!"),
                isClosable=False,
                parent=self,
            )
            a0.ignore()
            return
        tmp = tmp[0].toLocalFile()
        if not os.path.isfile(tmp):
            # self.textEdit.setText("请拽入文件，而不是文件夹")
            InfoBar.error(
                title=self.tr("error"),
                content=self.tr("Please drag in a file, not a folder!"),
                isClosable=False,
                parent=self,
            )
            a0.ignore()
            return
        a0.accept()

    def dropEvent(self, a0: QDropEvent):
        super().dropEvent(a0)
        file = a0.mimeData().urls()[0].toLocalFile()
        self.label_filepath.setText(file)
