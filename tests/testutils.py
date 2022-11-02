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
import random
import string
import difflib
from regfmt import CommandLineParser
from regfmt import RegisterFormat
from io import StringIO

def auditAttributeExistence(testbench: unittest.TestCase, obj, attributes):
    for attribute in attributes:
        testbench.assertTrue(hasattr(obj, attribute), '{} missing attribute: {}'.format(obj, attribute))


def randomAsciiString(k: int = 5):
    data = string.ascii_letters + string.digits
    result = ''.join(random.choices(data, k=k))
    return result


def fileCompareContents(test_filename: str, control_filename: str):
    with open(test_filename) as infile:
        testLines = infile.readlines()

    with open(control_filename) as infile:
        controlLines = infile.readlines()

    diff = list(difflib.unified_diff(testLines, controlLines, fromfile=test_filename, tofile=control_filename))
    return diff


def run_register_format(args):
    clp = CommandLineParser(exit_on_error=False)
    parsedArgs = clp.parser.parse_args(args)
    registerFormat = RegisterFormat(parsedArgs)
    registerFormat.stderr = StringIO()
    result = registerFormat.run()
    stderr_output = registerFormat.stderr.getvalue()
    return (result, stderr_output)
