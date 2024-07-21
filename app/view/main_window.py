from qfluentwidgets import NavigationItemPosition, FluentIcon
from app.view.main_window_base import MainWindowBase
from app.view import (
    DemoInterface,
    FileTreeInterface,
    SecretFileInterface,
    EZVideoEditorInterface,
    HashlibInterface,
    WorkoutTimerInterface,
)


class MainWindow(MainWindowBase):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle(self.tr("Tools Collection"))
        self.theme_button.setToolTip(self.tr("Toggle theme"))
        self.demo_interface = DemoInterface(self)
        self.file_tree_interface = FileTreeInterface(
            self, "app/config/file_tree_config.json"
        )
        self.secret_file_interface = SecretFileInterface(self)
        self.ez_video_editor_interface = EZVideoEditorInterface(self)
        self.hashlib_interface = HashlibInterface(self)
        self.workout_timer_interface = WorkoutTimerInterface(self)
        self.__init_navigation()
        self.splash_screen.finish()

    def __init_navigation(self):
        pos = NavigationItemPosition.SCROLL
        self.addSubInterface(
            self.demo_interface,
            FluentIcon.TAG,
            self.demo_interface.windowTitle(),
            pos,
        )
        self.addSubInterface(
            self.file_tree_interface,
            FluentIcon.BOOK_SHELF,
            self.file_tree_interface.windowTitle(),
            pos,
        )
        self.addSubInterface(
            self.secret_file_interface,
            FluentIcon.VPN,
            self.secret_file_interface.windowTitle(),
            pos,
        )
        self.addSubInterface(
            self.ez_video_editor_interface,
            FluentIcon.VIDEO,
            self.ez_video_editor_interface.windowTitle(),
            pos,
        )
        self.addSubInterface(
            self.hashlib_interface,
            FluentIcon.CODE,
            self.hashlib_interface.windowTitle(),
            pos,
        )
        self.addSubInterface(
            self.workout_timer_interface,
            FluentIcon.FLAG,
            self.workout_timer_interface.windowTitle(),
            pos,
        )
