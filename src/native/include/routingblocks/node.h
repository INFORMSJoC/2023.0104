/*
 * Copyright (c) 2023 Patrick S. Klein (@libklein)
 *
 * Permission is hereby granted, free of charge, to any person obtaining a copy of
 * this software and associated documentation files (the "Software"), to deal in
 * the Software without restriction, including without limitation the rights to
 * use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of
 * the Software, and to permit persons to whom the Software is furnished to do so,
 * subject to the following conditions:
 *
 * The above copyright notice and this permission notice shall be included in all
 * copies or substantial portions of the Software.
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 * IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
 * FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
 * COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER
 * IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
 * CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
 */


#ifndef _routingblocks_NODE_H
#define _routingblocks_NODE_H

#include <routingblocks/arc.h>
#include <routingblocks/types.h>
#include <routingblocks/vertex.h>

#include <concepts>
#include <memory>
#include <span>
#include <vector>

namespace routingblocks {

    namespace detail {
        struct label_holder {
            std::shared_ptr<void> _data;

            label_holder(std::shared_ptr<void> data) : _data(std::move(data)){};

            // TODO Specialize std::get instead
            template <typename T> T& get() { return *static_cast<T*>(_data.get()); }

            template <typename T> const T& get() const {
                return *static_cast<const T*>(_data.get());
            }
        };
    }  // namespace detail

    class Evaluation;

    class Node {
      public:
        using label_holder_t = detail::label_holder;
        using fwd_label_t = label_holder_t;
        using bwd_label_t = label_holder_t;

      private:
        fwd_label_t _forward_label;
        bwd_label_t _backward_label;
        const routingblocks::Vertex* _vertex;

      public:
        Node(const routingblocks::Vertex& vertex, fwd_label_t fwd_label, bwd_label_t bwd_label)
            : _forward_label(std::move(fwd_label)),
              _backward_label(std::move(bwd_label)),
              _vertex(&vertex) {}

        void update_forward(Evaluation& evaluation, const Node& pred_node, const Arc& arc);

        void update_backward(Evaluation& evaluation, const Node& succ_node, const Arc& arc);

        [[nodiscard]] cost_t cost(Evaluation& evaluation) const;

        [[nodiscard]] std::vector<resource_t> cost_components(Evaluation& evaluation) const;

        [[nodiscard]] VertexID vertex_id() const { return _vertex->id; };
        [[nodiscard]] std::string_view vertex_strid() const { return _vertex->str_id; };
        [[nodiscard]] const Vertex& vertex() const { return *_vertex; };

        [[nodiscard]] const fwd_label_t& forward_label() const { return _forward_label; };
        [[nodiscard]] const bwd_label_t& backward_label() const { return _backward_label; };
        [[nodiscard]] bool feasible(Evaluation& evaluation) const;

        [[nodiscard]] bool operator==(const Node& other) const { return _vertex == other._vertex; }

        [[nodiscard]] bool operator!=(const Node& other) const { return !(other == *this); }

        friend std::ostream& operator<<(std::ostream& out, const Node& n) {
            out << n.vertex_strid();
            return out;
        }
    };

    // using route_segment = std::span<const Node>;
    class route_segment : public std::span<const Node> {
      public:
        using std::span<const Node>::span;

        template <class IteratorType> route_segment(IteratorType begin, IteratorType end)
            : std::span<const Node>(&*begin, &*end) {}
    };

    inline route_segment singleton_route_segment(const Node& node) {
        return route_segment{&node, 1};
    }

}  // namespace routingblocks

#endif  //_routingblocks_NODE_H
