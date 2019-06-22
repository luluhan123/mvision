#!/usr/bin/env python3
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtWidgets import QWidget, QApplication, QPushButton, QLabel, QVBoxLayout, QFrame, QGridLayout, QHBoxLayout, QFileDialog
from PyQt5.QtCore import pyqtSignal, Qt
import getpass
import os
import sys


class MSAStartWindow(QWidget):
    """

    """
    exitSystem = pyqtSignal()
    workspaceConfigured = pyqtSignal()
    work_space_icon_change = pyqtSignal()

    def __init__(self, controller=None, background_color="", global_font_color="", global_font=None):
        QWidget.__init__(self)

        path = os.path.dirname(os.path.realpath(__file__))
        temp = path.split("src")

        self.controller = controller
        self.globalBackgroundColor = background_color
        self.globalFontColor = global_font_color
        self.globalFont = global_font

        self.desktop = QApplication.desktop()
        width = self.desktop.width()
        height = self.desktop.height()

        self.appWidth = width*0.3
        self.appHeight = height*0.35

        self.appX = (width - self.appWidth) / 2
        self.appY = (height - self.appHeight) / 2
        self.setGeometry(self.appX, self.appY, self.appWidth, self.appHeight)

        self.mousePointerMove = None
        self.mousePosition = None
        self.mouseLeftButtonPressed = False

        # ----------------------------------------------------------
        # configure the appearance of the graphical interface
        # ----------------------------------------------------------
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setWindowOpacity(1.0)
        self.setMouseTracking(True)
        self.setAutoFillBackground(True)
        self.setStyleSheet("background-color:" + self.globalBackgroundColor + "; color: " + self.globalFontColor + ";")
        self.setFont(self.globalFont)

        self.img1 = QPixmap(temp[0] + "img/title-bar.png")

        self.startWindow_pic = QLabel()
        self.startWindow_pic.setFixedSize(self.appWidth, 20)
        self.img1.scaled(self.startWindow_pic.size(), Qt.KeepAspectRatio)
        self.startWindow_pic.setPixmap(self.img1)

        self.startWindow_blank = QLabel()
        self.startWindow_blank.setFixedSize(self.appWidth * 0.5, 20)

        self.startWindowTitle = QLabel("MedSee Analyseur V2.0")
        self.startWindowTitle.setFixedSize(self.appWidth, self.appHeight*0.1)
        self.startWindowTitle.setStyleSheet("background-color:" + self.globalBackgroundColor + "; color: " + self.globalFontColor + ";")
        self.startWindowTitle.setFont(QFont("System", 14, QFont.Bold, False))
        self.startWindowTitle.setAlignment(Qt.AlignCenter)

        self.workspacePushButton = QPushButton()
        self.workspacePushButton.setText("workspace")
        self.workspacePushButton.setStyleSheet("background-color:" + self.globalBackgroundColor + "; color: " + self.globalFontColor + ";")
        self.workspacePushButton.setFixedSize(self.appWidth*0.2, self.appHeight * 0.1)
        self.workspacePushButton.setFlat(True)

        self.workspaceLabel = QLabel()
        if sys.platform == 'darwin':
            self.workspaceLabel.setText("/Users/" + getpass.getuser() + "/Documents/dat/CTSAWorkspace/")
        elif sys.platform == 'win32':
            self.workspaceLabel.setText("C:\\Users\\" + getpass.getuser() + "\\Documents\\CTSAWorkspace\\")
        else:
            self.workspaceLabel.setText("/home/" + getpass.getuser() + "/Documents/dat/CTSAWorkspace/")

        self.workspaceLabel.setStyleSheet("background-color:" + self.globalBackgroundColor + "; color: " + self.globalFontColor + "; border-width:0px 0px 1px 0px; border-color:" + self.globalFontColor)
        self.workspaceLabel.setFixedSize(self.appWidth * 0.6, self.appHeight * 0.1)
        self.workspaceLabel.setAlignment(Qt.AlignCenter)

        self.targetSpacePushButton = QPushButton()
        self.targetSpacePushButton.setText("targetSpace")
        self.targetSpacePushButton.setStyleSheet("background-color:" + self.globalBackgroundColor + "; color: " + self.globalFontColor + ";")
        self.targetSpacePushButton.setFixedSize(self.appWidth * 0.2, self.appHeight * 0.1)
        self.targetSpacePushButton.setFlat(True)

        self.targetSpaceLabel = QLabel()
        if sys.platform == 'darwin':
            self.targetSpaceLabel.setText("/Users/" + getpass.getuser() + "/Documents/" + "dat/CTSAWorkspace/")
        elif sys.platform == 'win32':
            self.targetSpaceLabel.setText("C:\\Users\\" + getpass.getuser() + "\\Documents\\CTSAWorkspace")
        else:
            self.targetSpaceLabel.setText("/home/" + getpass.getuser() + "/Documents/" + "dat/CTSAWorkspace/")
        self.targetSpaceLabel.setStyleSheet("background-color:" + self.globalBackgroundColor + "; color: " + self.globalFontColor + "; border-width:0px 0px 1px 0px; border-color:" + self.globalFontColor)
        self.targetSpaceLabel.setFixedSize(self.appWidth * 0.6, self.appHeight * 0.1)
        self.targetSpaceLabel.setAlignment(Qt.AlignCenter)

        self.startWindowConfigurationSpace = QFrame()
        self.startWindowConfigurationSpace.setFixedSize(self.appWidth, self.appHeight*0.8)
        self.startWindowConfigurationSpaceLayout = QGridLayout(self.startWindowConfigurationSpace )
        self.startWindowConfigurationSpaceLayout.addWidget(self.workspacePushButton, 0, 0)
        self.startWindowConfigurationSpaceLayout.addWidget(self.workspaceLabel, 0, 1)
        self.startWindowConfigurationSpaceLayout.addWidget(self.targetSpacePushButton, 1, 0)
        self.startWindowConfigurationSpaceLayout.addWidget(self.targetSpaceLabel, 1, 1)

        self.confirmPushButton = QPushButton()
        self.confirmPushButton.setText("confirm")
        self.confirmPushButton.setFixedSize(self.appWidth*0.13, self.appHeight*0.05)
        self.confirmPushButton.setContentsMargins(0, 0, 0, 7)
        self.confirmPushButton.setFlat(True)

        self.canclePushButton = QPushButton()
        self.canclePushButton.setText("cancel")
        self.canclePushButton.setFixedSize(self.appWidth*0.13, self.appHeight*0.05)
        self.canclePushButton.setContentsMargins(0, 0, 0, 7)
        self.canclePushButton.setFlat(True)

        self.spacer = QLabel()
        self.spacer.setFixedSize(self.appWidth*0.72, self.appHeight*0.05)

        self.startWindowIndicationBar = QLabel()
        self.startWindowIndicationBar.setFixedSize(self.appWidth, self.appHeight*0.1)
        self.startWindowIndicationBarLayout = QHBoxLayout(self.startWindowIndicationBar)
        self.startWindowIndicationBarLayout.addWidget(self.spacer)
        self.startWindowIndicationBarLayout.addWidget(self.canclePushButton)
        self.startWindowIndicationBarLayout.addWidget(self.confirmPushButton)
        self.startWindowIndicationBarLayout.setSpacing(1)
        self.startWindowIndicationBar.setContentsMargins(0, 0, 0, 0)

        self.startWindowLayout = QVBoxLayout(self)
        self.startWindowLayout.addWidget(self.startWindowTitle)
        self.startWindowLayout.addWidget(self.startWindowConfigurationSpace)
        self.startWindowLayout.addWidget(self.startWindowIndicationBar)
        self.startWindowLayout.setSpacing(0)
        self.startWindowLayout.setContentsMargins(0, 0, 0, 0)

        self.workspacePushButton.clicked.connect(self.choose_workspace_path)
        self.confirmPushButton.clicked.connect(self.confirm)
        self.canclePushButton.clicked.connect(self.cancel)
        self.targetSpacePushButton.clicked.connect(self.choose_target_workspace_path)

    def cancel(self):
        self.work_space_icon_change.emit()
        self.close()

    def confirm(self):
        self.controller.set_global_workspace(str(self.workspaceLabel.text()))
        self.workspaceConfigured.emit()
        self.close()

    def choose_target_workspace_path(self):
        file_path = QFileDialog.getExistingDirectory(self, 'MedSight file choosing', "/Users/" + getpass.getuser() + "/Documents/")
        file_path = str(file_path) + '/'
        self.targetSpaceLabel.setText(file_path)

    def choose_workspace_path(self):
        file_path = QFileDialog.getExistingDirectory(self, 'MedSight file choosing', "/Users/" + getpass.getuser() + "/Documents/")
        file_path = str(file_path) + '/'
        self.workspaceLabel.setText(file_path)

    def close_system(self):
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
