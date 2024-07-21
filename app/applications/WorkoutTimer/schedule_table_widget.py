from PyQt5.QtWidgets import QTableWidgetItem, QWidget, QHBoxLayout
from PyQt5.QtCore import QTime
from qfluentwidgets import (
    TableWidget,
    TimePicker,
    TransparentToolButton,
    FluentIcon,
)


class ScheduleTableWidget(TableWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.horizontalHeader().setVisible(False)

    def __new_buttons(self, row: int):
        # up
        _button_up = TransparentToolButton(self)
        _button_up.setIcon(FluentIcon.UP)
        _button_up.setToolTip(self.tr("Move up"))
        _button_up.clicked.connect(lambda: self.move_row(row, row - 1))
        # down
        _button_down = TransparentToolButton(self)
        _button_down.setIcon(FluentIcon.DOWN)
        _button_down.setToolTip(self.tr("Move down"))
        _button_down.clicked.connect(lambda: self.move_row(row, row + 1))
        # remove
        _button_remove = TransparentToolButton(self)
        _button_remove.setIcon(FluentIcon.REMOVE)
        _button_remove.setToolTip(self.tr("Remove"))
        _button_remove.clicked.connect(lambda: self.remove_row(row))
        # widget
        _widget_button = QWidget(self)
        _h_layout = QHBoxLayout(_widget_button)
        _h_layout.addWidget(_button_up)
        _h_layout.addWidget(_button_down)
        _h_layout.addWidget(_button_remove)
        return _widget_button

    def add_empty_row(self):
        """
        添加空行
        """
        self.add_row(self.tr("New Activity"))

    def add_row(self, activity: str, time: int = 0):
        """
        添加行
        :param activity: 活动
        :param time: 时间（秒）
        """
        _current_row = self.rowCount()
        self.insertRow(_current_row)
        # activity
        self.setItem(_current_row, 0, QTableWidgetItem(activity))
        # time
        _time_picker = TimePicker(self)
        _time_picker.setSecondVisible(True)
        _time_picker.setTime(QTime(0, 0).addSecs(time))
        self.setCellWidget(_current_row, 1, _time_picker)
        # operation
        _widget = self.__new_buttons(_current_row)
        self.setCellWidget(_current_row, 2, _widget)
        self.horizontalHeader().setVisible(True)
        self.resizeColumnsToContents()
        self.resizeRowsToContents()

    def move_row(self, source_row: int, target_row: int):
        """
        移动行
        :param source_row: 源行
        :param target_row: 目标行
        """
        if target_row < 0 or target_row >= self.rowCount():
            return
        _source_activity = self.item(source_row, 0).text()
        _source_time = self.cellWidget(source_row, 1).getTime()
        self.item(source_row, 0).setText(self.item(target_row, 0).text())
        self.cellWidget(source_row, 1).setTime(self.cellWidget(target_row, 1).getTime())
        self.item(target_row, 0).setText(_source_activity)
        self.cellWidget(target_row, 1).setTime(_source_time)

    def remove_row(self, row: int):
        """
        移除行
        :param row: 行
        """
        for _row in range(self.rowCount() - 1, row, -1):
            _widget = self.__new_buttons(_row - 1)
            self.setCellWidget(_row, 2, _widget)
        self.removeRow(row)

    def get_time(self, row: int):
        """
        获取时间
        :param row: 行
        """
        if row < 0 or row >= self.rowCount():
            return -1
        _time = self.cellWidget(row, 1).getTime()
        _time = QTime(0, 0).secsTo(_time)
        return _time

    def get_activity(self, row: int):
        """
        获取活动
        :param row: 行
        """
        if row < 0 or row >= self.rowCount():
            return ""
        return self.item(row, 0).text()

    def get_data(self):
        """
        获取数据
        """
        _data = {}
        for _row in range(self.rowCount()):
            _activity = self.item(_row, 0).text()
            _time = self.get_time(_row)
            _data[_row] = {"activity": _activity, "time": _time}
        return _data

    def load_data(self, data: dict):
        """
        加载数据
        :param data: 数据
        """
        self.clearContents()
        self.setRowCount(0)
        try:
            for _, _value in data.items():
                self.add_row(_value["activity"], _value["time"])
            return True
        except Exception as e:
            print(e)
            return False
