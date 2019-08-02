"""
Last updated on 07/01/2015

@author: Cheng WANG,
"""

from PyQt5.QtCore import QSize
from PyQt5.QtWidgets import QPushButton


class LittleSIATLabel(QPushButton):
    def __init__(self, parent=None, width=0, height=0):
        super(LittleSIATLabel, self).__init__(parent)
        self.setStyleSheet('QPushButton{background-color:transparent; margin-right:6px; border-image: url(:/siat.png);}; border:0px;')
        self.setFixedSize(QSize(width, height))
        self.setAcceptDrops(True)
        self.setFlat(True)

    def dragEnterEvent(self, e):
        self.setStyleSheet('QPushButton{border-image: url(:/upload_files.png);}; border:0px;')
        if e.mimeData().hasUrls():
            e.acceptProposedAction()

    def dropEvent(self, event):
        self.setStyleSheet('QPushButton{border-image: url(:/siat.png);}; border:0px;')
        for url in event.mimeData().urls():
            file_path = url.toLocalFile()
            self.parent().add_file_from_path(file_path)