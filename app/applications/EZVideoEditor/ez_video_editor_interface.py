import os
from typing import Optional
import ffmpeg
from vlc import MediaPlayer
from PyQt5.QtWidgets import QWidget, QFileDialog
from PyQt5.QtCore import QTimer, QTime, QUrl
from qfluentwidgets import FluentIcon, InfoBar, InfoBarPosition
from ui_ez_video_editor_interface import Ui_EZVideoEditorInterface


def ms2str(ms: int):
    """
    将毫秒转换为 "hh:mm:ss.zzz" 格式的字符串。
    :param ms: 毫秒数
    """
    return QTime(0, 0).addMSecs(ms).toString("hh:mm:ss.zzz")


def ms2name(ms: int):
    """
    将毫秒转换为 "hh.mm.ss.zzz" 格式的字符串。
    :param ms: 毫秒数
    """
    return QTime(0, 0).addMSecs(ms).toString("hh.mm.ss.zzz")


class EZVideoEditorInterface(Ui_EZVideoEditorInterface, QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        # 状态
        self.is_playing = False
        # 播放器
        self.player: MediaPlayer = MediaPlayer()
        self.video_play_widget.set_player(self.player)
        self.video_play_widget.video_accepted.connect(self.open_video_url)
        # 进度条更新
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_player_state)
        self.timer.start(50)
        # 进度条点击和拖动
        self.video_slider.sliderClicked.connect(self.set_player_time)
        self.video_slider.sliderMoved.connect(self.set_player_time)
        # 按钮图标
        self.button_play.setIcon(FluentIcon.PLAY)
        self.button_set_start.setIcon(FluentIcon.STOP_WATCH)
        self.button_set_end.setIcon(FluentIcon.STOP_WATCH)
        self.button_cut.setIcon(FluentIcon.CUT)
        self.hyperlink_ffmpeg.setIcon(FluentIcon.LINK)
        self.hyperlink_vlc.setIcon(FluentIcon.LINK)
        # 视频信息
        self.video_info = {
            "start_time": 0,
            "end_time": 0,
            "video_url": QUrl(),
        }

    def __play_video(self):
        self.player.play()
        self.button_play.setIcon(FluentIcon.PAUSE)
        self.is_playing = True

    def __pause_video(self):
        self.player.pause()
        self.button_play.setIcon(FluentIcon.PLAY)
        self.is_playing = False

    def _reload_video(self):
        self.player.set_mrl(self.video_info["video_url"].toString())
        self.__play_video()

    def _init_video_info(self):
        self.video_info["start_time"] = 0
        self.video_info["end_time"] = self.player.get_length()
        self.start_time_label.setText(ms2str(0))
        self.end_time_label.setText(ms2str(self.video_info["end_time"]))

    def open_video_url(self, file_url: Optional[QUrl] = None):
        """
        打开视频文件，如果没有指定文件则打开文件对话框
        :param file_url: 视频文件url
        """
        if not file_url:
            file_url = QFileDialog.getOpenFileUrl()[0]
        if not file_url:
            return
        self.video_info["video_url"] = file_url
        self.player.set_mrl(file_url.toString())  # 选取视频文件
        QTimer.singleShot(50, self._init_video_info)
        self.__play_video()  # 播放视频

    def update_player_state(self):
        """
        更新播放器状态
        """
        if self.player.get_length() <= 0:
            return
        current_time = self.player.get_time()
        total_time = self.player.get_length()
        # 更新总时长
        if total_time != self.video_slider.maximum():
            self.video_slider.setMaximum(total_time)
            self.duration_time_label.setText(ms2str(total_time))
        # 更新当前时间
        if current_time > total_time:
            current_time = 0
        self.video_slider.setValue(current_time)
        self.position_time_label.setText(ms2str(current_time))
        # 播放结束，重新播放
        if self.is_playing != self.player.is_playing():
            QTimer.singleShot(10, self._reload_video)

    def set_player_time(self, time: int):
        """
        设置播放器时间
        :param time: 时间
        """
        time = max(time, 0)
        self.player.set_time(time)

    def toggle_video_play_state(self):
        """
        切换视频播放/暂停状态
        """
        if self.player.get_length() <= 0:
            return
        if self.is_playing:
            self.__pause_video()
        else:
            self.__play_video()

    def play_next_second(self):
        """
        播放下一秒
        """
        self.player.set_time(self.player.get_time() + 1000)

    def play_previous_second(self):
        """
        播放上一秒
        """
        self.player.set_time(self.player.get_time() - 1000)

    def play_next_frame(self):
        """
        播放下一帧
        """
        self.player.set_time(self.player.get_time() + 40)

    def play_previous_frame(self):
        """
        播放上一帧
        """
        self.player.set_time(self.player.get_time() - 40)

    def __ckeck_video(self):
        if self.video_info["video_url"].isEmpty():
            InfoBar.error(
                title=self.tr("error"),
                content=self.tr("Drop a video file first!"),
                isClosable=False,
                position=InfoBarPosition.BOTTOM_LEFT,
                duration=2000,
                parent=self,
            )
            return False
        return True

    def set_start_time(self):
        """
        设置剪辑的开始时间
        """
        if not self.__ckeck_video():
            return
        _time = self.player.get_time()
        self.video_info["start_time"] = _time
        self.start_time_label.setText(ms2str(_time))
        InfoBar.success(
            title=self.tr("success"),
            content=self.tr("Start time set successfully!"),
            isClosable=False,
            position=InfoBarPosition.BOTTOM_RIGHT,
            duration=2000,
            parent=self,
        )

    def set_end_time(self):
        """
        设置剪辑的结束时间
        """
        if not self.__ckeck_video():
            return
        _time = self.player.get_time()
        self.video_info["end_time"] = _time
        self.end_time_label.setText(ms2str(_time))
        InfoBar.success(
            title=self.tr("success"),
            content=self.tr("End time set successfully!"),
            isClosable=False,
            position=InfoBarPosition.BOTTOM_RIGHT,
            duration=2000,
            parent=self,
        )

    def video_cut(self):
        """
        剪辑视频
        """
        # 视频文件不存在，返回
        if not self.__ckeck_video():
            return
        start_time = self.video_info["start_time"]
        end_time = self.video_info["end_time"]
        filename = self.video_info["video_url"].toLocalFile()
        output_file = f"{os.path.splitext(filename)[0]}[{ms2name(start_time)}-{ms2name(end_time)}].mp4"
        # 视频剪辑文件已存在，返回
        if os.path.exists(output_file):
            InfoBar.error(
                title=self.tr("error"),
                content=self.tr("The video clip already exists!"),
                isClosable=False,
                position=InfoBarPosition.BOTTOM_LEFT,
                duration=2000,
                parent=self,
            )
            return
        # 剪辑视频
        start_time = start_time / 1000
        end_time = end_time / 1000
        try:
            ffmpeg.input(filename, ss=start_time, to=end_time).output(
                output_file, c="copy"
            ).run()
        except ffmpeg.Error as e:
            InfoBar.error(
                title=self.tr("error"),
                content=str(e),
                isClosable=False,
                position=InfoBarPosition.BOTTOM_LEFT,
                duration=2000,
                parent=self,
            )
            return
        # 提示剪辑成功
        InfoBar.success(
            title=self.tr("success"),
            content=self.tr("Video clip saved successfully!"),
            isClosable=False,
            position=InfoBarPosition.BOTTOM_RIGHT,
            duration=2000,
            parent=self,
        )
