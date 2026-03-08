#!/usr/bin/env python3

from typing import Any
from PyQt6.QtGui import QColor, QPainter, QPixmap
from PyQt6.QtWidgets import QMainWindow
from PyQt6.QtCore import Qt
from flyin.vars import Vars
from flyin.widget import Widget
from flyin.navigator import Navigator
from flyin.visualization import Visualization
from flyin.stats import Stats


class Window(QMainWindow):
    '''
    Class used to manage the app and the event
    '''

    def __init__(self, vars: Vars) -> None:
        '''
        Initialize the app
        '''
        super().__init__()

        from flyin.engine import Engine

        self.engine: Engine = Engine(self)
        self.vars: Vars = vars

        super().setWindowTitle("Tobikomu")
        super().resize(self.width(), self.height())

        self.setMinimumSize(800, 600)

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
                0.8, 0.2, 0.2, 0.75, "Stats",
                self, self.engine, self.vars
            )
        ]

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
            QColor("black"), QColor("black")
        )

        size: int = (self.width() + self.height()) // 2

        logo: QPixmap = QPixmap("assets/icons/logo.png").scaled(
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
