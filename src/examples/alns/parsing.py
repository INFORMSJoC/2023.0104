# Copyright (c) 2023 Patrick S. Klein (@libklein)
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of
# this software and associated documentation files (the "Software"), to deal in
# the Software without restriction, including without limitation the rights to
# use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of
# the Software, and to permit persons to whom the Software is furnished to do so,
# subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
# FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
# COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER
# IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
# CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

from typing import Callable, Dict, Union
from pathlib import Path
from itertools import product
from math import sqrt
import routingblocks as rb


def parse_instance(instance_path: Path):
    str_fields = ['StringID', 'Type']
    with open(instance_path) as instance_stream:
        fields = instance_stream.readline().split()
        # Parse the vertices
        vertices = []
        for line in instance_stream:
            tokens = line.split()
            if len(tokens) == 0:
                break
            vertex = {key: (x if key in str_fields else float(x)) for key, x in zip(fields, tokens)}
            vertices.append(vertex)
        # Parse the parameters
        parameters = {}
        for line in instance_stream:
            key, *_, value = line.split()
            # Remove surrounding / characters and parse the value
            parameters[key] = float(value[1:-1])

    # Create a mapping from pairs of vertices to arcs
    arcs = {}
    for i in vertices:
        for j in vertices:
            # Compute distance
            distance = sqrt((i['x'] - j['x']) ** 2 + (i['y'] - j['y']) ** 2)
            # Compute travel time (distance / average velocity)
            travel_time = distance / parameters['v']
            # Compute consumption (consumption rate * travel time / recharging rate)
            consumption = parameters['r'] * travel_time / parameters['g']
            arcs[i['StringID'], j['StringID']] = dict(distance=distance, travel_time=travel_time,
                                                      consumption=consumption)

    return vertices, arcs, parameters


def create_instance(serialized_vertices, serialized_arcs) -> rb.Instance:
    instance_builder = rb.utility.InstanceBuilder(create_vertex=rb.adptw.create_adptw_vertex,
                                                  create_arc=rb.adptw.create_adptw_arc)
    # Create and register the vertices
    for vertex in serialized_vertices:
        # Create problem-specific data held by vertices
        vertex_data = rb.adptw.VertexData(vertex['x'], vertex['y'], vertex['demand'], vertex['ReadyTime'],
                                          vertex['DueDate'],
                                          vertex['ServiceTime'])
        # Register the vertex depending on it's type
        if vertex['Type'] == 'd':
            instance_builder.set_depot(vertex['StringID'], vertex_data)
        elif vertex['Type'] == 'c':
            instance_builder.add_customer(vertex['StringID'], vertex_data)
        else:
            instance_builder.add_station(vertex['StringID'], vertex_data)

    # Create and register the arcs
    for (i, j), arc in serialized_arcs.items():
        # Create problem-specific data held by arcs
        arc_data = rb.adptw.ArcData(arc['distance'], arc['consumption'], arc['travel_time'])
        instance_builder.add_arc(i, j, arc_data)

    # Create instance
    return instance_builder.build()
