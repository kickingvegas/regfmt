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

from regfmt.cssstyles import *
from xml.dom.minidom import parseString
from PIL import ImageFont
from collections import UserList
from regfmt import BASE_FONT_NAME

BASE_FONT_SIZE = 12


def bboxWidth(bbox):
    return (bbox[2] - bbox[0])


def bboxHeight(bbox):
    return (bbox[3] - bbox[1])


def matrixMult(X, Y):
    result = [[sum(a*b for a, b in zip(X_row, Y_col)) for Y_col in zip(*Y)] for X_row in X]
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


def numToUnitString(num, unit: str = ''):
    if unit == '':
        result = '{0}'.format(num)
    else:
        result = '{0}{1}'.format(num, unit)
    return result


def cssFontToImageFont(fontFamily, fontSize):
    result = None
    for baseFontname in fontFamily:
        baseFontSize = fontSize

        # !!!: only pt is supported for geometry calculations

        if 'pt' in baseFontSize:
            baseFontSize = int(round(float(baseFontSize.replace('pt', ''))))
        else:
            try:
                baseFontSize = int(float(round(baseFontSize)))
            except:
                message = ('WARNING: body font-size specification of "{}" is unsupported in '
                           'CSS file for sizing the geometry of register fields. '
                           'Coercing font size value to {}pt.\n')
                sys.stderr.write(message.format(fontSize, BASE_FONT_SIZE))
                baseFontSize = BASE_FONT_SIZE

        try:
            result = ImageFont.truetype(baseFontname, baseFontSize)
            break
        except OSError:
            continue

    if result is None:
        result = ImageFont.truetype(BASE_FONT_NAME, baseFontSize)

    return result


def getTextFrame(text, font, anchor='ls', baseDPI=96.0):
    """
    use baseline by default

    scalingFactor adjusts for the screen resolution which presumes 96 DPI.

    :param text:
    :param font:
    :param anchor:
    :return:
    """
    scalingFactor = baseDPI / 64.0
    bbox64 = font.getbbox(text=text, anchor=anchor)
    bbox = tuple(map(lambda x: x * scalingFactor, bbox64))
    length = font.getlength(text=text)
    frame = Frame(x=bbox[0],
                  y=(bbox[1] * -1),
                  width=bboxWidth(bbox),
                  height=bboxHeight(bbox))
    return frame


def getBitFieldSize(font):
    emFrame = getTextFrame(text='M', font=font)
    emFrame.size.width *= 2
    emFrame.size.height *= 4
    return emFrame.size


class Group(UserList):
    def writeDOM(self, children, doc):
        """
        Recursive routine to populate children with all DOM elements corresponding
        to the nodes in this instance of Group.

        :param children: list of DOM elements
        :param doc: SVG XML document
        :return: none
        """
        for element in self.data:
            if isinstance(element, Group):
                element.writeDOM(children, doc)
            else:
                shape: Shape = element
                children.append(shape.writeDOM(doc))

    def translate(self, dx: float = 0.0, dy: float = 0.0):
        for element in self.data:
            if isinstance(element, Group):
                element.translate(dx, dy)
            else:
                # print('translating {0} by {1}, {2}'.format(element, dx, dy))
                shape: Shape = element
                shape.translate(dx, dy)


class Point:
    def __init__(self, x: float = 0.0, y: float = 0.0):
        self.x: float = x
        self.y: float = y


class Size:
    def __init__(self, width: float = 0.0, height: float = 0.0):
        self.width: float = width
        self.height: float = height


class Frame:
    def __init__(self, x: float = 0.0, y: float = 0.0, width: float = 0.0, height: float = 0.0):
        self.origin: Point = Point(x, y)
        self.size: Size = Size(width, height)


class Geometry:
    def writeDOM(self, doc):
        # virtual method; intended to be overridden
        pass

    def translate(self, dx: float = 0.0, dy: float = 0.0):
        # virutal method; indented to be overwritten
        pass


class Shape(Geometry):
    def __init__(self, x: float = 0.0, y: float = 0.0, width: float = 0.0, height: float = 0.0):
        Geometry.__init__(self)
        self.frame: Frame = Frame(x, y, width, height)

    def origin(self):
        return self.frame.origin

    def size(self):
        return self.frame.size

    def setOrigin(self, x: float = 0.0, y: float = 0.0):
        self.frame.origin.x = x
        self.frame.origin.y = y

    def setSize(self, width: float = 0.0, height: float = 0.0):
        self.frame.size.width = width
        self.frame.size.height = height

    def translate(self, dx: float = 0.0, dy: float = 0.0):
        T = translateTransform(dx, dy)
        V = vector2D(self.origin().x, self.origin().y)
        transformedV = matrixMult(T, V)
        newX, newY = coordinateFromVector2D(transformedV)
        self.setOrigin(newX, newY)


class Line(Geometry):
    def __init__(self,
                 x1: float = 0.0,
                 y1: float = 0.0,
                 x2: float = 0.0,
                 y2: float = 0.0,
                 style: LineStyle = LineStyle()):
        Geometry.__init__(self)
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.style: LineStyle = style

    def writeDOM(self, doc):
        lineElement = doc.createElement('line')
        lineElement.setAttribute('x1', str(self.x1))
        lineElement.setAttribute('y1', str(self.y1))
        lineElement.setAttribute('x2', str(self.x2))
        lineElement.setAttribute('y2', str(self.y2))
        lineElement.setAttribute('stroke', self.style.stroke)
        lineElement.setAttribute('stroke-width', self.style.strokeWidth)
        lineElement.setAttribute('stroke-linecap', self.style.strokeLinecap.value)
        return lineElement

    def translate(self, dx: float = 0.0, dy: float = 0.0):
        T = translateTransform(dx, dy)
        V = vector2D(self.x1, self.y1)
        transformedV = matrixMult(T, V)
        newX, newY = coordinateFromVector2D(transformedV)
        self.x1 = newX
        self.y1 = newY

        V = vector2D(self.x2, self.y2)
        transformedV = matrixMult(T, V)
        newX, newY = coordinateFromVector2D(transformedV)
        self.x2 = newX
        self.y2 = newY


class Rect(Shape):
    def __init__(self,
                 x: float = 0.0, y: float = 0.0, width: float = 0.0, height: float = 0.0,
                 style: RectStyle = RectStyle(),
                 ):
        Shape.__init__(self, x, y, width, height)
        self.style: RectStyle = style

    def writeDOM(self, doc):
        rectElement = doc.createElement('rect')
        rectElement.setAttribute('x', str(self.frame.origin.x))
        rectElement.setAttribute('y', str(self.frame.origin.y))
        rectElement.setAttribute('width', str(self.frame.size.width))
        rectElement.setAttribute('height', str(self.frame.size.height))
        rectElement.setAttribute('fill', self.style.fill)
        rectElement.setAttribute('stroke', self.style.stroke)
        rectElement.setAttribute('stroke-width', self.style.strokeWidth)
        rectElement.setAttribute('stroke-linecap', self.style.strokeLinecap.value)
        return rectElement


class Text(Shape):
    def __init__(self,
                 text="something",
                 x: float = 0.0, y: float = 0.0, width: float = 0.0, height: float = 0.0,
                 textAnchor: str = 'start',
                 style: TextStyle = TextStyle()
                 ):

        Shape.__init__(self, x, y, width, height)
        self.text = text
        self.textAnchor = textAnchor
        self.style = style

    def writeDOM(self, doc):
        textElement = doc.createElement('text')
        textElement.setAttribute('x', str(self.frame.origin.x))
        textElement.setAttribute('y', str(self.frame.origin.y))
        textElement.setAttribute('font-size', self.style.fontSize)
        textElement.setAttribute('font-family', ','.join(self.style.fontFamily))
        textElement.setAttribute('font-style', self.style.fontStyle.value)
        textElement.setAttribute('font-weight', self.style.fontWeight.value)
        textElement.setAttribute('text-anchor', self.textAnchor)
        textElement.setAttribute('fill', self.style.fill)

        if '<sub>' in self.text:
            # don't think this is going to work.
            newText = '<p>{}</p>'.format(self.text)
            xmlFragment = parseString(newText)
            textNode = xmlFragment.documentElement

        else:
            textNode = doc.createTextNode(self.text)
        textElement.appendChild(textNode)
        return textElement


if __name__ == '__main__':
    group = Group()
    group.append(Rect((0, 0, 10, 10)))
    group.append(Rect((0, 5, 29, 12)))
    group.append(Text())
    
    topGroup = Group()
    
    topGroup.append(group)
