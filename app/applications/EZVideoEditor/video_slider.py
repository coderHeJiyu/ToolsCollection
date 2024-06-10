from PyQt5.QtCore import pyqtSignal
from qfluentwidgets import Slider


class VideoSlider(Slider):
    sliderClicked = pyqtSignal(int)

    def __init__(self, parent=None):
        super().__init__(parent)

    def mousePressEvent(self, QMouseEvent):  # 单击事件
        super().mousePressEvent(QMouseEvent)
        value = QMouseEvent.localPos().x()
        value = round(
            value / self.width() * self.maximum()
        )  # 根据鼠标点击的位置和slider的长度算出百分比
        self.sliderClicked.emit(value)
