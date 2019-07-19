#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
MainWindow of the IHM to contain all the graphic component

author: Cheng WANG

last edited: February 2015
"""

import os.path
import sys
from PyQt5.QtGui import QPixmap, QFont, QIcon
from PyQt5.QtWidgets import QWidget, QApplication, QPushButton, QHBoxLayout, QLineEdit, QProgressBar, QLabel, QVBoxLayout
from PyQt5.QtCore import pyqtSignal, Qt, QSize
from MSAView.MSAMainWindow.MSAImageWorkSpace.MSAWorkSpace import MSAWorkSpace
from MSAView.MSAMainWindow.MSAToolBar.MSAToolBar import MSAToolBar
from MSAView.MSAMainWindow.IHMTool.MSAScreen import MSAScreen
from MSAView.MSAStartWindow.MSAStartWindow import MSAStartWindow
from MSAView.MSAVolumeWindow.MSAFourPaneViewer import FourPanelViewer
from MSAView.MSAMainWindow.IHMTool.MSAVesselSegmentation import MSAVesselSegmentation
from MSAView.MSAMainWindow.IHMTool.MSAParameterSetting import MSAParameterSetting
from MSAView.MSAMainWindow.IHMTool.MSAPreferenceSettingWindow import MSAPreferenceSettingWindow
from MSAView.MSAMainWindow.IHMTool.AddPatientWindow import AddPatientWindow
from MSAView.MSAMainWindow.IHMTool.MSANetworkConfigurationWindow import MSANetworkConfigurationWindow
from MSAView.MSAMainWindow.IHMTool.ObjectEvent import ObjectEvent


class MSAMainWindow(QWidget):
    imageSequenceLoaded = pyqtSignal()
    volumeImageLoaded = pyqtSignal()
    messageCacheFetched = pyqtSignal()
    enableGuidewireTrackingAlgorithm = pyqtSignal()
    changeToTheme1 = pyqtSignal()
    change_color = pyqtSignal()
    selected_file_color_change = pyqtSignal()
    system_setting_clicked = pyqtSignal()
    parameter_button_icon_change = pyqtSignal()
    change_font_size = pyqtSignal()
    windowClosed = pyqtSignal()

    def __init__(self, controller=None):
        super(MSAMainWindow, self).__init__()

        self.controller = controller

        path = os.path.dirname(os.path.realpath(__file__))
        temp = path.split("src")

        # ----------------------------------------------------------------------------------------------------------------------
        # initialise variables  MSAVesselSegmentation
        # ----------------------------------------------------------------------------------------------------------------------
        self.screens = []
        self.appWidth = 0
        self.appHeight = 0
        self.appX = 0
        self.appY = 0
        self.ihm_factor = 1

        self.globalBackgroundColor = "rgb(67, 67, 67)"
        self.globalFontColor = "rgb(211, 211, 211)"

        if sys.platform == 'darwin':
            self.globalFont = QFont("System", 11, QFont.Light, True)
        else:
            self.globalFont = QFont("Monospace", 9, QFont.AnyStyle, True)

        self.current_sequence = None
        self.target_image_width = 512
        self.target_image_height = 512
        self.set_global_image_size(self.target_image_width, self.target_image_height)

        # ----------------------------------------------------------------------------------------------------------------------
        # positioning the Graphical tool in the middle of the screen (or secondary screen)
        # ----------------------------------------------------------------------------------------------------------------------
        self.desktop = QApplication.desktop()
        self.screen_count = self.desktop.screenCount()
        self.primary_screen_index = self.desktop.primaryScreen()

        for i in range(self.screen_count):
            screen = MSAScreen()
            screen.set_index(self.primary_screen_index + i)
            screen.set_rect(self.desktop.screenGeometry(self.primary_screen_index + i))
            self.screens.append(screen)

        if self.screen_count == 1:
            width = self.desktop.width()
            height = self.desktop.height()

            if width <= 2000:
                self.ihm_factor = 1
                self.globalBackgroundColor = "rgb(51, 51, 51)"
            else:
                self.ihm_factor = 2

            self.appWidth = self.target_image_width * 2 * self.ihm_factor + 256 * self.ihm_factor
            self.appHeight = self.target_image_height * self.ihm_factor + 256 * self.ihm_factor + 72 * self.ihm_factor
            print(self.appWidth, self.appHeight)
            self.appX = (width - self.appWidth) / 2
            self.appY = (height - self.appHeight) / 2
            self.setMinimumWidth(self.appWidth)
            self.setMinimumHeight(self.appHeight)
            self.setGeometry(self.appX, self.appY, self.appWidth, self.appHeight)

        elif self.screen_count > 1:
            width = self.screens[1].get_rect().width()
            height = self.screens[1].get_rect().height()
            x = self.screens[1].get_rect().x()
            y = self.screens[1].get_rect().y()

            if self.target_image_width < 512:
                self.appWidth = 512 * 2 + 256
                self.appHeight = 512 + 328
            else:
                self.appWidth = self.target_image_width * 2 + 256
                self.appHeight = self.target_image_height + 328

            self.setMinimumWidth(self.appWidth)
            self.setMinimumHeight(self.appHeight)

            self.move(x + (width - self.appWidth) / 2, y + (height - self.appHeight) / 2)
            self.resize(self.appWidth, self.appHeight)

        self.normalSize = True
        self.mouseStat = True

        # ----------------------------------------------------------------------------------------------------------------------
        # configure the appearance of the graphic tool
        # ----------------------------------------------------------------------------------------------------------------------
        self.setWindowFlags(Qt.FramelessWindowHint)  # | Qt.WindowStaysOnTopHint)
        self.setWindowOpacity(1.0)
        self.setMouseTracking(True)
        self.setAutoFillBackground(True)

        self.vesselSegmentationWindow = None
        self.parameterSettingWindow = MSAParameterSetting(self.controller, self.globalBackgroundColor, self.globalFontColor, self.globalFont)
        self.preferenceSettingWindow = MSAPreferenceSettingWindow(self.controller, self.globalBackgroundColor, self.globalFontColor, self.globalFont)
        self.startWindow = None
        self.networkConfigurationWindow = None
        self.workConfigurationWindow = None
        self.addPatientWindow = None

        # ----------------------------------------------------------------------------------------------------------------------
        # initialise the principal components of the graphic tool
        # ----------------------------------------------------------------------------------------------------------------------
        self.toolBar = MSAToolBar(self,
                                  self.controller,
                                  self.ihm_factor,
                                  self.appWidth,
                                  32 * self.ihm_factor,
                                  self.globalBackgroundColor,
                                  self.globalFontColor,
                                  self.globalFont)

        self.workspace = MSAWorkSpace(self, self.controller,
                                      self.ihm_factor,
                                      self.appWidth,
                                      self.appHeight - 52 * self.ihm_factor - 2,
                                      self.globalBackgroundColor,
                                      self.globalFontColor,
                                      self.globalFont,
                                      self.target_image_width, self.target_image_height)

        self.closeButton = QPushButton()
        self.closeButton.setStyleSheet("background-color: " + self.globalBackgroundColor + "; color:" + self.globalFontColor + ";")
        self.closeButton.setIcon(QIcon(":/red-close.png"))
        self.closeButton.setFixedSize(15 * self.ihm_factor, 15 * self.ihm_factor)
        self.closeButton.setIconSize(QSize(13 * self.ihm_factor, 13 * self.ihm_factor))
        self.closeButton.setFlat(True)

        self.maximizeButton = QPushButton()
        self.maximizeButton.setFixedSize(15 * self.ihm_factor, 15 * self.ihm_factor)
        self.maximizeButton.setStyleSheet("background-color: " + self.globalBackgroundColor + "; color:" + self.globalFontColor + ";")
        self.maximizeButton.setIcon(QIcon(":/blue-min.png"))
        self.maximizeButton.setIconSize(QSize(13 * self.ihm_factor, 13 * self.ihm_factor))
        self.maximizeButton.setFlat(True)

        self.minimizeButton = QPushButton()
        self.minimizeButton.setFixedSize(15 * self.ihm_factor, 15 * self.ihm_factor)
        self.minimizeButton.setStyleSheet("background-color: " + self.globalBackgroundColor + "; color:" + self.globalFontColor + ";")
        self.minimizeButton.setIcon(QIcon(":/yellow-min.png"))
        self.minimizeButton.setIconSize(QSize(13 * self.ihm_factor, 13 * self.ihm_factor))
        self.minimizeButton.setFlat(True)

        self.guiControlBar = QPushButton()
        self.guiControlBar.setFixedSize(self.appWidth * 0.04, 20 * self.ihm_factor)
        self.guiControlBar.setFlat(True)
        self.guiControlBar.setStyleSheet("background-color: " + self.globalBackgroundColor + "; color:" + self.globalFontColor + ";")
        self.guiControlBarLayout = QHBoxLayout(self.guiControlBar)
        self.guiControlBarLayout.addWidget(self.closeButton)
        self.guiControlBarLayout.addWidget(self.minimizeButton)
        self.guiControlBarLayout.addWidget(self.maximizeButton)
        self.guiControlBarLayout.setSpacing(1)
        self.guiControlBarLayout.setContentsMargins(0, 0, 0, 0)

        self.button_clicked_label = QLineEdit("tooltips")
        self.button_clicked_label.setFixedSize(self.appWidth * 0.4, 18 * self.ihm_factor)
        self.button_clicked_label.setStyleSheet("background-color: transparent; border: 0px solid " + self.globalFontColor)
        self.button_clicked_label.setContentsMargins(0, 0, 0, 0)

        self.progress_display_label = QProgressBar()
        self.progress_display_label.setFixedSize(self.appWidth * 0.14, 15 * self.ihm_factor)
        self.progress_display_label.setStyleSheet("QProgressBar::chunk{background:qlineargradient(spread:pad,x1:0,y1:0,x2:1,y2:0,stop:0 white,stop:1 " + self.globalBackgroundColor + ")}")
        self.progress_display_label.setValue(100)
        self.progress_display_label.setAlignment(Qt.AlignCenter)

        self.blankLabel = QLabel()
        self.blankLabel.setFixedSize(self.appWidth * 0.52, 18 * self.ihm_factor)
        self.blankLabel.setStyleSheet("background-color: transparent; border: 0px solid " + self.globalFontColor)

        self.statusBar = QLabel()
        self.statusBar.setFixedSize(self.appWidth, 20 * self.ihm_factor)
        self.statusBar.setStyleSheet("background-color: " + self.globalBackgroundColor + "; color:" + self.globalFontColor + ";")
        self.statusBarLayout = QHBoxLayout(self.statusBar)
        self.statusBarLayout.addWidget(self.guiControlBar)
        self.statusBarLayout.addWidget(self.progress_display_label)
        self.statusBarLayout.addWidget(self.button_clicked_label)
        self.statusBarLayout.addWidget(self.blankLabel)
        self.statusBarLayout.setSpacing(1)
        self.statusBarLayout.setContentsMargins(0, 0, 0, 0)

        # --------------------------------F--------------------------------------------------------------------------------------
        # generate a vertical layout to contains all the component upon
        # ----------------------------------------------------------------------------------------------------------------------
        self.mainLayout = QVBoxLayout(self)
        self.mainLayout.addWidget(self.toolBar)
        self.mainLayout.addWidget(self.workspace)
        self.mainLayout.addWidget(self.statusBar)
        self.mainLayout.setSpacing(0)
        self.mainLayout.setContentsMargins(0, 0, 0, 0)

        # ----------------------------------------------------------------------------------------------------------------------
        # signaux/slots configuration
        # ----------------------------------------------------------------------------------------------------------------------
        self.closeButton.clicked.connect(self.ferme)
        self.minimizeButton.clicked.connect(self.do_minimize_gui)
        self.maximizeButton.clicked.connect(self.do_maximize_gui)
        self.workspace.maximizeSignal.connect(self.do_maximize_gui)
        self.workspace.minimizeSignal.connect(self.do_minimize_gui)
        self.workspace.vesselSegmentationWindow.connect(self.vessel_segmention_window_setting)
        self.workspace.parameterWindowSetting.connect(self.parameter_window_setting)
        self.workspace.closeSignal.connect(self.ferme)

        ObjectEvent(self.guiControlBar).MouseEnter.connect(self.close_button_entered)
        ObjectEvent(self.guiControlBar).MouseLeave.connect(self.close_button_leaved)
        self.controller.imageSequenceLoaded.connect(self.is_image_sequence_loaded)
        self.controller.volumeImageLoaded.connect(self.is_volume_image_loaded)
        self.toolBar.enableGuidewireTrackingAlgorithm.connect(self.enable_guidewire_tracking)
        self.toolBar.enableEvaluationAlgorithm.connect(self.enable_evaluation)
        self.toolBar.messageCacheFetched.connect(self.configure_message_cache)
        self.toolBar.buttonMessage[str].connect(self.update_button_message)
        self.workspace.buttonMessage[str].connect(self.update_button_message)

        self.toolBar.systemStatusChanged[bool].connect(self.system_state_changed)
        self.toolBar.networkConfigurationDisplay.connect(self.network_configuration_window_display)
        self.toolBar.addPatientWindowDisplay.connect(self.add_patient_window_display)
        self.toolBar.startWindowDisplay.connect(self.start_window_display)
        self.toolBar.volumeRenderWindowDisplay.connect(self.generate_volume_renderer_window)
        self.toolBar.openWindowDisplay.connect(self.parameter_setting_window)
        self.toolBar.themeWindowSetting.connect(self.theme_setting_apply)

        self.preferenceSettingWindow.changeToTheme1.connect(self.theme_setting_apply)
        self.preferenceSettingWindow.change_color.connect(self.system_color_apply)
        self.preferenceSettingWindow.selected_file_color_change.connect(self.change_selected_file_color)
        self.preferenceSettingWindow.system_setting_clicked.connect(self.system_button_icon_change)
        self.parameterSettingWindow.parameter_button_icon_change.connect(self.parameter_setting_button_icon_changed)
        self.preferenceSettingWindow.change_font_size.connect(self.system_font_size_change)
        self.workspace.updateCurrentSequence[str].connect(self.update_current_sequence_information)

    def close_button_entered(self):
        self.closeButton.setIconSize(QSize(13 * self.ihm_factor, 13 * self.ihm_factor))
        self.closeButton.setIcon(QIcon(":/cancle.png"))
        self.maximizeButton.setIconSize(QSize(13 * self.ihm_factor, 13 * self.ihm_factor))
        self.maximizeButton.setIcon(QIcon(":/add.png"))
        self.minimizeButton.setIconSize(QSize(13 * self.ihm_factor, 13 * self.ihm_factor))
        self.minimizeButton.setIcon(QIcon(":/substract.png"))
        self.button_clicked_label.setText("close this window")

    def close_button_leaved(self):
        self.closeButton.setIconSize(QSize(13 * self.ihm_factor, 13 * self.ihm_factor))
        self.closeButton.setIcon(QIcon(":/red-close.png"))
        self.maximizeButton.setIconSize(QSize(13 * self.ihm_factor, 13 * self.ihm_factor))
        self.maximizeButton.setIcon(QIcon(":/blue-min.png"))
        self.minimizeButton.setIconSize(QSize(13 * self.ihm_factor, 13 * self.ihm_factor))
        self.minimizeButton.setIcon(QIcon(":/yellow-min.png"))

    def update_current_sequence_information(self, current_sequence_info):
        self.toolBar.set_current_sequence_information(current_sequence_info)

    def configure_message_cache(self):
        self.controller.set_message_cache(self.toolBar.fetch_input_message(), self.toolBar.fetch_output_message())

    def system_font_size_change(self):
        font_size_change = int(self.preferenceSettingWindow.font_size_lineEdit.text())
        self.globalFont = QFont("System", font_size_change, QFont.AnyStyle, False)

    def parameter_setting_button_icon_changed(self):
        self.workspace.paraset_button_icon_change()

    def change_selected_file_color(self):
        self.globalBackgroundColor = self.preferenceSettingWindow.color_select_lineEdit.currentText()
        self.toolBar.setStyleSheet("background-color: " + self.globalBackgroundColor)
        self.statusBar.setStyleSheet("background-color: " + self.globalBackgroundColor)

    def work_space_icon_change(self):
        self.toolBar.work_space_icon_change()

    def system_button_icon_change(self):
        self.toolBar.system_button_icon_change()

    def vascular_button_icon_change(self):
        self.workspace.enable_vascular_button_clicked(True)

    def system_color_apply(self):
        self.globalBackgroundColor = self.preferenceSettingWindow.color_select_lineEdit.currentText()
        self.update_background_color(self.globalBackgroundColor)

    def update_background_color(self, background_color):
        self.workspace.update_background_color(background_color)
        self.toolBar.update_background_color(background_color)
        self.statusBar.setStyleSheet("background-color: " + background_color)

    def update_button_message(self, message):
        self.button_clicked_label.setText(message)

    def zoom_in_tooltip(self):
        self.button_clicked_label.setText("zoomIn")

    def gvf_tooltip(self):
        self.button_clicked_label.setText("gvf")

    def apply_basic_parameter(self):
        self.workspace.set_global_window_and_level(int(self.windowline.text()), int(self.levelline.text()))
        self.workspace.set_global_voi(int(self.boxwline.text()), int(self.boxhline.text()))

    def set_global_image_size(self, w, h):
        self.controller.set_global_image_size(w, h)

    def enable_guidewire_tracking(self):
        self.workspace.enable_guidewire_tracking()

    def enable_evaluation(self):
        self.workspace.enable_evaluation()

    def is_image_sequence_loaded(self):
        self.workspace.set_image_sequence_loaded()

    def is_volume_image_loaded(self):
        self.update_x_ray_sequences()

    def ferme(self):
        self.controller.close_communication_stack()

        if self.vesselSegmentationWindow is not None:
            self.vesselSegmentationWindow.close()

        if self.parameterSettingWindow is not None:
            self.parameterSettingWindow.close()

        if self.preferenceSettingWindow is not None:
            self.preferenceSettingWindow.close()

        self.close()

    def do_display(self):
        self.update_x_ray_sequences()
        self.show()

    def start_window_display(self):
        if self.startWindow is None:
            self.startWindow = MSAStartWindow(self.controller, self.globalBackgroundColor, self.globalFontColor, self.globalFont)
            self.startWindow.workspaceConfigured.connect(self.do_display)
            self.startWindow.exitSystem.connect(self.close)
        self.startWindow.display()

    def update_x_ray_sequences(self):
        self.workspace.update_x_ray_sequences()

    # -------------------------------------------------------------------------------------------------------------------------------------------
    #  LiENA network configuration window
    # -------------------------------------------------------------------------------------------------------------------------------------------
    def network_configuration_window_display(self):
        # self.toolBar.enable_communication_window_clicked(False)
        if self.networkConfigurationWindow is None:
            self.networkConfigurationWindow = MSANetworkConfigurationWindow(self.controller, self.ihm_factor, self.globalBackgroundColor, self.globalFontColor, self.globalFont)
            self.networkConfigurationWindow.windowClosed.connect(self.network_configuration_window_closed)
        self.networkConfigurationWindow.display()

    def network_configuration_window_closed(self):
        self.toolBar.communication_window_icon_change()
        self.networkConfigurationWindow = None

    def add_patient_window_display(self):
        # self.toolBar.enable_addPatient_button_clicked(False)
        if self.addPatientWindow is None:
            self.addPatientWindow = AddPatientWindow(self.controller, self.globalBackgroundColor, self.globalFontColor, self.globalFont)
        self.addPatientWindow.display()

    def vessel_segmention_window_setting(self):
        # self.workspace.enable_vascular_button_clicked(False)
        self.vesselSegmentationWindow = MSAVesselSegmentation(self.controller, self.globalBackgroundColor, self.globalFontColor, self.globalFont)
        # self.connect(self.vesselSegmentationWindow, pyqtSignal("vascular_button_clicked()"), self.vascular_button_icon_change)
        self.vesselSegmentationWindow.display()

    def add_patient_icon_change(self):
        self.toolBar.add_patient_icon_change()
        self.addPatientWindow = None

    def system_state_changed(self, flag):
        pass
        # self.workspace.amplify_img_view(flag)
        # self.workspace.modify_window_value(flag)

    def set_current_sequence_path(self, path):
        self.controller.set_current_sequence_path(path)

    def draw_background(self):
        self.setStyleSheet("background-color: orange;")

    def do_maximize_gui(self):
        self.showMaximized()

    def do_minimize_gui(self):
        self.showMinimized()

    def parameter_window_setting(self):
        self.parameterSettingWindow.display()
        self.workspace.enable_paraset_button_clicked(False)

    def parameter_setting_window(self):
        self.preferenceSettingWindow.display()
        self.toolBar.enable_parameter_setting_button(False)

    def theme_setting_apply(self):
        print('theme1')

    def apply_button_ensure(self):
        print('ensure')

    def vascular_button_icon_change(self):
        self.workspace.vascular_button_icon_change()

    def paraset_button_icon_change(self):
        self.workspace.paraset_button_icon_change()

    def display(self):
        if self.controller.check_system_meta_file():
            self.controller.set_global_workspace_by_meta_file()
            self.update_x_ray_sequences()
            self.show()
        else:
            self.startWindow = MSAStartWindow(self.controller, self.globalBackgroundColor, self.globalFontColor, self.globalFont)
            self.startWindow.workspaceConfigured.connect(self.do_display)
            self.startWindow.exitSystem.connect(self.close)
            self.startWindow.display()

    def generate_volume_renderer_window(self):
        self.current_sequence = self.controller.get_current_sequence_folder()
        if self.current_sequence is None:
            return

        if sys.platform == 'darwin':
            volume_file_path = self.current_sequence + '/volume/volume.mha'
        elif sys.platform == 'win32':
            volume_file_path = self.current_sequence + '\\volume\\volume.mha'
        else:
            volume_file_path = self.current_sequence + '/volume/volume.mha'

        if os.path.isfile(volume_file_path):
            print(volume_file_path)
            self.close()
            print(self.appWidth, self.appHeight)
            vrw = FourPanelViewer(self.controller, self.ihm_factor, self.appX, self.appY, self.appWidth, self.appHeight, self.globalBackgroundColor, self.globalFontColor, self.globalFont)
            vrw.closeSignal.connect(self.display)
            vrw.display()
            vrw.do_display_meta_file(volume_file_path)
