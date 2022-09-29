import argparse

class CommandLineParser:
    def __init__(self):
        self.parser = argparse.ArgumentParser(description="regfmt - generate SVG")
        self.parser.add_argument('-v', '--version',
                                 action='store_true',
                                 help='print version information and exit')
        
        self.parser.add_argument('-o', '--output',
                                 action='store',
                                 default='-',
                                 help='output file')

        self.parser.add_argument('input', nargs='?', default='input.yaml',
                                 help='input register format YAML file (default: input.yaml)')
                
    def run(self):
        return self.parser.parse_args()
