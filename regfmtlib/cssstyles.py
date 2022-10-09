from enum import Enum

class StrokeLinecap(Enum):
    butt = 'butt'
    round = 'round'
    square = 'square'

class FontStyle(Enum):
    normal = 'normal'
    italic = 'italic'
    oblique = 'oblique'

class TextStyle:
    def __init__(self,
                 fontFamily: [str]=['Futura', 'Helvetica', 'Arial', 'Verdana', 'sans-serif'],
                 fontSize: str = '12pt',
                 fontStyle: FontStyle=FontStyle.normal,
                 fill: str = 'black'):
        self.fontFamily = fontFamily
        self.fontSize = fontSize
        self.fontStyle = fontStyle
        self.fill = fill

class RectStyle:
    def __init__(self,
                 fill: str='none',
                 stroke: str='black',
                 strokeWidth: float=0.5,
                 strokeLinecap: StrokeLinecap = StrokeLinecap.butt
                 ):
        # CSS color type
        self.fill: str = fill
        # CSS color type
        self.stroke: str = stroke
        self.strokeWidth: float = strokeWidth
        self.strokeLinecap: StrokeLinecap = strokeLinecap

class BaseStyle(TextStyle, RectStyle):
    def __init__(self):
        TextStyle.__init__(self)
        RectStyle.__init__(self)

class StyleSheet:
    def __init__(self):
        self.body = BaseStyle()
        self.register = RectStyle()
        self.field = RectStyle()
        self.registerName = TextStyle()
        self.fieldName = TextStyle()
        self.fieldIndex = TextStyle(fontSize='10pt')
