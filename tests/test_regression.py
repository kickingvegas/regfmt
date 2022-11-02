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
import errno
from tests.testutils import run_register_format, fileCompareContents


class TestRegression(unittest.TestCase):

    def test_missingWidth2(self):
        controlFileName = 'tests/data/{}.yaml'.format('missing-width')
        message = "ERROR: YAML file \"{}\" in path \"$.registers[0].fields[1].width\": None is not of type 'integer'\n"
        args = [controlFileName]
        result, stderr_output = run_register_format(args)
        self.assertEqual(result, errno.EINVAL)
        self.assertEqual(stderr_output, message.format(controlFileName))

    def test_float_for_int(self):
        controlName = 'float-for-int'
        outputName = 'tests/output/{}.svg'.format(controlName)
        inputName = 'tests/data/{}.yaml'.format(controlName)
        controlName = 'tests/control/{}.svg'.format(controlName)
        args = ['-o',
                outputName,
                inputName]
        result, stderr_output = run_register_format(args)
        self.assertEqual(result, 0)

        diff = fileCompareContents(test_filename=outputName, control_filename=controlName)
        self.assertEqual(len(diff), 0, "File miscompare: {}, {}".format(outputName, controlName))
        os.unlink(outputName)

if __name__ == '__main__':
    unittest.main()
