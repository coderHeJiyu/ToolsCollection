import os
import sys

current_directory = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_directory)

from secret_file_interface import SecretFileInterface

__all__ = ["SecretFileInterface"]

if __name__ == "__main__":
    from PyQt5.QtWidgets import QApplication

    app = QApplication(sys.argv)
    widget = SecretFileInterface()
    widget.show()
    sys.exit(app.exec_())
