from enum import Enum
from qfluentwidgets import FluentIconBase, Theme, getIconColor


class MoreIcon(FluentIconBase, Enum):
    FILE = "File"
    CHEVRON_LEFT = "ChevronLeft"
    CHEVRON_RIGHT = "ChevronRight"
    CHEVRONS_LEFT = "ChevronsLeft"
    CHEVRONS_RIGHT = "ChevronsRight"

    def path(self, theme=Theme.AUTO):
        return f":/icons/images/icons/{self.value}_{getIconColor(theme)}.svg"
