import hashlib
from PyQt5.QtCore import QThread, pyqtSignal


class HashThread(QThread):
    """
    Hash线程
    """

    task_finished = pyqtSignal(dict)

    def __init__(self, type_: int, content: str):
        """
        :param data: 数据
        """
        super().__init__()
        self.__type = type_
        self.__content = content

    def run(self):
        """
        运行线程
        """
        if self.__type == 0:
            _data = self.__content.encode()
        else:
            with open(self.__content, "rb") as fp:
                _data = fp.read()
        _md5 = hashlib.md5(_data).hexdigest()
        _sha1 = hashlib.sha1(_data).hexdigest()
        _sha256 = hashlib.sha256(_data).hexdigest()
        _sha512 = hashlib.sha512(_data).hexdigest()
        self.task_finished.emit(
            {
                "md5": _md5,
                "sha1": _sha1,
                "sha256": _sha256,
                "sha512": _sha512,
            }
        )
