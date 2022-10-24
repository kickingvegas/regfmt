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
from regfmt import Endian
from regfmt import Field

DEFAULT_WIDTH = Constants.DEFAULT_WIDTH


class Register:
    def __init__(self, parent, config=None, width: int = DEFAULT_WIDTH, endian: Endian = Endian.bigBit):
        self.name: str = None
        self.width: int = width
        self.endian: Endian = endian
        self.fields: [Field] = None
        # parent is type TopLevel
        self.parent = parent
        if config:
            self.initFromConfig(config)

    def initFromConfig(self, config):
        self.name = config['name']
        self.width = config['width'] if 'width' in config else self.parent.width
        self.endian = config['endian'] if 'endian' in config else self.parent.endian

        if 'fields' in config:
            fields = []
            for fieldConfig in config['fields']:
                field = Field(config=fieldConfig)
                fields.append(field)

            self.fields = fields
