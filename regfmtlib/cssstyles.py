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
                 fontStyle: FontStyle = None,
                 fontWeight: FontWeight = None,
                 fill: str = None):
        self.fontFamily = fontFamily
        self.fontSize = fontSize
        self.fontStyle = fontStyle
        self.fontWeight = fontWeight
        self.fill = fill


class LineStyle:
    def __init__(self,
                 stroke: str = 'grey',
                 strokeWidth: str = '0.5',
                 strokeLinecap: StrokeLinecap = StrokeLinecap.butt
                 ):
        self.stroke: str = stroke
        self.strokeWidth: str = strokeWidth
        self.strokeLinecap: StrokeLinecap = strokeLinecap


class RectStyle:
    def __init__(self,
                 fill: str = None,
                 stroke: str = None,
                 strokeWidth: str = None,
                 strokeLinecap: StrokeLinecap = None
                 ):
        # TODO: support fill opacity
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
        self.fieldNameLine = LineStyle()
