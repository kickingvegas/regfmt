##
# Copyright 2022 Charles Y. Choi
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import argparse


class CommandLineParser:
    def __init__(self, exit_on_error: bool = True):
        description = ("%(prog)s - generate SVG diagrams of control "
                       "register-style data formats")

        epilog = ("Input file details can be found at "
                  "<https://github.com/kickingvegas/regfmt>. "
                  "Please report issues to "
                  "<https://github.com/kickingvegas/regfmt/issues>.")

        self.parser = argparse.ArgumentParser(description=description,
                                              epilog=epilog,
                                              exit_on_error=exit_on_error)

        self.parser.add_argument('-v', '--version',
                                 action='store_true',
                                 help='print version information and exit')

        self.parser.add_argument('-o', '--output',
                                 action='store',
                                 default='-',
                                 help="output file (default: '-' for stdout)")

        self.parser.add_argument('-s', '--style',
                                 action='store',
                                 default=None,
                                 help='CSS style file')

        self.parser.add_argument('-t', '--template',
                                 action='store',
                                 choices=['yaml', 'css', 'yamlcss'],
                                 default=None,
                                 help='Generate template YAML and/or CSS files')

        self.parser.add_argument('input',
                                 nargs='?',
                                 default='input.yaml',
                                 help=('input register format YAML file '
                                       '(default: input.yaml)'))

    def run(self):
        return self.parser.parse_args()
