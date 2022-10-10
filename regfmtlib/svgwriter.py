import os
from xml.dom.minidom import getDOMImplementation
from regfmtlib import TopLevel
from regfmtlib import Register
from PIL import ImageFont
import tinycss2
from regfmtlib.cssstyles import *
from regfmtlib.svggeometry import *
from regfmtlib.cssparser import parseCSS, cascadeStyles

BASE_FONT_SIZE = 12

class SVGWriter:
    def __init__(self, registerDB: TopLevel, outfile, configFileName=None):
        self.registerDB = registerDB
        self.outfile = outfile
        self.styleSheet = StyleSheet()
        parseCSS(configFileName=configFileName, styleSheet=self.styleSheet)
        cascadeStyles(self.styleSheet)

        baseFontname = self.styleSheet.body.fontFamily[0]
        baseFontSize = self.styleSheet.body.fontSize

        # TODO: figure out a cleaner mapping of CSS font size to ImageFont
        if 'pt' in baseFontSize:
            baseFontSize = int(float(baseFontSize.replace('pt', '')))

        else:
            # give up
            baseFontSize = 12

        self.font = ImageFont.truetype(baseFontname, baseFontSize)

    def createDocument(self):
        dom = getDOMImplementation()
        doc = dom.createDocument(None, 'svg', None)
        topElement = doc.documentElement
        topElement.setAttribute('version', '1.1')
        topElement.setAttribute('xmlns', "http://www.w3.org/2000/svg")
        return doc, topElement

    def writeSVG(self):
        doc, topElement = self.createDocument()
        children = []

        registers: [Register] = self.registerDB.registers
        bitFieldSize = self.getBitFieldSize(self.font)

        # Initialize container for geometry
        topGroup = Group()

        # Generate groups, each group holding a single register
        # layoutGeometry, transformGeometry, writeDOM, compositeSVG

        # Layout Geometry - all decisions on the graphical layout of a register instance are done here.
        for register in registers:
            # define untransformed geometry for register
            registerHeight = bitFieldSize.height
            registerWidth = bitFieldSize.width * register.width

            registerGroup = Group()
            topGroup.append(registerGroup)

            if register.name is not None:
                registerNameBbox = self.font.getbbox(register.name, anchor='lt')
                registerNameHeight = bboxHeight(registerNameBbox)
                registerGroup.append(Text(register.name,
                                          x = registerWidth + 10,
                                          y = registerNameHeight + (registerHeight/2.0) - (registerNameHeight / 2.0),
                                          style=self.styleSheet.registerName
                                          ))

            displacementX = 0
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

                if field.name is not None:
                    fieldNameBbox = self.font.getbbox(field.name, anchor='la')
                    fieldNameHeight = bboxHeight(fieldNameBbox)
                    fieldNameWidth = bboxWidth(fieldNameBbox)

                    registerGroup.append(Text(field.name,
                                              x=fieldNameBbox[0] + (fieldWidth/2.0) + displacementX,
                                              y=fieldNameBbox[3] + (fieldHeight/2.0) - (fieldNameHeight/2.0),
                                              textAnchor='middle',
                                              style=self.styleSheet.fieldName
                                              ))

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

                displacementX += fieldWidth

            #break

        # Transform Geometry
        displacementY = 0
        for group in topGroup:
            group.translate(0, displacementY)
            displacementY += (bitFieldSize.height + 5)

        # Write DOM and composite to SVG
        self.compositeSVG(doc, topElement, topGroup, self.outfile)

    def getBitFieldSize(self, font):
        """
        Return unit size of a bit field to be rendered in SVG.

        :param font:
        :return: instance of Size()
        """
        bbox = font.getbbox('M', anchor='lt')
        x = bbox[0]
        y = bbox[1]
        width = bboxWidth(bbox) * 2
        height = bboxHeight(bbox) * 4
        return Size(width, height)

    def compositeSVG(self, doc, topElement, topGroup, outfile):
        children = []
        topGroup.writeDOM(children, doc)
        for child in children:
            topElement.appendChild(child)
        doc.writexml(outfile, encoding='utf-8', addindent="  ", newl="\n")
