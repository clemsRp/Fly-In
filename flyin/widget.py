#!/usr/bin/env python3

from pathlib import Path
from typing import Any, TYPE_CHECKING
from abc import abstractmethod, ABC
from PyQt6.QtGui import QPainter, QColor, QFont, QFontMetrics
from flyin.engine import Engine
from flyin.vars import Vars

if TYPE_CHECKING:
    from flyin.window import Window


class Widget(ABC):
    '''
    Class that represent a widget
    '''

    def __init__(
                self, x: int | float, y: int | float,
                width: int | float, height: int | float, title: str,
                window: "Window", engine: Engine, vars: Vars
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
        self.display: str = ""
        self.index = 0
        self.hovered: Any = None

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
        font: QFont = QFont("Arial", font_size)
        metrics: QFontMetrics = QFontMetrics(font)

        text_width: int = metrics.horizontalAdvance(self.title)
        end_x: int = int(start_x + text_width)

        self.engine.draw_rectangle(
            painter,
            start_x,
            start_y,
            int(self.width * self.window.width() - gap),
            int(self.height * self.window.height() - gap),
            1, QColor("white"), QColor("#031035")
        )

        self.engine.draw_rectangle(
            painter,
            start_x - gap + 1,
            start_y,
            gap - 2,
            int(self.height * self.window.height() - gap),
            1, QColor("#031035"), QColor("#031035")
        )

        self.engine.draw_rectangle(
            painter,
            int((self.x + self.width) * self.window.width() + 1),
            start_y,
            gap,
            int(self.height * self.window.height() - gap),
            1, QColor("#031035"), QColor("#031035")
        )

        if end_x <= start_x + int(self.width * self.window.width() - gap):

            self.engine.draw_button(
                painter,
                start_x + 25, start_y,
                self.title, font_size,
                QColor("white"), QColor("#031035")
            )

    def wheelEvent(self, event: Any) -> bool:
        return True

    def mousePressEventLeft(self, event: Any) -> str | Path:
        return ""

    def mousePressEventRight(self, event: Any) -> str | Path:
        return ""

    def mouseMoveEvent(self, event: Any) -> Any:
        pass

    def keyPressEvent(self, move: str) -> None:
        pass

    def display_datas(res) -> None:
        pass

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
