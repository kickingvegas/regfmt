from regfmtlib.cssstyles import *

from collections import UserList

def bboxWidth(bbox):
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

def numToUnitString(num, unit: str=''):
    if unit == '':
        result = '{0}'.format(num)
    else:
        result = '{0}{1}'.format(num, unit)
    return result

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

    def translate(self, dx: float=0.0, dy: float=0.0):
        for element in self.data:
            if isinstance(element, Group):
                element.translate(dx, dy)
            else:
                #print('translating {0} by {1}, {2}'.format(element, dx, dy))
                shape: Shape = element
                shape.translate(dx, dy)

class Point:
    def __init__(self, x: float=0.0, y: float=0.0):
        self.x: float = x
        self.y: float = y

class Size:
    def __init__(self, width: float=0.0, height: float=0.0):
        self.width: float = width
        self.height: float = height

class Frame:
    def __init__(self, x: float = 0.0, y: float = 0.0, width: float = 0.0, height: float = 0.0):
        self.origin: Point = Point(x, y)
        self.size: Size = Size(width, height)

class Shape:
    def __init__(self, x: float = 0.0, y: float = 0.0, width: float = 0.0, height: float = 0.0):
        self.frame: Frame = Frame(x, y, width, height)

    def origin(self):
        return self.frame.origin

    def size(self):
        return self.frame.size

    def setOrigin(self, x: float=0.0, y: float=0.0):
        self.frame.origin.x = x
        self.frame.origin.y = y

    def setSize(self, width: float=0.0, height: float=0.0):
        self.frame.size.width = width
        self.frame.size.height = height

    def writeDOM(self, doc):
        # virtual method; intended to be overridden
        pass

    def translate(self, dx: float=0.0, dy: float=0.0):
        T = translateTransform(dx, dy)
        V = vector2D(self.origin().x, self.origin().y)
        transformedV = matrixMult(T, V)
        newX, newY = coordinateFromVector2D(transformedV)
        self.setOrigin(newX, newY)

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
        rectElement.setAttribute('stroke-width', str(self.style.strokeWidth))
        rectElement.setAttribute('stroke-linecap', self.style.strokeLinecap.value)
        return rectElement

class Text(Shape):
    def __init__(self,
                 text="something",
                 x: float = 0.0, y: float = 0.0, width: float = 0.0, height: float = 0.0,
                 textAnchor: str='start',
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
        textElement.setAttribute('text-anchor', self.textAnchor)
        textElement.setAttribute('fill', self.style.fill)

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
    


        
