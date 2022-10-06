from collections import UserList

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

class Bounds:
    def __init__(self, bbox=(0.0, 0.0, 0.0, 0.0)):
        x1, y1, x2, y2 = bbox
        width = x2 - x1
        height = y2 - y1
        
        self.origin: Point = Point(x1, y1)
        self.size: Size = Size(width, height)

class Shape:
    def __init__(self, bbox=(0.0, 0.0, 0.0, 0.0)):
        self.bounds: Bounds = Bounds(bbox=bbox)

    def setWidth(self, width: float=0.0):
        self.bounds.size.width = width
        
    def setHeight(self, height: float=0.0):
        self.bounds.size.height = height

    def setX(self, x: float=0.0):
        self.bounds.origin.x = x
        
    def setY(self, y: float=0.0):
        self.bounds.origin.y = y
        

class Rect(Shape):
    def __init__(self, bbox=(0.0, 0.0, 0.0, 0.0)):
        Shape.__init__(self, bbox=bbox)
        # have a bunch of attributes?
        pass

class Text(Shape):
    def __init__(self, text="something"):
        # calculate bbox 
        Shape.__init__(self)
        pass
    

if __name__ == '__main__':
    
    group = Group()
    group.append(Rect((0, 0, 10, 10)))
    group.append(Rect((0, 5, 29, 12)))
    group.append(Text())
    
    topGroup = Group()
    
    topGroup.append(group)
    


        
