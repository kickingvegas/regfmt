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
from regfmt import Field
from tests.testutils import auditAttributeExistence, randomAsciiString


class TestField(unittest.TestCase):
    def test_attributes(self):
        field = Field()
        attributes = ['name', 'width', 'leftIndex', 'rightIndex']
        auditAttributeExistence(self, field, attributes)

    def test_init_config(self):
        config = {'name': randomAsciiString(k=10),
                  'width': random.randint(0, 512)}
        field = Field(config=config)

        self.assertEqual(field.name, config['name'])
        self.assertEqual(field.width, config['width'])

        controlLeftIndex = random.randint(0, 512)
        controlRightIndex = random.randint(0, 512)

        field.leftIndex = controlLeftIndex
        field.rightIndex = controlRightIndex

        self.assertEqual(field.leftIndex, controlLeftIndex)
        self.assertEqual(field.rightIndex, controlRightIndex)


if __name__ == '__main__':
    unittest.main()
    
