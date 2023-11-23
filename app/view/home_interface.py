from PyQt5.QtWidgets import QWidget, QHBoxLayout
from PyQt5.QtCore import Qt
from qfluentwidgets import SubtitleLabel, setFont


class HomeInterface(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setObjectName("homeInterface")
        self.setWindowTitle(self.tr("Home"))
        self.label = SubtitleLabel(self.tr("Home"), self)
        setFont(self.label, 24)
        self.hBoxLayout = QHBoxLayout(self)
        self.label.setAlignment(Qt.AlignCenter)
        self.hBoxLayout.addWidget(self.label, 1, Qt.AlignCenter)
