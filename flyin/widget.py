#!/usr/bin/env python3

from abc import abstractmethod, ABC
from PyQt6.QtGui import QPainter, QColor, QFont
from PyQt6.QtWidgets import QMainWindow
from flyin.engine import Engine
from flyin.vars import Vars


class Widget(ABC):
    '''
    Class that represent a widget
    '''

    def __init__(
                self, x: int | float, y: int | float,
                width: int | float, height: int | float, title: str,
                window: QMainWindow, engine: Engine, vars: Vars
            ) -> None:
        '''
        Initialize the widget

        Args:
            x: int = The widget x start in %
            y: int = The widget y start in %
            width: int= The widget width in %
            height: int = The widget height in %
            title: str = The widget title
            window: QMainWindow = The window to draw
            painter: QPainter = The painter
        Return:
            None
        '''
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.title = title
        self.window = window
        self.engine = engine
        self.vars = vars

    def common_draw(self, painter: QPainter) -> None:
        '''
        Draw the common part of all the widgets

        Args:
            None
        Return:
            None
        '''
        gap: int = 10
        font_size: int = 15

        start_x: int = int(self.x * self.window.width() + gap)
        start_y: int = max([
            int(self.y * self.window.height() + gap),
            100
        ])

        end_x: int = int(start_x + (len(self.title) + 5) * 0.6 * font_size)

        self.engine.draw_rectangle(
            painter,
            start_x,
            start_y,
            int(self.width * self.window.width() - gap),
            int(self.height * self.window.height() - gap),
            1, QColor("white"), QColor(0, 0, 0, 0)
        )

        if end_x <= start_x + int(self.width * self.window.width() - gap):

            self.engine.draw_line(
                painter,
                start_x + 25, start_y, end_x, start_y,
                1, QColor("black")
            )

            self.engine.draw_rectangle(
                painter,
                start_x + 25,
                start_y - font_size,
                end_x - start_x - 25,
                2 * font_size,
                1, QColor("white"), QColor(0, 0, 0, 0)
            )

            self.engine.write_text(
                painter,
                start_x + 35, start_y + int(0.5 * font_size),
                self.title, QColor("white"), QFont("Arial", font_size)
            )

    @abstractmethod
    def draw(self, painter: QPainter) -> None:
        '''
        Draw the personal part

        Args:
            None
        Return:
            None
        '''
        self.common_draw(painter)
