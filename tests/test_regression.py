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
import errno


class TestRegression(unittest.TestCase):

    def test_missingWidth(self):
        controlFileName = 'tests/data/{}.yaml'.format('missing-width')
        clp = CommandLineParser(exit_on_error=False)
        parsedArgs = clp.parser.parse_args([controlFileName])

        registerFormat = RegisterFormat(parsedArgs)
        registerFormat.stderr = StringIO()
        result = registerFormat.run()
        testValue = registerFormat.stderr.getvalue()
        self.assertEqual(errno.EINVAL, result)
        message = "ERROR: YAML file \"{}\" in path \"$.registers[0].fields[1].width\": None is not of type 'integer'\n"
        self.assertEqual(testValue, message.format(controlFileName))


if __name__ == '__main__':
    unittest.main()
