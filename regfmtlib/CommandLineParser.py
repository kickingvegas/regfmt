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
    def __init__(self):
        self.parser = argparse.ArgumentParser(description="regfmt - generate SVG")
        self.parser.add_argument('-v', '--version',
                                 action='store_true',
                                 help='print version information and exit')
        
        self.parser.add_argument('-o', '--output',
                                 action='store',
                                 default='-',
                                 help='output file')

        self.parser.add_argument('-c', '--config',
                                 action='store',
                                 default=None,
                                 help='CSS configuration file')

        self.parser.add_argument('input', nargs='?', default='input.yaml',
                                 help='input register format YAML file (default: input.yaml)')
                
    def run(self):
        return self.parser.parse_args()
