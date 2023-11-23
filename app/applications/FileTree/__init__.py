import os
import sys

current_directory = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_directory)

from file_tree_interface import FileTreeInterface

__all__ = ["FileTreeInterface"]

if __name__ == "__main__":
    from PyQt5.QtWidgets import QApplication

    app = QApplication(sys.argv)
    widget = FileTreeInterface(None, "config.json")
    widget.show()
    sys.exit(app.exec_())
