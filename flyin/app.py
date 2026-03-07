#!/usr/bin/env python3

import sys
from PyQt6.QtWidgets import QApplication, QWidget
from flyin.vars import Vars
from flyin.window import MyWidget, Window


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

        width: int = window.win_width
        height: int = window.win_height - 125

        main_widget = QWidget()
        window.setCentralWidget(main_widget)

        nav = MyWidget(
            int(0.2 * width) - 15, height - 20,
            window._draw_file_navigator, "black", window
        )

        visu = MyWidget(
            int(0.6 * width) - 10, height - 20,
            window._draw_visualization, "black", window
        )
        stats = MyWidget(
            int(0.2 * width) - 15, height - 20,
            window._draw_stats, "black", window
        )

        nav.move(10, 125)
        visu.move(int(0.2 * width) + 5, 125)
        stats.move(int(0.8 * width) + 5, 125)

        window.show()

        sys.exit(super().exec())
