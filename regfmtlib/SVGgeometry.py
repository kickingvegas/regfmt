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

class Group(UserList):
    def render(self):
        pass

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

class Rect(Shape):
    def __init__(self,
                 x: float = 0.0, y: float = 0.0, width: float = 0.0, height: float = 0.0,
                 fill = 'none',
                 stroke = 'black',
                 strokeWidth = 1,
                 strokeLinecap = 'square'
                 ):
        Shape.__init__(self, x, y, width, height)
        self.fill = fill
        self.stroke = stroke
        self.strokeWidth = strokeWidth
        self.strokeLinecap = strokeLinecap

    def writeDOM(self, doc):
        rectElement = doc.createElement('rect')
        rectElement.setAttribute('x', str(self.frame.origin.x))
        rectElement.setAttribute('y', str(self.frame.origin.y))
        rectElement.setAttribute('width', str(self.frame.size.width))
        rectElement.setAttribute('height', str(self.frame.size.height))
        rectElement.setAttribute('fill', self.fill)
        rectElement.setAttribute('stroke', self.stroke)
        rectElement.setAttribute('stroke-width', str(self.strokeWidth))
        rectElement.setAttribute('stroke-linecap', self.strokeLinecap)
        return rectElement


class Text(Shape):
    def __init__(self,
                 text="something",
                 x: float = 0.0, y: float = 0.0, width: float = 0.0, height: float = 0.0,
                 fontSize="12pt",
                 fontFamily="Futura, Helvetica, sans-serif",
                 textAnchor="start",
                 fill="black"
                 ):

        Shape.__init__(self, x, y, width, height)
        self.text = text
        self.fontSize = fontSize
        self.fontFamily = fontFamily
        self.textAnchor = textAnchor
        self.fill = fill

    def writeDOM(self, doc):
        textElement = doc.createElement('text')
        textElement.setAttribute('x', str(self.frame.origin.x))
        textElement.setAttribute('y', str(self.frame.origin.y))
        textElement.setAttribute('font-size', self.fontSize)
        textElement.setAttribute('font-family', self.fontFamily)
        textElement.setAttribute('text-anchor', self.textAnchor)
        textElement.setAttribute('fill', self.fill)

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
    


        
