#!/usr/bin/env python3

import sys
from PyQt6.QtWidgets import QApplication
from flyin.vars import Vars
from flyin.window import Window


class App(QApplication):
    '''
    Class used to manage the app and the event
    '''

    def __init__(self, vars: Vars) -> None:
        '''
        Initialize the App

        Args:
            vars: Vars = All the "global" variables
        Return:
            None
        '''
        super().__init__([])
        self.vars: Vars = vars

    def launch(self) -> None:
        '''
        Launch the App

        Args:
            None
        Return:
            None
        '''
        window = Window(self.vars)

        window.show()

        sys.exit(super().exec())
