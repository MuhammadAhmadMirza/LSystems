# L-systems in Python

This project provides an implementation of **L-systems** (Lindenmayer systems) using **Python** and **Pygame**. L-systems are a mathematical model used to describe the growth of plants and other organic structures through recursive string rewriting.

![Demo](/src/assets/images/demo.gif)

## What are L-systems?

L-systems are a formal grammar system invented by **Aristid Lindenmayer** in 1968. They are particularly well-suited for modeling the growth of plants, trees, and fractals. The system consists of:

- **Alphabet**: A set of symbols that can be replaced (or rewritten).
- **Axiom**: The initial state of the system.
- **Production rules**: A set of rules that define how each symbol in the alphabet is replaced by a string of symbols.

Each iteration or generation of the system produces a new string based on the production rules. When visualized, L-systems can create complex, fractal-like structures that resemble plant growth, tree branches, and more.

## Features

- **Preset L-systems**: The following preset L-systems are available in the project:
    1. **Dragon Curve**
    2. **Tree**
    3. **Mandala**
    4. **Planet**
    5. **Pentigree**
    6. **Hex Fractal**
    7. **Wings**
    8. **Snowflake**
    9. **Tentacle Fractal**

## Prerequisites

- **Python 3.x**

### Required Libraries

- `pygame`

To install the required libraries, you can use the following command:

```bash
pip install -r requirements.txt
```

## Documentation

For more information, check out the [Conway's Game of Life Documentation](/docs/LSystems.md)

## License

This project is licensed under the MIT License - see the [LICENSE](/docs/LICENSE) file for details.
