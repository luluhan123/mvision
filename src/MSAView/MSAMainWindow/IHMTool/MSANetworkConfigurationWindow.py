#!/usr/bin/env python

from PyQt5.QtCore import pyqtSignal, Qt, QSize
from PyQt5.QtWidgets import QWidget, QApplication, QTableWidget, QSpacerItem, QPushButton, QSizePolicy, QLabel, QHBoxLayout, QVBoxLayout, QLineEdit, QGridLayout
from PyQt5.QtGui import QIcon
from MSAView.MSAMainWindow.IHMTool.MSAPlottingBoard import MSAPlottingBoard


class MSANetworkConfigurationWindow(QWidget):

    windowClosed = pyqtSignal()
    newConnection = pyqtSignal()

    def __init__(self, controller=None, ihm_factor=1, background_color="", global_font_color="", global_font=None):
        QWidget.__init__(self)

        self.controller = controller
        self.ihm_factor = ihm_factor
        self.globalBackgroundColor = background_color
        self.globalFontColor = global_font_color
        self.globalFont = global_font

        self.mousePointerMove = None
        self.mousePosition = None
        self.mouseLeftButtonPressed = False

        self.doHandShakeButtonClicked = False

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

        self.communicationTable = QTableWidget()
        self.communicationTable.setFixedSize(self.appWidth, self.appHeight* 0.3)
        self.communicationTable.setRowCount(6)
        self.communicationTable.setColumnCount(6)
        self.communicationTable.setHorizontalHeaderLabels(['device', 'address', 'port', 'transmission', 'reception', 'control'])
        self.communicationTable.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.communicationTable.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.communicationTable.verticalHeader().hide()
        self.communicationTable.setAutoScroll(True)
        self.communicationTable.setContentsMargins(3, 0, 3, 0)

        self.communicationTable.setColumnWidth(0, self.appWidth*0.15)
        self.communicationTable.setColumnWidth(1, self.appWidth * 0.25)
        self.communicationTable.setColumnWidth(2, self.appWidth * 0.15)
        self.communicationTable.setColumnWidth(3, self.appWidth * 0.15)
        self.communicationTable.setColumnWidth(4, self.appWidth * 0.15)
        self.communicationTable.setColumnWidth(5, self.appWidth * 0.15)


        spacer_item = QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Expanding)

        self.right_blank = QLabel()
        self.right_blank.setFixedSize(self.appWidth*0.9, self.appHeight*0.05)

        self.closeButton = QPushButton()
        self.closeButton.setStyleSheet("background:transparent")
        self.closeButton.setIcon(QIcon(":/cancle.png"))
        self.closeButton.setFixedSize(self.appWidth*0.03, self.appWidth*0.03)
        self.closeButton.setIconSize(QSize(self.appWidth*0.03, self.appWidth*0.029))
        self.closeButton.setFlat(True)

        self.maximizeButton = QPushButton()
        self.maximizeButton.setFixedSize(self.appWidth*0.03, self.appHeight*0.04)
        self.maximizeButton.setStyleSheet("background:transparent")
        self.maximizeButton.setIcon(QIcon(":/add.png"))
        self.maximizeButton.setIconSize(QSize(self.appWidth*0.03, self.appWidth*0.028))
        self.maximizeButton.setFlat(True)

        self.minimizeButton = QPushButton()
        self.minimizeButton.setStyleSheet("background:transparent")
        self.minimizeButton.setFixedSize(self.appWidth*0.03, self.appHeight*0.04)
        self.minimizeButton.setIcon(QIcon(":/substract.png"))
        self.minimizeButton.setIconSize(QSize(self.appWidth*0.03, self.appWidth*0.028))
        self.minimizeButton.setFlat(True)

        self.toolbarLabel = QLabel()
        self.toolbarLabel.setFixedSize(self.appWidth, self.appHeight*0.05)
        self.toolbarLabel.setStyleSheet("background-color: " + self.globalBackgroundColor)
        self.toolbarLabelLayout = QHBoxLayout(self.toolbarLabel)
        self.toolbarLabelLayout.addWidget(self.closeButton)
        self.toolbarLabelLayout.addWidget(self.minimizeButton)
        self.toolbarLabelLayout.addWidget(self.maximizeButton)
        self.toolbarLabelLayout.addWidget(self.right_blank)
        self.toolbarLabelLayout.setSpacing(1)
        self.toolbarLabelLayout.setContentsMargins(0, 0, 0, 0)

        self.localIPLabel = QLabel()
        self.localIPLabel.setText("local PC: ")
        self.localIPLabel.setFixedSize(self.appWidth * 0.15, self.appHeight * 0.04)
        self.localIPLabel.setStyleSheet("border: 0px solid blue; margin-left:6px; color: " + self.globalFontColor)
        self.localIPLabel.setCursor(Qt.PointingHandCursor)
        self.localIPLabel.setFont(self.globalFont)

        self.ipAddressLabel = QLabel('IP')
        self.ipAddressLabel.setStyleSheet("border: 0px solid blue; margin-left:6px; color: " + self.globalFontColor)
        self.ipAddressLabel.setFixedSize(self.appWidth * 0.05, self.appHeight * 0.04)
        self.ipAddressLabel.setFont(self.globalFont)

        self.ipAddressLineEdit = QLineEdit()
        self.ipAddressLineEdit.setFixedSize(self.appWidth * 0.25, self.appHeight * 0.04)
        self.ipAddressLineEdit.setStyleSheet("border: 1px solid " + self.globalFontColor + "; border-radius: 0px;padding: 2 2px;background: transparent;selection-background-color: skyBlue; color: " + self.globalFontColor)
        self.ipAddressLineEdit.setFont(self.globalFont)

        self.localPortLabel = QLabel('Port')
        self.localPortLabel.setStyleSheet("margin-left:10px; color: " + self.globalFontColor)
        self.localPortLabel.setFixedSize(self.appWidth * 0.1, self.appHeight * 0.04)
        self.localPortLabel.setFont(self.globalFont)

        self.localPortLineEdit = QLineEdit()
        self.localPortLineEdit.setFixedSize(self.appWidth * 0.25, self.appHeight * 0.04)
        self.localPortLineEdit.setStyleSheet("border: 1px solid " + self.globalFontColor + "; border-radius: 0px;padding: 2 2px;background: transparent;selection-background-color: skyBlue; color: " + self.globalFontColor)
        self.localPortLineEdit.setFont(self.globalFont)

        self.targetPCLabel = QLabel()
        self.targetPCLabel.setText("target PC: ")
        self.targetPCLabel.setFixedSize(self.appWidth * 0.15, self.appHeight * 0.04)
        self.targetPCLabel.setStyleSheet("border: 0px solid blue; margin-left:6px; color: " + self.globalFontColor)
        self.targetPCLabel.setCursor(Qt.PointingHandCursor)
        self.targetPCLabel.setFont(self.globalFont)

        self.targetIPLabel = QLabel('IP')
        self.targetIPLabel.setFixedSize(self.appWidth * 0.05, self.appHeight * 0.04)
        self.targetIPLabel.setStyleSheet("border: 0px solid blue; margin-left:6px; color: " + self.globalFontColor)
        self.targetIPLabel.setFont(self.globalFont)

        self.targetIPLineEdit = QLineEdit("192.168.1.172")
        self.targetIPLineEdit.setFixedSize(self.appWidth * 0.25, self.appHeight * 0.04)
        self.targetIPLineEdit.setStyleSheet("border: 1px solid " + self.globalFontColor + "; border-radius: 0px;padding: 2 2px;background: transparent;selection-background-color: skyBlue; color: " + self.globalFontColor)
        self.targetIPLineEdit.setCursor(Qt.PointingHandCursor)
        self.targetIPLineEdit.setFont(self.globalFont)

        self.targetPortLabel = QLabel('Port')
        self.targetPortLabel.setFixedSize(self.appWidth * 0.1, self.appHeight * 0.04)
        self.targetPortLabel.setStyleSheet("margin-left:10px; color: " + self.globalFontColor)
        self.targetPortLabel.setFont(self.globalFont)

        self.targetPortLineEdit = QLineEdit("10704")
        self.targetPortLineEdit.setFixedSize(self.appWidth * 0.25, self.appHeight * 0.04)
        self.targetPortLineEdit.setStyleSheet("border: 1px solid " + self.globalFontColor + "; border-radius: 0px;padding: 2 2px;background: transparent;selection-background-color: skyBlue; color: " + self.globalFontColor)
        self.targetPortLineEdit.setFont(self.globalFont)

        self.getLocalIpPortButton = QPushButton()
        self.getLocalIpPortButton.setFixedSize(self.appHeight * 0.04, self.appHeight * 0.04)
        self.getLocalIpPortButton.setStyleSheet("background:transparent")
        self.getLocalIpPortButton.setIcon(QIcon(":/cancle.png"))
        self.getLocalIpPortButton.setIconSize(QSize(self.appHeight * 0.04, self.appHeight * 0.04))
        self.getLocalIpPortButton.setFlat(True)

        self.doHandShakeButton = QPushButton()
        self.doHandShakeButton.setStyleSheet("background:transparent")
        self.doHandShakeButton.setIcon(QIcon(":/connect-start.png"))
        self.doHandShakeButton.setFixedSize(self.appHeight * 0.04, self.appHeight * 0.04)
        self.doHandShakeButton.setIconSize(QSize(self.appHeight * 0.04, self.appHeight * 0.04))
        self.doHandShakeButton.setFlat(True)

        spacer = QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Expanding)

        self.settingWindow = QWidget()
        self.settingWindow.setFixedSize(self.appWidth,  self.appHeight*0.15)
        self.settingWindow_Layout = QGridLayout(self.settingWindow)
        self.settingWindow_Layout.addWidget(self.localIPLabel,          0, 0)
        self.settingWindow_Layout.addWidget(self.ipAddressLabel,        0, 1)
        self.settingWindow_Layout.addWidget(self.ipAddressLineEdit,     0, 2)
        self.settingWindow_Layout.addWidget(self.localPortLabel,        0, 3)
        self.settingWindow_Layout.addWidget(self.localPortLineEdit,     0, 4)
        self.settingWindow_Layout.addWidget(self.getLocalIpPortButton,  0, 5)
        self.settingWindow_Layout.addWidget(self.targetPCLabel,         1, 0)
        self.settingWindow_Layout.addWidget(self.targetIPLabel,         1, 1)
        self.settingWindow_Layout.addWidget(self.targetIPLineEdit,      1, 2)
        self.settingWindow_Layout.addWidget(self.targetPortLabel,       1, 3)
        self.settingWindow_Layout.addWidget(self.targetPortLineEdit,    1, 4)
        self.settingWindow_Layout.addWidget(self.doHandShakeButton,     1, 5)
        self.settingWindow_Layout.addItem(spacer,                       1, 6)
        self.settingWindow_Layout.setSpacing(0)
        self.settingWindow_Layout.setContentsMargins(2, 0, 0, 0)

        self.preserveWindow = QWidget()
        self.preserveWindow.setFixedSize(self.appWidth, self.appHeight * 0.55)

        self.plotting_board = MSAPlottingBoard(1, self.controller, self.ihm_factor,self.appWidth, self.appHeight * 0.5, self.globalBackgroundColor, self.globalFontColor, self.globalFont)
        self.plotting_board.setStyleSheet("background-color: rgb(246, 246, 246)")

        self.setting_Window_Layout = QVBoxLayout(self)
        self.setting_Window_Layout.addWidget(self.toolbarLabel)
        self.setting_Window_Layout.addWidget(self.communicationTable)
        self.setting_Window_Layout.addWidget(self.plotting_board)
        self.setting_Window_Layout.addWidget(self.settingWindow)
        self.setting_Window_Layout.setSpacing(1)
        self.setting_Window_Layout.setContentsMargins(0, 0, 0, 0)

        self.connexion()

    def connexion(self):

        self.closeButton.clicked.connect(self.close_system)
        self.doHandShakeButton.clicked.connect(self.do_handshake_button_clicked)
        self.controller.newConnection.connect(self.get_local_addr_port)

    def get_local_addr_port(self):
        addr = self.controller.get_handshake_commit_addr()
        port = self.controller.get_handshake_commit_port()
        self.ipAddressLineEdit.setText(addr)
        self.localPortLineEdit.setText(port)

    def do_handshake_button_clicked(self):
        if self.doHandShakeButtonClicked:
            self.doHandShakeButton.setIcon(QIcon(":/connect-start.png"))
            self.controller.close_session_request(0)

        else:
            self.doHandShakeButton.setIcon(QIcon(":/connect-pasue.png"))
            ip = str(self.targetIPLineEdit.text())
            port = int(self.targetPortLineEdit.text())
            self.controller.do_handshake(ip, port)

        self.doHandShakeButtonClicked = not self.doHandShakeButtonClicked

    def close_system(self):
        self.windowClosed.emit()
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
