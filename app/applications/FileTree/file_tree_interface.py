import os
import json
from PyQt5.QtGui import QDragEnterEvent, QDropEvent
from PyQt5.QtWidgets import QWidget, QFileDialog
from qfluentwidgets import FluentIcon, InfoBar
from ui_file_tree_interface import Ui_FileTreeInterface
from file_tree_generator import FileTreeGenerator


class FileTreeInterface(Ui_FileTreeInterface, QWidget):
    def __init__(self, parent=None, config_path=None):
        super().__init__(parent)
        self.setupUi(self)
        self.button_folder.setIcon(FluentIcon.FOLDER)
        self.button_copy.setIcon(FluentIcon.COPY)
        self.button_draw.setIcon(FluentIcon.ACCEPT)
        self.__file_tree_generator = None
        self.__config_path = config_path
        self.__load_kwargs()

    def __get_kwargs(self):
        """
        Get the kwargs
        """
        kwargs = {}
        kwargs["max_depth"] = self.spin_box_depth.value()
        _ignore_names = self.edit_ignore_names.toPlainText()
        kwargs["ignore_names"] = _ignore_names.split("\n") if _ignore_names else []
        zip_suffix = self.edit_zip_suffix.toPlainText()
        kwargs["zip_suffix"] = zip_suffix.split("\n") if zip_suffix else []
        kwargs["zip_suffix_minimum"] = self.spin_box_zip.value()
        return kwargs

    def __save_kwargs(self):
        """
        Save the kwargs to the config file
        """
        if not self.__config_path:
            return
        _save = {
            "max_depth": self.spin_box_depth.value(),
            "ignore_names": self.edit_ignore_names.toPlainText(),
            "zip_suffix": self.edit_zip_suffix.toPlainText(),
            "zip_suffix_minimum": self.spin_box_zip.value(),
        }
        with open(self.__config_path, "w", encoding="utf-8") as f:
            json.dump(_save, f)

    def __load_kwargs(self):
        """
        Load the kwargs from the config file
        """
        if not self.__config_path:
            return
        if not os.path.exists(self.__config_path):
            return
        with open(self.__config_path, "r", encoding="utf-8") as f:
            _load = f.read()
        _load = json.loads(_load)
        self.spin_box_depth.setValue(_load["max_depth"])
        self.edit_ignore_names.setPlainText(_load["ignore_names"])
        self.edit_zip_suffix.setPlainText(_load["zip_suffix"])
        self.spin_box_zip.setValue(_load["zip_suffix_minimum"])

    def open_folder(self, folder_path=None):
        """
        Open a folder and generate the file tree
        """
        if not folder_path:
            folder_path = QFileDialog.getExistingDirectory(
                self, self.tr("Select Folder")
            )
        if folder_path:
            self.edit_folder.setPlainText(folder_path)
            self.__file_tree_generator = FileTreeGenerator(folder_path)
            self.draw()

    def copy(self):
        """
        Copy the content of the output to clipboard
        """
        self.edit_output.selectAll()
        self.edit_output.copy()
        self.edit_output.moveCursor(1)
        # show info bar
        InfoBar.success(
            title=self.tr("Copy"),
            content=self.tr("Successfully copied to clipboard"),
            parent=self,
        )

    def draw(self):
        """
        Draw the file tree
        """
        self.__save_kwargs()
        if not self.__file_tree_generator:
            InfoBar.error(
                title=self.tr("Error"),
                content=self.tr("Please select a folder first"),
                duration=-1,
                parent=self,
            )
            return
        try:
            self.__file_tree_generator.reset(**self.__get_kwargs())
            self.edit_output.setText(self.__file_tree_generator.draw(cmd=False))
            return
        except ValueError as e:
            InfoBar.error(
                title=self.tr("Error"),
                content=str(e),
                duration=-1,
                parent=self,
            )

    def dragEnterEvent(self, a0: QDragEnterEvent):
        super().dragEnterEvent(a0)
        if not a0.mimeData().hasUrls():
            return
        folder_path = a0.mimeData().urls()[0]
        if not folder_path.isLocalFile():
            return
        folder_path = folder_path.toLocalFile()
        if os.path.isdir(folder_path):
            a0.acceptProposedAction()

    def dropEvent(self, a0: QDropEvent):
        super().dropEvent(a0)
        folder_path = a0.mimeData().urls()[0].toLocalFile()
        self.open_folder(folder_path)
