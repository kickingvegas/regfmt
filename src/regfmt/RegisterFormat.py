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
import errno
import os
import sys
from regfmt import VERSION
from regfmt import CommandLineParser
from regfmt import InputLoadAndValidate
from regfmt import TopLevel
from regfmt import DRCChecker
from regfmt import SVGWriter
from jsonschema.exceptions import ValidationError
from yaml.scanner import ScannerError
from tinycss2.ast import Declaration, ParseError
from regfmt import write_yaml_css_templates


class RegisterFormat:
    def __init__(self, parsedArguments):
        self.version = VERSION
        self.stdout = sys.stdout
        self.stdin = sys.stdin
        self.stderr = sys.stderr
        self.parsedArguments = parsedArguments

    def run(self):
        parsedArguments = self.parsedArguments

        if parsedArguments.version:
            self.stdout.write('{0}\n'.format(self.version))
            return 0

        if parsedArguments.template:
            return write_yaml_css_templates(template_type=parsedArguments.template)

        if parsedArguments.output != '-':
            outfile = open('{0}'.format(parsedArguments.output), 'w')
            self.stdout = outfile

        if not os.path.exists(parsedArguments.input):
            message = 'ERROR: file "{0}" not found.\n'
            self.stderr.write(message.format(parsedArguments.input))
            return errno.ENOENT

        # Load and validate input YAML
        loader = InputLoadAndValidate(self.parsedArguments)

        try:
            inputYAML = loader.loadAndValidate()
            # print(inputYAML)
        except ValidationError as err:
            message = 'ERROR: YAML file "{}" in path "{}": {}'
            self.stderr.write(message.format(self.parsedArguments.input,
                                             err.json_path,
                                             err.message))

            # print(err.json_path)
            # print(err.message)
            # print(err.path)
            # print(err.relative_path)
            # print(err.absolute_path)
            # print(err.context)
            # print(err.cause)
            # print(err.instance)
            # print(err.validator)
            # print(err.schema_path)
            # print(dir(err))

            return errno.EINVAL
        except ScannerError as err:
            self.stderr.write('ERROR: {0}\n'.format(err))
            return errno.EINVAL

        except:
            print('wtf')
            raise

        # Deserialize input YAML into native object DB
        registerDB = TopLevel(config=inputYAML)

        # DRC Check native object DB
        drcChecker = DRCChecker()
        drcChecker.check(registerDB)
        drcChecker.subIndexFields(registerDB)

        # Render SVG
        try:
            svgWriter = SVGWriter(registerDB,
                                  self.stdout,
                                  configFileName=self.parsedArguments.style)
        except FileNotFoundError as err:
            message = 'ERROR: {}: "{}"  Exiting…\n'.format(err.strerror, err.filename)
            self.stderr.write(message)
            return err.errno

        except ValueError as err:
            if len(err.args) and isinstance(err.args[0], Declaration):
                errorDeclaration: Declaration = err.args[0]
                errorMessage: str = err.args[1]
                message = 'ERROR: {} (line {}, row {}): {}\n'.format(self.parsedArguments.style,
                                                                     errorDeclaration.source_line,
                                                                     errorDeclaration.source_column,
                                                                     errorMessage)
                self.stderr.write(message)

            elif len(err.args) and isinstance(err.args[0], ParseError):
                parseError: ParseError = err.args[0]
                errorMessage: str = err.args[1]
                self.stderr.write(errorMessage)

            else:
                message = 'ERROR: {} Exiting…\n'.format(err.args[0])
                self.stderr.write(message)

            return errno.EINVAL

        svgWriter.writeSVG()

        # wrap up
        if self.stdout != sys.stdout:
            self.stdout.close()

        return 0


if __name__ == '__main__':
    app = RegisterFormat(CommandLineParser().run())
    app.run()
