#!/usr/bin/env python3

import vtk
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QWidget, QPushButton, QLabel, QHBoxLayout, QListWidget, QFrame, QVBoxLayout, QListWidgetItem
from PyQt5.QtCore import pyqtSignal, QSize
from MSAView.MSAMainWindow.MSAImageWorkSpace.ProcessWindow import ProcessWindow
from MSAView.MSAMainWindow.IHMTool.ObjectEvent import ObjectEvent


class ResultViewer(QWidget):
    # signals
    doClearScreens = pyqtSignal()
    buttonMessage = pyqtSignal(str)
    mesaureDistanceState = pyqtSignal(bool)
    coordinateState = pyqtSignal(bool)
    tracerBoxState = pyqtSignal(bool)
    tracerPointsState = pyqtSignal(bool)
    initialPointsSign = pyqtSignal(bool)

    def __init__(self, parent=None, controller=None, ihm_factor=1, width=0, height=0, target_image_width=0, target_image_height=0,  background_color="", global_font_color="", global_font=None):
        QWidget.__init__(self)

        # variable locale
        self.parent = parent
        self.controller = controller
        self.ihm_factor = ihm_factor
        self.width = width
        self.height = height

        self.target_image_width = target_image_width
        self.target_image_height = target_image_height

        self.globalBackgroundColor = background_color
        self.globalFontColor = global_font_color
        self.globalFont = global_font

        self.box_w = 0
        self.box_h = 0
        self.window = 0
        self.level = 0

        self.drawPointButtonClicked = False
        self.locateButtonClicked = False
        self.zoomInButtonClicked = False
        self.zoomOutButtonClicked = False
        self.locationButtonClicked = False
        self.compassesButtonClicked = False
        self.cutButtonClicked = False
        self.triangleButtonClicked = False
        self.file1ButtonClicked = False
        self.noteButtonClicked = False
        self.lightButtonClicked = False
        self.initialPointsSignButtonClicked = False
        self.chartButtonClicked = False

        self.scaleMagnify = vtk.vtkImageMagnify()
        self.shrink = vtk.vtkImageShrink3D()
        self.mapper = vtk.vtkImageMapper()

        self.xRayImageWidth = self.target_image_width
        self.xRayImageHeight = self.target_image_height

        # configure properties
        self.setFixedSize(self.width, self.height)
        self.setStyleSheet("background-color:" + self.globalBackgroundColor + "; border: 0px solid orange")

        self.imageProcessingViewerWidth = self.target_image_width*self.ihm_factor
        self.imageProcessingViewerHeight = self.target_image_height*self.ihm_factor

        self.imageProcessingViewer = ProcessWindow(self, self.controller, self.imageProcessingViewerWidth, self.imageProcessingViewerHeight, self.target_image_width, self.target_image_height, self.globalBackgroundColor, self.globalFontColor, self.globalFont)

        self.zoomInButton = QPushButton()
        self.zoomInButton.setStyleSheet("background:transparent; color:white")
        self.zoomInButton.setIcon(QIcon(":/shrink.png"))
        self.zoomInButton.setMouseTracking(True)
        self.zoomInButton.setFixedSize(QSize(20*self.ihm_factor, 20*self.ihm_factor))
        self.zoomInButton.setIconSize(QSize(16*self.ihm_factor, 16*self.ihm_factor))
        self.zoomInButton.setFlat(False)

        self.zoomOutButton = QPushButton()
        self.zoomOutButton.setStyleSheet("background:transparent; color:white")
        self.zoomOutButton.setIcon(QIcon(":/enlarge.png"))
        self.zoomOutButton.setMouseTracking(True)
        self.zoomOutButton.setFixedSize(QSize(20*self.ihm_factor, 20*self.ihm_factor))
        self.zoomOutButton.setIconSize(QSize(16*self.ihm_factor, 16*self.ihm_factor))
        self.zoomOutButton.setFlat(False)

        self.renewButton = QPushButton()
        self.renewButton.setStyleSheet("background:transparent; color:white")
        self.renewButton.setIcon(QIcon(":/renew.png"))
        self.renewButton.setMouseTracking(True)
        self.renewButton.setFixedSize(QSize(20*self.ihm_factor, 20*self.ihm_factor))
        self.renewButton.setIconSize(QSize(16*self.ihm_factor, 16*self.ihm_factor))
        self.renewButton.setFlat(False)

        self.lightButton = QPushButton()
        self.lightButton.setStyleSheet("background:transparent; color:white")
        self.lightButton.setIcon(QIcon(":/light.png"))
        self.lightButton.setFixedSize(QSize(20*self.ihm_factor, 20*self.ihm_factor))
        self.lightButton.setIconSize(QSize(16*self.ihm_factor, 16*self.ihm_factor))
        self.lightButton.setFlat(False)

        self.triangleButton = QPushButton()
        self.triangleButton.setStyleSheet("background:transparent; color:white")
        self.triangleButton.setIcon(QIcon(":/triangle.png"))
        self.triangleButton.setFixedSize(QSize(20*self.ihm_factor, 20*self.ihm_factor))
        self.triangleButton.setIconSize(QSize(16*self.ihm_factor, 16*self.ihm_factor))
        self.triangleButton.setFlat(False)

        self.chartButton = QPushButton()
        self.chartButton.setStyleSheet("background:transparent; color:white")
        self.chartButton.setIcon(QIcon(":/chart.png"))
        self.chartButton.setFixedSize(QSize(20*self.ihm_factor, 20*self.ihm_factor))
        self.chartButton.setIconSize(QSize(16*self.ihm_factor, 16*self.ihm_factor))
        self.chartButton.setFlat(False)

        self.block1Button = QPushButton()
        self.block1Button.setStyleSheet("background:transparent; color:white")
        self.block1Button.setIcon(QIcon(":/block1.png"))
        self.block1Button.setFixedSize(QSize(20*self.ihm_factor, 20*self.ihm_factor))
        self.block1Button.setIconSize(QSize(16*self.ihm_factor, 16*self.ihm_factor))
        self.block1Button.setFlat(False)

        self.compassesButton = QPushButton()
        self.compassesButton.setStyleSheet("background:transparent; color:white")
        self.compassesButton.setIcon(QIcon(":/compasses.png"))
        self.compassesButton.setFixedSize(QSize(20*self.ihm_factor, 20*self.ihm_factor))
        self.compassesButton.setIconSize(QSize(18*self.ihm_factor, 18*self.ihm_factor))
        self.compassesButton.setFlat(False)

        self.cutButton = QPushButton()
        self.cutButton.setStyleSheet("background:transparent; color:white")
        self.cutButton.setIcon(QIcon(":/cut.png"))
        self.cutButton.setFixedSize(QSize(20*self.ihm_factor, 20*self.ihm_factor))
        self.cutButton.setIconSize(QSize(18*self.ihm_factor, 18*self.ihm_factor))
        self.cutButton.setFlat(False)

        self.drawPointButton = QPushButton()
        self.drawPointButton.setStyleSheet("background:transparent; color:white")
        self.drawPointButton.setIcon(QIcon(":/drawline.png"))
        self.drawPointButton.setFixedSize(QSize(20*self.ihm_factor, 20*self.ihm_factor))
        self.drawPointButton.setIconSize(QSize(18*self.ihm_factor, 18*self.ihm_factor))
        self.drawPointButton.setFlat(False)

        self.file1Button = QPushButton()
        self.file1Button.setStyleSheet("background:transparent; color:white")
        self.file1Button.setIcon(QIcon(":/file1.png"))
        self.file1Button.setFixedSize(QSize(20*self.ihm_factor, 20*self.ihm_factor))
        self.file1Button.setIconSize(QSize(18*self.ihm_factor, 18*self.ihm_factor))
        self.file1Button.setFlat(False)

        self.locateButton = QPushButton()
        self.locateButton.setStyleSheet("background:transparent; color:white")
        self.locateButton.setIcon(QIcon(":/locate.png"))
        self.locateButton.setFixedSize(QSize(20*self.ihm_factor, 20*self.ihm_factor))
        self.locateButton.setIconSize(QSize(18*self.ihm_factor, 18*self.ihm_factor))
        self.locateButton.setFlat(False)

        self.locationButton = QPushButton()
        self.locationButton.setStyleSheet("background:transparent; color:white")
        self.locationButton.setIcon(QIcon(":/location.png"))
        self.locationButton.setFixedSize(QSize(20*self.ihm_factor, 20*self.ihm_factor))
        self.locationButton.setIconSize(QSize(18*self.ihm_factor, 18*self.ihm_factor))
        self.locationButton.setFlat(False)

        self.noteButton = QPushButton()
        self.noteButton.setStyleSheet("background:transparent; color:white")
        self.noteButton.setIcon(QIcon(":/note.png"))
        self.noteButton.setFixedSize(QSize(20*self.ihm_factor, 20*self.ihm_factor))
        self.noteButton.setIconSize(QSize(18*self.ihm_factor, 18*self.ihm_factor))
        self.noteButton.setFlat(False)

        self.controlBar = QLabel()
        self.controlBar.setStyleSheet("background-color:" + self.globalBackgroundColor)
        self.controlBar.setFixedHeight(20*self.ihm_factor)
        self.controlBarLayout = QHBoxLayout(self.controlBar)
        self.controlBarLayout.addWidget(self.renewButton)
        self.controlBarLayout.addWidget(self.drawPointButton)
        self.controlBarLayout.addWidget(self.cutButton)
        self.controlBarLayout.addWidget(self.locationButton)
        self.controlBarLayout.addWidget(self.triangleButton)
        self.controlBarLayout.addWidget(self.zoomInButton)
        self.controlBarLayout.addWidget(self.zoomOutButton)
        self.controlBarLayout.addWidget(self.lightButton)
        self.controlBarLayout.addWidget(self.compassesButton)
        self.controlBarLayout.addWidget(self.file1Button)
        self.controlBarLayout.addWidget(self.chartButton)
        self.controlBarLayout.addWidget(self.locateButton)
        self.controlBarLayout.addWidget(self.noteButton)
        self.controlBarLayout.addWidget(self.block1Button)
        self.controlBarLayout.setSpacing(0)
        self.controlBarLayout.setContentsMargins(0, 0, 0, 0)

        self.dataVisualizationArea = QListWidget()
        self.dataVisualizationArea.setFixedSize(self.target_image_width*self.ihm_factor-62, 256*self.ihm_factor)
        self.dataVisualizationArea.setStyleSheet("background-color:transparent; color:" + self.globalFontColor)
        self.dataVisualizationArea.setViewMode(QListWidget.IconMode)

        self.dataVisualizationAreaControlArea = QLabel()
        self.dataVisualizationAreaControlArea.setFixedSize(62, 256*self.ihm_factor)
        self.dataVisualizationAreaControlArea.setStyleSheet("background-color:transparent; color:" + self.globalFontColor)

        self.imageFilesArea = QFrame()
        self.imageFilesArea.setFixedSize(self.target_image_width*self.ihm_factor, 256*self.ihm_factor)
        self.imageFilesAreaLayout = QHBoxLayout(self.imageFilesArea)
        self.imageFilesAreaLayout.addWidget(self.dataVisualizationArea)
        self.imageFilesAreaLayout.addWidget(self.dataVisualizationAreaControlArea)
        self.imageFilesAreaLayout.setContentsMargins(0, 0, 0, 0)
        self.imageFilesAreaLayout.setSpacing(0)

        self.resultViewerLayout = QVBoxLayout(self)
        self.resultViewerLayout.addWidget(self.imageProcessingViewer)
        self.resultViewerLayout.addWidget(self.controlBar)
        self.resultViewerLayout.addWidget(self.imageFilesArea)
        self.resultViewerLayout.setContentsMargins(0, 0, 0, 0)
        self.resultViewerLayout.setSpacing(0)

        self.set_connections()

    def set_connections(self):
        self.renewButton.clicked.connect(self.renew_button_clicked)
        self.drawPointButton.clicked.connect(self.draw_point_button_clicked)
        self.cutButton.clicked.connect(self.cut_button_clicked)
        self.locationButton.clicked.connect(self.location_button_clicked)
        self.zoomInButton.clicked.connect(self.zoom_in_button_clicked)
        self.locateButton.clicked.connect(self.locate_Button_located)
        self.zoomOutButton.clicked.connect(self.zoom_out_button_clicked)
        self.compassesButton.clicked.connect(self.compasses_button_clicked)
        self.triangleButton.clicked.connect(self.triangle_button_clicked)
        self.file1Button.clicked.connect(self.file1Button_clicked)
        self.noteButton.clicked.connect(self.noteButton_clicked)
        self.lightButton.clicked.connect(self.lightButton_clicked)
        self.block1Button.clicked.connect(self.initial_points_button_clicked)
        self.chartButton.clicked.connect(self.chart_button_clicked)
        self.dataVisualizationArea.itemDoubleClicked["QListWidgetItem *"].connect(self.do_visualise_a_picture)

        ObjectEvent(self.renewButton).MouseHovered.connect(self.renew_tooltip)
        ObjectEvent(self.drawPointButton).MouseHovered.connect(self.draw_point_tooltip)
        ObjectEvent(self.cutButton).MouseHovered.connect(self.cut_tooltip)
        ObjectEvent(self.locationButton).MouseHovered.connect(self.location_tooltip)
        ObjectEvent(self.zoomInButton).MouseHovered.connect(self.zoomIn_tooltip)
        ObjectEvent(self.locateButton).MouseHovered.connect(self.locate_tooltip)
        ObjectEvent(self.zoomOutButton).MouseHovered.connect(self.zoomOut_tooltip)
        ObjectEvent(self.compassesButton).MouseHovered.connect(self.compasses_tooltip)
        ObjectEvent(self.triangleButton).MouseHovered.connect(self.triangle_tooltip)
        ObjectEvent(self.file1Button).MouseHovered.connect(self.file1_tooltip)
        ObjectEvent(self.noteButton).MouseHovered.connect(self.note_tooltip)
        ObjectEvent(self.lightButton).MouseHovered.connect(self.light_tooltip)
        ObjectEvent(self.block1Button).MouseHovered.connect(self.block1_tooltip)
        ObjectEvent(self.chartButton).MouseHovered.connect(self.chart_tooltip)

    def initial_points_button_clicked(self):
        self.initialPointsSignButtonClicked = not self.initialPointsSignButtonClicked
        if self.initialPointsSignButtonClicked:
            self.block1Button.setIcon(QIcon(":/block2.png"))
        else:
            self.block1Button.setIcon(QIcon(":/block1.png"))
        self.initialPointsSign.emit(self.initialPointsSignButtonClicked)

    def triangle_button_clicked(self):
        self.triangleButtonClicked = not self.triangleButtonClicked
        if self.triangleButtonClicked:
            self.triangleButton.setIcon(QIcon(":/triangle2.png"))
        else:
            self.triangleButton.setIcon(QIcon(":/triangle.png"))
        self.mesaureDistanceState.emit(self.triangleButtonClicked)

    def location_button_clicked(self):
        self.locationButtonClicked = not self.locationButtonClicked
        if self.locationButtonClicked:
            self.locationButton.setIcon(QIcon(":/location2.png"))
        else:
            self.locationButton.setIcon(QIcon(":/location.png"))
        self.coordinateState.emit(self.locationButtonClicked)

    def cut_button_clicked(self):
        self.cutButtonClicked = not self.cutButtonClicked
        if self.cutButtonClicked:
            self.cutButton.setIcon(QIcon(":/cut2.png"))
        else:
            self.cutButton.setIcon(QIcon(":/cut.png"))
        self.tracerBoxState.emit(self.cutButtonClicked)

    def draw_point_button_clicked(self):
        self.drawPointButtonClicked = not self.drawPointButtonClicked
        if self.drawPointButtonClicked:
            self.drawPointButton.setIcon(QIcon(":/drawline2.png"))
        else:
            self.drawPointButton.setIcon(QIcon(":/drawline.png"))
        self.tracerPointsState.emit(self.drawPointButtonClicked)

    def renew_button_clicked(self):
        self.doClearScreens.emit()

    def chart_button_clicked(self):
        self.chartButtonClicked = not self.chartButtonClicked
        if self.chartButtonClicked:
            self.chartButton.setIcon(QIcon(":/chart2.png"))
        else:
            self.chartButton.setIcon(QIcon(":/chart.png"))

    def lightButton_clicked(self):
        self.lightButtonClicked = not self.lightButtonClicked
        if self.lightButtonClicked:
            self.lightButton.setIcon(QIcon(":/light2.png"))
        else:
            self.lightButton.setIcon(QIcon(":/light.png"))

    def noteButton_clicked(self):
        self.noteButtonClicked = not self.noteButtonClicked
        if self.noteButtonClicked:
            self.noteButton.setIcon(QIcon(":/file2.png"))
        else:
            self.noteButton.setIcon(QIcon(":/note.png"))

    def file1Button_clicked(self):
        self.file1ButtonClicked = not self.file1ButtonClicked
        if self.file1ButtonClicked:
            self.file1Button.setIcon(QIcon(":/file3.png"))
        else:
            self.file1Button.setIcon(QIcon(":/file1.png"))

    def compasses_button_clicked(self):
        self.compassesButtonClicked = not self.compassesButtonClicked
        if self.compassesButtonClicked:
            self.compassesButton.setIcon(QIcon(":/compasses2.png"))
        else:
            self.compassesButton.setIcon(QIcon(":/compasses.png"))

    def zoom_out_button_clicked(self):
        self.zoomOutButtonClicked = not self.zoomOutButtonClicked
        if self.zoomOutButtonClicked:
            self.zoomOutButton.setIcon(QIcon(":/enlarge2.png"))
        else:
            self.zoomOutButton.setIcon(QIcon(":/enlarge.png"))

    def locate_Button_located(self):
        self.locateButtonClicked = not self.locateButtonClicked
        if self.locateButtonClicked:
            self.locateButton.setIcon(QIcon(":/locate2.png"))
        else:
            self.locateButton.setIcon(QIcon(":/locate.png"))

    def zoom_in_button_clicked(self):
        self.zoomInButtonClicked = not self.zoomInButtonClicked
        if self.zoomInButtonClicked:
            self.zoomInButton.setIcon(QIcon(":/shrink2.png"))
        else:
            self.zoomInButton.setIcon(QIcon(":/shrink.png"))

    def set_global_window_and_level(self, window, level):
        self.window = window
        self.level = level
        self.imageProcessingViewer.set_global_window_and_level(window, level)

    def set_global_voi(self, w, h):
        self.box_w = w
        self.box_h = h
        self.imageProcessingViewer.set_global_voi(w, h)

    def do_visualise_a_picture(self):
        img = self.controller.get_image_by_name(str(self.dataVisualizationArea.currentItem().text()))
        self.imageProcessingViewer.display_vtk_image(img)

    def clear_all_picture(self):
        self.dataVisualizationArea.clear()

    def add_a_picture(self, filename, pngpath):
        item = QListWidgetItem(filename)
        item.setIcon(QIcon(pngpath))
        self.dataVisualizationArea.addItem(item)

    def do_plot_distance_flow(self, distance_flow):
        self.dataVisualizationArea.do_plot_distance_flow(distance_flow)

    def clear(self):
        self.imageProcessingViewer.clear()

    def clear_all(self):
        self.imageProcessingViewer.clear()
        self.dataVisualizationArea.clear()

    def update_all(self):
        self.imageProcessingViewer.update()

    def show_button_clicked(self):
        output = self.ctSequenceViewer.fetch_guide_wire()
        self.display(output)

    def display_numpy_image(self, input):
        self.imageProcessingViewer.display(input)

    def display_frangi(self, input):
        self.imageProcessingViewer.display_vtk_image(input)

    def display_local_frangi(self,input):
        self.imageProcessingViewer.disply_frangi(input)

    def update_background_color(self, color_string):
        color = QColor(color_string)
        self.controlBar.setStyleSheet("background-color: " + color_string)
        self.imageProcessingViewer.update_background_color(color.red(), color.green(), color.blue())
        self.imageFilesArea.setStyleSheet("background-color: " + color_string)

    def renew_tooltip(self):
        self.buttonMessage.emit("renew")

    def chart_tooltip(self):
        self.buttonMessage.emit("chart")

    def draw_point_tooltip(self):
        self.buttonMessage.emit("draw point")

    def cut_tooltip(self):
        self.buttonMessage.emit("cut")

    def block1_tooltip(self):
        self.buttonMessage.emit("block")

    def file1_tooltip(self):
        self.buttonMessage.emit("open file")

    def note_tooltip(self):
        self.buttonMessage.emit("note")

    def light_tooltip(self):
        self.buttonMessage.emit("light")

    def zoomOut_tooltip(self):
        self.buttonMessage.emit("zoomOut")

    def compasses_tooltip(self):
        self.buttonMessage.emit("compasses")

    def triangle_tooltip(self):
        self.buttonMessage.emit("triangle")

    def location_tooltip(self):
        self.buttonMessage.emit("location")

    def zoomIn_tooltip(self):
        self.buttonMessage.emit("zoomIn")

    def locate_tooltip(self):
        self.buttonMessage.emit("locate")