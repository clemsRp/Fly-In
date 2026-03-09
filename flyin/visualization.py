#!/usr/bin/env python3

from PyQt6.QtGui import QPainter, QColor
from PyQt6.QtWidgets import QMainWindow
from flyin.widget import Widget
from flyin.graph import Node, Connection
from flyin.engine import Engine
from flyin.vars import Vars


class Visualization(Widget):
    '''
    Class for the visualization
    '''

    def __init__(
                self, x: int | float, y: int | float,
                width: int | float, height: int | float, title: str,
                window: QMainWindow, engine: Engine, vars: Vars
            ) -> None:
        super().__init__(x, y, width, height, title, window, engine, vars)

    def _draw_connection(
                self,
                painter: QPainter, connection: Connection,
                cell_x: int, cell_y: int
            ) -> None:
        '''
        Draw a connection inside the window

        Args:
            painter: QPainter = The painter
            connection: Connection = The connection to draw
            cell_x: int = The x size of a cell
            cell_y: int = The y size of a cell
        Return:
            None
        '''
        n1: Node = connection.start
        n2: Node = connection.end
        x1: int = int(cell_x // 2 + (n1.x + 0.5) * cell_x)
        y1: int = int(cell_y // 2 + (n1.y + 0.5) * cell_y)
        x2: int = int(cell_x // 2 + (n2.x + 0.5) * cell_x)
        y2: int = int(cell_y // 2 + (n2.y + 0.5) * cell_y)

        start_x: int = int(self.x * self.window.width())
        start_y: int = int(self.y * self.window.height())

        self.engine.draw_line(
            painter,
            int(start_x + x1), int(start_y + y1),
            int(start_x + x2), int(start_y + y2),
            1, QColor("white")
        )

    def _draw_node(
                self,
                painter: QPainter, node: Node,
                cell_x: int, cell_y: int
            ) -> None:
        '''
        Draw a connection inside the window

        Args:
            painter: QPainter = The painter
            connection: Connection = The connection to draw
            cell_x: int = The x size of a cell
            cell_y: int = The y size of a cell
        Return:
            None
        '''
        x: int = int(cell_x // 2 + (node.x + 0.5) * cell_x)
        y: int = int(cell_y // 2 + (node.y + 0.5) * cell_y)

        diameter: int = min([cell_x, cell_y])
        diameter = min([diameter, 150])

        x -= int(diameter * 0.7 / 2)
        y -= int(diameter * 0.7 / 2)

        content_color: str = "orange"
        if node.color != "":
            content_color = node.color

        border_color: str = content_color
        if self.vars.vars["start_hub"] == node:
            border_color = "red"
        if self.vars.vars["end_hub"] == node:
            border_color = "green"

        start_x: int = int(self.x * self.window.width())
        start_y: int = int(self.y * self.window.height())

        self.engine.draw_circle(
            painter,
            int(start_x + x), int(start_y + y), int(diameter * 0.7),
            2, QColor(border_color), QColor(content_color)
        )

    def _draw_visualization(
                self, painter: QPainter
            ) -> None:
        '''
        Draw the visualization

        Args:
            painter: QPainter = The painter
        Return:
            None
        '''
        mini = [1000000, 1000000]
        maxi = [-1000000, -1000000]

        for node in self.vars.vars["graph"].keys():
            if node.x < mini[0]:
                mini[0] = node.x
            if node.x > maxi[0]:
                maxi[0] = node.x
            if node.y < mini[1]:
                mini[1] = node.y
            if node.y > maxi[1]:
                maxi[1] = node.y

        cell_x: int = maxi[0] - mini[0] + 2
        cell_y: int = maxi[1] - mini[1] + 2

        cell_x = int(0.6 * self.window.width() // cell_x)
        cell_y = int((self.window.height() - 150) // cell_y)

        for liste in self.vars.vars["graph"].values():
            for (node, connection) in liste:
                self._draw_connection(
                    painter, connection, cell_x, cell_y
                )

        for node in self.vars.vars["graph"].keys():
            self._draw_node(
                painter, node, cell_x, cell_y
            )

    def draw(self, painter: QPainter) -> None:
        '''
        Draw the personal part

        Args:
            None
        Return:
            None
        '''
        self.common_draw(painter)
        self._draw_visualization(painter)
