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
from regfmt import Register, Field, TopLevel, Constants, Endian
from tests.testutils import auditAttributeExistence, randomAsciiString


class TestRegister(unittest.TestCase):
    def test_attributes(self):
        topLevel = TopLevel()
        register = Register(parent=topLevel)

        attributes = ['name', 'width', 'endian', 'fields', 'parent']
        auditAttributeExistence(self, register, attributes)

        self.assertEqual(register.width, Constants.DEFAULT_WIDTH)
        self.assertEqual(register.endian, Endian.bigBit)
        self.assertEqual(register.parent, topLevel)

    def test_init_config(self):
        config = { 'name': randomAsciiString(k=10),
                   'width' : random.randint(0, 512),
                   'endian' : Endian.littleBit }

        fields = [ {'name': randomAsciiString(k=random.randint(1, 8)),
                    'width': random.randint(1, 512)}]
        config['fields'] = fields

        register = Register(parent=TopLevel(), config=config)

        self.assertEqual(register.name, config['name'])
        self.assertEqual(register.width, config['width'])
        self.assertEqual(register.endian, config['endian'])

        for field in register.fields:
            self.assertIsInstance(field, Field)


if __name__ == '__main__':
    unittest.main()
    
