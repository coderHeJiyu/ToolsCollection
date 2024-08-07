import os
import sys

current_directory = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_directory)

from hashlib_interface import HashlibInterface

__all__ = ["HashlibInterface"]

if __name__ == "__main__":
    from PyQt5.QtWidgets import QApplication

    app = QApplication(sys.argv)
    widget = HashlibInterface()
    widget.show()
    sys.exit(app.exec_())
