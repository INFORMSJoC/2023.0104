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

from __future__ import annotations

import itertools
import random
from collections import defaultdict
from pathlib import Path
from typing import Tuple, Callable, Dict, List

import pytest

import helpers

from fixtures import *

import sys

try:
    import routingblocks as evrptw
except ModuleNotFoundError:
    pass


def create_node(vertex, evaluation):
    return evrptw.Node(vertex, evaluation.create_forward_label(vertex), evaluation.create_backward_label(vertex))


def test_node_construction(adptw_instance, mock_evaluation):
    for vertex in adptw_instance:
        node = create_node(vertex, mock_evaluation)
        assert node.vertex_id == vertex.vertex_id


def test_node_forward_update(adptw_instance, mock_evaluation):
    instance = adptw_instance
    depot_node = create_node(instance.depot, mock_evaluation)

    vertex = instance.get_customer(0)
    arc = instance.get_arc(depot_node.vertex_id, vertex.vertex_id)
    node = create_node(vertex, mock_evaluation)

    expected_forward_label = mock_evaluation.propagate_forward(depot_node.forward_label, instance.depot,
                                                               vertex, arc)
    node.update_forward(mock_evaluation, depot_node, arc)
    actual_forward_label = node.forward_label
    assert expected_forward_label == actual_forward_label


def test_node_backward_update(adptw_instance, mock_evaluation):
    instance = adptw_instance
    depot_node = create_node(instance.depot, mock_evaluation)

    vertex = instance.get_customer(0)
    arc = instance.get_arc(depot_node.vertex_id, vertex.vertex_id)
    node = create_node(vertex, mock_evaluation)

    expected_forward_label = mock_evaluation.propagate_backward(depot_node.backward_label, instance.depot,
                                                                vertex, arc)
    node.update_backward(mock_evaluation, depot_node, arc)
    actual_backward_label = node.backward_label
    assert expected_forward_label == actual_backward_label
