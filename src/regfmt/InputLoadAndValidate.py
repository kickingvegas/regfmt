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

from jsonschema import validate
from yaml import Loader, load, safe_load

INPUT_SCHEMA_YAML = """
type: object
properties: 
  width:
     type: integer
     minimum: 1

  endian:
     $ref: "#/$defs/endian"

  registers:
     type: array
     items:
       $ref: "#/$defs/register"

  layout:
    type: object
    properties:
      field-name-align:
        enum:
          - center
          - stair-left

required:
  - width
  - registers
  - endian

$defs:
  endian:
    enum:
      - littleByte
      - bigByte
      - littleBit
      - bigBit

  field:
    type: object
    properties:
      name:
        type: 
          - string
          - "null"
      width:
        type: integer
    required:
      - width

  register:
    type: object
    properties:
      name:
        type: 
          - string
          - "null"
      width:
        type: integer

      endian:
        $ref: "#/$defs/endian"

      fields:
        type: array
        items:
          $ref: "#/$defs/field"

    required:
      - fields
"""


class InputLoadAndValidate:
    def __init__(self, parsedArguments):
        self.parsedArguments = parsedArguments

    def loadAndValidate(self):
        inputYAML = self.loadInput(self.parsedArguments)
        schemaYAML = self.loadInputSchema(INPUT_SCHEMA_YAML)
        validate(inputYAML, schemaYAML)
        return inputYAML
        
    def loadInput(self, parsedArguments):
        with open(parsedArguments.input, 'r') as infile:
            yamlConfig = load(infile, Loader=Loader)
        return yamlConfig

    def loadInputSchema(self, schemaString):
        yamlConfig = safe_load(schemaString)
        return yamlConfig
