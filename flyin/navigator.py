#!/usr/bin/env python3

from pathlib import Path
from typing import Any
from PyQt6.QtGui import QPainter, QColor, QFont, QPixmap
from PyQt6.QtWidgets import QMainWindow
from flyin.widget import Widget
from flyin.engine import Engine
from flyin.vars import Vars


class Navigator(Widget):
    '''
    Class for the navigator
    '''

    def __init__(
                self, x: int | float, y: int | float,
                width: int | float, height: int | float, title: str,
                window: QMainWindow, engine: Engine, vars: Vars
            ) -> None:
        super().__init__(x, y, width, height, title, window, engine, vars)

        self.icons: dict[str, str] = {
            "folder": "assets/icons/folder.svg"
        }

        self.files: list[dict[str, Any]] = self._init_files()
        self._pixmap_cache = {}
        self.hovered: str = ""

    def get_pixmap(self, path: str) -> QPixmap:
        '''
        Return the needed img

        Args:
            None
        Return:
            None
        '''
        if path not in self._pixmap_cache:
            self._pixmap_cache[path] = QPixmap(path).scaled(
                int(1.3 * self.window.font_size),
                int(1.3 * self.window.font_size)
            )
        return self._pixmap_cache[path]

    def _img_path(self, file) -> str:
        '''
        Return the path of the image
        corresponding to the file/directory

        Args:
            file = The needed image's file
        Return:
            res: str = The path to the image
        '''
        if file.is_dir():
            return "assets/icons/folder.svg"
        elif file.name == "Makefile":
            return "assets/icons/makefile.svg"
        return "assets/icons/" + file.suffix[1:] + ".svg"

    def _is_displayable(self, file: Path) -> bool:
        '''
        Return True is the file/folder is displayable

        Args:
            None
        Return:
            None
        '''
        parents = file.parents
        for f in self.files:
            for parent in parents:
                same_name: bool = f["name"] == parent.name
                is_dir_open: bool = f["is_dir"] and not f["is_open"]
                if same_name and is_dir_open:
                    return False

        return True

    def _init_files(self) -> list[dict[str, Any]]:
        '''
        Initializethe files

        Args:
            None
        Return:
            None
        '''
        res: list[dict[str, Any]] = list()
        root: Path = Path(".")
        files = [file for file in list(root.iterdir())[::-1]]
        to_skip: list[str] = [
            "__pycache__"
        ]

        while files != []:
            file = files.pop()
            temp: dict[str, Any] = {
                "file": file,
                "name": file.name,
                "img_path": self._img_path(file)
            }

            if file.name[0] == "." or file.name in to_skip:
                continue
            temp["is_dir"] = False
            if file.is_dir():
                temp["is_dir"] = True
                temp["is_open"] = True
                for f in list(file.iterdir())[::-1]:
                    files.append(f)

            temp["nb_tab"] = 0

            parent = list(filter(lambda f: f["name"] == file.parent.name, res))
            if parent != []:
                temp["nb_tab"] = parent[0]["nb_tab"] + 1

            res.append(temp)

        return res

    def _draw_tree(self, painter: QPainter) -> None:
        '''
        Draw the tree

        Args:
            painter: QPainter = The painter
        Return:
            None
        '''
        index: int = 0

        for file in self.files:

            temp_y: int = int(
                self.y * self.window.height() +
                index * self.window.font_size * 1.5 + 42
            )
            end_y: int = (self.y + self.height) * self.window.height()
            if temp_y >= int(end_y - self.window.font_size):
                break

            if self._is_displayable(file["file"]):

                if file["name"] == self.hovered:
                    self.engine.draw_rectangle(
                        painter,
                        int(
                            self.x * self.window.width() +
                            self.window.font_size + 2
                        ),
                        int(
                            self.y * self.window.height() +
                            index * self.window.font_size * 1.5 + 42
                        ),
                        int(
                            (self.x + self.width) * self.window.width() - 18
                        ),
                        int(self.window.font_size * 1.5), 1,
                        QColor(0, 0, 0, 0), QColor(245, 232, 130, 30)
                    )

                painter.drawPixmap(
                    int(
                        self.x * self.window.width() +
                        2 * self.window.font_size +
                        24 * file["nb_tab"]
                    ),
                    int(
                        self.y * self.window.height() +
                        index * self.window.font_size * 1.5 + 42
                    ),
                    self.get_pixmap(file["img_path"])
                )

                self.engine.write_text(
                    painter,
                    int(
                        self.x * self.window.width() +
                        3.5 * self.window.font_size +
                        24 * file["nb_tab"]
                    ),
                    int(
                        self.y * self.window.height() +
                        index * self.window.font_size * 1.5 + 55
                    ),
                    file["name"], QColor("white"),
                    QFont("Arial", self.window.font_size)
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
        self._draw_tree(painter)

    def mousePressEvent(self, event):
        '''
        Handle the mouse event

        Args:
            None
        Return:
            None
        '''
        displayed_files: list[str] = list()
        for file in self.files:
            if self._is_displayable(file["file"]):
                displayed_files.append(file)

        index: int = int(
            (event.pos().y() - (self.y * self.window.height() + 42))
            // (self.window.font_size * 1.5)
        )

        if index >= len(displayed_files):
            return

        for file in self.files:
            search_file = file["name"] == displayed_files[index]["name"]
            if search_file and file["is_dir"]:
                self.hovered = file["name"]
                file["is_open"] = not file["is_open"]
            elif search_file:
                self.hovered = file["name"]
                return file["file"]

        return ""

    def mouseMoveEvent(self, event):
        '''
        Handle the mouse event

        Args:
            None
        Return:
            None
        '''
        displayed_files: list[str] = list()
        for file in self.files:
            if self._is_displayable(file["file"]):
                displayed_files.append(file)

        index: int = int(
            (event.pos().y() - (self.y * self.window.height() + 42))
            // (self.window.font_size * 1.5)
        )

        if index >= len(displayed_files):
            return

        for file in self.files:
            search_file = file["name"] == displayed_files[index]["name"]
            if search_file and file["is_dir"]:
                self.hovered = file["name"]
            elif search_file:
                self.hovered = file["name"]
