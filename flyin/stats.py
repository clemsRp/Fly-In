#!/usr/bin/env python3

from typing import TYPE_CHECKING
from PyQt6.QtGui import QPainter
from flyin.widget import Widget
from flyin.engine import Engine
from flyin.vars import Vars

if TYPE_CHECKING:
    from flyin.window import Window


class Stats(Widget):
    '''
    Class for the stats
    '''

    def __init__(
                self, x: int | float, y: int | float,
                width: int | float, height: int | float, title: str,
                window: "Window", engine: Engine, vars: Vars
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
