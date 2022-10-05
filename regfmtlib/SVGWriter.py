import sys
from xml.dom.minidom import getDOMImplementation
from regfmtlib.TopLevel import TopLevel
from regfmtlib.Register import Register
from PIL import ImageFont

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
        #self.writeScratch()

        doc, topElement = self.createDocument()
        
        # append all new nodes to topElement
        field0 = self.writeRect(doc, x=0, y=0, width=100, height=50, stroke='black')
        field1 = self.writeRect(doc, x=100, y=0, width=100, height=50, stroke='black')
        text0 = self.writeText(doc, "A1", x='0', y='0.5in')

        children = [field0, field1, text0]
        for child in children:
            topElement.appendChild(child)

        doc.writexml(self.outfile, encoding='utf-8', addindent = "  ", newl="\n")
        

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
                  textAnchor="left",
                  fill="blue"):
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
