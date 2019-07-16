"""
Last updated on 07/01/2015

@author: Cheng WANG,
"""
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QSize
from PyQt5.QtWidgets import QWidget, QLineEdit,QVBoxLayout, QFrame, QListWidgetItem
from src.MSAView.MSAMainWindow.MSAToolBar.MSASessionListWidget import SessionListWidget


class SessionChooseList(QWidget):
    def __init__(self, parent=None, ihm_factor=1, controller=None, width=0, height=0, background_color="", global_font_color="", global_font=None):
        super(SessionChooseList, self).__init__()
        self.parent = parent
        self.ihm_factor = ihm_factor
        self.controller = controller
        self.width = width
        self.height = height
        self.globalBackgroundColor = background_color
        self.globalFontColor = global_font_color
        self.globalFont = global_font

        # -----------------------------------------------------------
        # private attributes initialization for parameter filter area  255, 229,204
        # -----------------------------------------------------------
        self.cmdline_string = ""
        self.filterCmdLine = QLineEdit("x-ray sequence on cardiovascular")
        self.filterCmdLine.setStyleSheet("border: 1px solid "+self.globalFontColor+";"
                                         "border-radius: 0px; border-width:0px 0px 1px 0px;"
                                         "selection-background-color: orange; "
                                         "color: " + self.globalFontColor + ";")

        self.filterCmdLine.setFont(self.globalFont)
        self.filterCmdLine.setFixedSize(self.width, 30*self.ihm_factor)

        self.sessionListWidget = SessionListWidget(self, self.ihm_factor,  self.globalBackgroundColor, self.globalFontColor, self.globalFont)
        self.sessionListWidget.setFixedSize(self.width, self.height - 30*self.ihm_factor)
        self.sessionListWidget.verticalScrollBar().setStyleSheet("background-color: " + self.globalBackgroundColor)
        self.sessionListWidget.setFrameStyle(QFrame.NoFrame)

        my_layout = QVBoxLayout(self)
        my_layout.addWidget(self.filterCmdLine)
        my_layout.addWidget(self.sessionListWidget)
        my_layout.setSpacing(0)
        my_layout.setContentsMargins(0, 0, 0, 0)

        self.update_x_ray_sequences()

    def chose(self):
        index = int(str(self.filterCmdLine.text()))
        self.parent.choose_start_point_by_index(index)

    def update_x_ray_sequences(self):
        self.sessionListWidget.clear()

        sequences = self.controller.get_sequence_existed()

        for filename in sequences:
            title_item = QListWidgetItem(filename)
            title_item.setIcon(QIcon(":/title.png"))
            title_item.setFont(self.globalFont)
            title_item.setSizeHint(QSize(80*self.ihm_factor, 25*self.ihm_factor))
            self.sessionListWidget.addItem(title_item)

    def display(self, pos):
        self.show()
        self.move(pos.x() + 150, pos.y() + 10)

    def update_background_color(self, color_string):
        self.filterCmdLine.setStyleSheet("background-color: " + color_string)
        self.sessionListWidget.setStyleSheet("background-color: " + color_string)
