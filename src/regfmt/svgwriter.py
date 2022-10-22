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

from xml.dom.minidom import getDOMImplementation
from regfmt import TopLevel, FieldNameAlign
from regfmt import Register
from regfmt.svggeometry import *
from regfmt.cssparser import parseCSS, cascadeStyles
from regfmt.centeralignlayout import writeFieldNameCenterSVG
from regfmt.stairleftlayout import writeStairLeftSVG

class SVGWriter:
    def __init__(self, registerDB: TopLevel, outfile, configFileName=None):
        self.registerDB = registerDB
        self.outfile = outfile
        self.styleSheet = StyleSheet()
        try:
            parseCSS(configFileName=configFileName, styleSheet=self.styleSheet)
        except FileNotFoundError as err:
            message = 'ERROR: {}: "{}"  Exiting…\n'.format(err.strerror, err.filename)
            sys.stderr.write(message)
            sys.exit(err.errno)

        except ValueError as err:
            message = 'ERROR: {} Exiting…\n'.format(err.args[0])
            sys.stderr.write(message)
            sys.exit(1)


        cascadeStyles(self.styleSheet)
        self.font = cssFontToImageFont(fontFamily=self.styleSheet.body.fontFamily,
                                       fontSize=self.styleSheet.body.fontSize)

    def createDocument(self, origin=None, size=None):
        dom = getDOMImplementation()
        doc = dom.createDocument(None, 'svg', None)
        topElement = doc.documentElement
        topElement.setAttribute('version', '1.1')
        topElement.setAttribute('xmlns', "http://www.w3.org/2000/svg")
        if origin:
            topElement.setAttribute('x', str(origin.x))
            topElement.setAttribute('y', str(origin.y))

        if size:
            topElement.setAttribute('width', str(size.width))
            topElement.setAttribute('height', str(size.height))

        return doc, topElement


    def compositeSVG(self, doc, topElement, topGroup, outfile):
        children = []
        topGroup.writeDOM(children, doc)
        for child in children:
            topElement.appendChild(child)
        doc.writexml(outfile, encoding='utf-8', addindent="  ", newl="\n")

    def writeSVG(self, registerDB: TopLevel = None):
        if registerDB is None:
            registerDB = self.registerDB

        # Layout Geometry - all decisions on the graphical layout of a register instance are done here.

        # Initialize container for geometry
        topGroup = Group()
        if registerDB.layout.fieldNameAlign == FieldNameAlign.center:
            origin, size = writeFieldNameCenterSVG(registerDB=registerDB,
                                                   topGroup=topGroup,
                                                   styleSheet=self.styleSheet,
                                                   font=self.font)

        elif registerDB.layout.fieldNameAlign == FieldNameAlign.stairLeft:
            origin, size = writeStairLeftSVG(registerDB=registerDB,
                                             topGroup=topGroup,
                                             styleSheet=self.styleSheet,
                                             font=self.font)
            #origin, size = self.writeFieldNameStairLeftSVG(registerDB, topGroup)

        doc, topElement = self.createDocument(origin=origin, size=size)

        # Write DOM and composite to SVG
        self.compositeSVG(doc, topElement, topGroup, self.outfile)

    def writeFieldNameStairLeftSVG(self, registerDB, topGroup):
        registers: [Register] = registerDB.registers
        bitFieldSize = self.getBitFieldSize(self.font)
        # Generate groups, each group holding a single register
        # layoutGeometry, transformGeometry, writeDOM, compositeSVG
        for register in registers:
            # define untransformed geometry for register
            registerHeight = bitFieldSize.height
            registerWidth = bitFieldSize.width * register.width

            registerGroup = Group()
            topGroup.append(registerGroup)

            if register.name is not None:
                registerNameBbox = self.font.getbbox(register.name, anchor='lt')
                registerNameHeight = bboxHeight(registerNameBbox)
                registerNameWidth = bboxWidth(registerNameBbox)
                registerGroup.append(Text(register.name,
                                          x=registerWidth + 10,
                                          y=registerNameHeight + (registerHeight / 2.0) - (registerNameHeight / 2.0),
                                          style=self.styleSheet.registerName
                                          ))

            displacementX = 0
            fieldDisplacementY = 0

            fieldNames = list(filter(lambda x: x is not None, [field.name for field in register.fields]))
            fieldCount = len(fieldNames)
            fieldNameHeight = 0

            for name in fieldNames:
                fieldNameBbox = self.font.getbbox(name, anchor='la')
                fieldNameHeight = bboxHeight(fieldNameBbox)
                break

            fieldDisplacementY = (fieldNameHeight + 10.0) * (fieldCount)

            for field in register.fields:
                fieldWidth = field.width * bitFieldSize.width
                fieldHeight = registerHeight

                fieldX = 0
                fieldY = 0

                T = translateTransform(displacementX, 0.0)
                V = vector2D(fieldX, fieldY)
                transformedV = matrixMult(T, V)
                fieldX, fieldY = coordinateFromVector2D(transformedV)

                registerGroup.append(Rect(x=fieldX,
                                          y=fieldY,
                                          width=fieldWidth,
                                          height=fieldHeight,
                                          style=self.styleSheet.field))

                # TODO: support stair layout

                fieldNameBbox = self.font.getbbox(field.name, anchor='la')
                fieldNameHeight = bboxHeight(fieldNameBbox)
                fieldNameWidth = bboxWidth(fieldNameBbox)

                # print(fieldDisplacementY)
                registerGroup.append(Text(field.name,
                                          x=fieldNameBbox[0] + (fieldWidth / 2.0) + displacementX + 3,
                                          y=fieldNameBbox[3] + fieldDisplacementY + fieldNameHeight + 10,
                                          textAnchor='left',
                                          style=self.styleSheet.fieldName
                                          ))
                fieldDisplacementY -= (fieldNameHeight + 10.0)

                # Draw Line
                registerGroup.append(Line(x1=displacementX + (fieldWidth / 2.0),
                                          y1=registerHeight,
                                          x2=displacementX + (fieldWidth / 2.0),
                                          y2=fieldNameBbox[3] + fieldDisplacementY + fieldNameHeight * 2 + 15,
                                          style=self.styleSheet.fieldNameLine))

                if field.width > 1:
                    registerGroup.append(Text(str(field.leftIndex),
                                              x=fieldX + 3,
                                              y=fieldY + fieldHeight - 3,
                                              textAnchor='start',
                                              style=self.styleSheet.fieldIndex
                                              ))

                    registerGroup.append(Text(str(field.rightIndex),
                                              x=fieldX + fieldWidth - 3,
                                              y=fieldY + fieldHeight - 3,
                                              textAnchor='end',
                                              style=self.styleSheet.fieldIndex
                                              ))
                else:
                    registerGroup.append(Text(str(field.leftIndex),
                                              x=fieldX + (fieldWidth / 2.0),
                                              y=fieldY + fieldHeight - 3,
                                              textAnchor='middle',
                                              style=self.styleSheet.fieldIndex
                                              ))

                displacementX += fieldWidth

            # break
        # Transform Geometry

        # TODO: need to fix stairLeft for multiple registers

        displacementY = 0
        for group in topGroup:
            group.translate(0, displacementY)
            displacementY += (fieldNameHeight + 10.0) * (fieldCount)

        # TODO: implement this for real.
        #origin = Point()
        #size = Size(width=registerWidth + registerNameWidth + 20,
        #height=registerHeight)

        return (None, None)
