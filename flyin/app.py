#!/usr/bin/env python3

import sys
from pathlib import Path
from typing import List, Tuple, Any
from PyQt6.QtWidgets import QMainWindow, QApplication
from PyQt6.QtWidgets import QWidget
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QColor, QPainter, QPen, QBrush, QPixmap
from flyin.vars import Vars
from flyin.graph import Node, Connection


class MyWidget(QWidget):
    def __init__(
                self, width: int, height: int,
                func, color: str = "red",
                parent: Any = None
            ) -> None:
        '''
        Initialize the widget

        Args:
            width: int = The widget width
            height: int = The widget height
            color: str = The widget color
            parent: Any = The widget parent
        Return:
            None
        '''
        super().__init__(parent)
        self.parent = parent
        self.width = width
        self.height = height
        self.func = func
        self.color = color
        self.setFixedSize(width, height)

    def paintEvent(self, event):
        painter = QPainter(self)

        self.parent.engine.draw_rectangle(
            painter,
            0, 0, self.width, self.height, 1,
            QColor("white"), QColor(0, 0, 0, 0)
        )

        self.func(self, painter)


class Window(QMainWindow):
    '''
    Class used to manage the app and the event
    '''

    def __init__(self, vars: Vars) -> None:
        '''
        Initialize the app
        '''
        super().__init__()

        screen = QApplication.primaryScreen()
        size = screen.size()
        self.win_width: int = size.width()
        self.win_height: int = size.height() - 150

        self.vars: Vars = vars

        super().setWindowTitle("Tobikomu")
        super().resize(self.win_width, self.win_height)

        self.img_paths = {
                ".py": QPixmap("assets/icons/py.svg").scaled(
                    15, 15,
                    Qt.AspectRatioMode.KeepAspectRatio,
                    Qt.TransformationMode.SmoothTransformation
                ),
                ".txt": QPixmap("assets/icons/txt.svg").scaled(
                    15, 15,
                    Qt.AspectRatioMode.KeepAspectRatio,
                    Qt.TransformationMode.SmoothTransformation
                ),
                "folder": QPixmap("assets/icons/folder.svg").scaled(
                    15, 15,
                    Qt.AspectRatioMode.KeepAspectRatio,
                    Qt.TransformationMode.SmoothTransformation
                ),
                ".svg": QPixmap("assets/icons/svg.svg").scaled(
                    15, 15,
                    Qt.AspectRatioMode.KeepAspectRatio,
                    Qt.TransformationMode.SmoothTransformation
                ),
                "makefile": QPixmap("assets/icons/makefile.svg").scaled(
                    15, 15,
                    Qt.AspectRatioMode.KeepAspectRatio,
                    Qt.TransformationMode.SmoothTransformation
                ),
                ".md": QPixmap("assets/icons/md.svg").scaled(
                    15, 15,
                    Qt.AspectRatioMode.KeepAspectRatio,
                    Qt.TransformationMode.SmoothTransformation
                ),
                ".toml": QPixmap("assets/icons/toml.svg").scaled(
                    15, 15,
                    Qt.AspectRatioMode.KeepAspectRatio,
                    Qt.TransformationMode.SmoothTransformation
                ),
                "logo": QPixmap("assets/icons/logo.png").scaled(
                    200, 100,
                    Qt.AspectRatioMode.KeepAspectRatio,
                    Qt.TransformationMode.SmoothTransformation
                ),
                ".png": QPixmap("assets/icons/png.svg").scaled(
                    15, 15,
                    Qt.AspectRatioMode.KeepAspectRatio,
                    Qt.TransformationMode.SmoothTransformation
                ),
                ".lock": QPixmap("assets/icons/lock.svg").scaled(
                    15, 15,
                    Qt.AspectRatioMode.KeepAspectRatio,
                    Qt.TransformationMode.SmoothTransformation
                )
            }

        self.engine: Engine = Engine(self)

    def show(self) -> None:
        '''
        Execute the window
        '''
        super().show()

    def paintEvent(self, event) -> None:
        '''
        Manage the events

        Args:
            None
        Return:
            None
        '''
        painter = QPainter(self)

        self.engine.draw_rectangle(
            painter,
            0, 0, self.win_width, self.win_height, 5,
            QColor("black"), QColor("black")
        )

        painter.drawPixmap(
            self.win_width // 2 - 100, 15,
            self.img_paths["logo"]
        )

    def _draw_tree(self, painter: QPainter, root_folder: str = ".") -> None:
        '''
        Draw the file tree

        Args:
            None
        Return:
            None
        '''
        line: int = 12
        nb_line: int = 1

        root: Path = Path(root_folder).resolve()
        ignore_list: List[str] = ["__pycache__", ".venv"]

        for element in sorted(root.rglob('*')):

            relative_path: Path = element.relative_to(root)
            parties: Tuple[Any] = relative_path.parts

            if any(p.startswith('.') for p in parties):
                continue

            if any(p in ignore_list for p in parties):
                continue

            deep: int = len(parties) - 1
            indentation: str = "    " * deep

            y_pos = int(line + line * nb_line * 1.5)
            x_pos = line + (deep * 20)
            prefixe = "     "

            if element.name == "Makefile":
                painter.drawPixmap(
                    x_pos, y_pos - line,
                    self.img_paths["makefile"]
                )

            elif element.is_file() and element.suffix in self.img_paths:
                painter.drawPixmap(
                    x_pos, y_pos - line,
                    self.img_paths[element.suffix]
                )

            elif element.is_dir():
                painter.drawPixmap(
                    x_pos, y_pos - line,
                    self.img_paths["folder"]
                )

            text: str = f"{indentation}{prefixe}{element.name}"

            self.engine.write_text(
                painter,
                line, y_pos,
                text, QColor("white"), QFont("Arial", line)
            )

            nb_line += 1

    def _draw_file_navigator(
                self, widget: QWidget, painter: QPainter
            ) -> None:
        '''
        Draw the file navigator

        Args:
            painter: QPainter = The painter
        Return:
            None
        '''
        self._draw_tree(painter)

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

        self.engine.draw_line(
            painter,
            x1, y1, x2, y2,
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

        self.engine.draw_circle(
            painter,
            x, y, int(diameter * 0.7),
            2, QColor(border_color), QColor(content_color)
        )

    def _draw_visualization(
                self, widget: QWidget, painter: QPainter
            ) -> None:
        '''
        Draw the visualization

        Args:
            painter: QPainter = The painter
        Return:
            None
        '''
        mini = [float("inf"), float("inf")]
        maxi = [-float("inf"), -float("inf")]

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

        cell_x = int(0.6 * self.win_width // cell_x)
        cell_y = int((self.win_height - 150) // cell_y)

        for liste in self.vars.vars["graph"].values():
            for (node, connection) in liste:
                self._draw_connection(
                    painter, connection, cell_x, cell_y
                )

        for node in self.vars.vars["graph"].keys():
            self._draw_node(
                painter, node, cell_x, cell_y
            )

    def _draw_stats(
                self, widget: QWidget, painter: QPainter
            ) -> None:
        '''
        Draw the stats

        Args:
            painter: QPainter = The painter
        Return:
            None
        '''
        pass


class Engine:
    '''
    Class used to draw inside a given window
    '''

    def __init__(self, window) -> None:
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


class App(QApplication):
    '''
    Class used to manage the app and the event
    '''

    def __init__(self, vars: Vars) -> None:
        '''
        Initialize the App

        Args:
            None
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
