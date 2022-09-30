from regfmtlib import TopLevel
from regfmtlib import Constants
from regfmtlib import Endian
from regfmtlib import Field

DEFAULT_WIDTH = Constants.Constants.DEFAULT_WIDTH

class Register:
    def __init__(self, parent: TopLevel, config=None, width: int=DEFAULT_WIDTH, endian: Endian=Endian.bigByte):
        self.name: str = None
        self.width: int = DEFAULT_WIDTH
        self.endian: Endian = endian
        self.fields: [Field] = None
        self.parent: TopLevel = parent
        if config:
            self.initFromConfig(config)

    def initFromConfig(self, config):
        self.name = config['name']
        self.width = config['width'] if 'width' in config else self.parent.width
        self.endian = config['endian'] if 'endian' in config else self.parent.endian

        if 'fields' in config:
            fields = []
            for fieldConfig in config['fields']:
                field = Field.Field(config=fieldConfig)
                fields.append(field)

            self.fields = fields
