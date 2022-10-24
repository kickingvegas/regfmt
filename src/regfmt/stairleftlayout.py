from regfmt.svggeometry import *
from regfmt import Register


def writeStairLeftSVG(registerDB, topGroup, styleSheet, font, registerSpacing=5):
    bitFieldSize = getBitFieldSize(font=font)

    registers: [Register] = registerDB.registers
    parentOrigin = Point()
    parentSize = Size(height=(bitFieldSize.height + registerSpacing) * len(registers))

    maxFieldDisplacementYs = []
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

        fieldNames = list(filter(lambda x: x is not None, [field.name for field in register.fields]))
        fieldCount = len(fieldNames)

        fieldFrames = tuple(map(lambda x: getTextFrame(text=x, font=styleSheet.fieldName.truetype()), fieldNames))
        fieldHeights = tuple(map(lambda x: x.size.height, fieldFrames))
        maxFieldHeight = max(fieldHeights)

        fieldDisplacementY = (maxFieldHeight + 10.0) * fieldCount
        maxFieldDisplacementYs.append(fieldDisplacementY)

        counter = 0
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

            if field.name:
                fieldNameFrame = fieldFrames[counter]

                fieldNameX = (fieldWidth / 2.0) + displacementX + 3.0
                fieldNameY = fieldHeight + fieldNameFrame.origin.y + fieldDisplacementY + 10.0

                newParentWidth = fieldNameX + fieldNameFrame.size.width
                if parentSize.width < newParentWidth:
                    parentSize.width = newParentWidth

                registerGroup.append(Text(text=field.name,
                                          x=fieldNameX,
                                          y=fieldNameY,
                                          textAnchor='left',
                                          style=styleSheet.fieldName))

                registerGroup.append(Line(x1=displacementX + (fieldWidth / 2.0),
                                          y1=registerHeight,
                                          x2=displacementX + (fieldWidth / 2.0),
                                          y2=fieldNameY,
                                          style=styleSheet.fieldNameLine))

                fieldDisplacementY -= (maxFieldHeight + 10)

                if parentSize.height < fieldNameY:
                    parentSize.height = fieldNameY

                counter += 1

            displacementX += fieldWidth

    counter2 = 0
    for group in topGroup:
        group.translate(0, displacementY)
        displacementY += (bitFieldSize.height * 2.0 + registerSpacing + maxFieldDisplacementYs[counter2])
        if parentSize.height < displacementY:
            parentSize.height = displacementY
        counter2 += 1

    return (parentOrigin, parentSize)

