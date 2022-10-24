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
from regfmt import Endian


class TestEndian(unittest.TestCase):
    def test_littleByte(self):
        self.assertEqual(Endian.littleByte.value, "littleByte")

    def test_bigByte(self):
        self.assertEqual(Endian.bigByte.value, "bigByte")
        
    def test_littleBit(self):
        self.assertEqual(Endian.littleBit.value, "littleBit")

    def test_bigBit(self):
        self.assertEqual(Endian.bigBit.value, "bigBit")


if __name__ == '__main__':
    unittest.main()
    
