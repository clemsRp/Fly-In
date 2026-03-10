#!/usr/bin/env python3

from PyQt6.QtGui import QPixmap, QPainter


class Drone:
    '''
    Class that represent a drone
    '''

    def __init__(
                self, x: int, y: int, img_path: str,
            ) -> None:
        '''
        Initialize the drone

        Args:
            None
        Return:
            None
        '''
        self.x: int = x
        self.y: int = y
        self.img: QPixmap = QPixmap(img_path).scaled(75, 75)

    def draw(self, painter: QPainter) -> None:
        '''
        Draw the drone

        Args:
            None
        Return:
            None
        '''
        painter.drawPixmap(
            self.x, self.y,
            self.img
        )
