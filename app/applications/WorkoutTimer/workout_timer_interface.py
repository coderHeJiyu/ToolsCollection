import os
import json
from PyQt5.QtWidgets import QTableWidgetItem, QWidget, QFileDialog
from qfluentwidgets import FluentIcon, MessageBox, InfoBar
from ui_workout_timer_interface import Ui_WorkoutTimerInterface


def secs2time(secs: int) -> str:
    if secs >= 3600:
        _hour = secs // 3600
        _minute = secs % 3600 // 60
        _second = secs % 60
        return f"{_hour:02d}:{_minute:02d}:{_second:02d}"
    _minute = secs // 60
    _second = secs % 60
    return f"{_minute:02d}:{_second:02d}"


class WorkoutTimerInterface(Ui_WorkoutTimerInterface, QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.__current_event = 0
        self.__is_timer_running = False
        self.__init_components()

    def __init_components(self):
        self.button_timer.setIcon(FluentIcon.FLAG)
        self.button_add_row.setIcon(FluentIcon.ADD_TO)
        self.button_save.setIcon(FluentIcon.SAVE)
        self.button_load.setIcon(FluentIcon.DOCUMENT)
        self.button_reset.setIcon(FluentIcon.SYNC)
        self.timer_ring.time_up.connect(self.__next_event)

    def __play_current_event(self):
        self.__is_timer_running = self.timer_ring.start()
        self.checkBox_readonly.setEnabled(not self.__is_timer_running)

    def __set_current_event(self):
        self.__is_timer_running = False
        self.checkBox_readonly.setEnabled(True)
        _activity = self.widget_schedule.get_activity(self.__current_event)
        self.label_event.setText(_activity)
        _time = self.widget_schedule.get_time(self.__current_event)
        self.timer_ring.reset_secs(_time)
        self.widget_schedule_readonly.selectRow(self.__current_event)

    def __next_event(self):
        if self.__is_timer_running:
            self.timer_ring.stop()
            self.__is_timer_running = False
            self.checkBox_readonly.setEnabled(True)
        self.__current_event += 1
        if self.__current_event >= self.widget_schedule.rowCount():
            InfoBar.info(
                title=self.tr("Finished!"),
                content=self.tr("All events have been completed!"),
                duration=-1,
                parent=self,
            )
            return
        self.__set_current_event()

    def play(self):
        """
        开始事件
        """
        if not self.checkBox_readonly.isChecked():
            InfoBar.warning(
                title=self.tr("Warning"),
                content=self.tr("Please set the readonly mode first!"),
                parent=self,
            )
            return
        if not self.__is_timer_running:
            self.__play_current_event()
            return
        _w = MessageBox(
            self.tr("Are you sure?"),
            self.tr("The timer is running, do you want to skip the current event?"),
            self,
        )
        if _w.exec_():
            self.__next_event()
            self.__play_current_event()

    def reset(self):
        self.__current_event = 0
        self.__set_current_event()

    def __set_readonly_data(self):
        _data = self.widget_schedule.get_data()
        self.widget_schedule_readonly.setRowCount(len(_data))
        for _key, _value in _data.items():
            self.widget_schedule_readonly.setItem(
                _key, 0, QTableWidgetItem(_value["activity"])
            )
            self.widget_schedule_readonly.setItem(
                _key, 1, QTableWidgetItem(secs2time(_value["time"]))
            )
        self.widget_schedule_readonly.resizeColumnsToContents()
        self.widget_schedule_readonly.resizeRowsToContents()

    def set_readonly(self, readonly: bool):
        """
        设置只读状态
        :param readonly: 是否只读
        """
        self.widget_buttons.setHidden(readonly)
        self.stacked_widget.setCurrentIndex(1 if readonly else 0)
        if readonly:
            self.__set_readonly_data()
            self.reset()

    def save_as_json(self):
        """
        保存为 JSON
        """
        _file_path, _ = QFileDialog.getSaveFileName(
            self,
            self.tr("Save as json file"),
            "",
            "Json " + self.tr("files") + " (*.json)",
        )
        if not _file_path:
            return
        _data = self.widget_schedule.get_data()
        with open(_file_path, "w", encoding="utf-8") as _file:
            _file.write(json.dumps(_data))

    def load_from_json(self):
        """
        从 JSON 加载
        """
        _file_path, _ = QFileDialog.getOpenFileName(
            self,
            self.tr("Load from json file"),
            "",
            "Json " + self.tr("files") + " (*.json)",
        )
        if not os.path.exists(_file_path):
            return
        with open(_file_path, "r", encoding="utf-8") as _file:
            data = json.load(_file)
        self.widget_schedule.load_data(data)
