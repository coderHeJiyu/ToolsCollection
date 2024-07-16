import os
from PyQt5.QtWidgets import QWidget
from qfluentwidgets import FluentIcon, InfoBar, StateToolTip
from ui_hashlib_interface import Ui_HashlibInterface
from hash_thread import HashThread


class HashlibInterface(Ui_HashlibInterface, QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.__current_tab = "0"
        self.__count = {"add": 0, "remove": 0}
        self.__data = {}
        self.__hash__trhead = None
        self.stateTooltip = None
        self.add_new_tab()
        self.__init_components()

    def __init_components(self):
        self.combobox_type.addItem(self.tr("Text"))
        self.combobox_type.addItem(self.tr("File"))
        self.button_hash.setIcon(FluentIcon.DOWN)

    def add_new_tab(self):
        _routekey = str(self.__count["add"])
        self.tab_bar.addTab(
            routeKey=_routekey,
            text=self.tr("New Tab"),
        )
        self.__data[_routekey] = {}
        self.__count["add"] += 1
        self.widget.show()

    def remove_tab(self, index: int):
        self.__count["remove"] += 1
        if self.__count["add"] == self.__count["remove"]:
            self.__count = {"add": 0, "remove": 0}
            self.widget.hide()
        self.tab_bar.removeTab(index)

    def set_current_tab(self, index: int):
        self.__data[self.__current_tab] = {
            "type": self.combobox_type.currentIndex(),
            "input": self.widget_input.read(),
            "md5": self.edit_md5.text(),
            "sha1": self.edit_sha1.text(),
            "sha256": self.edit_sha256.text(),
            "sha512": self.edit_sha512.toPlainText(),
        }
        _routekey = self.tab_bar.tabItem(index).routeKey()
        self.__current_tab = _routekey
        _index = self.__data[_routekey].get("type", 0)
        self.combobox_type.setCurrentIndex(_index)
        self.widget_input.write(self.__data[_routekey].get("input", {}))
        self.edit_md5.setText(self.__data[_routekey].get("md5", ""))
        self.edit_sha1.setText(self.__data[_routekey].get("sha1", ""))
        self.edit_sha256.setText(self.__data[_routekey].get("sha256", ""))
        self.edit_sha512.setPlainText(self.__data[_routekey].get("sha512", ""))

    def get_hash(self):
        _data = self.widget_input.read()
        _type = _data.get("page", 0)
        _content = _data.get("text", "") if _type == 0 else _data.get("filepath", "")
        if _data.get("page", 0) == 1 and not os.path.isfile(_content):
            InfoBar.error(
                title=self.tr("error"),
                content=self.tr("File does not exist!"),
                isClosable=False,
                parent=self,
            )
            return
        self.__hash__trhead = HashThread(type_=_type, content=_content)
        self.__hash__trhead.task_finished.connect(self.__update_hash)
        self.__hash__trhead.start()
        # 显示状态提示框
        self.stateTooltip = StateToolTip(
            self.tr("Calculating hash..."),
            self.tr("Please wait patiently"),
            self.window(),
        )
        self.stateTooltip.move(self.stateTooltip.getSuitablePos())
        self.stateTooltip.show()

    def __update_hash(self, data: dict):
        self.edit_md5.setText(data.get("md5", ""))
        self.edit_sha1.setText(data.get("sha1", ""))
        self.edit_sha256.setText(data.get("sha256", ""))
        self.edit_sha512.setPlainText(data.get("sha512", ""))
        # 隐藏状态提示框
        self.stateTooltip.setContent(self.tr("finished!") + " 😆")
        self.stateTooltip.setState(True)
        self.stateTooltip = None
