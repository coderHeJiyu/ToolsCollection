from PyQt5.QtWidgets import QWidget
from qfluentwidgets import FluentIcon
from ui_demo_interface import Ui_DemoInterface


class DemoInterface(Ui_DemoInterface, QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)