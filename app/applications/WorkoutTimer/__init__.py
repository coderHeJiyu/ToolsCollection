import os
import sys

current_directory = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_directory)

from workout_timer_interface import WorkoutTimerInterface

__all__ = ["WorkoutTimerInterface"]

if __name__ == "__main__":
    from PyQt5.QtWidgets import QApplication

    app = QApplication(sys.argv)
    widget = WorkoutTimerInterface()
    widget.show()
    sys.exit(app.exec_())
