import os
import sys

current_directory = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_directory)

from ez_video_editor_interface import EZVideoEditorInterface

__all__ = ["EZVideoEditorInterface"]

if __name__ == "__main__":
    from PyQt5.QtWidgets import QApplication

    app = QApplication(sys.argv)
    widget = EZVideoEditorInterface()
    widget.show()
    sys.exit(app.exec_())
