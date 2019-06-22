#!/usr/bin/env python

from PyQt5.QtCore import pyqtSignal, QSize, Qt, QObject
from PyQt5.QtWidgets import QWidget, QApplication, QGridLayout, QRadioButton, QGroupBox, QPushButton, QSpacerItem, QSizePolicy, QLabel, QHBoxLayout, QTreeWidgetItem, QTreeWidget, QLineEdit, QVBoxLayout, QComboBox, QCheckBox
from PyQt5.QtGui import QPixmap, QIcon, QFont, QColor
import os


class MSAPreferenceSettingWindow(QWidget):

    changeToTheme1 = pyqtSignal()
    change_color = pyqtSignal()
    system_setting_clicked = pyqtSignal()
    selected_file_color_change = pyqtSignal()
    change_font_size = pyqtSignal()

    def __init__(self, controller=None, background_color="", global_font_color="", global_font=None):
        super(QWidget, self).__init__()

        path = os.path.dirname(os.path.realpath(__file__))
        temp = path.split("src")

        self.img1 = QPixmap(temp[0] + "img/background1.png")

        self.controller = controller
        self.globalBackgroundColor = background_color
        self.globalFontColor = global_font_color
        self.globalFont = global_font

        self.desktop = QApplication.desktop()

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
        self.closeButton.setFixedSize(20, 20)
        self.closeButton.setIconSize(QSize(15, 15))
        self.closeButton.setFlat(True)

        self.maximizeButton = QPushButton()
        self.maximizeButton.setFixedSize(20, 20)
        self.maximizeButton.setStyleSheet("background:transparent")
        self.maximizeButton.setIcon(QIcon(":/add.png"))
        self.maximizeButton.setIconSize(QSize(15, 15))
        self.maximizeButton.setFlat(True)

        self.minimizeButton = QPushButton()
        self.minimizeButton.setStyleSheet("background:transparent")
        self.minimizeButton.setFixedSize(20, 20)
        self.minimizeButton.setIcon(QIcon(":/substract.png"))
        self.minimizeButton.setIconSize(QSize(15, 15))
        self.minimizeButton.setFlat(True)

        self.toolbarLabel = QLabel()
        self.toolbarLabel.setFixedSize(self.appWidth, 20)
        self.toolbarLabel.setStyleSheet("background-color: white")
        self.toolbarLabelLayout = QHBoxLayout(self.toolbarLabel)
        self.toolbarLabelLayout.addWidget(self.closeButton)
        self.toolbarLabelLayout.addWidget(self.minimizeButton)
        self.toolbarLabelLayout.addWidget(self.maximizeButton)
        self.toolbarLabelLayout.addItem(spacer_item)
        self.toolbarLabelLayout.setSpacing(1)
        self.toolbarLabelLayout.setContentsMargins(0, 0, 0, 0)

        self.search_button = QPushButton()
        self.search_button.setStyleSheet("background:transparent")
        self.search_button.setFixedSize(20, 20)
        self.search_button.setIcon(QIcon(":/searchButton.png"))
        self.search_button.setIconSize(QSize(15, 15))
        self.search_button.setFlat(True)

        self.search_LineEdit = QLineEdit()
        self.search_LineEdit.setStyleSheet("background:transparent; border: 1px solid " + self.globalBackgroundColor)

        self.search_label = QLabel()
        self.search_label.setFixedHeight(20)
        self.search_label.setStyleSheet("background:transparent;border:0px solid " + self.globalBackgroundColor)
        self.search_label_Layout = QHBoxLayout(self.search_label)
        self.search_label_Layout.addWidget(self.search_button)
        self.search_label_Layout.addWidget(self.search_LineEdit)
        self.search_label_Layout.setSpacing(1)
        self.search_label_Layout.setContentsMargins(3, 3, 3, 0)

        self.general_setting = QTreeWidget()
        self.general_setting.setHeaderHidden(True)
        self.general_setting.setStyleSheet("border: 0px solid white")
        self.general_setting.setContentsMargins(0, 5, 0, 0)
        self.general_setting.setStyleSheet("QTreeView::item:hover{background-color:rgb(66, 66, 68)}" "QTreeView::item:selected{background-color:rgb(0,110,86)}");

        self.color_setting = QTreeWidgetItem(self.general_setting)
        self.color_setting.setText(0, 'Color')

        self.system_color_child = QTreeWidgetItem(self.color_setting)
        self.system_color_child.setText(0, 'System color')

        self.current_child = QTreeWidgetItem(self.color_setting)
        self.current_child.setText(0, 'Current componnet color')

        self.fileselect_color_child = QTreeWidgetItem(self.current_child)
        self.fileselect_color_child.setText(0, 'FileselectArea')

        self.patientInfo_color_child = QTreeWidgetItem(self.current_child)
        self.patientInfo_color_child.setText(0, 'PatientInfoArea')
        self.toolBar_color_child = QTreeWidgetItem(self.current_child)
        self.toolBar_color_child.setText(0, 'Toolbar')
        self.statusBar_color_child = QTreeWidgetItem(self.current_child)
        self.statusBar_color_child.setText(0, 'StatusBar color')

        self.font_setting = QTreeWidgetItem(self.general_setting)
        self.font_setting.setText(0, 'Font')

        self.familySelect_child = QTreeWidgetItem(self.font_setting)
        self.familySelect_child.setText(0, 'Family')

        self.size_child = QTreeWidgetItem(self.font_setting)
        self.size_child.setText(0, 'Size')

        self.linespace_child = QTreeWidgetItem(self.font_setting)
        self.linespace_child.setText(0, 'LineSpacing')

        self.bold_child = QTreeWidgetItem(self.font_setting)
        self.bold_child.setText(0, 'Bold')

        self.italic_child = QTreeWidgetItem(self.font_setting)
        self.italic_child.setText(0, 'Italic')

        self.style_tree = QTreeWidgetItem(self.general_setting)
        self.style_tree.setText(0, 'System style')

        self.ifont_style = QTreeWidgetItem(self.style_tree)
        self.ifont_style.setText(0, 'Style1')

        self.sys2_style = QTreeWidgetItem(self.style_tree)
        self.sys2_style.setText(0, 'Style2')

        self.sys3_style = QTreeWidgetItem(self.style_tree)
        self.sys3_style.setText(0, 'Style3')

        self.sys4_style = QTreeWidgetItem(self.style_tree)
        self.sys4_style.setText(0, 'Style4')

        self.language_tree = QTreeWidgetItem(self.general_setting)
        self.language_tree.setText(0, 'Language')
        self.lan_Eng = QTreeWidgetItem(self.language_tree)
        self.lan_Eng.setText(0, 'English')
        self.lan_Franch = QTreeWidgetItem(self.language_tree)
        self.lan_Franch.setText(0, 'Franch')

        self.left_down_area = QLabel()
        self.left_down_area.setFixedSize(self.appWidth*0.35, self.appHeight-50)
        self.left_down_area.setStyleSheet("border: 0px solid white")
        self.left_down_Layout = QVBoxLayout(self.left_down_area)
        self.left_down_Layout.addWidget(self.general_setting)
        self.left_down_Layout.setSpacing(7)
        self.left_down_Layout.setContentsMargins(0, 0, 0, 0)

        self.left_select_area = QLabel()
        self.left_select_area.setFixedWidth(self.appWidth*0.35)
        self.left_select_area.setStyleSheet("background-color: rgb(221, 221, 221)")
        self.left_area_Layout = QVBoxLayout(self.left_select_area)
        self.left_area_Layout.addWidget(self.search_label)
        self.left_area_Layout.addWidget(self.left_down_area)
        self.left_area_Layout.addItem(QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Expanding))
        self.left_area_Layout.setSpacing(8)
        self.left_area_Layout.setContentsMargins(0, 0, 0, 0)

        self.name_lineEdit = QLineEdit('')
        self.name_lineEdit.setFixedSize(self.appWidth*0.2, 25)
        self.name_lineEdit.setStyleSheet("border: 0px solid " + self.globalFontColor)
        self.name_lineEdit.setFont(QFont("System", 15, QFont.AnyStyle, False))
        self.name_lineEdit.setContentsMargins(10, 0, 0, 0)

        self.name_lineEdit2 = QLineEdit('')
        self.name_lineEdit2.setFixedSize(self.appWidth * 0.45, 25)
        self.name_lineEdit2.setStyleSheet("border: 0px solid " + self.globalFontColor)
        self.name_lineEdit2.setFont(QFont("System", 10, QFont.AnyStyle, False))
        self.name_lineEdit2.setContentsMargins(10, 0, 0, 0)

        self.name_label = QLabel()
        self.name_label.setFixedSize(self.appWidth * 0.65, 25)
        self.name_label.setStyleSheet("border: 0px solid " + self.globalFontColor)
        self.name_label_layout = QHBoxLayout(self.name_label)
        self.name_label_layout.addWidget(self.name_lineEdit)
        self.name_label_layout.addWidget(self.name_lineEdit2)
        self.name_label_layout.setSpacing(1)
        self.name_label_layout.setContentsMargins(7, 0, 3, 0)

        self.declare_label = QLabel()
        self.declare_label.setFixedSize(self.appWidth*0.65, 25)
        self.declare_label.setStyleSheet("border: 0px solid " + self.globalFontColor)
        self.declare_label.setFont(QFont("System", 13, QFont.AnyStyle, False))
        self.declare_label.setContentsMargins(10, 0, 0, 0)

        self.font_select_label = QLabel('Family:')
        self.font_select_label.setFixedSize(self.appWidth*0.22, 25)

        self.font_select_lineEdit = QComboBox()
        self.font_select_lineEdit.setStyleSheet("margin-left:3px; border: 1px solid " + self.globalFontColor)
        self.font_select_lineEdit.setFixedSize(self.appWidth*0.25, 25)
        self.font_select_lineEdit.addItem('itatic')
        self.font_select_lineEdit.addItem('Bold')
        self.font_select_lineEdit.addItem('Helivator')

        self.font_style_select = QLabel()
        self.font_style_select.setFixedSize(self.appWidth*0.65, 25)
        self.font_select_layout = QHBoxLayout(self.font_style_select)
        self.font_select_layout.addWidget(self.font_select_label)
        self.font_select_layout.addWidget(self.font_select_lineEdit)
        self.font_select_layout.addItem(QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Expanding))
        self.font_select_layout.setSpacing(0)
        self.font_select_layout.setContentsMargins(0, 0, 0, 0)

        self.font_size_label = QLabel('Size:')
        self.font_size_label.setFixedSize(self.appWidth*0.22, 25)

        self.font_size_lineEdit = QLineEdit()
        self.font_size_lineEdit.setFixedSize(self.appWidth*0.1, 25);
        self.font_size_lineEdit.setStyleSheet("border: 1px solid " + self.globalFontColor)

        self.font_size_select = QLabel()
        self.font_size_select.setFixedSize(self.appWidth * 0.65, 25)
        self.font_size_layout = QHBoxLayout(self.font_size_select)
        self.font_size_layout.addWidget(self.font_size_label)
        self.font_size_layout.addWidget(self.font_size_lineEdit)
        self.font_size_layout.addItem(QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Expanding))
        self.font_size_layout.setSpacing(1)
        self.font_size_layout.setContentsMargins(0, 0, 0, 0)

        self.line_space_label = QLabel('LineSpacing:')
        self.line_space_label.setFixedSize(self.appWidth * 0.22, 25)

        self.line_space_lineEdit = QLineEdit()
        self.line_space_lineEdit.setFixedSize(self.appWidth * 0.3, 25)
        self.line_space_lineEdit.setStyleSheet("border: 1px solid " + self.globalFontColor)

        self.line_space_select = QLabel()
        self.line_space_select.setFixedSize(self.appWidth * 0.65, 25)
        self.line_space_layout = QHBoxLayout(self.line_space_select)
        self.line_space_layout.addWidget(self.line_space_label)
        self.line_space_layout.addWidget(self.line_space_lineEdit)
        self.line_space_layout.addItem(QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Expanding))
        self.line_space_layout.setSpacing(1)
        self.line_space_layout.setContentsMargins(0, 0, 0, 0)

        self.italic_checkbox = QCheckBox("Italic")
        self.italic_checkbox.setFixedSize(self.appWidth*0.3, 25)

        self.bold_checkBox = QCheckBox("Bold")
        self.bold_checkBox.setFixedSize(self.appWidth*0.3, 25)

        self.underline_checkBox = QCheckBox("Underline")
        self.underline_checkBox.setFixedSize(self.appWidth * 0.3, 25)

        self.font_checkBox = QLabel()
        self.font_checkBox.setFixedSize(self.appWidth*0.63, 20)
        self.font_checkBox_layout = QHBoxLayout(self.font_checkBox)
        self.font_checkBox_layout.addWidget(self.italic_checkbox)
        self.font_checkBox_layout.addWidget(self.bold_checkBox)
        self.font_checkBox_layout.addWidget(self.underline_checkBox)
        self.font_checkBox_layout.setSpacing(1)
        self.font_checkBox_layout.setContentsMargins(1, 0, 1, 0)

        self.font_color_select_label = QLabel('Font-Color:')
        self.font_color_select_label.setFixedSize(self.appWidth * 0.22, 25)

        self.font_color_select_lineEdit = QComboBox()
        self.font_color_select_lineEdit.setFixedSize(self.appWidth * 0.25, 25)
        self.font_color_select_lineEdit.setStyleSheet("margin-left:3px; border: 1px solid " + self.globalFontColor)
        self.fillColorlist(self.font_color_select_lineEdit)

        self.font_color_space_select = QLabel()
        self.font_color_space_select.setFixedSize(self.appWidth * 0.65, 25)
        self.font_color_space_select.setStyleSheet("border: 0px solid " + self.globalFontColor)
        self.font_color_space_select_layout = QHBoxLayout(self.font_color_space_select)
        self.font_color_space_select_layout.addWidget(self.font_color_select_label)
        self.font_color_space_select_layout.addWidget(self.font_color_select_lineEdit)
        self.font_color_space_select_layout.addItem(QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Expanding))
        self.font_color_space_select_layout.setSpacing(1)
        self.font_color_space_select_layout.setContentsMargins(0, 0, 0, 0)

        self.font_window_design = QLabel()
        self.font_window_design.setFixedSize(self.appWidth*0.65, self.appHeight-90)
        self.font_window_layout = QVBoxLayout(self.font_window_design)
        self.font_window_layout.addWidget(self.font_size_select)
        self.font_window_layout.addWidget(self.line_space_select)
        self.font_window_layout.addWidget(self.font_style_select)
        self.font_window_layout.addWidget(self.font_color_space_select)
        self.font_window_layout.addWidget(self.font_checkBox)
        self.font_window_layout.addItem(QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Expanding))
        self.font_window_layout.setSpacing(8)
        self.font_window_layout.setContentsMargins(10, 0, 0, 0)

        self.color_select_label = QLabel('Color:')
        self.color_select_label.setFixedSize(self.appWidth * 0.22, 25)

        self.color_select_lineEdit = QComboBox()
        self.color_select_lineEdit.setFixedSize(self.appWidth*0.33, 25)
        self.color_select_lineEdit.setStyleSheet("border: 1px solid "  + self.globalFontColor)
        self.fillColorlist(self.color_select_lineEdit)

        self.color_blank = QLabel()
        self.color_blank.setFixedSize(self.appWidth * 0.05, 25)

        self.color_space_select = QGroupBox('System color')
        self.color_space_select.setFixedSize(self.appWidth * 0.65, self.appHeight*0.15)
        self.color_space_select.setStyleSheet("border: 0px solid " + self.globalFontColor)
        self.color_space_layout = QHBoxLayout(self.color_space_select)
        self.color_space_layout.addWidget(self.color_select_label)
        self.color_space_layout.addWidget(self.color_select_lineEdit)
        self.color_space_layout.addWidget(self.color_blank)
        self.color_space_layout.setSpacing(1)
        self.color_space_layout.setContentsMargins(0, 0, 0, 0)

        self.current_component_label = QLabel('Fileselect color:')
        self.current_component_label.setFixedSize(self.appWidth * 0.22, self.appHeight * 0.05)

        self.current_component_color_select = QComboBox()
        self.current_component_color_select.setFixedSize(self.appWidth * 0.33, self.appHeight * 0.05)
        self.current_component_color_select.setStyleSheet("border: 1px solid " + self.globalFontColor)
        self.fillColorlist(self.current_component_color_select)

        self.file_select_blank = QLabel()
        self.file_select_blank.setFixedSize(self.appWidth * 0.05, self.appHeight*0.05)

        self.current_component_color = QLabel()
        self.current_component_color.setFixedSize(self.appWidth * 0.65, self.appHeight * 0.05)
        self.current_component_color_layout = QHBoxLayout(self.current_component_color)
        self.current_component_color_layout.addWidget(self.current_component_label)
        self.current_component_color_layout.addWidget(self.current_component_color_select)
        self.current_component_color_layout.addWidget(self.file_select_blank)
        self.current_component_color_layout.setSpacing(1)
        self.current_component_color_layout.setContentsMargins(0, 0, 0, 0)

        self.patient_widget_color_label = QLabel('PatientInfo color:')
        self.patient_widget_color_label.setFixedSize(self.appWidth * 0.22, self.appHeight * 0.05)

        self.patient_widget_color_lineEdit = QComboBox()
        self.patient_widget_color_lineEdit.setFixedSize(self.appWidth * 0.33, self.appHeight * 0.05)
        self.patient_widget_color_lineEdit.setStyleSheet("border: 1px solid " + self.globalFontColor)
        self.fillColorlist(self.patient_widget_color_lineEdit)

        self.patient_widget_color_blank = QLabel()
        self.patient_widget_color_blank.setFixedSize(self.appWidth * 0.05, self.appHeight * 0.05)

        self.patient_widget_color_select = QLabel()
        self.patient_widget_color_select.setFixedSize(self.appWidth * 0.65, self.appHeight * 0.05)
        self.patient_widget_color_layout = QHBoxLayout(self.patient_widget_color_select)
        self.patient_widget_color_layout.addWidget(self.patient_widget_color_label)
        self.patient_widget_color_layout.addWidget(self.patient_widget_color_lineEdit)
        self.patient_widget_color_layout.addWidget(self.patient_widget_color_blank)
        self.patient_widget_color_layout.setSpacing(1)
        self.patient_widget_color_layout.setContentsMargins(0, 0, 0, 0)

        self.toolbar_color_label = QLabel('ToolBar  color:')
        self.toolbar_color_label.setFixedSize(self.appWidth * 0.22, self.appHeight * 0.05)

        self.toolbar_color_lineEdit = QComboBox()
        self.toolbar_color_lineEdit.setFixedSize(self.appWidth * 0.33, self.appHeight * 0.05)
        self.toolbar_color_lineEdit.setStyleSheet("border: 1px solid " + self.globalFontColor)
        self.fillColorlist(self.toolbar_color_lineEdit)

        self.toolbar_color_blank = QLabel()
        self.toolbar_color_blank.setFixedSize(self.appWidth * 0.05, self.appHeight * 0.05)

        self.toolbar_color = QLabel()
        self.toolbar_color.setFixedSize(self.appWidth * 0.65, self.appHeight * 0.05)
        self.toolbar_color_layout = QHBoxLayout(self.toolbar_color)
        self.toolbar_color_layout.addWidget(self.toolbar_color_label)
        self.toolbar_color_layout.addWidget(self.toolbar_color_lineEdit)
        self.toolbar_color_layout.addWidget(self.toolbar_color_blank)
        self.toolbar_color_layout.setSpacing(1)
        self.toolbar_color_layout.setContentsMargins(0, 0, 0, 0)

        self.statusBar_color_label = QLabel('StatusBar color:')
        self.statusBar_color_label.setFixedSize(self.appWidth * 0.22, self.appHeight * 0.05)

        self.statusBar_color_lineEdit = QComboBox()
        self.statusBar_color_lineEdit.setFixedSize(self.appWidth * 0.33, self.appHeight * 0.05)
        self.statusBar_color_lineEdit.setStyleSheet("border: 1px solid " + self.globalFontColor)
        self.fillColorlist(self.statusBar_color_lineEdit)

        self.statusBar_color_blank = QLabel()
        self.statusBar_color_blank.setFixedSize(self.appWidth * 0.05, self.appHeight * 0.05)

        self.statusBar_color = QLabel()
        self.statusBar_color.setFixedSize(self.appWidth * 0.65, self.appHeight * 0.05)
        self.statusBar_color_layout = QHBoxLayout(self.statusBar_color)
        self.statusBar_color_layout.addWidget(self.statusBar_color_label)
        self.statusBar_color_layout.addWidget(self.statusBar_color_lineEdit)
        self.statusBar_color_layout.addWidget(self.statusBar_color_blank)
        self.statusBar_color_layout.setSpacing(1)
        self.statusBar_color_layout.setContentsMargins(0, 0, 0, 0)

        self.current_color_select = QGroupBox('Component color select')
        self.current_color_select.setFixedSize(self.appWidth * 0.65, self.appHeight *0.45)
        self.current_color_select.setStyleSheet("border: 0px solid " + self.globalFontColor)
        self.current_color_select_layout = QVBoxLayout(self.current_color_select)
        self.current_color_select_layout.addWidget(self.current_component_color)
        self.current_color_select_layout.addWidget(self.patient_widget_color_select)
        self.current_color_select_layout.addWidget(self.toolbar_color)
        self.current_color_select_layout.addWidget(self.statusBar_color)
        self.current_color_select_layout.setSpacing(1)
        self.current_color_select_layout.setContentsMargins(0, 0, 0, 0)

        self.color_window_design = QLabel()
        self.color_window_design.setFixedSize(self.appWidth * 0.65, self.appHeight* 0.8)
        self.color_window_layout = QVBoxLayout(self.color_window_design)
        self.color_window_layout.addWidget(self.color_space_select)
        self.color_window_layout.addWidget(self.current_color_select)
        self.color_window_layout.addItem(QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Expanding))
        self.color_window_layout.setSpacing(8)
        self.color_window_layout.setContentsMargins(10, 0, 0, 0)

        self.theme1_setting = QPushButton()
        self.theme1_setting.setFixedSize(self.appWidth * 0.32, self.appHeight * 0.2)
        self.theme1_setting.setIcon(QIcon(":/background1.png"))
        self.theme1_setting.setIconSize(QSize(self.appWidth * 0.32, self.appHeight * 0.2))
        self.theme1_setting.setStyleSheet("border: 0px solid red")
        self.theme1_setting.setFlat(True)

        self.theme2_setting = QPushButton()
        self.theme2_setting.setFixedSize(self.appWidth * 0.32, self.appHeight * 0.2)
        self.theme2_setting.setIcon(QIcon(":/background1.png"))
        self.theme2_setting.setIconSize(QSize(self.appWidth * 0.32, self.appHeight * 0.2))
        self.theme2_setting.setStyleSheet("border: 0px solid red")

        self.theme3_setting = QPushButton()
        self.theme3_setting.setFixedSize(self.appWidth * 0.32, self.appHeight * 0.2)
        self.theme3_setting.setIcon(QIcon(":/background1.png"))
        self.theme3_setting.setIconSize(QSize(self.appWidth * 0.32, self.appHeight * 0.2))
        self.theme3_setting.setStyleSheet("border: 0px solid red")

        self.theme4_setting = QPushButton()
        self.theme4_setting.setFixedSize(self.appWidth * 0.32, self.appHeight * 0.2)
        self.theme4_setting.setIcon(QIcon(":/background1.png"))
        self.theme4_setting.setIconSize(QSize(self.appWidth * 0.32, self.appHeight * 0.2))
        self.theme4_setting.setStyleSheet("border: 0px solid red")

        self.theme5_setting = QPushButton()
        self.theme5_setting.setFixedSize(self.appWidth * 0.32, self.appHeight * 0.2)
        self.theme5_setting.setIcon(QIcon(":/background1.png"))
        self.theme5_setting.setIconSize(QSize(self.appWidth * 0.32, self.appHeight * 0.2))
        self.theme5_setting.setStyleSheet("border: 0px solid red")

        self.theme6_setting = QPushButton()
        self.theme6_setting.setFixedSize(self.appWidth * 0.32, self.appHeight * 0.2)
        self.theme6_setting.setIcon(QIcon(":/background1.png"))
        self.theme6_setting.setIconSize(QSize(self.appWidth * 0.32, self.appHeight * 0.2))
        self.theme6_setting.setStyleSheet("border: 0px solid red")

        self.theme1_name = QLabel('theme1')
        self.theme1_name.setStyleSheet("color: rgb(0, 110, 86)")
        self.theme1_name.setFixedSize(self.appWidth * 0.32, self.appHeight * 0.05)
        self.theme1_name.setAlignment(Qt.AlignCenter)

        self.theme2_name = QLabel('theme2')
        self.theme2_name.setStyleSheet("color: rgb(0, 110, 86)")
        self.theme2_name.setFixedSize(self.appWidth * 0.32, self.appHeight * 0.05)
        self.theme2_name.setAlignment(Qt.AlignCenter)

        self.theme3_name = QLabel('theme3')
        self.theme3_name.setStyleSheet("color: rgb(0, 110, 86)")
        self.theme3_name.setFixedSize(self.appWidth * 0.32, self.appHeight * 0.05)
        self.theme3_name.setAlignment(Qt.AlignCenter)

        self.theme4_name = QLabel('theme4')
        self.theme4_name.setStyleSheet("color: rgb(0, 110, 86)")
        self.theme4_name.setFixedSize(self.appWidth * 0.32, self.appHeight * 0.05)
        self.theme4_name.setAlignment(Qt.AlignCenter)

        self.theme5_name = QLabel('theme5')
        self.theme5_name.setStyleSheet("color: rgb(0, 110, 86)")
        self.theme5_name.setFixedSize(self.appWidth * 0.32, self.appHeight * 0.05)
        self.theme5_name.setAlignment(Qt.AlignCenter)

        self.theme6_name = QLabel('theme6')
        self.theme6_name.setStyleSheet("color: rgb(0, 110, 86)")
        self.theme6_name.setFixedSize(self.appWidth * 0.32, self.appHeight * 0.05)
        self.theme6_name.setAlignment(Qt.AlignCenter)

        self.style_window_design = QLabel()
        self.style_window_design.setFixedSize(self.appWidth * 0.65, self.appHeight*0.8)
        self.style_window_layout = QGridLayout(self.style_window_design)
        self.style_window_layout.addWidget(self.theme1_setting, 0, 0)
        self.style_window_layout.addWidget(self.theme2_setting, 0, 1)
        self.style_window_layout.addWidget(self.theme1_name, 1, 0)
        self.style_window_layout.addWidget(self.theme2_name, 1, 1)
        self.style_window_layout.addWidget(self.theme3_setting, 2, 0)
        self.style_window_layout.addWidget(self.theme4_setting, 2, 1)
        self.style_window_layout.addWidget(self.theme3_name, 3, 0)
        self.style_window_layout.addWidget(self.theme4_name, 3, 1)
        self.style_window_layout.addWidget(self.theme5_setting, 4, 0)
        self.style_window_layout.addWidget(self.theme6_setting, 4, 1)
        self.style_window_layout.addWidget(self.theme5_name, 5, 0)
        self.style_window_layout.addWidget(self.theme6_name, 5, 1)
        self.style_window_layout.addItem(QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Expanding))
        self.style_window_layout.setSpacing(1)
        self.style_window_layout.setContentsMargins(3, 0, 0, 0)

        self.language_eng_label = QRadioButton('English')
        self.language_eng_label.setFixedSize(self.appWidth * 0.25, 25)

        self.language_Fra_label = QRadioButton('Franch')
        self.language_Fra_label.setFixedSize(self.appWidth * 0.25, 25)

        self.language_window_design = QLabel()
        self.language_window_design.setFixedSize(self.appWidth * 0.65, self.appHeight - 90)
        self.language_window_layout = QVBoxLayout(self.language_window_design)
        self.language_window_layout.addWidget(self.language_eng_label)
        self.language_window_layout.addWidget(self.language_Fra_label)
        self.language_window_layout.addItem(QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Expanding))
        self.language_window_layout.setSpacing(8)
        self.language_window_layout.setContentsMargins(20, 0, 0, 0)

        self.font_set_widget = QWidget()
        self.font_set_widget.setFixedSize(self.appWidth*0.65, self.appHeight*0.8)
        self.font_set_Layout = QVBoxLayout(self.font_set_widget)
        self.font_set_Layout.addWidget(self.font_window_design)
        self.font_set_Layout.addWidget(self.color_window_design)
        self.font_set_Layout.addWidget(self.style_window_design)
        self.font_set_Layout.addWidget(self.language_window_design)
        self.font_set_Layout.setSpacing(0)
        self.font_set_Layout.setContentsMargins(0, 0, 0, 0)

        self.line_label = QLabel()
        self.line_label.setFixedSize(self.appWidth*0.65, self.appHeight* 0.02)
        self.line_label.setStyleSheet("border-top: 1px solid " + self.globalFontColor)

        self.right_set_area = QWidget()
        self.right_set_area.setFixedWidth(self.appWidth*0.65)
        self.right_set_area.setStyleSheet("background-color: rgb(185, 185, 185)")
        self.right_area_Layout = QVBoxLayout(self.right_set_area)
        self.right_area_Layout.addWidget(self.name_label)
        self.right_area_Layout.addWidget(self.declare_label)
        self.right_area_Layout.addWidget(self.line_label)
        self.right_area_Layout.addWidget(self.font_set_widget)
        self.right_area_Layout.setSpacing(5)
        self.right_area_Layout.setContentsMargins(0, 0, 0, 0)

        self.central_setting_Window = QWidget()
        self.central_setting_Window.setFixedWidth(self.appWidth)
        self.center_Layout = QHBoxLayout(self.central_setting_Window)
        self.center_Layout.addWidget(self.left_select_area)
        self.center_Layout.addWidget(self.right_set_area)
        self.center_Layout.setSpacing(0)
        self.center_Layout.setContentsMargins(0, 0, 0, 0)

        self.cancelButton = QPushButton("Cancle")
        self.cancelButton.setFont(self.globalFont)
        self.cancelButton.setStyleSheet("color: " + self.globalFontColor)
        self.cancelButton.setFixedSize(40, 20)
        self.cancelButton.setFlat(True)

        self.applyButton = QPushButton("Apply")
        self.applyButton.setFont(self.globalFont)
        self.applyButton.setStyleSheet("color: " + self.globalFontColor)
        self.applyButton.setFixedSize(40, 20)
        self.applyButton.setFlat(True)

        self.okButton = QPushButton("OK")
        self.okButton.setFont(self.globalFont)
        self.okButton.setStyleSheet("color: " + self.globalFontColor)
        self.okButton.setFixedSize(40, 20)
        self.okButton.setFlat(True)

        self.controlBar = QLabel()
        self.controlBar.setFixedSize(self.appWidth, 20)
        self.controlBar.setStyleSheet("background-color: white")
        self.controlBar_Layout = QHBoxLayout(self.controlBar)
        self.controlBar_Layout.addItem(QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Expanding))
        self.controlBar_Layout.addWidget(self.cancelButton)
        self.controlBar_Layout.addWidget(self.applyButton)
        self.controlBar_Layout.addWidget(self.okButton)
        self.controlBar_Layout.setSpacing(5)
        self.controlBar_Layout.setContentsMargins(0, 0, 0, 0)

        self.setting_Window_Layout = QVBoxLayout(self)
        self.setting_Window_Layout.addWidget(self.toolbarLabel)
        self.setting_Window_Layout.addWidget(self.central_setting_Window)
        self.setting_Window_Layout.addWidget(self.controlBar)
        self.setting_Window_Layout.setSpacing(0)
        self.setting_Window_Layout.setContentsMargins(0, 0, 0, 0)

        self.set_connections()

    def set_connections(self):
        self.closeButton.clicked.connect(self.close_system)
        #self.connect(self.general_setting, pyqtSignal('itemClicked(QTreeWidgetItem*, int)'), self.get_widget_Name)


        self.color_select_lineEdit.currentIndexChanged.connect(self.change_background_color)
        self.current_component_color_select.currentIndexChanged.connect(self.change_selected_file_color)
        self.font_size_lineEdit.textChanged.connect(self.system_font_change)

        self.theme1_setting.clicked.connect(self.theme1_setting_apply)

    def system_font_change(self):
        self.change_font_size.emit()

    def change_selected_file_color(self):
        self.selected_file_color_change.emit()

    def change_background_color(self):
        self.change_color.emit()

    def theme1_setting_apply(self):
        self.changeToTheme1.emit()

    def get_widget_Name(self, item):
        if item.text(0) == 'Color':
            self.name_lineEdit.setText('Color')
            self.declare_label.setText('Color options, local color, file color, ')
            self.color_window_design.show()
            self.font_window_design.close()
            self.style_window_design.close()
            self.language_window_design.close()
            self.name_lineEdit2.setText('')

        elif item.text(0) == 'Font':
            self.name_lineEdit.setText('Font')
            self.declare_label.setText('Font options, font size, font, line spacing ')
            self.color_window_design.close()
            self.font_window_design.show()
            self.style_window_design.close()
            self.language_window_design.close()
            self.name_lineEdit2.setText('')

        elif item.text(0) == 'System style':
            self.name_lineEdit.setText('Style')
            self.declare_label.setText('style selection, ifont, customer')
            self.color_window_design.close()
            self.font_window_design.close()
            self.language_window_design.close()
            self.style_window_design.show()
            self.name_lineEdit2.setText('')

        elif item.text(0) == 'Language':
            self.name_lineEdit.setText('Language')
            self.declare_label.setText('language options, English, French')
            self.language_window_design.show()
            self.color_window_design.close()
            self.font_window_design.close()
            self.style_window_design.close()
            self.name_lineEdit2.setText('')

        elif item.text(0) == 'System color':
            self.name_lineEdit.setText('Color')
            self.declare_label.setText('Color options, local color, file color, ')
            self.name_lineEdit2.setText('System color')
            self.color_window_design.show()
            self.font_window_design.close()
            self.style_window_design.close()
            self.language_window_design.close()

        elif item.text(0) == 'Current componnet color':
            self.name_lineEdit.setText('Color')
            self.declare_label.setText('Color options, local color, file color, ')
            self.name_lineEdit2.setText('Current componnet color')
            self.color_window_design.show()
            self.font_window_design.close()
            self.style_window_design.close()
            self.language_window_design.close()

    def close_system(self):
        self.system_setting_clicked.emit()
        self.close()

    def display(self):
        self.show()
        self.color_window_design.close()
        self.font_window_design.close()
        self.style_window_design.close()
        self.language_window_design.close()

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
            self.mousePointerMove = event.globalclosePos()
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

    def fillColorlist(self, color_select):
        for name in QColor.colorNames():
            pix = QPixmap(QSize(self.appWidth*0.3, 25))
            pix.fill(QColor(name))
            color_select.addItem(QIcon(pix), name)
