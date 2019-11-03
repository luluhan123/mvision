from PyQt5.QtWidgets import QLabel, QPushButton, QCheckBox, QHBoxLayout, QVBoxLayout, QFileDialog, QFrame
from PyQt5.QtGui import QPixmap, QIcon, QFont, QPalette, QBrush
from PyQt5.QtCore import pyqtSignal, QSize, Qt

from src.MSAView.MSAMainWindow.MSAToolBar.MSALogoLabel import LittleSIATLabel
from src.MSAView.MSAMainWindow.IHMTool.ObjectEvent import ObjectEvent
import os
import sys


class MSAToolBar(QLabel):

    enableGuidewireTrackingAlgorithm = pyqtSignal()
    enableEvaluationAlgorithm = pyqtSignal()
    messageCacheFetched = pyqtSignal()
    buttonMessage = pyqtSignal(str)
    systemStatusChanged = pyqtSignal(bool)
    networkConfigurationDisplay = pyqtSignal()
    addPatientWindowDisplay = pyqtSignal()
    startWindowDisplay = pyqtSignal()
    volumeRenderWindowDisplay = pyqtSignal()
    openWindowDisplay = pyqtSignal()
    themeWindowSetting = pyqtSignal()

    def __init__(self, parent, controller=None, ihm_factor=1, width=0, height=0, background_color="", global_font_color="", global_font=None):
        super(MSAToolBar, self).__init__()

        path = os.path.dirname(os.path.realpath(__file__))
        temp = path.split("src")

        # ------------------------------------------------------------------------------------------
        # Attributes initialization
        # ------------------------------------------------------------------------------------------
        self.controller = controller
        self.ihm_factor = ihm_factor
        self.parent = parent
        self.width = width
        self.height = height
        self.globalBackgroundColor = background_color
        self.globalFontColor = global_font_color
        self.globalFont = global_font

        self.workSpaceButtonClicked = False
        self.addPatientButtonClicked = False
        self.globalConfigurationButtonClicked = False
        self.TriDimensionalVolumeAnalyseButtonClicked = False
        self.communicationWindowClicked = False

        self.analyserMediator = None
        self.mousePointerMove = None
        self.mousePosition = None
        self.mouseLeftButtonPressed = False
        self.m_bMaxWin = False
        self.toolbarPickedUp = False
        self.intraOperative = False
        # self.leftPressButtonClicked = False
        self.m_rectRestoreWindow = self.parent.geometry()
        self.flag = False

        self.input_message_cache = None
        self.output_message_cache = None

        # ------------------------------------------------------------------------------------------
        # configure the appearance and the setting of the title bar
        # ------------------------------------------------------------------------------------------
        self.setFixedSize(self.width, self.height)
        self.setMouseTracking(True)
        self.setStyleSheet("background-color:" + self.globalBackgroundColor)

        # if sys.platform == 'win32':
        #     if self.ihm_factor == 1:
        #         self.setPixmap(QPixmap(temp[0] + "img\\title-bar.png"))
        #     elif self.ihm_factor == 2:
        #         self.setPixmap(QPixmap(temp[0] + "img\\title-bar-2560.png"))
        # else:
        #     if self.ihm_factor == 1:
        #         self.setPixmap(QPixmap(temp[0] + "img/title-bar.png"))
        #     elif self.ihm_factor == 2:
        #         self.setPixmap(QPixmap(temp[0] + "img/title-bar-2560.png"))

        # ------------------------------------------------------------------------------------------
        # components of the title bar
        # ------------------------------------------------------------------------------------------
        self.spacer = QLabel("MicroQ")
        self.spacer.setStyleSheet("background-color: transparent; color:rgb(210, 62, 90);")
        self.spacer.setAlignment(Qt.AlignLeft)
        self.spacer.setFont(QFont("Helvetica", 16, QFont.DemiBold, True))
        self.spacer.setFixedSize(220 * self.ihm_factor, self.height*0.95)

        self.loadSequenceButton = QPushButton()
        self.loadSequenceButton.setStyleSheet("background-color: transparent;")
        self.loadSequenceButton.setIcon(QIcon(":/1file.png"))
        self.loadSequenceButton.setMouseTracking(True)
        self.loadSequenceButton.setFixedSize(QSize(self.height * 0.9, self.height * 0.9))
        self.loadSequenceButton.setIconSize(QSize(self.height * 0.6, self.height * 0.6))
        self.loadSequenceButton.setFlat(True)

        self.TriDimensionalVolumeAnalyseButton = QPushButton()
        self.TriDimensionalVolumeAnalyseButton.setStyleSheet("background: transparent;")
        self.TriDimensionalVolumeAnalyseButton.setIcon(QIcon(":/3Dvision.png"))
        self.TriDimensionalVolumeAnalyseButton.setMouseTracking(True)
        self.TriDimensionalVolumeAnalyseButton.setFixedSize(QSize(self.height * 0.9, self.height * 0.9))
        self.TriDimensionalVolumeAnalyseButton.setIconSize(QSize(self.height * 0.6, self.height * 0.6))
        self.TriDimensionalVolumeAnalyseButton.setFlat(True)
        self.TriDimensionalVolumeAnalyseButton.setToolTip("3D display")

        self.globalConfigurationButton = QPushButton()
        self.globalConfigurationButton.setStyleSheet("background: transparent;")
        self.globalConfigurationButton.setToolTip('click here to open a session of x-ray image sequence')
        self.globalConfigurationButton.setIcon(QIcon(":/sysSetting1.png"))
        self.globalConfigurationButton.setMouseTracking(True)
        self.globalConfigurationButton.setFixedSize(QSize(self.height * 0.9, self.height * 0.9))
        self.globalConfigurationButton.setIconSize(QSize(self.height * 0.6, self.height * 0.6))
        self.globalConfigurationButton.setFlat(True)
        self.globalConfigurationButton.setToolTip("system Setting")

        self.workSpaceButton = QPushButton()
        self.workSpaceButton.setStyleSheet("background: transparent;")
        self.workSpaceButton.setToolTip('click here to open  the startWindow')
        self.workSpaceButton.setIcon(QIcon(":/frontPage.png"))
        self.workSpaceButton.setMouseTracking(True)
        self.workSpaceButton.setFixedSize(QSize(self.height * 0.9, self.height * 0.9))
        self.workSpaceButton.setIconSize(QSize(self.height * 0.6, self.height * 0.6))
        self.workSpaceButton.setFlat(True)
        self.workSpaceButton.setToolTip("open workSpaceWindow")

        self.addPatientButton = QPushButton()
        self.addPatientButton.setStyleSheet("background: transparent;")
        self.addPatientButton.setToolTip('click here to edit the patient information')
        self.addPatientButton.setIcon(QIcon(":/addPatient.png"))
        self.addPatientButton.setMouseTracking(True)
        self.addPatientButton.setFixedSize(QSize(self.height * 0.9, self.height * 0.9))
        self.addPatientButton.setIconSize(QSize(self.height * 0.6, self.height * 0.6))
        self.addPatientButton.setFlat(True)
        self.addPatientButton.setToolTip("Add Patient Info")

        self.spacerr = QLabel()
        self.spacerr.setFixedWidth(512*self.ihm_factor - self.height * 3.6 - self.width*0.16)

        self.currentSequenceInformationLabel = QLabel()
        self.currentSequenceInformationLabel.setFixedSize(self.width * 0.06, self.height*0.8)
        self.currentSequenceInformationLabel.setStyleSheet("background-color:transparent; color:" + self.globalFontColor + "; alignment:center;")
        self.currentSequenceInformationLabel.setFont(self.globalFont)

        self.trackingOptionCheckBox = QCheckBox('Tracking')
        self.trackingOptionCheckBox.setStyleSheet("background-color:transparent; color:" + self.globalFontColor + "; alignment:center; border: 1px solid cyan;")
        self.trackingOptionCheckBox.setFont(self.globalFont)
        self.trackingOptionCheckBox.setFixedSize(self.width*0.06, self.height*0.7)

        self.evaluateOptionCheckBox = QCheckBox('Evaluation')
        self.evaluateOptionCheckBox.setStyleSheet("background-color:transparent; color:" + self.globalFontColor + "; alignment:center; border: 1px solid cyan;")
        self.evaluateOptionCheckBox.setFont(self.globalFont)
        self.evaluateOptionCheckBox.setFixedSize(self.width * 0.07, self.height * 0.7)

        self.spacerrr = QLabel()
        self.spacerrr.setFixedWidth(512*self.ihm_factor - self.width*0.38)

        self.communicationWindow = QPushButton()
        self.communicationWindow.setStyleSheet("background: " + self.globalBackgroundColor)
        self.communicationWindow.setToolTip('click here to open the communication Window')
        self.communicationWindow.setIcon(QIcon(":/communicationWindow1.png"))
        self.communicationWindow.setMouseTracking(True)
        self.communicationWindow.setFixedSize(QSize(self.height * 0.9, self.height * 0.9))
        self.communicationWindow.setIconSize(QSize(self.height * 0.8, self.height * 0.6))
        self.communicationWindow.setFlat(True)
        self.communicationWindow.setToolTip("CommunicationWindow1")

        self.stateChooseButton = QCheckBox('intra-operation')
        self.stateChooseButton.setStyleSheet("QCheckBox{background-color:transparent; color:" + self.globalFontColor + "; alignment:center;}"
                                             "QCheckBox::indicator {width: "+str(15*self.ihm_factor)+"px;height: "+str(15*self.ihm_factor)+"px;}"
                                             "QCheckBox::indicator:checked {image: url(:/intra_operation.png);}"
                                             "QCheckBox::indicator:unchecked {image: url(:/not_in_operation.png);}")
        self.stateChooseButton.setFont(self.globalFont)
        self.stateChooseButton.setFixedSize(self.width*0.08, self.height*0.9)

        self.orgLabel = LittleSIATLabel(self, self.width*0.065, self.height*0.7)

        self.main_window = QFrame()
        self.main_window.setFixedSize(self.width, self.height*0.95)
        self.myLayout = QHBoxLayout(self.main_window)
        self.myLayout.addWidget(self.spacer)
        self.myLayout.addWidget(self.loadSequenceButton)
        self.myLayout.addWidget(self.addPatientButton)
        self.myLayout.addWidget(self.workSpaceButton)
        self.myLayout.addWidget(self.globalConfigurationButton)
        self.myLayout.addWidget(self.TriDimensionalVolumeAnalyseButton)
        self.myLayout.addWidget(self.spacerr)
        self.myLayout.addWidget(self.currentSequenceInformationLabel)
        self.myLayout.addWidget(self.trackingOptionCheckBox)
        self.myLayout.addWidget(self.evaluateOptionCheckBox)
        self.myLayout.addWidget(self.spacerrr)
        self.myLayout.addWidget(self.communicationWindow)
        self.myLayout.addWidget(self.stateChooseButton)
        self.myLayout.addWidget(self.orgLabel)
        self.myLayout.setSpacing(0)
        self.myLayout.setContentsMargins(0, 0, 0, 0)

        self.leftUnderBar = QLabel()
        self.leftUnderBar.setFixedSize(213, self.height*0.05)

        self.underBar = QLabel()
        self.underBar.setFixedSize(self.width-213, self.height*0.05)
        self.underBar.setStyleSheet("background-color:rgb(120, 240, 224);")

        self.totalUnderBar = QLabel()
        self.totalUnderBar.setFixedSize(self.width, self.height * 0.05)
        self.totalUnderBarLayout = QHBoxLayout(self.totalUnderBar)
        self.totalUnderBarLayout.addWidget(self.leftUnderBar)
        self.totalUnderBarLayout.addWidget(self.underBar)
        self.totalUnderBarLayout.setSpacing(0)
        self.totalUnderBarLayout.setContentsMargins(0, 0, 0, 0)

        self.monLayout = QVBoxLayout(self)
        self.monLayout.addWidget(self.main_window)
        self.monLayout.addWidget(self.totalUnderBar)
        self.monLayout.setSpacing(0)
        self.monLayout.setContentsMargins(0, 0, 0, 0)

        self.set_connections()

    def set_connections(self):
        self.loadSequenceButton.clicked.connect(self.choose_file)
        self.TriDimensionalVolumeAnalyseButton.clicked.connect(self.volume_rendering_window_display)
        self.stateChooseButton.stateChanged.connect(self.change_state)
        self.trackingOptionCheckBox.stateChanged.connect(self.enable_guidewire_tracking)
        self.evaluateOptionCheckBox.stateChanged.connect(self.enable_evaluation)
        self.globalConfigurationButton.clicked.connect(self.open_window_setting)
        self.workSpaceButton.clicked.connect(self.start_window_display)
        self.addPatientButton.clicked.connect(self.add_patient_window_display)
        self.communicationWindow.clicked.connect(self.communication_window_display)

        ObjectEvent(self.loadSequenceButton).MouseHovered.connect(self.load_sequence_tooltip)
        ObjectEvent(self.TriDimensionalVolumeAnalyseButton).MouseHovered.connect(self.volume_analyse_tooltip)
        ObjectEvent(self.stateChooseButton).MouseHovered.connect(self.state_choose_tooltip)
        ObjectEvent(self.globalConfigurationButton).MouseHovered.connect(self.configuration_tooltip)
        ObjectEvent(self.addPatientButton).MouseHovered.connect(self.add_patient_tooltip)
        ObjectEvent(self.workSpaceButton).MouseHovered.connect(self.workspace_button_tooltip)
        ObjectEvent(self.communicationWindow).MouseHovered.connect(self.communication_window_tooltip)

    def set_current_sequence_information(self, current_sequence_info):
        self.currentSequenceInformationLabel.setText(current_sequence_info)

    def fetch_output_message(self):
        return self.output_message_cache

    def fetch_input_message(self):
        return self.input_message_cache

    def change_state(self):
        self.intraOperative = not self.intraOperative

        if self.intraOperative:
            self.input_message_cache = self.controller.generate_input_cache()
            self.output_message_cache = self.controller.generate_output_cache()
            self.messageCacheFetched.emit()
            self.controller.launch_communication_stack()
        else:
            self.controller.terminate_communication_stack()

        self.systemStatusChanged.emit(self.intraOperative)

    def add_patient_tooltip(self):
        self.buttonMessage.emit("Add patient Info")

    def workspace_button_tooltip(self):
        self.buttonMessage.emit("select workPath")

    def communication_window_tooltip(self):
        self.buttonMessage.emit("communication Window")

    def communication_window_display(self):
        self.communicationWindowClicked = not self.communicationWindowClicked
        # if self.communicationWindowClicked:
        #     self.communicationWindow.setIcon(QIcon(":/communicationWindow.png"))
        # else:
        #     self.communicationWindow.setIcon(QIcon(":/communicationWindow1.png"))
        self.networkConfigurationDisplay.emit()

    def add_patient_window_display(self):
        self.addPatientButtonClicked = not self.addPatientButtonClicked
        # if self.addPatientButtonClicked:
        #     self.addPatientButton.setIcon(QIcon(":/addPatient1.png"))
        # else:
        #     self.addPatientButton.setIcon(QIcon(":/addPatient.png"))
        self.addPatientWindowDisplay.emit()

    def start_window_display(self):
        self.workSpaceButtonClicked = not self.workSpaceButtonClicked
        # if self.workSpaceButtonClicked:
        #     self.workSpaceButton.setIcon(QIcon(":/frontPage1.png"))
        # else:
        #     self.workSpaceButton.setIcon(QIcon(":/frontPage.png"))
        self.startWindowDisplay.emit()

    def load_sequence_tooltip(self):
        self.buttonMessage.emit("load patient sequence")

    def volume_analyse_tooltip(self):
        self.buttonMessage.emit("3D display")

    def state_choose_tooltip(self):
        self.buttonMessage.emit("state_choose")

    def configuration_tooltip(self):
        self.buttonMessage.emit("configuration")

    def enable_guidewire_tracking(self):
        self.enableGuidewireTrackingAlgorithm.emit()

    def enable_evaluation(self):
        self.enableEvaluationAlgorithm.emit()

    def choose_file(self):
        file_path = QFileDialog.getOpenFileName(self.parent, 'MedSight file choosing', './')

        target_file = file_path[0]

        if target_file.__contains__(".mha"):
            self.controller.do_read_volume_image_by_path(target_file)

    def volume_rendering_window_display(self):
        self.volumeRenderWindowDisplay.emit()

    def open_window_setting(self):
        self.globalConfigurationButtonClicked = not self.globalConfigurationButtonClicked
        # if self.globalConfigurationButtonClicked:
        #     self.globalConfigurationButton.setIcon(QIcon(":/sysSetting2.png"))
        # else:
        #     self.globalConfigurationButton.setIcon(QIcon(":/sysSetting1.png"))
        self.openWindowDisplay.emit()

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
            self.parent.move(self.parent.pos() + self.mousePointerMove - self.mousePosition)
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

    def draw_background(self):
        """
            - configure the background and the size of the graphical tool
        """

        pixmap = QPixmap(":/title-bar.png")
        palette = self.palette()
        palette.setBrush(QPalette.Background, QBrush(pixmap.scaled(QSize(self.width, self.height), Qt.IgnoreAspectRatio, Qt.SmoothTransformation)))
        self.setPalette(palette)

        # self.setMask(pixmap.mask())
        # self.setAutoFillBackground(True)

    def theme_setting_apply(self):
        self.themeWindowSetting.emit()

    def update_background_color(self, color_string):
        self.main_window.setStyleSheet("background-color: " + color_string)

    def system_button_icon_change(self):
        self.enable_parameter_setting_button(True)
        self.globalConfigurationButton.setIcon(QIcon(":/sysSetting1.png"))
        self.globalConfigurationButtonClicked = False

    def add_patient_icon_change(self):
        self.enable_addPatient_button_clicked(True)
        self.addPatientButton.setIcon(QIcon(":/addPatient.png"))
        self.addPatientButtonClicked = False

    def enable_parameter_setting_button(self, click_flag):
        self.globalConfigurationButton.setEnabled(click_flag)

    def enable_workSpace_button_clicked(self, click_flag):
        self.workSpaceButton.setEnabled(click_flag)

    def enable_addPatient_button_clicked(self, click_flag):
        self.addPatientButton.setEnabled(click_flag)

    def enable_communication_window_clicked(self, click_flag):
        self.communicationWindow.setEnabled(click_flag)

    def communication_window_icon_change(self):
        self.enable_communication_window_clicked(True)
        self.communicationWindow.setIcon(QIcon(":/communicationWindow1.png"))
        self.communicationWindowClicked = False

    def work_space_icon_change(self):
        self.enable_workSpace_button_clicked(True)
        self.workSpaceButton.setIcon(QIcon(":/frontPage.png"))
        self.workSpaceButtonClicked = False