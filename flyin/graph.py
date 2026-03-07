#!/usr/bin/env python3

import re
from typing import Dict


class Node:
    '''
    Class representing a node inside a graph

    Args:
        None
    Return:
        None
    '''

    def __init__(
                self, name: str, x: int, y: int,
                zone: str, color: str, max_drones: int
            ) -> None:
        '''
        Initialize a Node

        Args;
            name: str = The name of the node
            x: int = X coordinate of the node
            y: int = Y coordinate of the node
            zone: str = The node's zone type
            color: str = The node's color
            max_drones: int = The max number of drones possible in the node
        Return:
            None
        '''

        if " " in name or "-" in name:
            raise ValueError(f"Invalid name: '{name}'")
        elif zone not in ["normal", "blocked", "restricted", "priority"]:
            raise ValueError(f"Invalid zone type: '{zone}'")
        elif not re.fullmatch('^[a-z]+$', color):
            raise ValueError(f"Invalid color: '{color}'")
        elif max_drones < 1:
            raise ValueError(f"Invalid max_drones: '{max_drones}'")

        self.name: str = name
        self.x: int = x
        self.y: int = y
        self.zone: str = zone
        self.color: str = color
        self.max_drones: int = max_drones

    def __str__(self) -> str:
        '''
        Definition of how to print a node
        '''
        color: str = self.color
        if self.color == "":
            color = "None"
        return f"""
        +-----------------------+
        | NODE: {self.name}\t\t|
        +-----------------------+
        | Pos\t: ({self.x}, {self.y})\t|
        | Zone\t: {self.zone}\t|
        | Color\t: {color}\t\t|
        | Drones: {self.max_drones}\t\t|
        +-----------------------+
        """

    def __repr__(self) -> str:
        '''
        Definition of how to print a node
        '''
        return self.__str__()

    def __eq__(self, node) -> bool:
        '''
        Compare 2 nodes

        Args:
            node: Node = The compared node
        Return:
            res: bool = The result of the comparaison
        '''
        return self.name == node.name

    def __hash__(self) -> int:
        '''
        Hash the node object

        Args:
            None
        Return:
            res: int = The hash
        '''
        return hash((self.x, self.y))


class Connection:
    '''
    Class representing a connection between 2 nodes inside a graph
    '''

    def __init__(
                self, node1: Node, node2: Node,
                max_link_capacity: int
            ) -> None:
        '''
        Initialize a connection

        Args:
            node1: Node = The starting node
            node2: Node = The ending node
            max_link_capacity: int = The max number of drones possible
        Return:
            None
        '''

        if max_link_capacity < 1:
            raise ValueError(
                f"Invalid max_link_capacity: '{max_link_capacity}'"
            )

        self.start: Node = node1
        self.end: Node = node2
        self.max_link_capacity: int = max_link_capacity

    def __str__(self) -> str:
        '''
        Definition of how to print a connection
        '''
        import textwrap
        content: str = f"""
        [LINK] {self.start.name} <---> {self.end.name}
               Capacity: {self.max_link_capacity} drones
        """
        return textwrap.dedent(content).strip()

    def __repr__(self) -> str:
        '''
        Definition of how to print a connection
        '''
        return self.__str__()


class Graph(Dict):
    '''
    Class representing a graph using nodes and connections
    '''

    def __init__(self) -> None:
        '''
        Initiliaze the graph

        Args:
            None
        Return:
            None
        '''
        super().__init__()

    def add_node(
                self, name: str, x: int, y: int,
                zone: str, color: str, max_drones: int
            ) -> None:
        '''
        Add a node to the graph

        Args:
            name: str = The name of the node
            x: int = X coordinate of the node
            y: int = Y coordinate of the node
            zone: str = The node's zone type
            color: str = The node's color
            max_drones: int = The max number of drones possible in the node
        Return:
            None
        '''
        for node in self.keys():
            if node.name == name:
                raise ValueError(name + " is already a node")

        new_node: Node = Node(name, x, y, zone, color, max_drones)
        self[new_node] = list()

    def add_connection(
                self, node1: Node, node2: Node,
                max_link_capacity: int
            ) -> None:
        '''
        Add a connection to the graph

        Args:
            node1: Node = The starting node
            node2: Node = The ending node
            max_link_capacity: int = The max number of drones possible
        Return:
            None
        '''
        if node1.name == node2.name:
            raise ValueError("Start node and end node must be different nodes")

        for (node, connect) in self.items():
            cond1 = any(node2.name == n[0].name for n in connect)
            cond2 = any(node1.name == n[0].name for n in connect)

            if node1.name == node.name and cond1:
                raise ValueError(
                    f"{node1.name}-{node2.name} is already a connection"
                )
            elif node2.name == node.name and cond2:
                raise ValueError(
                    f"{node2.name}-{node1.name} is already a connection"
                )

        new_connection1: Connection = Connection(
            node1, node2, max_link_capacity
        )
        new_connection2: Connection = Connection(
            node2, node1, max_link_capacity
        )

        self[node1].append((node2, new_connection1))
        self[node2].append((node1, new_connection2))
