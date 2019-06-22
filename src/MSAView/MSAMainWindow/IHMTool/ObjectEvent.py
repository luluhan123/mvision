#!/usr/bin/python3
# -*- coding: utf-8 -*-
from PyQt5.QtCore import QEvent,QObject, pyqtSignal


class ObjectEvent(QObject):
    MouseHovered = pyqtSignal()
    MouseClicked = pyqtSignal()
    MouseReleased = pyqtSignal()
    DoubleClicked = pyqtSignal()
    MouseEnter = pyqtSignal()
    MouseLeave = pyqtSignal()
    mouseMoveEvent = pyqtSignal()

    def __init__(self, parent):
        QObject.__init__(self, parent)
        parent.setMouseTracking(True)
        parent.installEventFilter(self)

    def eventFilter(self, _, event):
        # if event.type() == QEvent.MouseMove:
        #     self.emit(SIGNAL("MouseMove"), event.pos())
        #
        #
        # elif event.type() == QEvent.MouseButtonDblClick:
        #     self.emit(SIGNAL("MouseDoubleClick"), event.pos())

        if event.type() == QEvent.Enter:
            self.MouseEnter.emit()
        elif event.type() == QEvent.Leave:
            self.MouseLeave.emit()
        elif event.type() == QEvent.HoverEnter:
            self.MouseHovered.emit()
        elif event.type() == QEvent.MouseButtonPress:
            self.MouseClicked.emit()
        elif event.type() == QEvent.MouseButtonRelease:
            self.MouseReleased.emit()
        elif event.type() == QEvent.MouseButtonDblClick:
            self.DoubleClicked.emit()
        elif event.type() == QEvent.MouseMove:
            self.mouseMoveEvent.emit()
        return False
