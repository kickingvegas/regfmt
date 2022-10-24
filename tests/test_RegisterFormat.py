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

import unittest
from regfmt import CommandLineParser
from regfmt import RegisterFormat
from io import StringIO
from regfmt import VERSION
import difflib
import errno

class TestRegisterFormat(unittest.TestCase):
    def test_example_files(self):
        examples = ['example_0001', 'example_0002', 'example_0003']

        for example in examples:
            clp = CommandLineParser()
            outfileName = 'tests/output/{}.svg'.format(example)
            infileName = 'tests/data/{}.yaml'.format(example)
            controlName = 'tests/control/{}.svg'.format(example)
            parsedArgs = clp.parser.parse_args(['-o', outfileName, infileName])
            result = RegisterFormat(parsedArgs).run()
            self.assertEqual(0, result)

            with open(outfileName) as infile:
                testLines = infile.readlines()

            with open(controlName) as infile:
                controlLines = infile.readlines()

            diff = list(difflib.unified_diff(testLines, controlLines, fromfile=outfileName, tofile=controlName))
            self.assertEqual(0, len(diff))

    def test_version(self):
        clp = CommandLineParser()
        parsedArgs = clp.parser.parse_args(['--version'])
        # !!!: for some reason version isn't set by argparse
        parsedArgs.version = True

        registerFormat = RegisterFormat(parsedArgs)
        registerFormat.stdout = StringIO()
        result = registerFormat.run()
        testValue = registerFormat.stdout.getvalue()

        self.assertEqual(0, result)
        self.assertEqual(testValue.strip(), VERSION)

    def test_missingFile(self):
        controlFileName = 'dummyfile.yaml'
        clp = CommandLineParser()
        parsedArgs = clp.parser.parse_args([controlFileName])

        registerFormat = RegisterFormat(parsedArgs)
        registerFormat.stderr = StringIO()
        result = registerFormat.run()
        testValue = registerFormat.stderr.getvalue()
        self.assertEqual(errno.ENOENT, result)
        message = 'ERROR: file "{0}" not found.\n'
        self.assertEqual(testValue, message.format(controlFileName))
    def test_missing_css(self):
        clp = CommandLineParser()
        controlFileName = "foo.css"
        message = 'ERROR: No such file or directory: "{}"  Exiting…\n'

        parsedArgs = clp.parser.parse_args(['-s', controlFileName, 'tests/data/example_0001.yaml'])
        registerFormat = RegisterFormat(parsedArgs)
        registerFormat.stderr = StringIO()
        result = registerFormat.run()
        testValue = registerFormat.stderr.getvalue()
        self.assertEqual(result, errno.ENOENT)
        self.assertEqual(testValue, message.format(controlFileName))

    def test_css_main(self):
        clp = CommandLineParser()
        controlFileName = "clean.css"
        message = 'ERROR: No such file or directory: "{}"  Exiting…\n'

        parsedArgs = clp.parser.parse_args(['-s',
                                            'tests/data/{}'.format(controlFileName),
                                            '-o',
                                            'tests/output/example_0001-clean.svg',
                                            'tests/data/example_0001.yaml'])
        registerFormat = RegisterFormat(parsedArgs)
        #registerFormat.stderr = StringIO()
        result = registerFormat.run()
        self.assertEqual(result, 0)
        #testValue = registerFormat.stderr.getvalue()
        #self.assertEqual(result, errno.ENOENT)
        #self.assertEqual(testValue, message.format(controlFileName))



if __name__ == '__main__':
    unittest.main()
