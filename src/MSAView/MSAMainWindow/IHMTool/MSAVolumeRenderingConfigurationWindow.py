from PyQt5.QtWidgets import QLabel
from PyQt5.QtCore import Qt


class MSAVolumeRenderingConfigurationWindow(QLabel):

    def __init__(self):
        QLabel.__init__(self)

        self.setFixedSize(512, 512)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)

    def display(self):
        self.show()
