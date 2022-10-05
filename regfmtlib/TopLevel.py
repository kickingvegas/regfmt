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
