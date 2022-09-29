from jsonschema import validate, exceptions
from yaml import Loader, Dumper, load, safe_load
from yaml.scanner import ScannerError
import sys

INPUT_SCHEMA_YAML="""
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
      registers:
        enum:
          - tb
          - lr

      register_name:
        enum:
          - left
          - right
          - top
          - bottom
          - null
      field_name:
        enum:
          - center
          - left
          - right

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
        type: string
      width:
        type: integer
    required:
      - width

  register:
    type: object
    properties:
      name:
        type: string
      width:
        type: integer

      endian:
        $ref: "#/$defs/endian"

      fields:
        type: array
        items:
          $ref: "#/$defs/field"

    required:
      - name
      - fields
"""

class InputLoadAndValidate:
    def __init__(self, parsedArguments):
        self.parsedArguments = parsedArguments
        inputYAML = self.loadInput()
        schemaYAML = self.loadInputSchema()

        try:
            result = validate(inputYAML, schemaYAML)
            if result is None:
                print("yaml validated")
            else:
                # this should never happen
                print('wtf')

        except exceptions.ValidationError as err:
            print(err.json_path)
            print(err.message)
            print(err.path)
            print(err.relative_path)
            print(err.absolute_path)
            print(err.context)
            print(err.cause)
            print(err.instance)
            print(err.validator)
            print(err.schema_path)
            print(dir(err))
        

    def loadInput(self):
        with open(self.parsedArguments.input, 'r') as infile:
            try:
                yamlConfig = load(infile, Loader=Loader)
            except ScannerError as err:
                sys.stderr.write('ERROR: {0}\n'.format(err))
                sys.exit(1)

        return yamlConfig

    
    def loadInputSchema(self):
        try:
            yamlConfig = safe_load(INPUT_SCHEMA_YAML)
        except ScannerError as err:
            sys.stderr.write('ERROR: {0}\n'.format(err))
            sys.exit(1)


        return yamlConfig


        
        
    
