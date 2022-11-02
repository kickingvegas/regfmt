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
import unittest
from regfmt import CommandLineParser
from regfmt import RegisterFormat
from io import StringIO
from regfmt import VERSION
import errno
from tests.testutils import randomAsciiString, fileCompareContents


class TestRegisterFormat(unittest.TestCase):
    def test_example_files(self):
        examples = ['example_0001', 'example_0002', 'example_0003']

        for example in examples:
            clp = CommandLineParser(exit_on_error=False)
            outfileName = 'tests/output/{}.svg'.format(example)
            infileName = 'tests/data/{}.yaml'.format(example)
            controlName = 'tests/control/{}.svg'.format(example)
            parsedArgs = clp.parser.parse_args(['-o', outfileName, infileName])
            result = RegisterFormat(parsedArgs).run()
            self.assertEqual(0, result)

            diff = fileCompareContents(outfileName, controlName)
            self.assertEqual(0, len(diff), 'FAILURE: {}.yaml'.format(example))

    def test_version(self):
        clp = CommandLineParser(exit_on_error=False)
        parsedArgs = clp.parser.parse_args(['--version'])
        registerFormat = RegisterFormat(parsedArgs)
        registerFormat.stdout = StringIO()
        result = registerFormat.run()
        testValue = registerFormat.stdout.getvalue()

        self.assertEqual(0, result)
        self.assertEqual(testValue.strip(), VERSION)

    def test_missingFile(self):
        controlFileName = '{}.yaml'.format(randomAsciiString(k=20))
        clp = CommandLineParser(exit_on_error=False)
        parsedArgs = clp.parser.parse_args([controlFileName])

        registerFormat = RegisterFormat(parsedArgs)
        registerFormat.stderr = StringIO()
        result = registerFormat.run()
        testValue = registerFormat.stderr.getvalue()
        self.assertEqual(errno.ENOENT, result)
        message = 'ERROR: file "{0}" not found.\n'
        self.assertEqual(testValue, message.format(controlFileName))

    def test_missing_css(self):
        clp = CommandLineParser(exit_on_error=False)
        controlFileName = "{}.css".format(randomAsciiString(k=20))
        message = 'ERROR: No such file or directory: "{}"  Exiting…\n'

        parsedArgs = clp.parser.parse_args(['-s', controlFileName, 'tests/data/example_0001.yaml'])
        registerFormat = RegisterFormat(parsedArgs)
        registerFormat.stderr = StringIO()
        result = registerFormat.run()
        testValue = registerFormat.stderr.getvalue()
        self.assertEqual(result, errno.ENOENT)
        self.assertEqual(testValue, message.format(controlFileName))

    def test_css_main(self):
        clp = CommandLineParser(exit_on_error=False)
        controlFileName = "clean.css"
        message = 'ERROR: No such file or directory: "{}"  Exiting…\n'

        parsedArgs = clp.parser.parse_args(['-s',
                                            'tests/data/{}'.format(controlFileName),
                                            '-o',
                                            'tests/output/example_0001-clean.svg',
                                            'tests/data/example_0001.yaml'])
        registerFormat = RegisterFormat(parsedArgs)
        # registerFormat.stderr = StringIO()
        result = registerFormat.run()
        self.assertEqual(result, 0)
        # testValue = registerFormat.stderr.getvalue()
        # self.assertEqual(result, errno.ENOENT)
        # self.assertEqual(testValue, message.format(controlFileName))

    def test_template_yaml(self):
        outputFilename = 'template.yaml'
        if os.path.exists(outputFilename):
            os.remove(outputFilename)

        clp = CommandLineParser(exit_on_error=False)
        args = ['-t', 'yaml']
        parsedArgs = clp.parser.parse_args(args)
        registerFormat = RegisterFormat(parsedArgs)
        result = registerFormat.run()
        self.assertEqual(result, 0)
        self.assertTrue(os.path.exists(outputFilename))

        controlFilename = 'tests/control/{}'.format(outputFilename)
        diff = fileCompareContents(test_filename=outputFilename, control_filename=controlFilename)
        self.assertEqual(0, len(diff), 'FAILURE: {} differs from {}'.format(outputFilename, controlFilename))
        os.remove(outputFilename)

    def test_template_css(self):
        outputFilename = 'template.css'
        if os.path.exists(outputFilename):
            os.remove(outputFilename)

        clp = CommandLineParser(exit_on_error=False)
        args = ['-t', 'css']
        parsedArgs = clp.parser.parse_args(args)
        registerFormat = RegisterFormat(parsedArgs)
        result = registerFormat.run()
        self.assertEqual(result, 0)
        self.assertTrue(os.path.exists(outputFilename))

        controlFilename = 'tests/control/{}'.format(outputFilename)
        diff = fileCompareContents(test_filename=outputFilename, control_filename=controlFilename)
        self.assertEqual(0, len(diff), 'FAILURE: {} differs from {}'.format(outputFilename, controlFilename))
        os.remove(outputFilename)

    def test_template_yamlcss(self):
        filenames = ['template.yaml', 'template.css']

        for filename in filenames:
            if os.path.exists(filename):
                os.remove(filename)

        clp = CommandLineParser(exit_on_error=False)
        args = ['-t', 'yamlcss']
        parsedArgs = clp.parser.parse_args(args)
        registerFormat = RegisterFormat(parsedArgs)
        result = registerFormat.run()
        self.assertEqual(result, 0)

        for filename in filenames:
            self.assertTrue(os.path.exists(filename))
            controlFilename = 'tests/control/{}'.format(filename)
            diff = fileCompareContents(test_filename=filename, control_filename=controlFilename)
            self.assertEqual(0, len(diff), 'FAILURE: {} differs from {}'.format(filename, controlFilename))
            os.remove(filename)


if __name__ == '__main__':
    unittest.main()
