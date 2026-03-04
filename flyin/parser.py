#!/usr/bin/env python3

import re
from typing import List, Dict, Tuple, Any
from flyin.graph import Node, Connection, Graph


class Parser:
    '''
    Class that parse a given file into a graph
    '''

    def __init__(self, filename: str) -> None:
        '''
        Initialize the parser

        Args:
            filename: str = The file's name to parse
        Return:
            None
        '''
        self.lines: List[str] = list()
        with open(filename, 'r') as f:
            content: str = f.read()
            brut_lines: List[str] = content.split("\n")
            for line in brut_lines:
                if line == "" or line[0] == "#":
                    continue
                elif "#" in line:
                    self.lines.append(line.split("#")[0])
                else:
                    self.lines.append(line)

            for line in self.lines:
                print(line)

    def _get_optional_data_line(self, option_string: str) -> Dict[str, str]:
        '''
        Return a dict corresponding to the optional parameters

        Args:
            option_string: str = The optional parameters
        Return:
            res: Dict[str, str] = The parsed optional parameters
        '''
        if not option_string:
            return {}

        return dict(re.findall(r"(\w+)\s*=\s*([^\s]+)", option_string))

    def _get_data_line(self, line: str) -> Dict[str, str]:
        '''
        Return a dict corresponding to the parameters of the node

        Args:
            line: str = The current line to parse
        Return:
            res: Dict[str, str] = The parsed parameters
        '''
        pattern = r"(\w+):\s+(\S+)\s+(-?\d+)\s+(-?\d+)(?:\s+\[(.*?)\])?"

        m = re.search(pattern, line)

        print(m)

        if not m:
            return None

        node_type = m.group(1)
        name = m.group(2)
        x = int(m.group(3))
        y = int(m.group(4))
        options_str = m.group(5)

        return {
            "type": node_type,
            "name": name,
            "x": x,
            "y": y,
            "options": self._parse_options(options_str)
        }

    def parser(self) -> Dict[Node, List[Tuple[Node, Connection]]]:
        '''
        Return the graph created with the parsed datas

        Args:
            None
        Return:
            graph: Dict[Node, List[Tuple[Node, Connection]]] =
                The final graph
        '''
        res: Dict[str, Any] = dict()

        graph: Graph = Graph()
        for line in self.lines:
            try:
                info_type = line.split(" ")[0]
                if info_type in ["start_hub:", "hub:", "end_hub:"]:
                    node: Node = Node(

                    )
                    if info_type == "start_hub:":
                        if "start_hub" in res.keys():
                            raise ValueError("Too many start_hub")
                        res["start_hub"] = node
                    elif info_type == "end_hub:":
                        if "end_hub" in res.keys():
                            raise ValueError("Too many end_hub")
                        res["end_hub"] = node
            except Exception:
                raise ValueError(f"Invalid line: '{line}'")
