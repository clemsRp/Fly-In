#!/usr/bin/env python3

from typing import KeysView, ValuesView, ItemsView, Any


class Vars:
    '''
    Class that stock all the variables
    '''

    def __init__(self) -> None:
        '''
        Initialize the class
        '''
        self.vars: dict[str, Any] = dict()

    def set_variable(self, key: str, value: Any) -> None:
        '''
        Set a variable value in the Vars class

        Args:
            key: str = The given key
            value: Any = The given value
        Return:
            None
        '''
        self.vars[key] = value

    def get_keys(self) -> KeysView[str]:
        '''
        Return the variables keys

        Args:
            None
        Return:
            res: KeysView = The variables keys
        '''
        return self.vars.keys()

    def get_values(self) -> ValuesView[Any]:
        '''
        Return the variables values

        Args:
            None
        Return:
            res:ValuesView = The variables values
        '''
        return self.vars.values()

    def get_items(self) -> ItemsView[str, Any]:
        '''
        Return the variables items

        Args:
            None
        Return:
            res: ItemsView = The variables items
        '''
        return self.vars.items()
