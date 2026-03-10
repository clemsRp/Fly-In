#!/usr/bin/env python3

import sys
from PyQt6.QtWidgets import QApplication
from flyin.window import Window


class App(QApplication):
    '''
    Class used to manage the app and the event
    '''

    def __init__(self) -> None:
        '''
        Initialize the App

        Args:
            None
        Return:
            None
        '''
        super().__init__([])

    def launch(self) -> None:
        '''
        Launch the App

        Args:
            None
        Return:
            None
        '''
        window = Window()

        window.show()

        sys.exit(super().exec())
