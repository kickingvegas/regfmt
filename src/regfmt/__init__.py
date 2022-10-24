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
from os import uname
VERSION = '0.9.0'
BASE_FONT_NAME = 'Helvetica'

unameObj = uname()
if unameObj.sysname == 'Linux':
    BASE_FONT_NAME = 'FreeSans'
elif unameObj.sysname == 'Windows':
    BASE_FONT_NAME = 'Arial'

from .InputLoadAndValidate import InputLoadAndValidate
from .Constants import Constants
from .Endian import Endian
from .Field import Field
from .Register import Register
from .TopLevel import FieldNameAlign, RegisterLayout, Layout, TopLevel
from .DRCChecker import DRCChecker
from .cssstyles import *
from .svggeometry import *
from .svgwriter import SVGWriter
from .centeralignlayout import *
from .stairleftlayout import *
from .CommandLineParser import CommandLineParser
from .RegisterTemplate import *
from .RegisterFormat import RegisterFormat

def main():
    app = RegisterFormat(CommandLineParser().run())
    return app.run()
