#!/usr/bin/env python

from PyQt5.QtWidgets import QWidget, QApplication, QSizePolicy, QSpacerItem, QPushButton, QLabel, QHBoxLayout, QVBoxLayout
from PyQt5.QtCore import pyqtSignal, Qt, QSize
from PyQt5.QtGui import QIcon


class MSAVesselSegmentation(QWidget):
    vascular_button_clicked = pyqtSignal()

    def __init__(self, controller=None, background_color="", global_font_color="", global_font=None):
        QWidget.__init__(self)

        self.controller = controller
        self.globalBackgroundColor = background_color
        self.globalFontColor = global_font_color
        self.globalFont = global_font

        self.mousePointerMove = None
        self.mousePosition = None
        self.mouseLeftButtonPressed = False

        self.desktop = QApplication.desktop()
        width = self.desktop.width()
        height = self.desktop.height()

        self.appWidth = width * 0.3
        self.appHeight = height * 0.35

        self.appX = (width - self.appWidth) / 2
        self.appY = (height - self.appHeight) / 2
        self.setGeometry(self.appX, self.appY, self.appWidth, self.appHeight)
        self.draw_background()

        # ----------------------------------------------------------
        # configure the appearance of the graphical interface
        # ----------------------------------------------------------
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setWindowOpacity(1.0)
        self.setMouseTracking(True)
        self.setAutoFillBackground(True)

        spacer_item = QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Expanding)

        self.closeButton = QPushButton()
        self.closeButton.setStyleSheet("background:transparent")
        self.closeButton.setIcon(QIcon(":/cancle.png"))
        self.closeButton.setFixedSize(self.appWidth*0.05, self.appHeight*0.05)
        self.closeButton.setIconSize(QSize(15, 15))
        self.closeButton.setFlat(True)

        self.maximizeButton = QPushButton()
        self.maximizeButton.setFixedSize(self.appWidth*0.05, self.appHeight*0.05)
        self.maximizeButton.setStyleSheet("background:transparent")
        self.maximizeButton.setIcon(QIcon(":/add.png"))
        self.maximizeButton.setIconSize(QSize(15, 15))
        self.maximizeButton.setFlat(True)

        self.minimizeButton = QPushButton()
        self.minimizeButton.setStyleSheet("background:transparent")
        self.minimizeButton.setFixedSize(self.appWidth*0.05, self.appHeight*0.05)
        self.minimizeButton.setIcon(QIcon(":/substract.png"))
        self.minimizeButton.setIconSize(QSize(15, 15))
        self.minimizeButton.setFlat(True)

        self.toolbarLabel = QLabel()
        self.toolbarLabel.setFixedSize(self.appWidth, self.appHeight*0.05)
        self.toolbarLabel.setStyleSheet("background-color: " + self.globalBackgroundColor)
        self.toolbarLabelLayout = QHBoxLayout(self.toolbarLabel)
        self.toolbarLabelLayout.addWidget(self.closeButton)
        self.toolbarLabelLayout.addWidget(self.minimizeButton)
        self.toolbarLabelLayout.addWidget(self.maximizeButton)
        self.toolbarLabelLayout.addItem(spacer_item)
        self.toolbarLabelLayout.setSpacing(1)
        self.toolbarLabelLayout.setContentsMargins(0, 0, 0, 0)

        self.vesselSegmentationWindow = QWidget()
        self.vesselSegmentationWindow.setFixedSize(self.appWidth, self.appHeight*0.95)

        self.vessel_Segmentation_Window_Layout = QVBoxLayout(self)
        self.vessel_Segmentation_Window_Layout.addWidget(self.toolbarLabel)
        self.vessel_Segmentation_Window_Layout.addWidget(self.vesselSegmentationWindow)
        self.vessel_Segmentation_Window_Layout.setSpacing(0)
        self.vessel_Segmentation_Window_Layout.setContentsMargins(0, 0, 0, 0)

        self.closeButton.clicked.connect(self.close_system)

    def close_system(self):
        self.vascular_button_clicked.emit()
        self.close()

    def display(self):
        self.show()

    def draw_background(self):
        """
            - configure the background and the size of the graphical tool
        """
        self.setStyleSheet("background-color: rgb(246, 246, 246)")

    def mousePressEvent(self, event):
        """
            -- get the mouse's left button clicked event
        :param event:
        """
        if event.button() == Qt.LeftButton:
            if (event.y() < 5) or (event.x() < 5):
                event.ignore()
                return
            self.mousePosition = event.globalPos()
            self.mouseLeftButtonPressed = True

    def mouseMoveEvent(self, event):
        """
            -- if the mouse is moving while it's left button has always been maintain clicked, then move the main window with the mouse's pointer
        :param event:
        """
        if self.mouseLeftButtonPressed:
            self.mousePointerMove = event.globalPos()
            self.move(self.pos() + self.mousePointerMove - self.mousePosition)
            self.mousePosition = self.mousePointerMove
        event.ignore()

    def mouseReleaseEvent(self, event):
        """
            -- get the mouse's left button release event
        :param event:
        """
        if event.button() == Qt.LeftButton:
            self.mouseLeftButtonPressed = False
        event.ignore()
