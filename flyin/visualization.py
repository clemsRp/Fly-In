#!/usr/bin/env python3

from typing import TYPE_CHECKING, Any
from PyQt6.QtGui import QPainter, QColor, QFont, QFontMetrics, QPixmap
from PyQt6.QtCore import Qt
from flyin.widget import Widget
from flyin.graph import Node, Connection
from flyin.engine import Engine
from flyin.vars import Vars

if TYPE_CHECKING:
    from flyin.window import Window


class Visualization(Widget):
    '''
    Class for the visualization
    '''

    def __init__(
                self, x: int | float, y: int | float,
                width: int | float, height: int | float, title: str,
                window: "Window", engine: Engine, vars: Vars
            ) -> None:
        super().__init__(x, y, width, height, title, window, engine, vars)

        self.state: str = "neutral"
        self.display: str = "graph"
        self.img_ratio: int = 1
        self.index: int = 0
        self.content_lines: list[str] = []

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

        color: str = "orange"
        if node.color != "":
            color = node.color

        start_x: int = int(self.x * self.window.width())
        start_y: int = int(self.y * self.window.height())

        self.engine.draw_circle(
            painter,
            int(start_x + x), int(start_y + y), int(diameter * 0.7),
            2, QColor("white"), QColor(color)
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

    def _draw_error(self, painter: QPainter, error: str) -> None:
        '''
        Draw the error

        Args:
            painter: QPainter = The painter
        Return:
            None
        '''
        font: QFont = QFont("Arial", 25)
        metrics = QFontMetrics(font)

        text_width = metrics.horizontalAdvance(error)
        text_height = metrics.height()

        self.engine.write_text(
            painter,
            self.window.width() // 2 - 156,
            self.window.height() // 2 + text_height,
            "ERROR: Invalid map",
            QColor("red"), QFont("Arial", 25)
        )

        self.engine.write_text(
            painter,
            self.window.width() // 2 - text_width // 2,
            self.window.height() // 2 + 40 + text_height,
            error,
            QColor("red"), QFont("Arial", 25)
        )

    def keyPressEvent(self, move: str) -> None:
        '''
        Handle the user choices

        Args:
            None
        Return:
            None
        '''
        if move == "pause" and self.state not in ["pause", "working"]:
            return
        self.state = move

    def draw(self, painter: QPainter) -> None:
        '''
        Draw the personal part

        Args:
            None
        Return:
            None
        '''
        self.common_draw(painter)

        text: str = ""
        if self.window.error == "":
            if self.display == "graph":
                text = self.window.filename
            else:
                text = self.vars.vars["visu_file"]
            start_x: int = int((self.x + self.width) * self.window.width())
            start_y: int = int(self.y * self.window.height()) + 10

            font: QFont = QFont("Arial", self.window.font_size)

            metrics = QFontMetrics(font)

            text_width = metrics.horizontalAdvance(str(text)) + 25
            text_height = metrics.height()

            self.engine.draw_rectangle(
                painter,
                start_x - text_width, start_y,
                text_width, text_height * 2, 1,
                QColor("white"), QColor("white")
            )

            self.engine.write_text(
                painter,
                start_x - text_width + 12,
                int(start_y + self.window.font_size * 1.5) + 2,
                text,
                QColor("black"), font
            )

        if self.window.error != "":
            self._draw_error(painter, self.window.error)
        elif self.display == "graph":
            self._draw_visualization(painter)

            if self.state == "start":
                self._draw_start(painter)
            elif self.state == "end":
                self._draw_end(painter)
            elif self.state == "start":
                self._draw_start(painter)
            elif self.state == "start":
                self._draw_start(painter)
        elif self.display == "img":
            size: int = int(min([
                self.width * self.window.width(),
                self.height * self.window.height()
            ]) * 0.7)
            x: int = int(
                self.x * self.window.width() +
                (self.width * self.window.width()) // 2 -
                size * self.img_ratio // 2
            )
            y: int = int(
                self.y * self.window.height() +
                (self.height * self.window.height()) // 2 -
                size * self.img_ratio // 2
            )
            painter.drawPixmap(
                x, y,
                QPixmap(self.vars.vars["visu_file"]).scaled(
                    int(size * self.img_ratio),
                    int(size * self.img_ratio),
                    Qt.AspectRatioMode.KeepAspectRatio,
                    Qt.TransformationMode.SmoothTransformation
                )
            )
        else:
            with open(self.vars.vars["visu_file"], 'r') as f:
                self.content_lines = f.readlines()

                for k in range(self.index, len(self.content_lines)):
                    num: str = (3 - len(str(k))) * " " + str(k) + "   "

                    y: int = int(
                        (k - self.index) * self.window.font_size * 1.5 +
                        self.y * self.window.height() + 55
                    )

                    if y > (self.y + self.height) * self.window.height():
                        break

                    self.engine.write_text(
                        painter,
                        int(self.x * self.window.width() + 35),
                        int(
                            (k - self.index) * self.window.font_size * 1.5 +
                            self.y * self.window.height() + 55
                        ),
                        num + self.content_lines[k],
                        QColor("white"), QFont("Arial", self.window.font_size)
                    )

    def wheelEvent(self, event: Any) -> bool:
        '''
        Handle the mouse wheel

        Args:
            None
        Return:
            None
        '''
        if self.display == "graph":
            return False

        delta = event.angleDelta().y()

        if delta > 0:
            if self.display == "img":
                self.img_ratio = max([self.img_ratio - 0.1, 0.2])
            elif len(self.content_lines) > 35:
                self.index -= 1
                if self.index < 0:
                    self.index += 1

        elif delta < 0:
            if self.display == "img":
                self.img_ratio = min([self.img_ratio + 0.1, 1.1])
            elif len(self.content_lines) > 35:
                self.index += 1
                if self.index >= len(self.content_lines):
                    self.index -= 1

        return True

    def _draw_start(self, painter: QPainter) -> None:
        '''
        Draw the start

        Args:
            None
        Return:
            None
        '''
        pass

    def _draw_end(self, painter: QPainter) -> None:
        '''
        Draw the start

        Args:
            None
        Return:
            None
        '''
        pass
