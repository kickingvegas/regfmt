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

from regfmtlib import Constants
from regfmtlib import Register
from regfmtlib import Endian

DEFAULT_WIDTH = Constants.DEFAULT_WIDTH

class TopLevel:
    def __init__(self, config=None):
        self.width: int = DEFAULT_WIDTH
        self.endian: Endian = Endian.bigByte
        self.registers: [Register] = []

        if config:
            self.width = config['width']
            self.endian = config['endian']

            if 'registers' in config:
                for registerConfig in config['registers']:
                    self.registers.append(Register(self, registerConfig))
