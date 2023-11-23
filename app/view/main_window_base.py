from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QSize
from qfluentwidgets import (
    NavigationItemPosition,
    NavigationToolButton,
    FluentWindow,
    SplashScreen,
    FluentIcon,
    toggleTheme,
    isDarkTheme,
)
from app.view.home_interface import HomeInterface
from app.view.setting_interface import SettingInterface

import app.common.resource


class MainWindowBase(FluentWindow):
    """
    Main Window
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.splash_screen = None
        self.__init_window()
        self.home_interface = HomeInterface(self)
        self.setting_interface = SettingInterface(self)
        self.__init_navigation()

    def __init_window(self):
        self.resize(960, 780)
        self.setMinimumWidth(760)
        self.setWindowIcon(QIcon(":/resource/images/logo.png"))

        # create splash screen
        self.splash_screen = SplashScreen(self.windowIcon(), self)
        self.splash_screen.setIconSize(QSize(106, 106))
        self.splash_screen.raise_()

        desktop = QApplication.desktop().availableGeometry()
        w, h = desktop.width(), desktop.height()
        self.move(w // 2 - self.width() // 2, h // 2 - self.height() // 2)
        self.show()
        QApplication.processEvents()

    def __init_navigation(self):
        # home interface
        self.addSubInterface(
            self.home_interface,
            FluentIcon.HOME,
            self.home_interface.windowTitle(),
            NavigationItemPosition.TOP,
        )
        self.navigationInterface.addSeparator()
        # theme button
        self.theme_button = NavigationToolButton(FluentIcon.BRIGHTNESS, self)
        self.navigationInterface.addWidget(
            "themeButton",
            self.theme_button,
            self.toggleTheme,
            NavigationItemPosition.BOTTOM,
        )
        self._updateThemeButtonIcon()
        # setting interface
        self.addSubInterface(
            self.setting_interface,
            FluentIcon.SETTING,
            self.setting_interface.windowTitle(),
            NavigationItemPosition.BOTTOM,
        )

    def toggleTheme(self):
        toggleTheme(save=True)
        self._updateThemeButtonIcon()

    def _updateThemeButtonIcon(self):
        if not isDarkTheme():
            self.theme_button.setIcon(FluentIcon.QUIET_HOURS)
        else:
            self.theme_button.setIcon(FluentIcon.BRIGHTNESS)
