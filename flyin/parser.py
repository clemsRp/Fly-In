#!/usr/bin/env python3

import re
from typing import List, Dict, Any
from flyin.vars import Vars
from flyin.graph import Node, Graph


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

    def _get_hub_option(self, option_string: str) -> Dict[str, str]:
        '''
        Return a dict corresponding to the optional parameters

        Args:
            option_string: str = The optional parameters
        Return:
            res: Dict[str, str] = The parsed optional parameters
        '''
        if not option_string:
            return {}

        return dict(
            re.findall(
                r"(color|zone|max_drones)=([^\s\]]+)",
                option_string
            )
        )

    def _get_hub(self, line: str, info_type: str) -> Dict[str, str]:
        '''
        Return a dict corresponding to the parameters of the node

        Args:
            line: str = The current line to parse
        Return:
            res: Dict[str, str] = The parsed parameters
        '''
        mandatory: str = r" ([^\s\-]+) (\-?[0-9]+) (\-?[0-9]+)"
        option: str = r"\s?(\[.+\])?"
        pattern = info_type + mandatory + option

        m = re.search(pattern, line)

        if not m:
            raise ValueError(f"Invalid line: '{line}'")

        name: str = m.group(1)
        x: int = int(m.group(2))
        y: int = int(m.group(3))
        options_str: str = m.group(4)

        options: Dict[str, str] = self._get_hub_option(options_str)

        res: Dict[str, Any] = {
            "name": name,
            "x": x,
            "y": y
        }

        # Zone
        if "zone" in options.keys():
            res["zone"] = options["zone"]
        else:
            res["zone"] = "normal"

        # Color
        if "color" in options.keys():
            res["color"] = options["color"]
        else:
            res["color"] = ""

        # Max drones
        if "max_drones" in options.keys():
            res["max_drones"] = int(options["max_drones"])
        else:
            res["max_drones"] = 1

        return res

    def _get_connection_option(self, option_string: str) -> Dict[str, str]:
        '''
        Return a dict corresponding to the optional parameters

        Args:
            option_string: str = The optional parameters
        Return:
            res: Dict[str, str] = The parsed optional parameters
        '''
        if not option_string:
            return {}

        return dict(re.findall(
                r"max_link_capacity=([\-?^\[\s\]]+)",
                option_string
            )
        )

    def _get_connection(self, line: str) -> Dict[str, str]:
        '''
        Return a dict corresponding to the parameters of the node

        Args:
            line: str = The current line to parse
        Return:
            res: Dict[str, str] = The parsed parameters
        '''
        pattern = r"connection: ([^\s\-]+)-([^\s\-]+)\s?(\[.+\])?"

        m = re.search(pattern, line)

        if not m:
            raise ValueError(f"Invalid line: '{line}'")

        node1: str = m.group(1)
        node2: str = m.group(2)
        options_str: str = m.group(3)

        options: Dict[str, str] = self._get_connection_option(options_str)

        res: Dict[str, Any] = {
            "node1": node1,
            "node2": node2
        }

        # Max link capacity
        if "max_link_capacity" in options.keys():
            res["max_link_capacity"] = int(options["max_link_capacity"])
        else:
            res["max_link_capacity"] = 1

        return res

    def _parse_line(
                self, variables: Vars, line: str
            ) -> None:
        '''
        Parse a given line

        Args:
            variables: Vars = The variables class
            line: str = The given line
        Return:
            None
        '''
        try:
            parts: List[str] = line.split(" ")
            info_type: str = parts[0]

            # Hub
            if info_type in ["start_hub:", "hub:", "end_hub:"]:
                params: Dict[str, Any] = self._get_hub(line, info_type)
                node: Node = Node(**params)
                variables.vars["graph"].add_node(**params)

                # Start hub
                if info_type == "start_hub:":
                    if "start_hub" in variables.get_keys():
                        raise ValueError("Too many start_hub")
                    variables.set_variable("start_hub", node)

                # End hub
                elif info_type == "end_hub:":
                    if "end_hub" in variables.get_keys():
                        raise ValueError("Too many end_hub")
                    variables.set_variable("end_hub", node)

            # Connection
            elif info_type == "connection:":
                params = self._get_connection(line)
                node_names: List[str] = [
                    node.name for node in variables.vars["graph"].keys()
                ]

                cond1 = params["node1"] not in node_names
                cond2 = params["node2"] not in node_names

                if cond1 or cond2:
                    raise ValueError(
                        "node1 and node2 must exist before connection"
                    )

                node1: Node = list(
                    filter(
                        lambda n: n.name == params["node1"],
                        list(variables.vars["graph"].keys())
                    )
                )[0]
                node2: Node = list(
                    filter(
                        lambda n: n.name == params["node2"],
                        list(variables.vars["graph"].keys())
                    )
                )[0]

                variables.vars["graph"].add_connection(
                    node1, node2, params["max_link_capacity"]
                )

            # Invalid line
            else:
                raise ValueError(f"Invalid line: '{line}'")

        except Exception as e:
            raise ValueError(f"Invalid line: '{line}'", e)

    def parser(self) -> Vars:
        '''
        Return the graph created with the parsed datas

        Args:
            None
        Return:
            variables: Vars = The variables class
        '''
        # Init Variables
        variables: Vars = Vars()
        graph: Graph = Graph()
        variables.set_variable("graph", graph)

        # Get nb_drones
        try:
            parts: List[str] = self.lines[0].split(" ")
            if parts[0] != "nb_drones:":
                raise ValueError(f"Invalid first line: '{self.lines[0]}'")
            nb_drones: int = int(parts[1])
            if nb_drones <= 0:
                raise ValueError(f"Invalid nb_drones: '{nb_drones}'")
            variables.set_variable("nb_drones", nb_drones)

        except Exception as e:
            raise ValueError(e)

        # Create Graph
        for line in self.lines[1:]:
            self._parse_line(variables, line)

        # Handle map errors
        if "start_hub" not in variables.get_keys():
            raise ValueError("Missing start_hub in map")
        elif "end_hub" not in variables.get_keys():
            raise ValueError("Missing end_hub in map")

        mini: List[int] = [float("inf"), float("inf")]
        for node in graph.keys():
            if node.x < mini[0]:
                mini[0] = node.x
            if node.y < mini[1]:
                mini[1] = node.y

        for (node1, liste) in graph.items():
            if mini[0] < 0:
                node1.x += -mini[0]
            if mini[1] < 0:
                node1.y += -mini[1]

        return variables
