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
import random
import unittest
from regfmt import CommandLineParser
from argparse import ArgumentError
from tests.testutils import randomAsciiString


class TestCommandLineParser(unittest.TestCase):
    def test_version(self):
        clp = CommandLineParser(exit_on_error=False)
        parsedArgs = clp.parser.parse_args(['-v'])
        self.assertTrue(parsedArgs.version)

    def test_arbitaryInput(self):
        control = 'inputHeyThere.yaml'
        clp = CommandLineParser(exit_on_error=False)
        parsedArgs = clp.parser.parse_args([control])
        self.assertEqual(parsedArgs.input, control)

    def test_defaultInput(self):
        control = 'input.yaml'
        clp = CommandLineParser(exit_on_error=False)
        parsedArgs = clp.parser.parse_args([])
        self.assertEqual(parsedArgs.input, control)

    def test_template(self):
        templateValues = ['css', 'yaml', 'yamlcss']
        for value in templateValues:
            clp = CommandLineParser(exit_on_error=False)
            parsedArgs = clp.parser.parse_args(['-t', value])
            self.assertEqual(parsedArgs.template, value)

    def test_template_bad_data(self):
        value = randomAsciiString(k=random.randint(1, 20))
        clp = CommandLineParser(exit_on_error=False)
        try:
            clp.parser.parse_args(['-t', value])
        except ArgumentError as err:
            self.assertIn('invalid choice:', err.args[1])


if __name__ == '__main__':
    unittest.main()
