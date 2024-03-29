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

from typing import List

import routingblocks


class RouteRemovalOperator(routingblocks.DestroyOperator):
    """
    Removes random routes from the solution. May remove more than the requested number of vertices.
    """

    def __init__(self, rng: routingblocks.Random):
        """
        :param rng: The :py:class:`routingblocks.Random` instance to use.
        """
        # Important: Do not use super()!
        routingblocks.DestroyOperator.__init__(self)
        self._rng = rng

    def can_apply_to(self, _solution: routingblocks.Solution) -> bool:
        return len(_solution) > 0

    def apply(self, evaluation: routingblocks.Evaluation, _solution: routingblocks.Solution,
              number_of_removed_vertices: int) -> List[
        int]:
        # Try to remove random routes
        removed_customers = []
        while len(_solution) > 0 and len(removed_customers) < number_of_removed_vertices:
            random_route_index = self._rng.randint(0, len(_solution) - 1)
            removed_customers.extend(x.vertex_id for x in _solution[random_route_index] if not x.vertex.is_depot)
            del _solution[random_route_index]
        return removed_customers

    def name(self) -> str:
        return "RouteRemoveOperator"
