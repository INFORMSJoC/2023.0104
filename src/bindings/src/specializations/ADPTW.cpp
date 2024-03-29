// Copyright (c) 2023 Patrick S. Klein (@libklein)
//
// Permission is hereby granted, free of charge, to any person obtaining a copy of
// this software and associated documentation files (the "Software"), to deal in
// the Software without restriction, including without limitation the rights to
// use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of
// the Software, and to permit persons to whom the Software is furnished to do so,
// subject to the following conditions:
//
// The above copyright notice and this permission notice shall be included in all
// copies or substantial portions of the Software.
//
// THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
// IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
// FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
// COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER
// IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
// CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

#include "routingblocks_bindings/specializations/ADPTW.h"

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

#include "routingblocks/ADPTWEvaluation.h"
#include "routingblocks_bindings/binding_helpers.hpp"

namespace routingblocks::bindings {

    void bind_adptw(pybind11::module_& m) {
        ::bindings::helpers::bind_concatenation_evaluation_specialization<ADPTWEvaluation>(
            pybind11::class_<ADPTWEvaluation, Evaluation>(m, "ADPTWEvaluation")
                .def(pybind11::init<resource_t, resource_t>()))
            .def_readwrite("overload_penalty_factor", &ADPTWEvaluation::overload_penalty_factor)
            .def_readwrite("resource_penalty_factor", &ADPTWEvaluation::overcharge_penalty_factor)
            .def_readwrite("time_shift_penalty_factor",
                           &ADPTWEvaluation::time_shift_penalty_factor);

        pybind11::class_<routingblocks::ADPTWVertexData>(m, "ADPTWVertexData")
            .def(pybind11::init<float, float, resource_t, resource_t, resource_t, resource_t>());
        pybind11::class_<routingblocks::ADPTWArcData>(m, "ADPTWArcData")
            .def(pybind11::init<resource_t, resource_t, resource_t>());
        m.def("create_adptw_vertex", &::bindings::helpers::vertex_constructor<ADPTWVertexData>);
        m.def("create_adptw_arc", &::bindings::helpers::arc_constructor<ADPTWArcData>);

        pybind11::class_<FRVCP<ADPTWLabel>>(m, "ADPTWFacilityPlacementOptimizer")
            .def(pybind11::init<>([](const Instance& instance, resource_t resource_capacity) {
                return FRVCP<ADPTWLabel>(instance, std::make_shared<Propagator<ADPTWLabel>>(
                                                       instance, resource_capacity));
            }))
            .def("optimize", &FRVCP<ADPTWLabel>::optimize,
                 "Solve the detour embedding problem for the specified route.");
    }

}  // namespace routingblocks::bindings