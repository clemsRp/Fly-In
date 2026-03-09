#!/usr/bin/env python3

from flyin.app import App


if __name__ == "__main__":
    try:
        app: App = App()
        app.launch()

    except Exception as e:
        print(e)
