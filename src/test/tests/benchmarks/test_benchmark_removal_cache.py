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

from random import random
from typing import List

import pytest

from fixtures import *

import routingblocks
from routingblocks import niftw

from .reference.removal_cache import RemovalCache, RemovalMove


def build_solution(evaluation: routingblocks.Evaluation, instance: routingblocks.Instance, raw_routes: List[List[int]]):
    return routingblocks.Solution(evaluation, instance,
                          [routingblocks.create_route(evaluation, instance, route) for route in raw_routes])


@pytest.fixture(
    params=['python', 'cpp']
)
def removal_cache_factory(request):
    if request.param == 'python':
        return RemovalCache
    elif request.param == 'cpp':
        return routingblocks.RemovalCache


def benchmark_removal_cache_rebuild(removal_cache, evaluation, solution: routingblocks.Solution):
    removal_cache.rebuild(evaluation, solution)


def benchmark_removal_cache_invalidate(removal_cache, route: routingblocks.Route, route_index: int):
    removal_cache.invalidate_route(route, route_index)


def benchmark_removal_cache_iterate(removal_cache, iterable):
    for _ in iterable:
        pass


@pytest.fixture
def instance_evaluation_solution(instance_parser, random_solution_factory):
    replenishment_time = 0.
    storage_capacity = 170.
    battery_capacity = 170.

    py_instance, instance = instance_parser('r101_21.txt')

    evaluation = niftw.Evaluation(battery_capacity, storage_capacity, replenishment_time)
    # Create routes for native evaluation
    randgen = random.Random(0)
    solution = random_solution_factory(instance, evaluation,
                                       vertices=list(instance.stations) + list(instance.customers), randgen=randgen)
    return instance, evaluation, solution


@pytest.mark.benchmark(group="removal_cache_rebuild")
def test_evaluation_benchmark_removal_cache_rebuild(instance_evaluation_solution, benchmark, removal_cache_factory):
    instance, evaluation, solution = instance_evaluation_solution

    cache = removal_cache_factory(instance)
    benchmark(benchmark_removal_cache_rebuild, removal_cache=cache, solution=solution, evaluation=evaluation)


@pytest.mark.benchmark(group="removal_cache_iterate")
def test_evaluation_benchmark_removal_cache_iterate(instance_evaluation_solution, benchmark, removal_cache_factory):
    instance, evaluation, solution = instance_evaluation_solution

    cache = removal_cache_factory(instance)
    cache.rebuild(evaluation, solution)

    moves_iter = cache.moves_in_order

    benchmark(benchmark_removal_cache_iterate, removal_cache=cache, iterable=moves_iter)


@pytest.mark.benchmark(group="removal_cache_invalidate")
def test_evaluation_benchmark_removal_cache_invalidate(instance_evaluation_solution, benchmark, removal_cache_factory):
    instance, evaluation, solution = instance_evaluation_solution

    cache = removal_cache_factory(instance)
    cache.rebuild(evaluation, solution)
    route_index = 2
    benchmark(benchmark_removal_cache_invalidate, removal_cache=cache, route=solution[route_index],
              route_index=route_index)
