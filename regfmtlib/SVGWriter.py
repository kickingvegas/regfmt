import sys
from xml.dom.minidom import getDOMImplementation
from regfmtlib import TopLevel
from regfmtlib import Register
from PIL import ImageFont

BASE_FONT_SIZE = 12

def bboxLength(bbox):
    return (bbox[2] - bbox[0])

def bboxHeight(bbox):
    return (bbox[3] - bbox[1])

def matrixMult(X, Y):
    result = [[sum(a*b for a,b in zip(X_row,Y_col)) for Y_col in zip(*Y)] for X_row in X]
    return result

def translateTransform(x, y):
    result = [[1.0, 0.0, x],
              [0.0, 1.0, y],
              [0.0, 0.0, 1.0]]
    return result

def vector2D(x, y):
    result = [[x], [y], [1.0]]
    return result

def coordinateFromVector2D(V):
    result = (V[0][0], V[1][0])
    return result

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

        self.renderSVG(doc, topElement, children, self.outfile)

    def renderSVG(self, doc, topElement, children, outfile):
        for child in children:
            topElement.appendChild(child)
        doc.writexml(self.outfile, encoding='utf-8', addindent="  ", newl="\n")

    def writeScratch(self):
        self.outfile.write('hey they clittiak\n')

        registers: [Register] = self.registerDB.registers
        registerNames: [string] = [register.name for register in registers]

        print(registerNames)

        for register in registers:
            registerName = register.name
            fieldNames: [string] = [field.name for field in register.fields]
            fieldIndexes = [(str(field.leftIndex), str(field.rightIndex)) for field in register.fields]

            print(fieldNames, registerName, fieldIndexes)

            for name in fieldNames:
                bbox = self.font.getbbox(name)
                length = self.font.getlength(name)
                print(name, bbox, length)

        

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
