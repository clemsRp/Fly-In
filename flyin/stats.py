#!/usr/bin/env python3

from typing import TYPE_CHECKING, Any
from PyQt6.QtGui import QPainter, QColor, QFont
from flyin.widget import Widget
from flyin.engine import Engine
from flyin.vars import Vars
from flyin.graph import Node, Connection

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

        self.hovered: Any = None

    def _draw_hover(self, painter: QPainter) -> None:
        '''
        Draw the hovered element

        Args:
            None
        Return:
            None
        '''
        if self.hovered is None:
            return

        if isinstance(self.hovered, Node):
            node: Node = self.hovered
            datas = {
                "name": node.name,
                "coor": str((node.x, node.y)),
                "zone": node.zone,
                "max_drones": str(node.max_drones)
            }

        else:
            c: Connection = self.hovered
            datas = {
                "start": c.start.name,
                "start coor": str((c.start.x, c.start.y)),
                "end": c.end.name,
                "end coor": str((c.end.x, c.end.y)),
                "max_link_capacity": str(c.max_link_capacity)
            }

        index: int = 0

        x: int = int(self.x * self.window.width() + 25)
        y: int = int(self.y * self.window.height() + 50)

        for (key, val) in datas.items():
            self.engine.write_text(
                painter,
                x, int(y + index * 1.5 * self.window.font_size),
                key + ": " + val,
                QColor("white"), QFont("Arial", self.window.font_size)
            )
            index += 1

    def draw(self, painter: QPainter) -> None:
        '''
        Draw the personal part

        Args:
            None
        Return:
            None
        '''
        self.common_draw(painter)

        self._draw_hover(painter)
