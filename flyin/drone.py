#!/usr/bin/env python3

from typing import TYPE_CHECKING
from PyQt6.QtGui import QMovie

if TYPE_CHECKING:
    from flyin.window import Window


class Drone:
    '''
    Class that represent a drone
    '''

    def __init__(
                self, window: "Window", x: int, y: int
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
        self.drone: QMovie = QMovie("assets/drone.gif")
        self.drone.frameChanged.connect(window.update)
        self.drone.start()
