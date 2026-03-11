#!/usr/bin/env python3

from pathlib import Path
from typing import Any, TYPE_CHECKING
from PyQt6.QtGui import QPainter, QColor, QFont, QPixmap
from PyQt6.QtCore import Qt
from flyin.widget import Widget
from flyin.engine import Engine
from flyin.vars import Vars

if TYPE_CHECKING:
    from flyin.window import Window


class Navigator(Widget):
    '''
    Class for the navigator
    '''

    def __init__(
                self, x: int | float, y: int | float,
                width: int | float, height: int | float, title: str,
                window: "Window", engine: Engine, vars: Vars
            ) -> None:
        super().__init__(x, y, width, height, title, window, engine, vars)

        self.icons: dict[str, str] = {
            "folder": "assets/icons/folder.svg"
        }

        self.files: list[dict[str, Any]] = self._init_files()
        self._pixmap_cache: dict[str, QPixmap] = {}
        self.hovered: int = 0
        self.mouse_y: int = 0
        self.index: int = 0

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

    def _img_path(self, file: Path) -> str:
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
        '''
        display_index: int = 0

        for file in self.files:
            if not self._is_displayable(file["file"]):
                continue

            pos_y: int = int(
                self.y * self.window.height() +
                display_index * self.window.font_size * 1.5 + 42 +
                self.mouse_y
            )

            view_top = int(self.y * self.window.height() + 25)
            view_bottom = int(
                (self.y + self.height) * self.window.height() -
                25
            )

            if view_top <= pos_y < view_bottom:
                cond: bool = self.hovered <= pos_y + 5 + int(
                    self.window.font_size * 1.5
                )
                if self.hovered >= pos_y + 5 and cond:
                    self.engine.draw_rectangle(
                        painter,
                        int(
                            self.x * self.window.width() +
                            self.window.font_size + 2
                        ),
                        pos_y + 5,
                        int((self.x + self.width) * self.window.width() - 18),
                        int(self.window.font_size * 1.5), 1,
                        QColor(0, 0, 0, 0), QColor(245, 232, 130, 30)
                    )

                painter.drawPixmap(
                    int(
                        self.x * self.window.width() +
                        2 * self.window.font_size + 24 * file["nb_tab"]
                    ),
                    pos_y + 3,
                    self.get_pixmap(file["img_path"])
                )

                self.engine.write_text(
                    painter,
                    int(
                        self.x * self.window.width() +
                        3.5 * self.window.font_size + 24 * file["nb_tab"]
                    ),
                    pos_y + int(self.window.font_size * 1.5),
                    file["name"], QColor("white"),
                    QFont("Arial", self.window.font_size)
                )

            display_index += 1
        self.index = display_index

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

    def mousePressEvent(self, event: Any) -> str | Path:
        '''
        Handle the mouse event

        Args:
            None
        Return:
            None
        '''
        if event.button() == Qt.MouseButton.LeftButton:
            displayed_files: list[dict[str, Any]] = list()
            for file in self.files:
                if self._is_displayable(file["file"]):
                    displayed_files.append(file)

            index: int = int(
                (event.pos().y() - (self.y * self.window.height() + 42) -
                 self.mouse_y)
                // (self.window.font_size * 1.5)
            )

            for file in self.files:
                search_file = file["name"] == displayed_files[index]["name"]
                if search_file and file["is_dir"]:
                    self.hovered = event.position().y()
                    file["is_open"] = not file["is_open"]
                elif search_file:
                    self.hovered = event.position().y()
                    return Path(file["file"])

            return "graph"

        elif event.button() == Qt.MouseButton.RightButton:
            displayed_files: list[dict[str, Any]] = list()
            for file in self.files:
                if self._is_displayable(file["file"]):
                    displayed_files.append(file)

            index: int = int(
                (event.pos().y() - (self.y * self.window.height() + 42) -
                 self.mouse_y)
                // (self.window.font_size * 1.5)
            )

            for file in self.files:
                search_file = file["name"] == displayed_files[index]["name"]
                if search_file and file["is_dir"]:
                    self.hovered = event.position().y()
                    file["is_open"] = not file["is_open"]
                elif search_file:
                    self.hovered = event.position().y()
                    return Path(file["file"])

            return "graph"

    def wheelEvent(self, event: Any) -> bool:
        '''
        Handle the mouse wheel

        Args:
            None
        Return:
            None
        '''
        liste: list[dict[str, Any]] = [
            f for f in self.files if self._is_displayable(f["file"])
        ]
        if len(liste) // self.window.font_size >= 35:
            return False

        delta = event.angleDelta().y()

        val: int = -int(
            self.window.font_size * 1.5 * (self.index + 5) -
            (self.x + self.height) * self.window.height()
        )

        cond1: bool = self.mouse_y < 0
        cond2: bool = self.mouse_y >= val

        if delta > 0 and cond1:
            self.mouse_y += int(self.window.font_size * 3)
        elif delta < 0 and cond2:
            self.mouse_y -= int(self.window.font_size * 3)
        return True

    def mouseMoveEvent(self, event: Any) -> None:
        '''
        Handle the mouse event

        Args:
            None
        Return:
            None
        '''
        displayed_files: list[dict[str, Any]] = list()
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
                self.hovered = event.pos().y()
            elif search_file:
                self.hovered = event.pos().y()
