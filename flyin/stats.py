#!/usr/bin/env python3

from PyQt6.QtGui import QPainter
from PyQt6.QtWidgets import QMainWindow
from flyin.widget import Widget
from flyin.engine import Engine
from flyin.vars import Vars


class Stats(Widget):
    '''
    Class for the stats
    '''

    def __init__(
                self, x: int | float, y: int | float,
                width: int | float, height: int | float, title: str,
                window: QMainWindow, engine: Engine, vars: Vars
            ) -> None:
        super().__init__(x, y, width, height, title, window, engine, vars)

    def draw(self, painter: QPainter) -> None:
        '''
        Draw the personal part

        Args:
            None
        Return:
            None
        '''
        self.common_draw(painter)
