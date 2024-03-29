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
import math
import random
import time
from collections import defaultdict
from pathlib import Path
from typing import Tuple, Callable, Dict, List, Iterable

import pytest

import helpers

from fixtures import *

import routingblocks

try:
    import routingblocks as alns
    from routingblocks import adptw
    from routingblocks import niftw
except ModuleNotFoundError:
    pass


def run_local_search(local_search: alns.LocalSearch, solution: alns.Solution, operators):
    local_search.optimize(solution, operators)


def create_operators(instance):
    return [
        alns.operators.SwapOperator_0_1(instance, None),
        alns.operators.SwapOperator_0_2(instance, None),
        alns.operators.SwapOperator_1_1(instance, None),
        alns.operators.SwapOperator_1_2(instance, None),
        alns.operators.InterRouteTwoOptOperator(instance, None)
    ]


@pytest.mark.benchmark(group="local-search")
@pytest.mark.parametrize("instance_name", ['c101_21.txt', 'r101_21.txt'])
@pytest.mark.parametrize("evaluation", ['adptw_native', 'niftw_native'])
def test_local_search_benchmark(instance_parser, instance_name,
                                random_solution_factory, evaluation, benchmark):
    py_instance, instance = instance_parser(instance_name)
    vehicle_battery_capacity = py_instance.parameters.battery_capacity_time
    vehicle_storage_capacity = py_instance.parameters.capacity
    evaluations = {
        'adptw_native': alns.adptw.Evaluation(vehicle_battery_capacity, vehicle_storage_capacity),
        'niftw_native': alns.niftw.Evaluation(vehicle_battery_capacity, vehicle_storage_capacity, 0)
    }
    evaluation = evaluations[evaluation]

    # Create routes
    randgen = random.Random(0)
    solution = random_solution_factory(instance, evaluation, randgen=randgen)
    local_search = alns.LocalSearch(instance, evaluation, None, routingblocks.BestImprovementPivotingRule())
    # Add operators
    operators = create_operators(instance)
    benchmark(run_local_search, solution=solution, local_search=local_search, operators=operators)
