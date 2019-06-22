#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Scripts to test LiENa middleware

author: Cheng WANG

last edited: December 2018
"""

import sys
from PyQt5.QtWidgets import QApplication
from src.LiENa.liena import Liena
from src.LiENa.LiENaBasic.lienaDefinition import *


def main():
    app = QApplication(sys.argv)

    communication_stack = Liena()
    communication_stack.register_device(SIAT_COCKPIT_VERSION_1, [SIAT_COCKPIT_VERSION_1, SIEMENS_CBCT_ARCADIS_ORBIC_VERSION_1, MEDSIGHT_INTERVENTIONAL_VASCULAR_ROBOT_VERSION_1])
    communication_stack.launch()
    # communication_stack.open_session_request(SIAT_COCKPIT_VERSION_1, "192.168.1.102", 10704)

    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
