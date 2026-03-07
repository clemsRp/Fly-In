#!/usr/bin/env python3

from flyin.app import App
from flyin.parser import Parser


if __name__ == "__main__":
    try:
        # parser = Parser("maps/hard/03_ultimate_challenge.txt")
        parser = Parser("maps/easy/01_linear_path.txt")
        vars = parser.parser()

        app: App = App(vars)
        app.launch()

    except Exception as e:
        print(e)
