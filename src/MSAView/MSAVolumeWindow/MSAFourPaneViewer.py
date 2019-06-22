#!/usr/bin/env python3
from PyQt5.QtGui import QIcon, QColor
from PyQt5.QtWidgets import QWidget, QApplication, QHBoxLayout, QVBoxLayout, QPushButton, QLabel
from PyQt5.QtCore import pyqtSignal, QSize, Qt, QFileInfo
from MSAView.MSAMainWindow.IHMTool.MSAPlottingBoard import MSAPlottingBoard
from MSAView.MSAVolumeWindow.MSACanvas3D import MSACanvas3D
from MSAView.MSAMainWindow.IHMTool.MSAVolumeRenderingConfigurationWindow import MSAVolumeRenderingConfigurationWindow


class FourPanelViewer(QWidget):

    closeSignal = pyqtSignal()

    def __init__(self, controller=None, ihm_factor=1, x=0, y=0, width=0, height=0, background_color="", global_font_color="", global_font=None):
        super(FourPanelViewer, self).__init__()

        self.controller = controller
        self.ihm_factor = ihm_factor
        self.appX = x
        self.appY = y
        self.appWidth = width
        self.appHeight = height
        self.globalBackgroundColor = background_color
        self.globalFontColor = global_font_color
        self.globalFont = global_font

        v = self.globalBackgroundColor.split('(')[1].split(')')[0].split(',')

        self.setGeometry(self.appX, self.appY, self.appWidth, self.appHeight)
        self.draw_background()

        self.metadata = {}

        self.buttonVesselClicked = False
        self.buttonIntegumentaryClicked = False
        self.buttonRespiratoryClicked = False
        self.buttonEndocrineClicked = False
        self.buttonDigestiveClicked = False
        self.buttonSkeletonClicked = False
        self.buttonBrainClicked = False
        self.buttonHeartClicked = False
        self.buttonCenterLineClicked = False
        self.buttonNervousClicked = False
        self.renderSettingButtonClicked = False
        self.rsw = None

        # ----------------------------------------------------------
        # configure the appearance of the graphical interface
        # ----------------------------------------------------------
        self.setWindowFlags(Qt.FramelessWindowHint)# | Qt.WindowStaysOnTopHint)
        self.setWindowOpacity(1.0)
        self.setMouseTracking(True)
        self.setAutoFillBackground(True)

        # ----------------------------------------------------------
        # construct graphical interface
        # ----------------------------------------------------------
        self.canvas3d = MSACanvas3D(self, self.controller, self.ihm_factor, self.appWidth * 0.96, self.appHeight, self.globalBackgroundColor, self.globalFontColor, self.globalFont)
        self.plottingBoard = MSAPlottingBoard(3, self.controller,self.ihm_factor, self.appWidth* 0.96, self.appHeight * 0.3)
        self.plottingBoard.set_background_color_string(background_color)

        self.centralWidget = QWidget()
        self.centralWidget.setFixedSize(self.appWidth * 0.96, self.appHeight)
        self.centralWidgetLayout = QVBoxLayout(self.centralWidget)
        self.centralWidgetLayout.addWidget(self.canvas3d)
        self.centralWidgetLayout.addWidget(self.plottingBoard)
        self.centralWidgetLayout.setContentsMargins(0, 0, 0, 0)
        self.centralWidgetLayout.setSpacing(0)

        self.buttonCenterLine = QPushButton()
        self.buttonCenterLine.setIcon(QIcon(":/2per2.png"))
        self.buttonCenterLine.setFixedSize(self.appWidth * 0.03, self.appHeight * 0.03)
        self.buttonCenterLine.setIconSize(QSize(self.appWidth * 0.025, self.appHeight * 0.025))
        self.buttonCenterLine.setFlat(True)

        self.buttonVessel = QPushButton()
        self.buttonVessel.setFixedSize(self.appWidth * 0.03, self.appHeight * 0.03)
        self.buttonVessel.setIcon(QIcon(":/1per1.png"))
        self.buttonVessel.setIconSize(QSize(self.appWidth * 0.025, self.appHeight * 0.025))
        self.buttonVessel.setFlat(True)

        self.buttonHeart = QPushButton()
        self.buttonHeart.setFixedSize(self.appWidth * 0.03, self.appHeight * 0.03)
        self.buttonHeart.setFlat(True)
        self.buttonHeart.setIcon(QIcon(":/3per3.png"))
        self.buttonHeart.setIconSize(QSize(self.appWidth * 0.025, self.appHeight * 0.025))

        self.buttonBrain = QPushButton()
        self.buttonBrain.setFixedSize(self.appWidth * 0.03, self.appHeight * 0.03)
        self.buttonBrain.setFlat(True)
        self.buttonBrain.setIcon(QIcon(":/4per4.png"))
        self.buttonBrain.setIconSize(QSize(self.appWidth * 0.025, self.appHeight * 0.025))

        self.buttonSkeleton = QPushButton()
        self.buttonSkeleton.setFixedSize(self.appWidth * 0.03, self.appHeight * 0.03)
        self.buttonSkeleton.setFlat(True)
        self.buttonSkeleton.setIcon(QIcon(":/5per5.png"))
        self.buttonSkeleton.setIconSize(QSize(self.appWidth * 0.025, self.appHeight * 0.025))

        self.buttonDigestive = QPushButton()
        self.buttonDigestive.setFixedSize(self.appWidth * 0.03, self.appHeight * 0.03)
        self.buttonDigestive.setFlat(True)
        self.buttonDigestive.setIcon(QIcon(":/6per6.png"))
        self.buttonDigestive.setIconSize(QSize(self.appWidth * 0.025, self.appHeight * 0.025))

        self.buttonEndocrine = QPushButton()
        self.buttonEndocrine.setFixedSize(self.appWidth * 0.03, self.appHeight * 0.03)
        self.buttonEndocrine.setFlat(True)
        self.buttonEndocrine.setIcon(QIcon(":/7per7.png"))
        self.buttonEndocrine.setIconSize(QSize(self.appWidth * 0.025, self.appHeight * 0.025))

        self.buttonRespiratory = QPushButton()
        self.buttonRespiratory.setFixedSize(self.appWidth * 0.03, self.appHeight * 0.03)
        self.buttonRespiratory.setFlat(True)
        self.buttonRespiratory.setIcon(QIcon(":/8per8.png"))
        self.buttonRespiratory.setIconSize(QSize(self.appWidth * 0.025, self.appHeight * 0.025))

        self.buttonIntegumentary = QPushButton()
        self.buttonIntegumentary.setFixedSize(self.appWidth * 0.03, self.appHeight * 0.03)
        self.buttonIntegumentary.setFlat(True)
        self.buttonIntegumentary.setIcon(QIcon(":/9per9.png"))
        self.buttonIntegumentary.setIconSize(QSize(self.appWidth * 0.025, self.appHeight * 0.025))

        self.buttonNervous = QPushButton()
        self.buttonNervous.setFixedSize(self.appWidth * 0.03, self.appHeight * 0.03)
        self.buttonNervous.setFlat(True)
        self.buttonNervous.setIcon(QIcon(":/10per10.png"))
        self.buttonNervous.setIconSize(QSize(self.appWidth * 0.025, self.appHeight * 0.025))

        self.spacer = QLabel()
        self.spacer.setFixedSize(self.appWidth*0.3, self.appHeight*0.6)

        self.renderSettingButton = QPushButton()
        self.renderSettingButton.setFixedSize(self.appWidth * 0.03, self.appHeight * 0.03)
        self.renderSettingButton.setFlat(True)
        self.renderSettingButton.setIcon(QIcon(":/persetting.png"))
        self.renderSettingButton.setIconSize(QSize(self.appWidth * 0.025, self.appHeight * 0.025))

        self.renderingButton = QPushButton(self)
        self.renderingButton.setFixedSize(self.appWidth * 0.03, self.appHeight * 0.03)
        self.renderingButton.setIconSize(QSize(self.appWidth * 0.025, self.appHeight * 0.025))
        self.renderingButton.setIcon(QIcon(":/11per11.png"))
        self.renderingButton.setFlat(True)

        self.manipulationBar = QLabel()
        self.manipulationBar.setStyleSheet("background-color: " + self.globalBackgroundColor)
        self.manipulationBar.setFixedSize(self.appWidth*0.03, self.appHeight)
        self.manipulationBarLayout = QVBoxLayout(self.manipulationBar)
        self.manipulationBarLayout.addWidget(self.buttonVessel)
        self.manipulationBarLayout.addWidget(self.buttonCenterLine)
        self.manipulationBarLayout.addWidget(self.buttonHeart)
        self.manipulationBarLayout.addWidget(self.buttonBrain)
        self.manipulationBarLayout.addWidget(self.buttonSkeleton)
        self.manipulationBarLayout.addWidget(self.buttonDigestive)
        self.manipulationBarLayout.addWidget(self.buttonEndocrine)
        self.manipulationBarLayout.addWidget(self.buttonRespiratory)
        self.manipulationBarLayout.addWidget(self.buttonIntegumentary)
        self.manipulationBarLayout.addWidget(self.buttonNervous)
        self.manipulationBarLayout.addWidget(self.renderSettingButton)
        self.manipulationBarLayout.addWidget(self.spacer)
        self.manipulationBarLayout.addWidget(self.renderingButton)
        self.manipulationBarLayout.setSpacing(20)
        self.manipulationBarLayout.setContentsMargins(0, 8, 0, 0)

        self.persiveArea = QLabel()
        self.persiveArea.setStyleSheet("background-color:"+self.globalBackgroundColor)
        self.persiveArea.setFixedSize(self.appWidth*0.01, self.appHeight*0.97)

        self.tissueControlBar = QLabel()
        self.tissueControlBar.setFixedSize(self.appWidth * 0.04, self.appHeight * 0.97)
        self.tissueControlBarLayout = QHBoxLayout(self.tissueControlBar)
        self.tissueControlBarLayout.addWidget(self.persiveArea)
        self.tissueControlBarLayout.addWidget(self.manipulationBar)
        self.tissueControlBarLayout.setSpacing(0)
        self.tissueControlBarLayout.setContentsMargins(0, 0, 0, 0)

        self.minimumButton = QPushButton(self)
        self.minimumButton.setFixedSize(self.appWidth * 0.019, self.appHeight * 0.03)
        self.minimumButton.setIconSize(QSize(self.appWidth * 0.010, self.appHeight * 0.0133))
        self.minimumButton.setIcon(QIcon(":/aa_minimize.png"))
        self.minimumButton.setFlat(True)

        self.closeButton = QPushButton(self)
        self.closeButton.setFixedSize(self.appWidth * 0.019, self.appHeight * 0.03)
        self.closeButton.setIconSize(QSize(self.appWidth * 0.005, self.appHeight * 0.01))
        self.closeButton.setIcon(QIcon(":/aa_close.png"))
        self.closeButton.setFlat(True)

        self.windowControl = QLabel()
        self.windowControl.setStyleSheet("background-color: " + self.globalBackgroundColor)
        self.windowControl.setFixedSize(self.appWidth * 0.04, self.appHeight * 0.03)
        self.windowControlLayout = QHBoxLayout(self.windowControl)
        self.windowControlLayout.addWidget(self.minimumButton)
        self.windowControlLayout.addWidget(self.closeButton)
        self.windowControlLayout.setSpacing(0)
        self.windowControlLayout.setContentsMargins(0, 0, 0, 0)

        self.rightBar = QLabel()
        self.rightBar.setFixedSize(self.appWidth * 0.04, self.appHeight)
        self.rightBarLayout = QVBoxLayout(self.rightBar)
        self.rightBarLayout.addWidget(self.tissueControlBar)
        self.rightBarLayout.addWidget(self.windowControl)
        self.rightBarLayout.setSpacing(0)
        self.rightBarLayout.setContentsMargins(0, 0, 0, 0)

        self.volumeWindowLayout = QHBoxLayout(self)
        self.volumeWindowLayout.addWidget(self.centralWidget)
        self.volumeWindowLayout.addWidget(self.rightBar)
        self.volumeWindowLayout.setSpacing(0)
        self.volumeWindowLayout.setContentsMargins(0, 0, 0, 0)

        self.renderingButtonCpt = 0

        self.closeButton.clicked.connect(self.close_system)
        self.renderingButton.clicked.connect(self.histogram_area_show)
        self.renderSettingButton.clicked.connect(self.rendering_configuration_window_display)
        self.buttonVessel.clicked.connect(self.vessel_button_clicked)
        self.buttonIntegumentary.clicked.connect(self.integumentary_button_clicked)
        self.buttonRespiratory.clicked.connect(self.respiratory_button_clicked)
        self.buttonEndocrine.clicked.connect(self.endocrine_button_clicked)
        self.buttonCenterLine.clicked.connect(self.centerline_button_clicked)
        self.buttonHeart.clicked.connect(self.heart_button_clicked)
        self.buttonBrain.clicked.connect(self.brain_button_clicked)
        self.buttonSkeleton.clicked.connect(self.skeleton_button_clicked)
        self.buttonDigestive.clicked.connect(self.digestive_button_clicked)
        self.buttonNervous.clicked.connect(self.nervous_button_clicked)

        self.histogram_area_show()

    def vessel_button_clicked(self):
        vessel_path = "/Users/lcc/Documents/dat/skin.stl"

        self.buttonVesselClicked = not self.buttonVesselClicked
        if self.buttonVesselClicked:
            self.buttonVessel.setIcon(QIcon(":/1per11.png"))

            self.canvas3d.stl_file_reader(vessel_path, 0, 0.1, 175, 238, 238, 1.0, 10)
            # self.do_display_stl_file(vessel_path)
        else:
            self.buttonVessel.setIcon(QIcon(":/1per1.png"))

    def centerline_button_clicked(self):
        self.buttonCenterLineClicked = not self.buttonCenterLineClicked

        self.canvas3d.read_centerline_by_path("C:\\Users\\cheng\\Documents\\CanalyserWorkspace\\PatientsDataware\\Zheng_Houyi__2014_07_03\\mra_tridimensionel__image\\centerlines\\centerline.txt")

        if self.buttonCenterLineClicked:
            self.buttonCenterLine.setIcon(QIcon(":/2per22.png"))
        else:
            self.buttonCenterLine.setIcon(QIcon(":/2per2.png"))

    def heart_button_clicked(self):
        self.buttonHeartClicked = not self.buttonHeartClicked
        if self.buttonHeartClicked:
            self.buttonHeart.setIcon(QIcon(":/3per33.png"))
        else:
            self.buttonHeart.setIcon(QIcon(":/3per3.png"))

    def brain_button_clicked(self):
        self.buttonBrainClicked = not self.buttonBrainClicked
        if self.buttonBrainClicked:
            self.buttonBrain.setIcon(QIcon(":/4per44.png"))
        else:
            self.buttonBrain.setIcon(QIcon(":/4per4.png"))

    def skeleton_button_clicked(self):
        self.buttonSkeletonClicked = not self.buttonSkeletonClicked
        if self.buttonSkeletonClicked:
            self.buttonSkeleton.setIcon(QIcon(":/5per55.png"))
        else:
            self.buttonSkeleton.setIcon(QIcon(":/5per5.png"))

    def digestive_button_clicked(self):
        self.buttonDigestiveClicked = not self.buttonDigestiveClicked
        if self.buttonDigestiveClicked:
            self.buttonDigestive.setIcon(QIcon(":/6per66.png"))
        else:
            self.buttonDigestive.setIcon(QIcon(":/6per6.png"))

    def endocrine_button_clicked(self):
        self.buttonEndocrineClicked = not self.buttonEndocrineClicked
        if self.buttonEndocrineClicked:
            self.buttonEndocrine.setIcon(QIcon(":/7per77.png"))
        else:
            self.buttonEndocrine.setIcon(QIcon(":/7per7.png"))

    def respiratory_button_clicked(self):
        self.buttonRespiratoryClicked = not self.buttonRespiratoryClicked
        if self.buttonRespiratoryClicked:
            self.buttonRespiratory.setIcon(QIcon(":/8per88.png"))
        else:
            self.buttonRespiratory.setIcon(QIcon(":/8per8.png"))

    def integumentary_button_clicked(self):
        self.buttonIntegumentaryClicked = not self.buttonIntegumentaryClicked
        if self.buttonIntegumentaryClicked:
            self.buttonIntegumentary.setIcon(QIcon(":/9per99.png"))
        else:
            self.buttonIntegumentary.setIcon(QIcon(":/9per9.png"))

    def nervous_button_clicked(self):
        self.buttonNervousClicked = not self.buttonNervousClicked
        if self.buttonNervousClicked:
            self.buttonNervous.setIcon(QIcon(":/10per1010.png"))
        else:
            self.buttonNervous.setIcon(QIcon(":/10per10.png"))

    def rendering_configuration_window_display(self):
        self.renderSettingButtonClicked = not self.renderSettingButtonClicked
        if self.renderSettingButtonClicked:
            self.renderSettingButton.setIcon(QIcon(":/persetting1.png"))
        else:
            self.renderSettingButton.setIcon(QIcon(":/persetting.png"))

        self.rsw = MSAVolumeRenderingConfigurationWindow()
        self.rsw.display()
        # rsw = QLabel()
        # rsw.resize(500, 500)
        # rsw.show()

    def disconnect_event(self):
        self.plottingBoard.disconnect_event()

    def histogram_area_show(self):
        if self.renderingButtonCpt % 2 == 0:
            self.plottingBoard.show()
            self.canvas3d.set_size(self.appWidth * 0.96, self.appHeight * 0.6)
            self.plottingBoard.setFixedSize(self.appWidth * 0.96, self.appHeight * 0.4)
        elif self.renderingButtonCpt % 2 == 1:
            self.plottingBoard.close()
            self.canvas3d.set_size(self.appWidth * 0.96, self.appHeight)
        self.renderingButtonCpt += 1

    def minimize_system(self):
        self.showMinimized()

    def close_system(self):
        self.close()
        #self.renderSetting.close()
        self.closeSignal.emit()

    def do_display_stl_file(self, file_path):
        self.canvas3d.do_display_stl_file(file_path)

    def do_display_meta_file(self, file_path):
        """
            display 3d volume image
        :param file_path:
        :return:
        """
        self.canvas3d.set_current_volume_path(file_path)
        self.canvas3d.launch()

    def display(self):
        """
            - display current window
        """
        self.show()

    def draw_background(self):
        """
            - configure the background and the size of the graphical tool
        """
        self.setStyleSheet("background-color: rgb(21,26,46)")
