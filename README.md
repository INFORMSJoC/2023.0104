[![INFORMS Journal on Computing Logo](https://INFORMSJoC.github.io/logos/INFORMS_Journal_on_Computing_Header.jpg)](https://pubsonline.informs.org/journal/ijoc)

# RoutingBlocks

This archive is distributed in association with the [INFORMS Journal on
Computing](https://pubsonline.informs.org/journal/ijoc) under the [MIT License](LICENSE).


This archive is distributed in association with the [INFORMS Journal on
Computing](https://pubsonline.informs.org/journal/ijoc) under the [MIT License](LICENSE).

The software and data in this repository are a snapshot of the software and data
that were used in the research reported on in the paper 
[RoutingBlocks: An open-source Python package for Vehicle Routing Problems with Intermediate Stops](https://doi.org/10.1287/ijoc.2023.0104) by P. S. Klein and Maximilian Schiffer. 
The snapshot is based on [this SHA](https://github.com/tumBAIS/RoutingBlocks/commit/2d2ee06c79b5d458b1aeeafd95a2b42b5441079a) 
in the development repository. 

**Important: This code is being developed on an on-going basis at 
[https://github.com/tumBAIS/RoutingBlocks](https://github.com/tumBAIS/routingblocks). Please go there if you would like to
get a more recent version or would like support**

## Cite

To cite the contents of this repository, please cite both the paper and this repo, using their respective DOIs.

[https://doi.org/10.1287/ijoc.2023.0104](https://doi.org/10.1287/ijoc.2023.0104)

[https://doi.org/10.1287/ijoc.2023.0104.cd](https://doi.org/10.1287/ijoc.2023.0104.cd)

Below is the BibTex for citing this snapshot of the repository.

```
@article{RoutingBlocks,
  author =        {P. S. Klein, M. Schiffer},
  publisher =     {INFORMS Journal on Computing},
  title =         {{RoutingBlocks}},
  year =          {2023},
  doi =           {10.1287/ijoc.2023.0104.cd},
  url =           {https://github.com/INFORMSJoC/2023.0104},
}  
```

## Description

`RoutingBlocks` is an open-source Python package for the implementation of algorithms for Vehicle Routing Problems with
Intermediate Stops.

It provides a set of modular algorithmic components and efficient data structures that can be used as building blocks
for problem-specific metaheuristic algorithms. These components are tailored specifically to tackle the challenges of
VRPIS, but can be used for other classes of vehicle routing problems as well.

## Installation

The package is available on PyPI and can be installed using `pip`:

```bash
pip install routingblocks
```

To obtain the version archived in this repository, run

```bash
pip install git+https://github.com/INFORMSJoC/2023.0104#subdirectory=src
```

instead.

## Features

* Efficient C++-based solution representation
* Customizable Local Search Solver
* Framework for ALNS-based metaheuristics
* Efficient native implementations of numerous destroy, repair, and local search operators
* Move caches implemented in native code to allow high-performance operator implementations in Python
* Support for custom [native extensions](https://github.com/tumBAIS/routingblocks-native-extension-example)

## Usage

We provide an [example implementation](https://github.com/tumBAIS/RoutingBlocks/tree/main/examples) of an ALNS-based
algorithm for
the [EVRPTW-PR](https://research.sabanciuniv.edu/id/eprint/26033/1/WP_EVRPTW-Partial_Recharge_KeskinCatay.pdf) as part
of this repository.

Further documentation is available
at [readthedocs](https://routingblocks.readthedocs.io/en/latest/getting_started.html).

## Contributing

Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.

See [CONTRIBUTING.md](CONTRIBUTING.md) for more information and documentation on setting up a development environment.

## License

[MIT](https://choosealicense.com/licenses/mit/)
