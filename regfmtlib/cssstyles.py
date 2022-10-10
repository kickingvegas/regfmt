from enum import Enum

class StrokeLinecap(Enum):
    butt = 'butt'
    round = 'round'
    square = 'square'

class FontStyle(Enum):
    normal = 'normal'
    italic = 'italic'
    oblique = 'oblique'

class FontWeight(Enum):
    normal = 'normal'
    bold = 'bold'
    bolder = 'bolder'
    lighter = 'lighter'

class TextStyle:
    def __init__(self,
                 fontFamily: [str] = None,
                 fontSize: str = None,
                 fontStyle: FontStyle=None,
                 fontWeight: str = None,
                 fill: str = None):
        self.fontFamily = fontFamily
        self.fontSize = fontSize
        self.fontStyle = fontStyle
        self.fontWeight = fontWeight
        self.fill = fill

class RectStyle:
    def __init__(self,
                 fill: str=None,
                 stroke: str=None,
                 strokeWidth: str=None,
                 strokeLinecap: StrokeLinecap = None
                 ):
        # CSS color type
        self.fill: str = fill
        # CSS color type
        self.stroke: str = stroke
        self.strokeWidth: str = strokeWidth
        self.strokeLinecap: StrokeLinecap = strokeLinecap

class BaseStyle(TextStyle, RectStyle):
    def __init__(self):
        TextStyle.__init__(self,
                           fontFamily=['Futura', 'Helvetica', 'Arial', 'sans-serif'],
                           fontSize='12pt',
                           fontStyle=FontStyle.normal,
                           fontWeight=FontWeight.normal,
                           fill='black')

        RectStyle.__init__(self,
                           fill='none',
                           stroke='black',
                           strokeWidth='0.5',
                           strokeLinecap=StrokeLinecap.butt)

class StyleSheet:
    def __init__(self):
        self.body = BaseStyle()
        self.register = RectStyle()
        self.field = RectStyle()
        self.registerName = TextStyle()
        self.fieldName = TextStyle()
        self.fieldIndex = TextStyle(fontSize='10pt')
