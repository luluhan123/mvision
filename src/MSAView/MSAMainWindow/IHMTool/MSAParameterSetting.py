#!/usr/bin/env python

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QWidget, QApplication, QSpacerItem, QLabel, QLineEdit, QGridLayout, QPushButton, QSizePolicy, QHBoxLayout, QVBoxLayout
from PyQt5.QtCore import pyqtSignal, Qt, QSize


class MSAParameterSetting(QWidget):
    parameter_button_icon_change = pyqtSignal()

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

        self.appWidth = width*0.3
        self.appHeight = height*0.35

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
        self.closeButton.setFixedSize(self.appWidth*0.035, self.appHeight*0.035)
        self.closeButton.setIconSize(QSize(self.appWidth*0.03, self.appHeight*0.03))
        self.closeButton.setFlat(True)

        self.maximizeButton = QPushButton()
        self.maximizeButton.setFixedSize(self.appWidth*0.035, self.appHeight*0.035)
        self.maximizeButton.setStyleSheet("background:transparent")
        self.maximizeButton.setIcon(QIcon(":/add.png"))
        self.maximizeButton.setIconSize(QSize(self.appWidth*0.03, self.appHeight*0.03))
        self.maximizeButton.setFlat(True)

        self.minimizeButton = QPushButton()
        self.minimizeButton.setStyleSheet("background:transparent")
        self.minimizeButton.setFixedSize(self.appWidth*0.035, self.appHeight*0.035)
        self.minimizeButton.setIcon(QIcon(":/substract.png"))
        self.minimizeButton.setIconSize(QSize(self.appWidth*0.03, self.appHeight*0.03))
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

        self.levelLabel = QLabel("level:")
        self.levelLabel.setFixedSize(self.appWidth*0.2, self.appHeight*0.08)
        self.levelLabel.setFont(self.globalFont)
        self.levelLabel.setStyleSheet("color: " + self.globalFontColor)

        self.levelLine = QLineEdit("424")
        self.levelLine.setFixedSize(self.appWidth * 0.3, self.appHeight*0.08)
        self.levelLine.setFont(self.globalFont)
        self.levelLine.setStyleSheet("border: 1px solid " + self.globalFontColor)

        self.windowLabel = QLabel("window:")
        self.windowLabel.setFixedSize(self.appWidth*0.2, self.appHeight*0.08)
        self.windowLabel.setFont(self.globalFont)
        self.windowLabel.setStyleSheet("color: " + self.globalFontColor)
        # self.windowLabel.setAlignment(Qt.AlignCenter)

        self.windowLine = QLineEdit("912")
        self.windowLine.setFixedSize(self.appWidth * 0.3, self.appHeight*0.08)
        self.windowLine.setFont(self.globalFont)
        self.windowLine.setStyleSheet("border: 1px solid " + self.globalFontColor)
        # self.windowLine.setAlignment(Qt.AlignCenter)

        self.maxLabel = QLabel("max:")
        self.maxLabel.setFixedSize(self.appWidth*0.2, self.appHeight*0.08)
        self.maxLabel.setFont(self.globalFont)
        self.maxLabel.setStyleSheet("color: " + self.globalFontColor)
        # self.maxLabel.setAlignment(Qt.AlignCenter)

        self.maxLine = QLineEdit()
        self.maxLine.setFixedSize(self.appWidth * 0.3, self.appHeight*0.08)
        self.maxLine.setFont(self.globalFont)
        self.maxLine.setStyleSheet("border: 1px solid " + self.globalFontColor)
        # self.maxLine.setAlignment(Qt.AlignCenter)

        self.minLabel = QLabel("min:")
        self.minLabel.setFixedSize(self.appWidth*0.2, self.appHeight*0.08)
        self.minLabel.setFont(self.globalFont)
        self.minLabel.setStyleSheet("color: " + self.globalFontColor)
        # self.minLabel.setAlignment(Qt.AlignCenter)

        self.minLine = QLineEdit()
        self.minLine.setFixedSize(self.appWidth * 0.3, self.appHeight*0.08)
        self.minLine.setFont(self.globalFont)
        self.minLine.setStyleSheet("color: " + self.globalFontColor)
        # self.minLine.setAlignment(Qt.AlignCenter)

        self.boxWidthLabel = QLabel("box_w:")
        self.boxWidthLabel.setFixedSize(self.appWidth * 0.2, self.appHeight*0.08)
        self.boxWidthLabel.setFont(self.globalFont)
        self.boxWidthLabel.setStyleSheet("color: " + self.globalFontColor)
        # self.boxWidthLabel.setAlignment(Qt.AlignCenter)

        self.boxWidthLineEdit = QLineEdit("128")
        self.boxWidthLineEdit.setFixedSize(self.appWidth * 0.3, self.appHeight*0.08)
        self.boxWidthLineEdit.setFont(self.globalFont)
        self.boxWidthLineEdit.setStyleSheet("color: " + self.globalFontColor)

        self.boxHeightLabel = QLabel("box_h:")
        self.boxHeightLabel.setFixedSize(self.appWidth * 0.2, self.appHeight*0.08)
        self.boxHeightLabel.setFont(self.globalFont)
        self.boxHeightLabel.setStyleSheet("color: " + self.globalFontColor)
        # self.boxHeightLabel.setAlignment(Qt.AlignCenter)

        self.boxHeightLineEdit = QLineEdit("128")
        self.boxHeightLineEdit.setFixedSize(self.appWidth * 0.3, self.appHeight*0.08)
        self.boxHeightLineEdit.setFont(self.globalFont)
        self.boxHeightLineEdit.setStyleSheet("color: " + self.globalFontColor)

        self.grayMaxLabel = QLabel("gray_Max:")
        self.grayMaxLabel.setFixedSize(self.appWidth * 0.2, self.appHeight*0.08)
        self.grayMaxLabel.setFont(self.globalFont)
        self.grayMaxLabel.setStyleSheet("color: " + self.globalFontColor)
        # self.grayMaxLabel.setAlignment(Qt.AlignCenter)

        self.grayMaxLine = QLineEdit("128")
        self.grayMaxLine.setFixedSize(self.appWidth * 0.3, self.appHeight*0.08)
        self.grayMaxLine.setFont(self.globalFont)
        self.grayMaxLine.setStyleSheet("color: " + self.globalFontColor)

        self.grayMinLabel = QLabel("gray_Min:")
        self.grayMinLabel.setFixedSize(self.appWidth * 0.2, self.appHeight*0.08)
        self.grayMinLabel.setFont(self.globalFont)
        self.grayMinLabel.setStyleSheet("color: " + self.globalFontColor)
        # self.grayMinLabel.setAlignment(Qt.AlignCenter)

        self.grayMinLine = QLineEdit("128")
        self.grayMinLine.setFixedSize(self.appWidth * 0.3, self.appHeight*0.08)
        self.grayMinLine.setFont(self.globalFont)
        self.grayMinLine.setStyleSheet("color: " + self.globalFontColor)

        self.parameter_SettingWindow = QWidget()
        self.parameter_SettingWindow.setFixedSize(self.appWidth, self.appHeight*0.9)
        self.parameter_Window_Layout = QGridLayout(self.parameter_SettingWindow)
        self.parameter_Window_Layout.addWidget(self.levelLabel, 0, 0)
        self.parameter_Window_Layout.addWidget(self.levelLine, 0, 1)
        self.parameter_Window_Layout.addWidget(self.windowLabel, 1, 0)
        self.parameter_Window_Layout.addWidget(self.windowLine, 1, 1)
        self.parameter_Window_Layout.addWidget(self.maxLabel, 2, 0)
        self.parameter_Window_Layout.addWidget(self.maxLine, 2, 1)
        self.parameter_Window_Layout.addWidget(self.minLabel, 3, 0)
        self.parameter_Window_Layout.addWidget(self.minLine, 3, 1)
        self.parameter_Window_Layout.addWidget(self.boxWidthLabel, 4, 0)
        self.parameter_Window_Layout.addWidget(self.boxWidthLineEdit, 4, 1)
        self.parameter_Window_Layout.addWidget(self.boxHeightLabel, 5, 0)
        self.parameter_Window_Layout.addWidget(self.boxHeightLineEdit, 5, 1)
        self.parameter_Window_Layout.addWidget(self.grayMaxLabel, 6, 0)
        self.parameter_Window_Layout.addWidget(self.grayMaxLine, 6, 1)
        self.parameter_Window_Layout.addWidget(self.grayMinLabel, 7, 0)
        self.parameter_Window_Layout.addWidget(self.grayMinLine, 7, 1)
        self.parameter_Window_Layout.addItem(QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Expanding))
        self.parameter_Window_Layout.setSpacing(1)
        self.parameter_Window_Layout.setContentsMargins(15, 10, 50, 0)

        self.cancelButton = QPushButton("Cancle")
        self.cancelButton.setFont(self.globalFont)
        self.cancelButton.setStyleSheet("color: " + self.globalFontColor)
        self.cancelButton.setFixedSize(self.appWidth*0.1, self.appHeight*0.05)
        self.cancelButton.setFlat(True)

        self.applyButton = QPushButton("Apply")
        self.applyButton.setFont(self.globalFont)
        self.applyButton.setStyleSheet("color: " + self.globalFontColor)
        self.applyButton.setFixedSize(self.appWidth*0.1, self.appHeight*0.05)
        self.applyButton.setFlat(True)

        self.okButton = QPushButton("OK")
        self.okButton.setFont(self.globalFont)
        self.okButton.setStyleSheet("color: " + self.globalFontColor)
        self.okButton.setFixedSize(self.appWidth*0.1, self.appHeight*0.05)
        self.okButton.setFlat(True)

        self.controlBar = QLabel()
        self.controlBar.setFixedSize(self.appWidth, self.appHeight*0.05)
        self.controlBar.setStyleSheet("background-color: white")
        self.controlBar_Layout = QHBoxLayout(self.controlBar)
        self.controlBar_Layout.addItem(QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Expanding))
        self.controlBar_Layout.addWidget(self.cancelButton)
        self.controlBar_Layout.addWidget(self.applyButton)
        self.controlBar_Layout.addWidget(self.okButton)
        self.controlBar_Layout.setSpacing(5)
        self.controlBar_Layout.setContentsMargins(0, 0, 0, 0)

        self.parameter_setting_Layout = QVBoxLayout(self)
        self.parameter_setting_Layout.addWidget(self.toolbarLabel)
        self.parameter_setting_Layout.addWidget(self.parameter_SettingWindow)
        self.parameter_setting_Layout.addWidget(self.controlBar)
        self.parameter_setting_Layout.setSpacing(0)
        self.parameter_setting_Layout.setContentsMargins(0, 0, 0, 0)

        self.closeButton.clicked.connect(self.close_system)

    def close_system(self):
        self.parameter_button_icon_change.emit()
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
