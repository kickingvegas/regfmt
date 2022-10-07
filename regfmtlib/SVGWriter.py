import sys
from xml.dom.minidom import getDOMImplementation
from regfmtlib import TopLevel
from regfmtlib import Register
from PIL import ImageFont
from regfmtlib.SVGgeometry import *

BASE_FONT_SIZE = 12


class SVGWriter:
    def __init__(self, registerDB: TopLevel, outfile):
        self.registerDB = registerDB
        self.outfile = outfile
        self.font = ImageFont.truetype('Helvetica', 12)

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
        

        # Layout Geometry
        for register in registers:
            # define untransformed geometry for register
            registerHeight = bitFieldSize.height

            registerGroup = Group()
            topGroup.append(registerGroup)

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

                registerGroup.append(Rect(x=fieldX, y=fieldY, width=fieldWidth, height=fieldHeight))

                fieldNameBbox = self.font.getbbox(field.name, anchor='la')
                fieldNameHeight = bboxHeight(fieldNameBbox)
                fieldNameWidth = bboxWidth(fieldNameBbox)

                registerGroup.append(Text(field.name,
                                          x=fieldNameBbox[0] + (fieldWidth/2.0) + displacementX,
                                          y=fieldNameBbox[3] + (fieldHeight/2.0) - (fieldNameHeight/2.0),
                                          textAnchor='middle'
                                          ))

                registerGroup.append(Text(str(field.leftIndex),
                                          x=fieldX + 3,
                                          y=fieldY + fieldHeight - 3,
                                          fontSize='10pt',
                                          textAnchor='start'
                                          ))

                registerGroup.append(Text(str(field.rightIndex),
                                          x=fieldX + fieldWidth - 3,
                                          y=fieldY + fieldHeight - 3,
                                          fontSize='10pt',
                                          textAnchor='end'
                                          ))

                displacementX += fieldWidth

            #break

        # 
        topGroup.flatten(children, doc)
        self.compositeSVG(doc, topElement, children, self.outfile)

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

    # deprecated    
    def oldWriteSVG(self):
        #self.writeScratch()

        doc, topElement = self.createDocument()

        children = []
        
        registers: [Register] = self.registerDB.registers
        registerNames: [string] = [register.name for register in registers]

        cx = self.font.getlength('M') * 3
        cBbox = self.font.getbbox('M', anchor='lt')


        cx = bboxLength(cBbox) * 2
        cy = bboxHeight(cBbox) * 4

        displacementY = 0
        for register in registers:
            registerWidth = register.width * cx
            registerHeight = cy

            displacementX = 0
            for field in register.fields:
                fieldWidth = field.width * cx
                fieldHeight = registerHeight

                fieldX = 0
                fieldY = 0

                #print((fieldX, fieldY, fieldWidth, fieldHeight), field.name)

                T = translateTransform(displacementX, displacementY)
                V = vector2D(fieldX, fieldY)

                tranformedV = matrixMult(T, V)
                #print(coordinateFromVector2D(tranformedV), (fieldWidth, fieldHeight))
                # self.renderField(field)

                fieldX, fieldY = coordinateFromVector2D(tranformedV)

                children.append(self.writeRect(doc,
                                               x=fieldX,
                                               y=fieldY,
                                               width=fieldWidth,
                                               height=fieldHeight,
                                               strokeWidth="0.5"))

                # write field name

                fieldNameBbox = self.font.getbbox(field.name, anchor='la')
                fieldNameHeight = bboxHeight(fieldNameBbox)
                fieldNameWidth = bboxLength(fieldNameBbox)

                #print(fieldNameBbox)

                fieldNameX = fieldNameBbox[0] + (fieldWidth/2.0) + displacementX
                # cheat? need to know what the actual bounding box is here.
                fieldNameY = fieldNameBbox[3] + (fieldHeight/2.0) - (fieldNameHeight/2.0) + displacementY

                #print(fieldNameX, fieldNameY)

                e = self.writeText(doc,
                                   field.name,
                                   x=str(fieldNameX),
                                   y=str(fieldNameY),
                                   textAnchor='middle')

                children.append(e)

                fieldLeftIndexX = fieldX + 3
                fieldLeftIndexY = fieldY + fieldHeight - 3

                eLeft = self.writeText(doc,
                                       str(field.leftIndex),
                                       x=str(fieldLeftIndexX),
                                       y=str(fieldLeftIndexY),
                                       fontSize='10pt',
                                       textAnchor='start')
                children.append(eLeft)

                fieldRightIndexX = fieldX + fieldWidth - 3
                fieldRightIndexY = fieldY + fieldHeight - 3

                eRight = self.writeText(doc,
                                        str(field.rightIndex),
                                        x=str(fieldRightIndexX),
                                        y=str(fieldRightIndexY),
                                        fontSize='10pt',
                                        textAnchor='end')
                children.append(eRight)

                displacementX += fieldWidth

            displacementY += (fieldHeight + fieldHeight/2.0)

        self.compositeSVG(doc, topElement, children, self.outfile)

    def compositeSVG(self, doc, topElement, children, outfile):
        for child in children:
            topElement.appendChild(child)
        doc.writexml(self.outfile, encoding='utf-8', addindent="  ", newl="\n")

    # deprecated
    def writeRect(self,
                  doc,
                  x=0,
                  y=0,
                  width=0,
                  height=0,
                  fill='none',
                  stroke='black',
                  strokeWidth='1',
                  strokeLinecap='square'):
        rectElement = doc.createElement('rect')
        rectElement.setAttribute('x', str(x))
        rectElement.setAttribute('y', str(y))
        rectElement.setAttribute('width', str(width))
        rectElement.setAttribute('height', str(height))
        rectElement.setAttribute('fill', fill)
        rectElement.setAttribute('stroke', stroke)
        rectElement.setAttribute('stroke-width', strokeWidth)
        rectElement.setAttribute('stroke-linecap', strokeLinecap)
        return rectElement

    # deprecated
    def writeText(self,
                  doc,
                  value,
                  x="0",
                  y="0",
                  fontSize="12pt",
                  fontFamily="Futura, Helvetica, sans-serif",
                  textAnchor="start",
                  fill="black"):
        # x, y are the lower left baseline of the text
        textElement = doc.createElement('text')
        textElement.setAttribute('x', x)
        textElement.setAttribute('y', y)
        textElement.setAttribute('font-size', fontSize)
        textElement.setAttribute('font-family', fontFamily)
        textElement.setAttribute('text-anchor', textAnchor)
        textElement.setAttribute('fill', fill)

        textNode = doc.createTextNode(value)
        textElement.appendChild(textNode)
        return textElement
