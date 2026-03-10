#!/usr/bin/env python3

from PyQt6.QtGui import QFont, QColor, QPainter, QPen, QBrush, QFontMetrics
from typing import Any


class Engine:
    '''
    Class used to draw inside a given window
    '''

    def __init__(self, window: Any) -> None:
        '''
        Initialize the engine

        Args:
            None
        Return:
            None
        '''
        self.window = window

    def write_text(
                self, painter: QPainter,
                x: int, y: int, text: str,
                color: QColor, font: QFont
            ) -> None:
        '''
        Write some text inside the window

        Args:
            painter: QPainter = The painter
            x: int = The x start of te text
            y: int = The y start of te text
            text: str = The text to write
            color: QColor = The text color
            font: QFont = The text font
        Return:
            None
        '''
        painter.setFont(font)
        painter.setPen(color)
        painter.drawText(x, y, text)

    def draw_line(
                self, painter: QPainter,
                x1: int, y1: int, x2: int, y2: int,
                pen_width: int, color: QColor
            ) -> None:
        '''
        Draw a line inside a window

        Args:
            painter: QPainter = The painter
            x1: int = The x start
            y1: int = The y start
            x2: int = The x end
            y2: int = The y end
            pen_width: int = The pen width
            color: QColor = The line color
        Return:
            None
        '''
        pen = QPen(color, pen_width)
        painter.setPen(pen)
        painter.drawLine(x1, y1, x2, y2)

    def draw_rectangle(
                self, painter: QPainter,
                x: int, y: int, width: int, height: int, pen_width: int,
                border_color: QColor, content_color: QColor
            ) -> None:
        '''
        Draw a rectangle inside a window

        Args:
            painter: QPainter = The painter
            x: int = The x start
            y: int = The y start
            width: int = The rectangle width
            height: int = The rectangle height
            pen_width: int = The pen width
            border_color: QColor = The color of the border
            content_color: QColor = The color of the content
        Return:
            None
        '''
        pen: QPen = QPen(border_color, pen_width)
        painter.setPen(pen)

        brush: QBrush = QBrush(content_color)
        painter.setBrush(brush)

        painter.drawRect(x, y, width, height)

    def draw_circle(
                self, painter: QPainter,
                x: int, y: int, diameter: int, pen_width: int,
                border_color: QColor, content_color: QColor
            ) -> None:
        '''
        Draw a circle inside a window

        Args:
            painter: QPainter = The painter
            x: int = The x
            y: int = The y
            diameter: int = The diameter
            pen_width: int = The pen width
            border_color: QColor = The color of the border
            content_color: QColor = The color of the content
        Return:
            None
        '''
        pen: QPen = QPen(border_color, pen_width)
        painter.setPen(pen)

        brush: QBrush = QBrush(content_color)
        painter.setBrush(brush)

        # Pour un cercle, width et height doivent être identiques
        painter.drawEllipse(x, y, diameter, diameter)

    def draw_button(
                self, painter: QPainter,
                x: int, y: int, text: str,
                font_size: int,
                border_color: QColor, content_color: QColor,
                width: int = -1
            ) -> None:
        '''
        Draw a button

        Args:
            None
        Return:
            None
        '''
        font: QFont = QFont("Arial", font_size)
        metrics: QFontMetrics = QFontMetrics(font)

        text_width: int = metrics.horizontalAdvance(text)
        if width != -1:
            text_width = width
        self.draw_line(
            painter,
            x, y,
            x + int(text_width + 1.5 * font_size),
            y,
            1, content_color
        )

        self.draw_rectangle(
            painter,
            x,
            y - font_size,
            int(text_width + 1.5 * font_size),
            2 * font_size,
            1, border_color, content_color
        )

        self.write_text(
            painter,
            int(x + font_size * 0.75),
            int(y + font_size * 0.5),
            text, border_color, font
        )
