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


class Field:
    def __init__(self, config=None):
        self.name: str = None
        self.width: int = None
        self.leftIndex: int = None
        self.rightIndex: int = None

        # !!!: Note config should already be validated.
        if config:
            if 'name' in config:
                self.name = config['name']
            if 'width' in config:
                self.width = config['width']
