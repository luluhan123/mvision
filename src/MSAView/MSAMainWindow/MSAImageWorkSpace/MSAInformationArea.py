#!/usr/bin/env python3

from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit, QGridLayout, QHBoxLayout, QCheckBox,QVBoxLayout,QPushButton, QSpacerItem, QSizePolicy, QFrame, QGroupBox
from PyQt5.QtCore import pyqtSignal, Qt, QSize
from PyQt5.QtGui import QIcon, QColor

from MSAView.MSAMainWindow.IHMTool.ObjectEvent import ObjectEvent
from MSAView.MSAMainWindow.MSAToolBar.MSASessionChooseList import SessionChooseList


class MSAInformationArea(QWidget):

    doVesselEnhancement = pyqtSignal()
    buttonMessage = pyqtSignal(str)
    parameterWindowSetting = pyqtSignal()
    vesselSegmentationWindow = pyqtSignal()

    def __init__(self, parent=None, controller=None, ihm_factor=1, width=0, height=0, background_color="", global_font_color="", global_font=None):
        """MSAInformationArea

            - This class represent the parameter and file information of the analyser

        Attributes:
            -

                *************************
                *                       *
                *                       *
                *  fileListTreeWidget   *
                *                       *
                *                       *
                *************************
                *  filterCmdLine        *
                *************************
                *                       *
                *                       *
                *  parameterListWidget  *
                *                       *
                *                       *
                *************************
        """

        QWidget.__init__(self)
        self.parent = parent
        self.controller = controller
        self.ihm_factor = ihm_factor
        self.vascularButtonClicked = False
        self.splineButtonClicked = False
        self.gvfButtonClicked = False
        self.pointtopointButtonClicked = False
        self.paraSetButtonClicked = False

        self.barWidth = 32*self.ihm_factor

        self.width = width - self.barWidth - 10*self.ihm_factor
        self.height = height

        self.globalBackgroundColor = background_color
        self.globalFontColor = global_font_color
        self.globalFont = global_font

        self.setStyleSheet("background-color:" + self.globalBackgroundColor + "; color:" + self.globalFontColor + ";")
        self.setFixedSize(width, self.height)

        self.window_level_list = [0, 128, 128, 256]

        # ------------------------------------------------------
        # patient's basic information
        # ------------------------------------------------------
        self.paNameLabel = QLabel()
        self.paNameLabel.setText("name : ")
        self.paNameLabel.setFixedSize(self.width * 0.25, self.height * 0.04)
        self.paNameLabel.setStyleSheet("margin-left:3px; color: " + self.globalFontColor)
        self.paNameLabel.setCursor(Qt.PointingHandCursor)
        self.paNameLabel.setFont(self.globalFont)

        self.perNameLineEdit = QLineEdit()
        self.perNameLineEdit.setFixedSize(self.width * 0.27, self.height * 0.04)
        self.perNameLineEdit.setFont(self.globalFont)
        self.perNameLineEdit.setStyleSheet("border: 1px solid " + self.globalFontColor + "; border-radius: 0px;padding: 2 2px; border-width:0px 0px 1px 0px; background: transparent;selection-background-color: skyBlue; color: " + self.globalFontColor)

        self.paAgeLabel = QLabel()
        self.paAgeLabel.setText("age : ")
        self.paAgeLabel.setFixedSize(self.width * 0.25, self.height * 0.04)
        self.paAgeLabel.setStyleSheet("margin-left:3px; color: " + self.globalFontColor)
        self.paAgeLabel.setCursor(Qt.PointingHandCursor)
        self.paAgeLabel.setFont(self.globalFont)

        self.perAgeLineEdit = QLineEdit()
        self.perAgeLineEdit.setFixedSize(self.width * 0.27, self.height * 0.04)
        self.perAgeLineEdit.setFont(self.globalFont)
        self.perAgeLineEdit.setStyleSheet("border: 1px solid " + self.globalFontColor + "; border-radius: 0px;padding: 2 2px; border-width:0px 0px 1px 0px; background: transparent;selection-background-color: skyBlue; color: " + self.globalFontColor)

        self.perWeightLabel = QLabel()
        self.perWeightLabel.setText("weight : ")
        self.perWeightLabel.setFixedSize(self.width * 0.25, self.height * 0.04)
        self.perWeightLabel.setStyleSheet("margin-left:3px; color: " + self.globalFontColor)
        self.perWeightLabel.setCursor(Qt.PointingHandCursor)
        self.perWeightLabel.setFont(self.globalFont)

        self.perWeightLineEdit = QLineEdit()
        self.perWeightLineEdit.setFixedSize(self.width * 0.27, self.height * 0.04)
        self.perWeightLineEdit.setFont(self.globalFont)
        self.perWeightLineEdit.setStyleSheet("border: 1px solid " + self.globalFontColor + "; border-radius: 0px;padding: 2 2px; border-width:0px 0px 1px 0px; background: transparent;selection-background-color: skyBlue; color: " + self.globalFontColor)

        self.perInforLabel = QLabel()
        self.perInforLabel.setFixedSize(self.width * 0.6, self.height * 0.13)
        self.perInforLabel.setStyleSheet("border:0px ; color: "+ self.globalFontColor)
        self.perInforLayout = QGridLayout(self.perInforLabel)
        self.perInforLayout.addWidget(self.paNameLabel, 0, 0)
        self.perInforLayout.addWidget(self.perNameLineEdit, 0, 1)
        self.perInforLayout.addWidget(self.paAgeLabel, 1, 0)
        self.perInforLayout.addWidget(self.perAgeLineEdit, 1, 1)
        self.perInforLayout.addWidget(self.perWeightLabel, 2, 0)
        self.perInforLayout.addWidget(self.perWeightLineEdit, 2, 1)
        self.perInforLayout.setContentsMargins(0, 0, 0, 0)
        self.perInforLayout.setSpacing(0)

        self.surgeryPictureEdit = QLabel("")
        self.surgeryPictureEdit.setFixedSize(self.width * 0.35, self.height * 0.13)
        self.surgeryPictureEdit.setStyleSheet("border: 1px solid " + self.globalFontColor + "; border-radius: 0px; padding: 2 2px; background: transparent; selection-background-color: skyBlue; color: " + self.globalFontColor)
        self.surgeryPictureEdit.setFont(self.globalFont)

        self.surgeryPictureWidget = QWidget()
        self.surgeryPictureWidget.setFixedSize(self.width*0.95, self.height * 0.13)
        self.surgeryPictureWidget.setStyleSheet("background-color: transparent; border:1px solider " + self.globalFontColor)
        self.surgeryPictureWidgetLayout = QHBoxLayout(self.surgeryPictureWidget)
        self.surgeryPictureWidgetLayout.addWidget(self.perInforLabel)
        self.surgeryPictureWidgetLayout.addWidget(self.surgeryPictureEdit)
        self.surgeryPictureWidgetLayout.setContentsMargins(0, 0, 0, 0)
        self.surgeryPictureWidgetLayout.setSpacing(0)

        self.surgeryIdLabel = QLabel()
        self.surgeryIdLabel.setText("surgery ID ： ")
        self.surgeryIdLabel.setFixedSize(self.width * 0.45, self.height * 0.04)
        self.surgeryIdLabel.setStyleSheet("margin-left:3px; color:" + self.globalFontColor)
        self.surgeryIdLabel.setCursor(Qt.PointingHandCursor)
        self.surgeryIdLabel.setFont(self.globalFont)

        self.surgeryIdEdit = QLineEdit()
        self.surgeryIdEdit.setFixedSize(self.width * 0.45, self.height * 0.04)
        self.surgeryIdEdit.setStyleSheet("border: 1px solid " + self.globalFontColor + "; border-radius: 0px; padding:2 2px; border-width:0px 0px 1px 0px; background:transparent;selection-background-color: skyBlue; color: " + self.globalFontColor)
        self.surgeryIdEdit.setFont(self.globalFont)

        self.surgeryIdWidget = QWidget()
        self.surgeryIdWidget.setFixedSize(self.width*0.95, self.height * 0.04)
        self.surgeryIdWidget.setStyleSheet("background-color: transparent; border:0px solid " + self.globalFontColor)
        self.surgeryIdWidgetLayout = QHBoxLayout(self.surgeryIdWidget)
        self.surgeryIdWidgetLayout.addWidget(self.surgeryIdLabel)
        self.surgeryIdWidgetLayout.addWidget(self.surgeryIdEdit)
        self.surgeryIdWidgetLayout.setContentsMargins(0, 0, 0, 0)
        self.surgeryIdWidgetLayout.setSpacing(0)

        self.patientNameLabel = QLabel()
        self.patientNameLabel.setText("patient name ： ")
        self.patientNameLabel.setFixedSize(self.width * 0.45, self.height * 0.04)
        self.patientNameLabel.setStyleSheet("margin-left:3px; color: " + self.globalFontColor)
        self.patientNameLabel.setCursor(Qt.PointingHandCursor)
        self.patientNameLabel.setFont(self.globalFont)

        self.patientNameEdit = QLineEdit()
        self.patientNameEdit.setFixedSize(self.width * 0.45, self.height * 0.04)
        self.patientNameEdit.setStyleSheet("border: 1px solid " + self.globalFontColor + "; border-radius: 0px;padding: 2 2px; border-width:0px 0px 1px 0px; background: transparent;selection-background-color: skyBlue; color: " + self.globalFontColor)
        self.patientNameEdit.setFont(self.globalFont)

        self.patientNameWidget = QWidget()
        self.patientNameWidget.setFixedSize(self.width*0.95, self.height * 0.04)
        self.patientNameWidget.setStyleSheet("background-color: transparent; "
                                             "border:1px solider " + self.globalFontColor)
        self.patientNameWidgetLayout = QHBoxLayout(self.patientNameWidget)
        self.patientNameWidgetLayout.addWidget(self.patientNameLabel)
        self.patientNameWidgetLayout.addWidget(self.patientNameEdit)
        self.patientNameWidgetLayout.setContentsMargins(0, 0, 0, 0)
        self.patientNameWidgetLayout.setSpacing(0)

        self.surgeryDateLabel = QLabel()
        self.surgeryDateLabel.setText("patient date ： ")
        self.surgeryDateLabel.setFixedSize(self.width * 0.45, self.height * 0.04)
        self.surgeryDateLabel.setStyleSheet("margin-left:3px; color: " + self.globalFontColor)
        self.surgeryDateLabel.setCursor(Qt.PointingHandCursor)
        self.surgeryDateLabel.setFont(self.globalFont)

        self.surgeryDateEdit = QLineEdit()
        self.surgeryDateEdit.setFixedSize(self.width * 0.45, self.height * 0.04)
        self.surgeryDateEdit.setStyleSheet("border: 1px solid " + self.globalFontColor + "; border-radius: 0px;padding: 2 2px; border-width:0px 0px 1px 0px; background: transparent;selection-background-color: skyBlue; color: " + self.globalFontColor)
        self.surgeryDateEdit.setFont(self.globalFont)

        self.surgeryDateWidget = QWidget()
        self.surgeryDateWidget.setFixedSize(self.width*0.95, self.height * 0.04)
        self.surgeryDateWidget.setStyleSheet("background-color: transparent; border:1px solider " + self.globalFontColor)
        self.surgeryDateWidgetLayout = QHBoxLayout(self.surgeryDateWidget)
        self.surgeryDateWidgetLayout.addWidget(self.surgeryDateLabel)
        self.surgeryDateWidgetLayout.addWidget(self.surgeryDateEdit)
        self.surgeryDateWidgetLayout.setContentsMargins(0, 0, 0, 0)
        self.surgeryDateWidgetLayout.setSpacing(0)

        self.maxLabel = QLabel("max : ")
        self.maxLabel.setFixedSize(self.width * 0.45, self.height * 0.04)
        self.maxLabel.setFont(self.globalFont)
        self.maxLabel.setStyleSheet("margin-left:3px; color: " + self.globalFontColor)
        # self.maxLabel.setAlignment(Qt.AlignCenter)

        self.maxline = QLineEdit()
        self.maxline.setFixedSize(self.width * 0.45, self.height * 0.04)
        self.maxline.setFont(self.globalFont)
        self.maxline.setStyleSheet("border: 1px solid " + self.globalFontColor + "; border-radius: 0px;padding: 2 2px; border-width:0px 0px 1px 0px; background: transparent;selection-background-color: skyBlue; color: " + self.globalFontColor)

        self.maxWidget = QWidget()
        self.maxWidget.setFixedSize(self.width*0.95, self.height * 0.04)
        self.maxWidget.setStyleSheet("background-color: transparent; border:1px solider " + self.globalFontColor)
        self.maxWidgetLayout = QHBoxLayout(self.maxWidget)
        self.maxWidgetLayout.addWidget(self.maxLabel)
        self.maxWidgetLayout.addWidget(self.maxline)
        self.maxWidgetLayout.setContentsMargins(0, 0, 0, 0)
        self.maxWidgetLayout.setSpacing(0)

        self.minLabel = QLabel("sugar : ")
        self.minLabel.setFixedSize(self.width * 0.45, self.height * 0.04)
        self.minLabel.setFont(self.globalFont)
        self.minLabel.setStyleSheet("margin-left:3px; color: " + self.globalFontColor)
        # self.minLabel.setAlignment(Qt.AlignCenter)

        self.minline = QLineEdit()
        self.minline.setFixedSize(self.width * 0.45, self.height * 0.04)
        self.minline.setFont(self.globalFont)
        self.minline.setStyleSheet("border: 1px solid " + self.globalFontColor + "; border-radius: 0px;padding: 2 2px; border-width:0px 0px 1px 0px; background: transparent;selection-background-color: skyBlue; color: " + self.globalFontColor)

        self.minWidget = QWidget()
        self.minWidget.setFixedSize(self.width*0.95, self.height * 0.04)
        self.minWidget.setStyleSheet("background-color: transparent; "
                                     "border:1px solider " + self.globalFontColor)
        self.minWidgetLayout = QHBoxLayout(self.minWidget)
        self.minWidgetLayout.addWidget(self.minLabel)
        self.minWidgetLayout.addWidget(self.minline)
        self.minWidgetLayout.setContentsMargins(0, 0, 0, 0)
        self.minWidgetLayout.setSpacing(0)

        self.lipidLabel = QLabel()
        self.lipidLabel.setText("lipid ： ")
        self.lipidLabel.setFixedSize(self.width * 0.45, self.height * 0.04)
        self.lipidLabel.setStyleSheet("margin-left:3px; color: " + self.globalFontColor)
        self.lipidLabel.setCursor(Qt.PointingHandCursor)
        self.lipidLabel.setFont(self.globalFont)

        self.lipidlineEdit = QLineEdit()
        self.lipidlineEdit.setFixedSize(self.width * 0.45, self.height * 0.04)
        self.lipidlineEdit.setStyleSheet("border: 1px solid " + self.globalFontColor + "; border-radius: 0px;padding: 2 2px; border-width:0px 0px 1px 0px; background: transparent;selection-background-color: skyBlue; color: " + self.globalFontColor)
        self.lipidlineEdit.setFont(self.globalFont)

        self.lipidWidget = QWidget()
        self.lipidWidget.setFixedSize(self.width*0.95, self.height * 0.04)
        self.lipidWidget.setStyleSheet("background-color: transparent; border:1px solider " + self.globalFontColor)
        self.lipidWidgetLayout = QHBoxLayout(self.lipidWidget)
        self.lipidWidgetLayout.addWidget(self.lipidLabel)
        self.lipidWidgetLayout.addWidget(self.lipidlineEdit)
        self.lipidWidgetLayout.setContentsMargins(0, 0, 0, 0)
        self.lipidWidgetLayout.setSpacing(0)

        self.smokeLabel = QCheckBox("smoke")
        self.smokeLabel.setFixedSize(self.width * 0.3, self.height * 0.035)
        self.smokeLabel.setStyleSheet("margin-left:3px; color: " + self.globalFontColor)
        self.smokeLabel.setCursor(Qt.PointingHandCursor)
        self.smokeLabel.setFont(self.globalFont)

        self.drinkineEdit = QCheckBox("drink")
        self.drinkineEdit.setFixedSize(self.width * 0.3, self.height * 0.035)
        self.drinkineEdit.setStyleSheet("border: 0px solid " + self.globalFontColor + "; border-radius: 0px;padding: 2 2px;background: transparent;selection-background-color: skyBlue; color: " + self.globalFontColor)
        self.drinkineEdit.setFont(self.globalFont)

        self.pressurelineEdit = QCheckBox("pressure ： ")
        self.pressurelineEdit.setFixedSize(self.width * 0.33, self.height * 0.035)
        self.pressurelineEdit.setStyleSheet("border: 0px solid " + self.globalFontColor + "; border-radius: 0px;padding: 2 2px;background: transparent;selection-background-color: skyBlue; color: " + self.globalFontColor)
        self.pressurelineEdit.setFont(self.globalFont)

        self.characterWidget = QWidget()
        self.characterWidget.setFixedSize(self.width*0.95, self.height * 0.035)
        self.characterWidget.setStyleSheet("background-color: transparent; border:1px solider " + self.globalFontColor)
        self.characterWidgetLayout = QHBoxLayout(self.characterWidget)
        self.characterWidgetLayout.addWidget(self.smokeLabel)
        self.characterWidgetLayout.addWidget(self.drinkineEdit)
        self.characterWidgetLayout.addWidget(self.pressurelineEdit)
        self.characterWidgetLayout.setContentsMargins(0, 0, 0, 0)
        self.characterWidgetLayout.setSpacing(0)

        self.infectionLabel = QLabel()
        self.infectionLabel.setText("infection ： ")
        self.infectionLabel.setFixedSize(self.width * 0.45, self.height * 0.04)
        self.infectionLabel.setStyleSheet("margin-left:3px; color: " + self.globalFontColor)
        self.infectionLabel.setCursor(Qt.PointingHandCursor)
        self.infectionLabel.setFont(self.globalFont)

        self.infectionlineEdit = QLineEdit()
        self.infectionlineEdit.setFixedSize(self.width * 0.45, self.height * 0.04)
        self.infectionlineEdit.setStyleSheet("border: 1px solid " + self.globalFontColor + "; border-radius: 0px;padding: 2 2px;  border-width:0px 0px 1px 0px; background: transparent;selection-background-color: skyBlue; color: " + self.globalFontColor)
        self.infectionlineEdit.setFont(self.globalFont)

        self.infectionWidget = QWidget()
        self.infectionWidget.setFixedSize(self.width*0.95, self.height * 0.04)
        self.infectionWidget.setStyleSheet("background-color: transparent; border:1px solider " + self.globalFontColor)
        self.infectionWidgetLayout = QHBoxLayout(self.infectionWidget)
        self.infectionWidgetLayout.addWidget(self.infectionLabel)
        self.infectionWidgetLayout.addWidget(self.infectionlineEdit)
        self.infectionWidgetLayout.setContentsMargins(0, 0, 0, 0)
        self.infectionWidgetLayout.setSpacing(0)

        self.picture_widget_spacer = QLabel()
        self.picture_widget_spacer.setFixedSize(self.width, self.height * 0.2)
        self.picture_widget_spacerLayout = QVBoxLayout(self.picture_widget_spacer)
        self.picture_widget_spacerLayout.addWidget(self.maxWidget)
        self.picture_widget_spacerLayout.addWidget(self.minWidget)
        self.picture_widget_spacerLayout.addWidget(self.lipidWidget)
        self.picture_widget_spacerLayout.addWidget(self.infectionWidget)
        self.picture_widget_spacerLayout.addWidget(self.characterWidget)
        self.picture_widget_spacerLayout.setContentsMargins(0, 10, 0, 0)
        self.picture_widget_spacerLayout.setSpacing(5)

        self.surgeryInformationArea = QLineEdit()
        self.surgeryInformationArea.setEnabled(False)
        self.surgeryInformationArea.setStyleSheet("border: 1px solid rgb(238, 156, 54); border-width:0px 1px 1px 0px;")
        self.surgeryInformationArea.setFixedSize(self.width, self.height * 0.51)
        self.surgeryInformationArea.setFont(self.globalFont)
        self.surgeryInformationAreaLayout = QVBoxLayout(self.surgeryInformationArea)
        self.surgeryInformationAreaLayout.addWidget(self.surgeryPictureWidget)  # 0.13
        self.surgeryInformationAreaLayout.addWidget(self.patientNameWidget)     # 0.04
        self.surgeryInformationAreaLayout.addWidget(self.surgeryDateWidget)     # 0.04
        self.surgeryInformationAreaLayout.addWidget(self.surgeryIdWidget)       # 0.04
        self.surgeryInformationAreaLayout.addWidget(self.maxWidget)
        self.surgeryInformationAreaLayout.addWidget(self.minWidget)
        self.surgeryInformationAreaLayout.addWidget(self.lipidWidget)
        self.surgeryInformationAreaLayout.addWidget(self.infectionWidget)
        self.surgeryInformationAreaLayout.addWidget(self.characterWidget)
        self.surgeryInformationAreaLayout.setContentsMargins(0, 1, 0, 0)
        self.surgeryInformationAreaLayout.setSpacing(1)

        # ------------------------------------------------------
        # image sequence database
        # ------------------------------------------------------
        self.sessionChooseList = SessionChooseList(self, self.ihm_factor, self.controller, self.width, self.height * 0.48, self.globalBackgroundColor, self.globalFontColor, self.globalFont)

        # ------------------------------------------------------
        # assemble two part gui
        # ------------------------------------------------------
        self.mainInformationArea = QWidget()
        self.mainInformationArea.setFixedSize(self.width, self.height)
        self.parameterViewLayout = QVBoxLayout(self.mainInformationArea)
        self.parameterViewLayout.addWidget(self.surgeryInformationArea)  # 0.3
        self.parameterViewLayout.addWidget(self.sessionChooseList)       # 0.46
        self.parameterViewLayout.setContentsMargins(0, 0, 0, 0)
        self.parameterViewLayout.setSpacing(0)

        spacer_item = QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Expanding)

        self.pointtopointButton = QPushButton()
        self.pointtopointButton.setIcon(QIcon(":/point2.png"))
        self.pointtopointButton.setFixedSize(30*self.ihm_factor, 30*self.ihm_factor)
        self.pointtopointButton.setIconSize(QSize(18*self.ihm_factor, 18*self.ihm_factor))
        self.pointtopointButton.setFlat(True)

        self.vascularButton = QPushButton()
        self.vascularButton.setFixedSize(30*self.ihm_factor, 30*self.ihm_factor)
        self.vascularButton.setIcon(QIcon(":/vasular.png"))
        self.vascularButton.setIconSize(QSize(28*self.ihm_factor, 28*self.ihm_factor))
        self.vascularButton.setFlat(True)

        self.splineButton = QPushButton()
        self.splineButton.setFixedSize(30*self.ihm_factor, 30*self.ihm_factor)
        self.splineButton.setIcon(QIcon(":/spline.png"))
        self.splineButton.setIconSize(QSize(20*self.ihm_factor, 20*self.ihm_factor))
        self.splineButton.setFlat(True)

        self.gvfButton = QPushButton()
        self.gvfButton.setIcon(QIcon(":/gvf.png"))
        self.gvfButton.setFixedSize(30*self.ihm_factor, 30*self.ihm_factor)
        self.gvfButton.setIconSize(QSize(20*self.ihm_factor, 20*self.ihm_factor))
        self.gvfButton.setFlat(True)

        self.blankLabel = QLabel()
        self.blankLabel.setFixedSize(30, 385*self.ihm_factor)

        self.paraSetButton = QPushButton()
        self.paraSetButton.setIcon(QIcon(":/gvf1.png"))
        self.paraSetButton.setFixedSize(30*self.ihm_factor, 30*self.ihm_factor)
        self.paraSetButton.setIconSize(QSize(20*self.ihm_factor, 20*self.ihm_factor))
        self.paraSetButton.setFlat(True)

        self.verticalBarControl = QWidget()
        self.verticalBarControl.setStyleSheet("background-color:" + self.globalBackgroundColor)
        self.verticalBarControl.setFixedSize(self.barWidth, self.height)
        self.verticalBarControl_layout = QVBoxLayout(self.verticalBarControl)
        self.verticalBarControl_layout.addWidget(self.vascularButton)
        self.verticalBarControl_layout.addWidget(self.pointtopointButton)
        self.verticalBarControl_layout.addWidget(self.splineButton)
        self.verticalBarControl_layout.addWidget(self.gvfButton)
        self.verticalBarControl_layout.addWidget(self.blankLabel)
        self.verticalBarControl_layout.addWidget(self.paraSetButton)
        self.verticalBarControl_layout.addItem(spacer_item)
        self.verticalBarControl_layout.setSpacing(5)
        self.verticalBarControl_layout.setContentsMargins(0, 0, 0, 0)

        self.mainLayout = QHBoxLayout(self)
        self.mainLayout.addWidget(self.mainInformationArea)
        self.mainLayout.addWidget(self.verticalBarControl)
        self.mainLayout.setSpacing(0)
        self.mainLayout.setContentsMargins(0, 0, 0, 0)

        self.leftTracerEnable1 = False
        self.leftShowGrayEnable = False
        self.leftScreenShotEnable = False
        self.leftTracerPointsEnable = False
        self.leftTracerBoxEnable = False
        self.leftMeasureDistanceEnable = False
        self.leftImgRotationEnable = False
        self.leftGenerateCurveEnable = False

        self.set_connections()

    def set_connections(self):
        self.paraSetButton.clicked.connect(self.parameter_setting_display)
        self.splineButton.clicked.connect(self.spline_button_clicked)
        self.pointtopointButton.clicked.connect(self.point_to_point_button_clicked)
        self.gvfButton.clicked.connect(self.gvf_button_clicked)
        self.vascularButton.clicked.connect(self.vessel_segmentation_configuration_window_display)

        ObjectEvent(self.vascularButton).MouseClicked.connect(self.do_vessel_enhancement)

        # self.connect(ObjectEvent(self.vascularButton), SIGNAL("DoubleClicked"), self.vessel_segmentation_configuration_window_display)
        ObjectEvent(self.pointtopointButton).MouseHovered.connect(self.pointtopointButton_tooltip)
        ObjectEvent(self.vascularButton).MouseHovered.connect(self.vascularButton_tooltip)
        ObjectEvent(self.splineButton).MouseHovered.connect(self.splineButton_tooltip)
        ObjectEvent(self.gvfButton).MouseHovered.connect(self.gvfButton_tooltip)
        ObjectEvent(self.paraSetButton).MouseHovered.connect(self.parasetButton_tooltip)

    def do_vessel_enhancement(self):
        self.doVesselEnhancement.emit()

    def vessel_segmentation_configuration_window_display(self):
        self.vascularButtonClicked = not self.vascularButtonClicked
        # if self.vascularButtonClicked:
        #     self.vascularButton.setIcon(QIcon(":/vasular1.png"))
        # else:
        #     self.vascularButton.setIcon(QIcon(":/vasular.png"))
        self.vesselSegmentationWindow.emit()

    def gvf_button_clicked(self):
        self.gvfButtonClicked = not self.gvfButtonClicked
        if self.gvfButtonClicked:
            self.gvfButton.setIcon(QIcon(":/gvf3.png"))
        else:
            self.gvfButton.setIcon(QIcon(":/gvf.png"))

    def point_to_point_button_clicked(self):
        self.pointtopointButtonClicked = not self.pointtopointButtonClicked
        if self.pointtopointButtonClicked:
            self.pointtopointButton.setIcon(QIcon(":/point3.png"))
        else:
            self.pointtopointButton.setIcon(QIcon(":/point2.png"))

    def spline_button_clicked(self):
        self.splineButtonClicked = not self.splineButtonClicked
        if self.splineButtonClicked:
            self.splineButton.setIcon(QIcon(":/spline1.png"))
        else:
            self.splineButton.setIcon(QIcon(":/spline.png"))

    def parasetButton_tooltip(self):
        self.buttonMessage.emit("parasetButton_tooltip")

    def gvfButton_tooltip(self):
        self.buttonMessage.emit("gvfButton_tooltip")

    def splineButton_tooltip(self):
        self.buttonMessage.emit("splineButton_tooltip")

    def vascularButton_tooltip(self):
        self.buttonMessage.emit("vascular_tooltip_segementation")

    def pointtopointButton_tooltip(self):
        self.buttonMessage.emit("point_to_point_tooltip")

    def update_x_ray_sequences(self):
        self.sessionChooseList.update_x_ray_sequences()

    def choose_start_point_by_index(self, index):
        self.parent.define_start_point(index)

    def parameter_setting_display(self):
        self.paraSetButtonClicked = not self.paraSetButtonClicked
        # if self.paraSetButtonClicked:
        #     self.paraSetButton.setIcon(QIcon(":/gvf4.png"))
        # else:
        #     self.paraSetButton.setIcon(QIcon(":/gvf1.png"))
        self.parameterWindowSetting.emit()

    def update_background_color(self, color_string):
        color = QColor(color_string)
        self.mainInformationArea.setStyleSheet("background-color: " + color_string)
        self.verticalBarControl.setStyleSheet("background-color: " + color_string)
        self.sessionChooseList.update_background_color(color_string)

    def enable_vascular_button_clicked(self, click_flag):
        self.vascularButton.setEnabled(click_flag)

    def enable_paraset_button_clicked(self, click_flag):
        self.paraSetButton.setEnabled(click_flag)

    def vascular_button_icon_change(self):
        self.enable_vascular_button_clicked(True)
        self.vascularButton.setIcon(QIcon(":/vasular.png"))
        self.vascularButtonClicked = False

    def paraset_button_icon_change(self):
        self.enable_paraset_button_clicked(True)
        self.paraSetButton.setIcon(QIcon(":/gvf1.png"))
        self.paraSetButtonClicked = False