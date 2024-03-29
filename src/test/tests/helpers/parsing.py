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

from .models import Vertex, Instance, Arc, VertexID, ArcID, Parameters, VertexType
from typing import Callable, Dict, Union
from pathlib import Path
from itertools import product
from math import sqrt


def parse_parameters(serialized_parameters: Dict[str, float], fleet_size: int) -> Parameters:
    return Parameters(battery_capacity=serialized_parameters['Q'], capacity=serialized_parameters['C'],
                      consumption_rate=serialized_parameters['r'], recharging_rate=1. / serialized_parameters['g'],
                      velocity=serialized_parameters['v'], fleet_size=fleet_size)


def create_arc_matrix(parameters: Parameters, vertices: Dict[VertexID, Vertex],
                      distance_fn: Callable[[Vertex, Vertex], float]) -> Dict[ArcID, Arc]:
    def _create_arc(u: Vertex, v: Vertex) -> Arc:
        distance = distance_fn(u, v)
        return Arc(distance=distance, consumption=parameters.consumption_rate * distance / parameters.recharging_rate,
                   travel_time=parameters.velocity * distance)

    return {
        (i, j): _create_arc(u, v) for (i, u), (j, v) in product(vertices.items(), repeat=2)
    }


def euclidean(u: Vertex, v: Vertex) -> float:
    return sqrt((u.x_coord - v.x_coord) ** 2 + (u.y_coord - v.y_coord) ** 2)


def parse_instance(instance_path: Path) -> Instance:
    vertices: Dict[VertexID, Vertex] = {}
    with open(instance_path) as instance_stream:
        # Discard first line (header)
        instance_stream.readline()
        # Set up reader
        fieldnames = ['vertex_id', 'vertex_type', 'x_coord', 'y_coord',
                      'demand', 'ready_time', 'due_date', 'service_time']
        # Parse vertices
        while (next_line := instance_stream.readline().strip()):
            if len(next_line) == 0:
                break

            line_fields = [x for x in next_line.split() if x]
            serialized_vertex: Dict[str, Union[str, float, VertexType]] = {
                field: (float(x) if field not in ('vertex_id', 'vertex_type') else x) for field, x in
                zip(fieldnames, line_fields)
            }

            # Parse vertex type
            serialized_vertex['vertex_type'] = VertexType(
                serialized_vertex['vertex_type'])
            # Parse the vertex
            vertices[serialized_vertex['vertex_id']] = Vertex(**serialized_vertex)  # type: ignore

        # Parse Parameters
        serialized_parameters: Dict[str, Union[float, int]] = {'n': len(vertices)}
        while (next_line := instance_stream.readline()):
            serialized_parameters[next_line.partition(' ')[0]] = float(
                next_line.partition('/')[-1][:-2])
        # Create from parsed
        parameters = parse_parameters(serialized_parameters, fleet_size=sum(
            1 for x in vertices.values() if x.is_customer))

    # Create Arcs
    arcs = create_arc_matrix(parameters=parameters, vertices=vertices,
                             distance_fn=euclidean)

    return Instance(parameters=parameters, vertices=vertices, arcs=arcs)
