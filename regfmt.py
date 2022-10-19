#!/usr/bin/env python3
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

import os
import sys
from regfmtlib import CommandLineParser
from regfmtlib import InputLoadAndValidate
from regfmtlib import TopLevel
from regfmtlib import DRCChecker
from regfmtlib import SVGWriter

VERSION = '0.1.0'


class RegisterFormat:
    def __init__(self, parsedArguments):
        self.version = VERSION
        self.stdout = sys.stdout
        self.stdin = sys.stdin
        self.stderr = sys.stderr
        self.parsedArguments = parsedArguments

        if parsedArguments.version:
            sys.stdout.write('{0}\n'.format(self.version))
            sys.exit(0)

        if parsedArguments.output != '-':
            outfile = open('{0}'.format(parsedArguments.output), 'w')
            self.stdout = outfile

        if not os.path.exists(parsedArguments.input):
            message = ('ERROR: file "{0}" does not exist. '
                       'Please specify an input file.\n')
            sys.stderr.write(message.format(parsedArguments.input))
            sys.exit(1)

    def run(self):
        # Load and validate input YAML
        loader = InputLoadAndValidate(self.parsedArguments)
        inputYAML = loader.loadAndValidate()
        # print(inputYAML)

        # Deserialize input YAML into native object DB
        registerDB = TopLevel(config=inputYAML)

        # DRC Check native object DB
        drcChecker = DRCChecker()
        drcChecker.check(registerDB)
        drcChecker.subIndexFields(registerDB)

        # Render SVG
        svgWriter = SVGWriter(registerDB,
                              self.stdout,
                              configFileName=self.parsedArguments.style)
        svgWriter.writeSVG()

        # wrap up
        if self.stdout != sys.stdout:
            self.stdout.close()


if __name__ == '__main__':
    app = RegisterFormat(CommandLineParser().run())
    app.run()
