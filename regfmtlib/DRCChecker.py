from regfmtlib import Register
from regfmtlib import Field
from regfmtlib import TopLevel
from regfmtlib import Endian
from operator import add
from functools import reduce
import sys

class DRCChecker:
    def __init__(self):
        self.foo = None
        self.errors = []


    def check(self, registerDB: TopLevel):
        # TODO: this should be a throwing method
        self.checkFieldWidths(registerDB)

    def checkFieldWidths(self, registerDB: TopLevel):
        registers: [Register] = registerDB.registers

        for register in registers:
            fields: [Field] = register.fields
            widths = [x.width for x in fields]
            sum = reduce(add, widths)
            if sum != register.width:
                message = 'DRC Violation: sum total of widths of fields ({0}) must equal the register width ({1}) for register {2}\n'.format(sum, register.width, register.name)
                self.errors.append(message)
            else:
                sys.stderr.write(repr(widths) + '\n')

        for message in self.errors:
            sys.stderr.write(message)

        return self.errors

    # TODO: check that field names do not repeat
    # TODO: check that fields are byte-sized for bigByte and littleByte

    def subIndexFields(self, registerDB: TopLevel):
        registers: [Register] = registerDB.registers

        for register in registers:
            endian = register.endian
            if endian in (Endian.bigBit.value, Endian.bigByte.value):
                count = register.width
            elif endian in (Endian.littleBit.value, Endian.littleByte.value):
                count = -1
            fields: [Field] = register.fields

            for field in fields:
                if endian in (Endian.bigBit.value, Endian.bigByte.value):
                    count -= 1
                    field.leftIndex = count
                    count -= (field.width - 1)
                    field.rightIndex = count
                    #print('{0}:{1} {2}'.format(field.leftIndex, field.rightIndex, field.name))

                elif endian == Endian.littleBit.value:
                    count += 1
                    field.leftIndex = count
                    count += (field.width - 1)
                    field.rightIndex = count
                    #print('{0}:{1} {2}'.format(field.leftIndex, field.rightIndex, field.name))

                elif endian == Endian.littleByte.value:
                    count += 1
                    field.rightIndex = count
                    count += (field.width - 1)
                    field.leftIndex = count
                    #print('{0}:{1} {2}'.format(field.leftIndex, field.rightIndex, field.name))

            #print('###')



