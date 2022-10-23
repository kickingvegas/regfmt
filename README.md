# regfmt

This project is a **work in progress**.

**regfmt** is a command line utility to generate SVG diagrams for control register-style data formats. It is inspired by the *dformat* command from the *troff* family of tools, however re-imagined using contemporary (circa 2022) file formats.

Example output SVG:

![example svg](http://yummymelon.com/images/example_0001.svg)

# Features

-   SVG output
-   Modern configuration input file formats
    -   YAML for register configuration
    -   CSS for styling SVG output

# Usage

    usage: regfmt [-h] [-v] [-o OUTPUT] [-s STYLE] [input]
    
    regfmt - generate SVG diagrams of control register-style data formats
    
    positional arguments:
      input                 input register format YAML file (default: input.yaml)
    
    optional arguments:
      -h, --help            show this help message and exit
      -v, --version         print version information and exit
      -o OUTPUT, --output OUTPUT
                            output file (default: '-' for stdout)
      -s STYLE, --style STYLE
                            CSS style file

