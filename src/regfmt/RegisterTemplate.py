#!/usr/bin/env python3
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
import os
import sys
import errno
from yaml import dump

WATERMARK = 'regfmt https://github.com/kickingvegas/regfmt'

CSS_TEMPLATE = """/**
 regfmt example CSS file
 */

body {
    font-family: Futura, Helvetica, Arial, Verdana, FreeSans;
    font-size: 12pt;
    font-style: normal;
    font-weight: normal;
    fill: white;
    stroke: black;
    stroke-width: 0.5;
    stroke-linecap: butt;
}

/*
register {
    fill: red;
    stroke: magenta;
    stroke-width: 0.1;
    stroke-linecap: butt;
}

field {
    fill: cyan;
    stroke: black;
    stroke-width: 0.3;
    stroke-linecap: butt;
}

field-name-line {
    stroke: orange;
    stroke-width: 1;
    stroke-linecap: butt;
}

register-name {
    font-size: 12pt;
    fill: black;
}

field-name {
    font-family: Helvetica;
    font-style: normal;
    font-weight: normal;
    font-size: 12pt;
    fill: blue;
}

field-index {
    font-size: 10pt;
    font-style: normal;
    font-weight: bold;
    fill: blue;
}
*/
"""


def write_yaml_template(outfile_name: str = 'template.yaml'):
    obj = {}

    obj['width'] = 8
    obj['endian'] = 'bigBit'

    registers = []

    register = {}
    register['name'] = 'R1'

    fields = []
    for index in range(4):
        field = {}
        field['name'] = 'A{}'.format(index)
        field['width'] = int(obj['width'] / 4)
        fields.append(field)

    register['fields'] = fields
    registers.append(register)

    obj['registers'] = registers

    obj['layout'] = {'field-name-align': 'stair-left'}

    if os.path.exists(outfile_name):
        sys.stderr.write('ERROR: {} exists. Please rename. Exiting…\n'.format(outfile_name))
        return errno.EEXIST

    with open('template.yaml', 'w') as outfile:
        outfile.write('# {}\n\n'.format(WATERMARK))
        dump(obj, outfile)
    return 0


def write_css_template(outfile_name: str = 'template.css'):
    if os.path.exists(outfile_name):
        sys.stderr.write('ERROR: {} exists. Please rename. Exiting…\n'.format(outfile_name))
        return errno.EEXIST
    
    with open(outfile_name, 'w') as outfile:
        outfile.write(CSS_TEMPLATE)
    return 0


def write_yaml_css_templates(template_type: str = 'css',
                             outfile_name: str = 'template.yaml',
                             outfile_css_name: str = 'template.css'):
    if template_type == 'css':
        return write_css_template(outfile_name=outfile_css_name)
    elif template_type == 'yaml':
        return write_yaml_template(outfile_name=outfile_name)
    elif template_type == 'yamlcss':
        result = write_css_template(outfile_name=outfile_css_name)
        result = result | write_yaml_template(outfile_name=outfile_name)
        return result
    else:
        raise ValueError('ERROR: undefined templateType: {}'.format(template_type))
