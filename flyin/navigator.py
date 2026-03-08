#!/usr/bin/env python3

from pathlib import Path
from PyQt6.QtGui import QPainter
from PyQt6.QtWidgets import QMainWindow
from flyin.widget import Widget
from flyin.engine import Engine
from flyin.vars import Vars


class Line:
    '''
    Class for a line of the navigtor
    '''

    def __init__(self) -> None:
        '''
        Initialize the line

        Args:
            None
        Return:
            None
        '''
        pass


class Navigator(Widget):
    '''
    Class for the navigator
    '''

    def __init__(
                self, x: int | float, y: int | float,
                width: int | float, height: int | float, title: str,
                window: QMainWindow, engine: Engine, vars: Vars
            ) -> None:
        super().__init__(x, y, width, height, title, window, engine, vars)

    def _draw_tree(self, painter: QPainter) -> None:
        '''
        Draw the tree

        Args:
            painter: QPainter = The painter
        Return:
            None
        '''
        root = Path(".")
        for element in root.iterdir():
            print(element)

    def draw(self, painter: QPainter) -> None:
        '''
        Draw the personal part

        Args:
            None
        Return:
            None
        '''
        self.common_draw(painter)
        self._draw_tree(painter)
