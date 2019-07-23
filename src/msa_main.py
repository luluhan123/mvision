#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
IHM to do analysis work on CT Image Sequence

author: Cheng WANG

last edited: January 2015
"""

import sys
import time
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import QApplication, QSplashScreen

from src.LiENa.liena import Liena
from src.MSAModel.MSAModel import MSAModel
from src.MSAController.MSAController import MSAController
from src.MSAProcessingUnit.CTSAProcessingFactory import CTSAProcessingFactory
from src.MSAView.MSAMainWindow.MSAMainWindow import MSAMainWindow
from src.Image.qrc_resources import *
# cmd for convert png files to resource code:pyrcc4.exe -o qrc_resources.py resources.qrc


def main():
    """
        -- the main procedure to generate the graphical tool
    """
    app = QApplication(sys.argv)
    app.setOrganizationName("MedSight")
    app.setApplicationName("MedSight")
    app.setWindowIcon(QIcon(":icon.png"))
    app.setStyle("cleanlooks")  # important, if not, icon can't adapt the size of button

    splash = QSplashScreen(QPixmap(":title.png"))
    splash.show()
    time.sleep(1)

    processing_factory = CTSAProcessingFactory()

    model = MSAModel(processing_factory)

    communication_stack = Liena()

    controller = MSAController(model, communication_stack)

    main_window = MSAMainWindow(controller)

    main_window.display()

    splash.finish(main_window)

    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
