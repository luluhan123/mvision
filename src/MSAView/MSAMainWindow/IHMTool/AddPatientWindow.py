#!/usr/bin/env python

from PyQt5.QtCore import pyqtSignal, Qt, QSize
from PyQt5.QtWidgets import QWidget, QApplication, QLabel, QHBoxLayout, QLineEdit, QGridLayout, QFrame, QVBoxLayout, QPushButton, QCheckBox, QSpacerItem, QSizePolicy
from PyQt5.QtGui import QIcon


class AddPatientWindow(QWidget):

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
        self.width = self.desktop.width()
        self.height = self.desktop.height()

        self.appWidth = self.width * 0.3
        self.appHeight = self.height * 0.35

        self.appX = (self.width - self.appWidth) / 2
        self.appY = (self.height - self.appHeight) / 2
        self.setGeometry(self.appX, self.appY, self.appWidth, self.appHeight)
        self.draw_background()

        # ----------------------------------------------------------
        # configure the appearance of the graphical interface
        # ----------------------------------------------------------
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setWindowOpacity(1.0)
        self.setMouseTracking(True)
        self.setAutoFillBackground(True)

        self.patient_name_label = QLabel()
        self.patient_name_label.setText("Name")
        self.patient_name_label.setFixedSize(self.appWidth * 0.2, self.appHeight * 0.04)
        self.patient_name_label.setStyleSheet("margin-left:6px; color: " + self.globalFontColor)
        self.patient_name_label.setCursor(Qt.PointingHandCursor)
        self.patient_name_label.setFont(self.globalFont)

        self.patient_name_lineEdit = QLineEdit()
        self.patient_name_lineEdit.setFixedSize(self.appWidth * 0.3, self.appHeight * 0.06)
        self.patient_name_lineEdit.setFont(self.globalFont)
        self.patient_name_lineEdit.setStyleSheet("border: 1px solid " + self.globalFontColor + "; border-radius: 0px;padding: 2 2px;background: transparent;selection-background-color: skyBlue; color: " + self.globalFontColor)

        self.patient_age_label = QLabel()
        self.patient_age_label.setText("Age")
        self.patient_age_label.setFixedSize(self.appWidth * 0.2, self.appHeight * 0.04)
        self.patient_age_label.setStyleSheet("margin-left:6px; color: " + self.globalFontColor)
        self.patient_age_label.setCursor(Qt.PointingHandCursor)
        self.patient_age_label.setFont(self.globalFont)

        self.patient_age_lineEdit = QLineEdit()
        self.patient_age_lineEdit.setFixedSize(self.appWidth * 0.3, self.appHeight * 0.06)
        self.patient_age_lineEdit.setFont(self.globalFont)
        self.patient_age_lineEdit.setStyleSheet("border: 1px solid " + self.globalFontColor + "; border-radius: 0px;padding: 2 2px;background: transparent;selection-background-color: skyBlue; color: " + self.globalFontColor)

        self.patient_weight_label = QLabel()
        self.patient_weight_label.setText("Weight")
        self.patient_weight_label.setFixedSize(self.appWidth * 0.2, self.appHeight * 0.04)
        self.patient_weight_label.setStyleSheet("margin-left:6px; color: " + self.globalFontColor)
        self.patient_weight_label.setCursor(Qt.PointingHandCursor)
        self.patient_weight_label.setFont(self.globalFont)

        self.patient_weight_lineEdit = QLineEdit()
        self.patient_weight_lineEdit.setFixedSize(self.appWidth * 0.3, self.appHeight * 0.06)
        self.patient_weight_lineEdit.setFont(self.globalFont)
        self.patient_weight_lineEdit.setStyleSheet("border: 1px solid " + self.globalFontColor + "; border-radius: 0px;padding: 2 2px;background: transparent;selection-background-color: skyBlue; color: " + self.globalFontColor)

        self.patient_information_label = QLabel()
        self.patient_information_label.setFixedSize(self.appWidth * 0.5, self.appHeight * 0.25)
        self.patient_information_label.setStyleSheet("border:0px ; color: " + self.globalFontColor)
        self.patient_information_layout = QGridLayout(self.patient_information_label)
        self.patient_information_layout.addWidget(self.patient_name_label, 0, 0)
        self.patient_information_layout.addWidget(self.patient_name_lineEdit, 0, 1)
        self.patient_information_layout.addWidget(self.patient_age_label, 1, 0)
        self.patient_information_layout.addWidget(self.patient_age_lineEdit, 1, 1)
        self.patient_information_layout.addWidget(self.patient_weight_label, 2, 0)
        self.patient_information_layout.addWidget(self.patient_weight_lineEdit, 2, 1)
        self.patient_information_layout.setContentsMargins(0, 0, 0, 0)
        self.patient_information_layout.setSpacing(0)

        self.surgeryPictureEdit = QLabel("")
        self.surgeryPictureEdit.setFixedSize(self.appWidth * 0.4, self.appHeight * 0.25)
        self.surgeryPictureEdit.setStyleSheet("border: 1px solid " + self.globalFontColor + "; border-radius: 0px; padding: 2 2px; background: transparent; selection-background-color: skyBlue; color: " + self.globalFontColor)
        self.surgeryPictureEdit.setFont(self.globalFont)

        self.surgeryPictureWidget = QWidget()
        self.surgeryPictureWidget.setFixedSize(self.appWidth, self.appHeight * 0.3)
        self.surgeryPictureWidget.setStyleSheet("background-color: transparent; border:1px solider " + self.globalFontColor)
        self.surgeryPictureWidgetLayout = QHBoxLayout(self.surgeryPictureWidget)
        self.surgeryPictureWidgetLayout.addWidget(self.patient_information_label)
        self.surgeryPictureWidgetLayout.addWidget(self.surgeryPictureEdit)
        self.surgeryPictureWidgetLayout.setContentsMargins(0, 0, 0, 0)
        self.surgeryPictureWidgetLayout.setSpacing(0)

        self.surgeryIdLabel = QLabel()
        self.surgeryIdLabel.setText("Surgery ID")
        self.surgeryIdLabel.setFixedSize(self.appWidth * 0.45, self.appHeight * 0.04)
        self.surgeryIdLabel.setStyleSheet("margin-left:6px; color:" + self.globalFontColor)
        self.surgeryIdLabel.setCursor(Qt.PointingHandCursor)
        self.surgeryIdLabel.setFont(self.globalFont)

        self.surgeryIdEdit = QLineEdit()
        self.surgeryIdEdit.setFixedSize(self.appWidth * 0.5, self.appHeight * 0.04)
        self.surgeryIdEdit.setStyleSheet("border: 1px solid " + self.globalFontColor + "; border-radius: 0px; padding:2 2px; background:transparent;selection-background-color: skyBlue; color: " + self.globalFontColor)
        self.surgeryIdEdit.setFont(self.globalFont)

        self.surgeryIdWidget = QWidget()
        self.surgeryIdWidget.setFixedSize(self.appWidth, self.appHeight * 0.06)
        self.surgeryIdWidget.setStyleSheet("background-color: transparent; border:1px solide " + self.globalFontColor)
        self.surgeryIdWidgetLayout = QHBoxLayout(self.surgeryIdWidget)
        self.surgeryIdWidgetLayout.addWidget(self.surgeryIdLabel)
        self.surgeryIdWidgetLayout.addWidget(self.surgeryIdEdit)
        self.surgeryIdWidgetLayout.setContentsMargins(0, 0, 0, 0)
        self.surgeryIdWidgetLayout.setSpacing(0)

        self.patientNameLabel = QLabel()
        self.patientNameLabel.setText("Patient Name")
        self.patientNameLabel.setFixedSize(self.appWidth * 0.45, self.appHeight * 0.04)
        self.patientNameLabel.setStyleSheet("margin-left:6px; color: " + self.globalFontColor)
        self.patientNameLabel.setCursor(Qt.PointingHandCursor)
        self.patientNameLabel.setFont(self.globalFont)

        self.patientNameEdit = QLineEdit()
        self.patientNameEdit.setFixedSize(self.appWidth * 0.5, self.appHeight * 0.06)
        self.patientNameEdit.setStyleSheet("border: 1px solid " + self.globalFontColor + "; border-radius: 0px;padding: 2 2px;background: transparent;selection-background-color: skyBlue; color: " + self.globalFontColor)
        self.patientNameEdit.setFont(self.globalFont)

        self.patientNameWidget = QWidget()
        self.patientNameWidget.setFixedSize(self.appWidth, self.appHeight * 0.06)
        self.patientNameWidget.setStyleSheet("background-color: transparent; "
                                             "border:1px solider " + self.globalFontColor)
        self.patientNameWidgetLayout = QHBoxLayout(self.patientNameWidget)
        self.patientNameWidgetLayout.addWidget(self.patientNameLabel)
        self.patientNameWidgetLayout.addWidget(self.patientNameEdit)
        self.patientNameWidgetLayout.setContentsMargins(0, 0, 0, 0)
        self.patientNameWidgetLayout.setSpacing(0)

        self.surgeryDateLabel = QLabel()
        self.surgeryDateLabel.setText("Patient date")
        self.surgeryDateLabel.setFixedSize(self.appWidth * 0.45, self.appHeight * 0.04)
        self.surgeryDateLabel.setStyleSheet("margin-left:6px; color: " + self.globalFontColor)
        self.surgeryDateLabel.setCursor(Qt.PointingHandCursor)
        self.surgeryDateLabel.setFont(self.globalFont)

        self.surgeryDateEdit = QLineEdit()
        self.surgeryDateEdit.setFixedSize(self.appWidth * 0.5, self.appHeight * 0.06)
        self.surgeryDateEdit.setStyleSheet("border: 1px solid " + self.globalFontColor + "; border-radius: 0px;padding: 2 2px;background: transparent;selection-background-color: skyBlue; color: " + self.globalFontColor)
        self.surgeryDateEdit.setFont(self.globalFont)

        self.surgeryDateWidget = QWidget()
        self.surgeryDateWidget.setFixedSize(self.appWidth, self.appHeight * 0.06)
        self.surgeryDateWidget.setStyleSheet("background-color: transparent; border:1px solider " + self.globalFontColor)
        self.surgeryDateWidgetLayout = QHBoxLayout(self.surgeryDateWidget)
        self.surgeryDateWidgetLayout.addWidget(self.surgeryDateLabel)
        self.surgeryDateWidgetLayout.addWidget(self.surgeryDateEdit)
        self.surgeryDateWidgetLayout.setContentsMargins(0, 0, 0, 0)
        self.surgeryDateWidgetLayout.setSpacing(0)

        self.maxLabel = QLabel("Max:")
        self.maxLabel.setFixedSize(self.appWidth * 0.45, self.appHeight * 0.04)
        self.maxLabel.setFont(self.globalFont)
        self.maxLabel.setStyleSheet("margin-left:6px; color: " + self.globalFontColor)
        # self.maxLabel.setAlignment(Qt.AlignCenter)

        self.max_lineEdit = QLineEdit()
        self.max_lineEdit.setFixedSize(self.appWidth * 0.5, self.appHeight * 0.06)
        self.max_lineEdit.setFont(self.globalFont)
        self.max_lineEdit.setStyleSheet("border: 1px solid " + self.globalFontColor + "; border-radius: 0px;padding: 2 2px;background: transparent;selection-background-color: skyBlue; color: " + self.globalFontColor)

        self.maxWidget = QWidget()
        self.maxWidget.setFixedSize(self.appWidth, self.appHeight * 0.06)
        self.maxWidget.setStyleSheet("background-color: transparent; border:1px solider " + self.globalFontColor)
        self.maxWidgetLayout = QHBoxLayout(self.maxWidget)
        self.maxWidgetLayout.addWidget(self.maxLabel)
        self.maxWidgetLayout.addWidget(self.max_lineEdit)
        self.maxWidgetLayout.setContentsMargins(0, 0, 0, 0)
        self.maxWidgetLayout.setSpacing(0)

        self.minLabel = QLabel("Sugar:")
        self.minLabel.setFixedSize(self.appWidth * 0.45, self.appHeight * 0.04)
        self.minLabel.setFont(self.globalFont)
        self.minLabel.setStyleSheet("margin-left:6px; color: " + self.globalFontColor)
        # self.minLabel.setAlignment(Qt.AlignCenter)

        self.min_lineEdit = QLineEdit()
        self.min_lineEdit.setFixedSize(self.appWidth * 0.5, self.appHeight * 0.06)
        self.min_lineEdit.setFont(self.globalFont)
        self.min_lineEdit.setStyleSheet("border: 1px solid " + self.globalFontColor + "; border-radius: 0px;padding: 2 2px;background: transparent;selection-background-color: skyBlue; color: " + self.globalFontColor)

        self.minWidget = QWidget()
        self.minWidget.setFixedSize(self.appWidth, self.appHeight * 0.06)
        self.minWidget.setStyleSheet("background-color: transparent; "
                                     "border:1px solider " + self.globalFontColor)
        self.minWidgetLayout = QHBoxLayout(self.minWidget)
        self.minWidgetLayout.addWidget(self.minLabel)
        self.minWidgetLayout.addWidget(self.min_lineEdit)
        self.minWidgetLayout.setContentsMargins(0, 0, 0, 0)
        self.minWidgetLayout.setSpacing(0)

        self.lipidLabel = QLabel()
        self.lipidLabel.setText("Lipid")
        self.lipidLabel.setFixedSize(self.appWidth * 0.45, self.appHeight * 0.04)
        self.lipidLabel.setStyleSheet("margin-left:6px; color: " + self.globalFontColor)
        self.lipidLabel.setCursor(Qt.PointingHandCursor)
        self.lipidLabel.setFont(self.globalFont)

        self.lipid_lineEdit = QLineEdit()
        self.lipid_lineEdit.setFixedSize(self.appWidth * 0.5, self.appHeight * 0.06)
        self.lipid_lineEdit.setStyleSheet("border: 1px solid " + self.globalFontColor + "; border-radius: 0px;padding: 2 2px;background: transparent;selection-background-color: skyBlue; color: " + self.globalFontColor)
        self.lipid_lineEdit.setFont(self.globalFont)

        self.lipidWidget = QWidget()
        self.lipidWidget.setFixedSize(self.appWidth, self.appHeight * 0.06)
        self.lipidWidget.setStyleSheet("background-color: transparent; border:1px solider " + self.globalFontColor)
        self.lipidWidgetLayout = QHBoxLayout(self.lipidWidget)
        self.lipidWidgetLayout.addWidget(self.lipidLabel)
        self.lipidWidgetLayout.addWidget(self.lipid_lineEdit)
        self.lipidWidgetLayout.setContentsMargins(0, 0, 0, 0)
        self.lipidWidgetLayout.setSpacing(0)

        self.smokeLabel = QCheckBox("Smoke")
        self.smokeLabel.setFixedSize(self.appWidth * 0.33, self.appHeight * 0.04)
        self.smokeLabel.setStyleSheet("margin-left:6px; color: " + self.globalFontColor)
        self.smokeLabel.setCursor(Qt.PointingHandCursor)
        self.smokeLabel.setFont(self.globalFont)

        self.drink_lineEdit = QCheckBox("Drink")
        self.drink_lineEdit.setFixedSize(self.appWidth * 0.33, self.appHeight * 0.04)
        self.drink_lineEdit.setStyleSheet("border: 0px solid " + self.globalFontColor + "; border-radius: 0px;padding: 2 2px;background: transparent;selection-background-color: skyBlue; color: " + self.globalFontColor)
        self.drink_lineEdit.setFont(self.globalFont)

        self.pressure_lineEdit = QCheckBox("Pressure")
        self.pressure_lineEdit.setFixedSize(self.appWidth * 0.33, self.appHeight * 0.04)
        self.pressure_lineEdit.setStyleSheet("border: 0px solid " + self.globalFontColor + "; border-radius: 0px;padding: 2 2px;background: transparent;selection-background-color: skyBlue; color: " + self.globalFontColor)
        self.pressure_lineEdit.setFont(self.globalFont)

        self.characterWidget = QWidget()
        self.characterWidget.setFixedSize(self.appWidth, self.appHeight * 0.045)
        self.characterWidget.setStyleSheet("background-color: transparent; border:1px solider " + self.globalFontColor)
        self.characterWidgetLayout = QHBoxLayout(self.characterWidget)
        self.characterWidgetLayout.addWidget(self.smokeLabel)
        self.characterWidgetLayout.addWidget(self.drink_lineEdit)
        self.characterWidgetLayout.addWidget(self.pressure_lineEdit)
        self.characterWidgetLayout.setContentsMargins(0, 0, 0, 0)
        self.characterWidgetLayout.setSpacing(0)

        self.infectionLabel = QLabel()
        self.infectionLabel.setText("Infection")
        self.infectionLabel.setFixedSize(self.appWidth * 0.45, self.appHeight * 0.04)
        self.infectionLabel.setStyleSheet("margin-left:6px; color: " + self.globalFontColor)
        self.infectionLabel.setCursor(Qt.PointingHandCursor)
        self.infectionLabel.setFont(self.globalFont)

        self.infection_lineEdit = QLineEdit()
        self.infection_lineEdit.setFixedSize(self.appWidth * 0.5, self.appHeight * 0.06)
        self.infection_lineEdit.setStyleSheet("border: 1px solid " + self.globalFontColor + "; border-radius: 0px;padding: 2 2px;background: transparent;selection-background-color: skyBlue; color: " + self.globalFontColor)
        self.infection_lineEdit.setFont(self.globalFont)

        self.infectionWidget = QWidget()
        self.infectionWidget.setFixedSize(self.appWidth, self.appHeight * 0.06)
        self.infectionWidget.setStyleSheet("background-color: transparent; border:1px solider " + self.globalFontColor)
        self.infectionWidgetLayout = QHBoxLayout(self.infectionWidget)
        self.infectionWidgetLayout.addWidget(self.infectionLabel)
        self.infectionWidgetLayout.addWidget(self.infection_lineEdit)
        self.infectionWidgetLayout.setContentsMargins(0, 0, 0, 0)
        self.infectionWidgetLayout.setSpacing(0)

        self.surgeryInformationArea = QFrame()
        self.surgeryInformationArea.setFixedSize(self.appWidth, self.appHeight *0.95)
        self.surgeryInformationArea.setFont(self.globalFont)
        self.surgeryInformationAreaLayout = QVBoxLayout(self.surgeryInformationArea)
        self.surgeryInformationAreaLayout.addWidget(self.surgeryPictureWidget)  # 0.25
        self.surgeryInformationAreaLayout.addWidget(self.patientNameWidget)  # 0.04
        self.surgeryInformationAreaLayout.addWidget(self.surgeryDateWidget)  # 0.04
        self.surgeryInformationAreaLayout.addWidget(self.surgeryIdWidget)  # 0.04
        self.surgeryInformationAreaLayout.addWidget(self.maxWidget)       #0.04
        self.surgeryInformationAreaLayout.addWidget(self.minWidget)       #0.04
        self.surgeryInformationAreaLayout.addWidget(self.lipidWidget)     #0.04
        self.surgeryInformationAreaLayout.addWidget(self.infectionWidget) #0.04
        self.surgeryInformationAreaLayout.addWidget(self.characterWidget) #0.045
        self.surgeryInformationAreaLayout.setContentsMargins(1, 0, 1, 0)
        self.surgeryInformationAreaLayout.setSpacing(1)

        self.blank = QLabel()
        self.blank.setFixedSize(self.appWidth, self.appHeight * 0.01)

        self.closeButton = QPushButton()
        self.closeButton.setStyleSheet("background:transparent")
        self.closeButton.setIcon(QIcon(":/cancle.png"))
        self.closeButton.setFixedSize(self.appWidth*0.038, self.appHeight*0.04)
        self.closeButton.setIconSize(QSize(self.appWidth*0.035, self.appHeight*0.035))
        self.closeButton.setFlat(True)

        self.maximizeButton = QPushButton()
        self.maximizeButton.setFixedSize(self.appWidth*0.04, self.appHeight*0.04)
        self.maximizeButton.setStyleSheet("background:transparent")
        self.maximizeButton.setIcon(QIcon(":/add.png"))
        self.maximizeButton.setIconSize(QSize(self.appWidth*0.035, self.appHeight*0.035))
        self.maximizeButton.setFlat(True)

        self.minimizeButton = QPushButton()
        self.minimizeButton.setStyleSheet("background:transparent")
        self.minimizeButton.setFixedSize(self.appWidth*0.04, self.appHeight*0.04)
        self.minimizeButton.setIcon(QIcon(":/substract.png"))
        self.minimizeButton.setIconSize(QSize(self.appWidth*0.035, self.appHeight*0.035))
        self.minimizeButton.setFlat(True)

        spacer_item = QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Expanding)

        self.toolbarLabel = QLabel()
        self.toolbarLabel.setFixedSize(self.appWidth, self.appHeight*0.05)
        self.toolbarLabel.setStyleSheet("background-color: " + self.globalBackgroundColor)
        self.toolbarLabelLayout = QHBoxLayout(self.toolbarLabel)
        self.toolbarLabelLayout.addWidget(self.closeButton)
        self.toolbarLabelLayout.addWidget(self.minimizeButton)
        self.toolbarLabelLayout.addWidget(self.maximizeButton)
        self.toolbarLabelLayout.addItem(spacer_item)
        self.toolbarLabelLayout.setSpacing(1)
        self.toolbarLabelLayout.setContentsMargins(1, 0, 0, 0)

        self.setting_Window_Layout = QVBoxLayout(self)
        self.setting_Window_Layout.addWidget(self.toolbarLabel)
        self.setting_Window_Layout.addWidget(self.surgeryInformationArea)
        # self.setting_Window_Layout.addWidget(self.blank)
        self.setting_Window_Layout.setSpacing(0)
        self.setting_Window_Layout.setContentsMargins(0, 0, 0, 0)

        self.closeButton.clicked.connect(self.close_system)

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
