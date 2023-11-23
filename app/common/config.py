from qfluentwidgets import (
    qconfig,
    QConfig,
    OptionsConfigItem,
    OptionsValidator,
    Theme,
    __version__,
)


class Config(QConfig):
    """Config of application"""

    dpiScale = OptionsConfigItem(
        "MainWindow",
        "DpiScale",
        "Auto",
        OptionsValidator([1, 1.25, 1.5, 1.75, 2, "Auto"]),
        restart=True,
    )
    language = OptionsConfigItem(
        "MainWindow",
        "Language",
        "Auto",
        OptionsValidator(["zh_CN", "en_US", "Auto"]),
        restart=True,
    )


cfg = Config()
cfg.themeMode.value = Theme.AUTO
qconfig.load("app/config/global_config.json", cfg)
