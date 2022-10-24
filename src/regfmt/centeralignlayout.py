from regfmt.svggeometry import *
from regfmt import Register


def writeFieldNameCenterSVG(registerDB, topGroup, styleSheet, font, registerSpacing=5):
    bitFieldSize = getBitFieldSize(font=font)

    registers: [Register] = registerDB.registers
    parentOrigin = Point()
    parentSize = Size(height=(bitFieldSize.height + registerSpacing) * len(registers))

    displacementY = 0

    for register in registers:
        registerGroup = Group()
        topGroup.append(registerGroup)

        registerHeight = bitFieldSize.height
        registerWidth = bitFieldSize.width * register.width

        if register.name:
            registerNameFrame = getTextFrame(text=register.name, font=styleSheet.registerName.truetype())

            x = registerWidth + 10
            y = registerNameFrame.size.height + (registerHeight/2.0) - (registerNameFrame.size.height/2.0)

            registerGroup.append(Text(text=register.name,
                                      x=x,
                                      y=y,
                                      style=styleSheet.registerName))

            newParentWidth = x + registerNameFrame.size.width
            if parentSize.width < newParentWidth:
                parentSize.width = newParentWidth

        displacementX = 0

        for field in register.fields:
            fieldWidth = field.width * bitFieldSize.width
            fieldHeight = registerHeight

            T = translateTransform(displacementX, 0.0)
            V = vector2D(0.0, 0.0)
            transformedV = matrixMult(T, V)
            fieldX, fieldY = coordinateFromVector2D(transformedV)

            registerGroup.append(Rect(x=fieldX,
                                      y=fieldY,
                                      width=fieldWidth,
                                      height=fieldHeight,
                                      style=styleSheet.field))

            if field.name:
                fieldNameFrame = getTextFrame(text=field.name, font=styleSheet.fieldName.truetype())

                fieldNameX = (fieldWidth / 2.0) + displacementX
                fieldNameY = fieldNameFrame.origin.y + (fieldHeight / 2.0) - (fieldNameFrame.size.height / 2.0)

                registerGroup.append(Text(text=field.name,
                                          x=fieldNameX,
                                          y=fieldNameY,
                                          textAnchor='middle',
                                          style=styleSheet.fieldName))

            if field.width > 1:
                registerGroup.append(Text(str(field.leftIndex),
                                          x=fieldX + 3,
                                          y=fieldY + fieldHeight - 3,
                                          textAnchor='start',
                                          style=styleSheet.fieldIndex
                                          ))

                registerGroup.append(Text(str(field.rightIndex),
                                          x=fieldX + fieldWidth - 3,
                                          y=fieldY + fieldHeight - 3,
                                          textAnchor='end',
                                          style=styleSheet.fieldIndex
                                          ))
            else:
                registerGroup.append(Text(str(field.leftIndex),
                                          x=fieldX + (fieldWidth / 2.0),
                                          y=fieldY + fieldHeight - 3,
                                          textAnchor='middle',
                                          style=styleSheet.fieldIndex
                                          ))

            displacementX += fieldWidth

    for group in topGroup:
        group.translate(0, displacementY)
        displacementY += (bitFieldSize.height + registerSpacing)

    return (parentOrigin, parentSize)

