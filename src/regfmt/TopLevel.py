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

from regfmt import Constants
from regfmt import Register
from regfmt import Endian
from enum import Enum

DEFAULT_WIDTH = Constants.DEFAULT_WIDTH


class FieldNameAlign(Enum):
    center = "center"
    stairLeft = 'stair-left'


class RegisterLayout(Enum):
    tb = "tb"


class Layout:
    def __init__(self,
                 fieldNameAlign: FieldNameAlign = FieldNameAlign.center,
                 registerLayout: RegisterLayout = RegisterLayout.tb):
        self.fieldNameAlign: FieldNameAlign = fieldNameAlign
        self.registerLayout: RegisterLayout = registerLayout


class TopLevel:
    def __init__(self, config=None, width: int = DEFAULT_WIDTH, endian: Endian = Endian.bigByte):
        self.width: int = width
        self.endian: Endian = endian
        self.registers: [Register] = []
        self.layout = Layout()

        if config:
            self.width = config['width']
            self.endian = config['endian']

            if 'registers' in config:
                for registerConfig in config['registers']:
                    self.registers.append(Register(self, registerConfig))

            if 'layout' in config:
                if 'field-name-align' in config['layout']:
                    self.layout.fieldNameAlign = FieldNameAlign(config['layout']['field-name-align'])

                if 'register-layout' in config['layout']:
                    self.layout.registerLayout = RegisterLayout(config['layout']['register-layout'])
