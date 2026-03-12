#!/usr/bin/env python3

from pathlib import Path
from typing import Any
from PyQt6.QtGui import QColor, QPainter, QPixmap
from PyQt6.QtWidgets import QMainWindow
from PyQt6.QtCore import Qt
from flyin.vars import Vars
from flyin.widget import Widget
from flyin.navigator import Navigator
from flyin.visualization import Visualization
from flyin.stats import Stats
from flyin.drone import Drone
from flyin.parser import Parser


class Window(QMainWindow):
    '''
    Class used to manage the app and the event
    '''

    def __init__(self) -> None:
        '''
        Initialize the app
        '''
        super().__init__()
        super().setWindowTitle("Tobikomu")
        super().resize(1920, 925)
        self.setMinimumSize(800, 600)
        self.setMouseTracking(True)

        from flyin.engine import Engine

        self.engine: Engine = Engine(self)
        self.parser: Parser = Parser()
        self.error: str = ""

        try:
            self.filename: str = "maps/challenger/01_the_impossible_dream.txt"
            self.vars: Vars = self.parser.parser(self.filename)
        except Exception as e:
            self.error = str(e)

        self.widgets: list[Widget] = [
            Navigator(
                0, 0.2, 0.2, 0.75, "Navigator",
                self, self.engine, self.vars
            ),
            Visualization(
                0.2, 0.2, 0.6, 0.75, "Visualization",
                self, self.engine, self.vars
            ),
            Stats(
                0.8, 0.2, 0.195, 0.75, "Stats",
                self, self.engine, self.vars
            )
        ]

        self.drones: list[Drone] = []

        self.font_size: int = 12

    def keyPressEvent(self, event: Any) -> None:
        '''
        Handle the key event

        Args:
            None
        Return:
            None
        '''
        if event.key() == Qt.Key.Key_S:
            self.widgets[1].keyPressEvent("start")
        elif event.key() == Qt.Key.Key_E:
            self.widgets[1].keyPressEvent("end")
        elif event.key() == Qt.Key.Key_P:
            self.widgets[1].keyPressEvent("pas")
        elif event.key() == Qt.Key.Key_A:
            self.widgets[1].keyPressEvent("animation")
        elif event.key() == Qt.Key.Key_W:
            self.widgets[1].keyPressEvent("pause")

    def wheelEvent(self, event: Any) -> None:
        '''
        Handle the mouse wheel

        Args:
            None
        Return:
            None
        '''
        x: int = event.position().x()
        y: int = event.position().y()

        if x <= int(0.2 * self.width()) and y >= int(0.2 * self.height()):
            if self.widgets[0].wheelEvent(event):
                self.update()

        elif x <= int(0.8 * self.width()) and y >= int(0.2 * self.height()):
            if self.widgets[1].wheelEvent(event):
                self.update()

    def mousePressEvent(self, event: Any) -> None:
        '''
        Handle the mouse event

        Args:
            None
        Return:
            None
        '''
        x: int = event.pos().x()
        y: int = event.pos().y()

        if x <= int(0.2 * self.width()) and y >= int(0.2 * self.height()):
            if event.button() == Qt.MouseButton.LeftButton:
                res: str | Path = self.widgets[0].mousePressEventLeft(
                    event
                )
                if res != "":
                    self.error = ""
                    try:
                        self.filename = str(res)
                        self.vars = self.parser.parser(str(self.filename))

                        self.widgets[1] = Visualization(
                            0.2, 0.2, 0.6, 0.75, "Visualization",
                            self, self.engine, self.vars
                        )

                    except Exception as e:
                        self.error = str(e)

            elif event.button() == Qt.MouseButton.RightButton:
                res: str | Path = self.widgets[0].mousePressEventRight(
                    event
                )
                if res != "":
                    self.error = ""
                    try:
                        if res.suffix in [".svg", ".png"]:
                            self.widgets[1].display = "img"
                        else:
                            self.widgets[1].display = "txt"
                            self.widgets[1].index = 0
                        self.vars.vars["visu_file"] = str(res)

                    except Exception as e:
                        self.error = str(e)

        self.update()

    def mouseMoveEvent(self, event: Any) -> None:
        '''
        Handle the mouse event

        Args:
            None
        Return:
            None
        '''
        x: int = event.pos().x()
        y: int = event.pos().y()

        if x <= int(0.2 * self.width()) and y >= int(0.2 * self.height()):
            self.widgets[0].mouseMoveEvent(event)

        self.update()

    def paintEvent(self, event: Any) -> None:
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
            0, 0, self.width(), self.height(), 5,
            QColor("#031035"), QColor("#031035")
        )

        size: int = (self.width() + self.height()) // 2

        logo: QPixmap = QPixmap("assets/logo.png").scaled(
            int(size * 0.15), int(size * 0.075),
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation
        )

        painter.drawPixmap(
            int(0.45 * self.width()),
            int(0.045 * self.height()),
            logo
        )

        for widget in self.widgets:
            widget.draw(painter)

        for drone in self.drones:
            drone.draw(painter)
