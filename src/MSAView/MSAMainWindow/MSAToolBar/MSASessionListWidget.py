"""
Last updated on 07/01/2015

@author: Cheng WANG,
"""

import os
import sys
from PyQt5.QtGui import QDrag
from PyQt5.QtWidgets import QListWidget, QAbstractItemView
from PyQt5.QtCore import QByteArray, QDataStream, QMimeData, QPoint, QIODevice, Qt


class SessionListWidget(QListWidget):
    def __init__(self, parent=None, ihm_factor=1, background_color="", global_font_color="", global_font=None):
        super(QListWidget, self).__init__(parent)
        self.parent = parent
        self.ihm_factor = ihm_factor
        self.globalBackgroundColor = background_color
        self.globalFontColor = global_font_color
        self.globalFont = global_font
        self.setFont(self.globalFont)
        self.setStyleSheet("QListWidget {show-decoration-selected: 2; color:" + self.globalFontColor + "}"
                           "QListWidget::item:alternate { background: transparent;}"
                           "QListWidget::item:selected {border: 0px;}"
                           "QListWidget::item:selected:!active {background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,stop: 0  rgb(230, 230,230), stop: 1  rgb(255, 255,255));color:"+self.globalBackgroundColor+";}"
                           "QListWidget::item:selected:active {background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,stop: 0  rgb(230, 230,230), stop: 1  rgb(255, 255,255));color:"+self.globalBackgroundColor+";}"
                           "QListWidget::item:hover {background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,stop: 0  rgb(230, 230,230), stop: 1  rgb(255, 255,255));color:"+self.globalBackgroundColor+"}")

        self.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.setDragEnabled(True)

    def dragEnterEvent(self, event):
        if event.mimeData().hasFormat("application/x-icon-and-text"):
            event.accept()
        else:
            event.ignore()

    def dragMoveEvent(self, event):
        if event.mimeData().hasFormat("application/x-icon-and-text"):
            event.setDropAction(Qt.MoveAction)
            event.accept()
        else:
            event.ignore()

    def startDrag(self, event):
        item = self.currentItem()
        icon = item.icon()
        data = QByteArray()
        stream = QDataStream(data, QIODevice.WriteOnly)
        stream.writeQString(item.text())
        stream << icon
        mimeData = QMimeData()
        mimeData.setData("application/x-icon-and-text", data)
        drag = QDrag(self)
        drag.setMimeData(mimeData)
        pixmap = icon.pixmap(24, 24)
        drag.setHotSpot(QPoint(12, 12))
        drag.setPixmap(pixmap)
        if drag.exec(Qt.MoveAction) == Qt.MoveAction:
            self.takeItem(self.row(item))