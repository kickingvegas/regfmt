import os
import sys

import tinycss2
from regfmtlib.cssstyles import *

classNameMap = {
                'register-name': 'registerName',
                'field-name': 'fieldName',
                'field-index': 'fieldIndex'
                }

def parseCSS(configFileName: str, styleSheet: StyleSheet):
    if configFileName is None:
        return

    if not os.path.exists(configFileName):
        # TODO: throw error; file does not exist
        return

    css = None
    with open(configFileName, 'r') as configFile:
        css = configFile.read()

    if css is None:
        # TODO: throw error; empty file
        return

    rules = tinycss2.parse_stylesheet(css, skip_comments=True, skip_whitespace=True)
    for rule in rules:
        # Extract declarations
        declarations = tinycss2.parse_declaration_list(rule.content,
                                                       skip_comments=True,
                                                       skip_whitespace=True)

        filterDeclarationErrors(configFileName, declarations)

        className = rule.prelude[0].value
        #print(className)

        if className not in ('body', 'register', 'field', 'register-name', 'field-name', 'field-index'):
            # list of legal names
            continue

        elif className == 'body':
            legalAttributes = ('font-family', 'font-size', 'font-style', 'font-weight',
                               'fill',
                               'stroke', 'stroke-width', 'stroke-linecap')
            for declaration in declarations:
                if declaration.name not in legalAttributes:
                    continue

                elif declaration.name == 'font-family':
                    styleSheet.body.fontFamily = extractFontFamily(declaration)

                elif declaration.name == 'font-size':
                    styleSheet.body.fontSize = extractFontSize(declaration)
                    styleSheet.registerName.fontSize = styleSheet.body.fontSize
                    styleSheet.fieldName.fontSize = styleSheet.body.fontSize
                    # TODO: deal with fieldIndex

                elif declaration.name == 'font-style':
                    styleSheet.body.fontStyle = extractEnum(declaration, FontStyle)

                elif declaration.name == 'font-weight':
                    styleSheet.body.fontWeight = extractEnum(declaration, FontWeight)

                elif declaration.name == 'fill':
                    styleSheet.body.fill = extractColor(declaration)

                elif declaration.name == 'stroke':
                    styleSheet.body.stroke = extractColor(declaration)

                elif declaration.name == 'stroke-width':
                    styleSheet.body.strokeWidth = extractDimensionalValue(declaration)

                elif declaration.name == 'stroke-linecap':
                    styleSheet.body.strokeLinecap = extractEnum(declaration, StrokeLinecap)

        elif className in ('register', 'field'):
            for declaration in declarations:
                if declaration.name == 'fill':
                    getattr(styleSheet, className).fill = extractColor(declaration)

                elif declaration.name == 'stroke':
                    getattr(styleSheet, className).stroke = extractColor(declaration)

                elif declaration.name == 'stroke-width':
                    getattr(styleSheet, className).strokeWidth = extractDimensionalValue(declaration)

                elif declaration.name == 'stroke-linecap':
                    getattr(styleSheet, className).strokeLinecap = extractEnum(declaration, StrokeLinecap)

        elif className in ('register-name', 'field-name', 'field-index'):
            for declaration in declarations:
                if declaration.name == 'font-family':
                    getattr(styleSheet, classNameMap[className]).fontFamily = extractFontFamily(declaration)

                elif declaration.name == 'font-size':
                    getattr(styleSheet, classNameMap[className]).fontSize = extractFontSize(declaration)

                elif declaration.name == 'font-style':
                    getattr(styleSheet, classNameMap[className]).fontStyle = extractEnum(declaration, FontStyle)

                elif declaration.name == 'font-weight':
                    getattr(styleSheet, classNameMap[className]).fontWeight = extractEnum(declaration, FontWeight)


def cascadeStyles(styleSheet):
    ## Cascade styles in StyleSheet
    # body > register, field if property.value is None
    # body > register-name, field-name, field-index if property.value is None
    # cascade rect style
    for obj in [styleSheet.register, styleSheet.field]:
        if getattr(obj, 'fill') is None:
            setattr(obj, 'fill', styleSheet.body.fill)
        if getattr(obj, 'stroke') is None:
            setattr(obj, 'stroke', styleSheet.body.stroke)
        if getattr(obj, 'strokeWidth') is None:
            setattr(obj, 'strokeWidth', styleSheet.body.strokeWidth)
        if getattr(obj, 'strokeLinecap') is None:
            setattr(obj, 'strokeLinecap', styleSheet.body.strokeLinecap)
    # cascade body text styles to child styles
    for obj in [styleSheet.registerName, styleSheet.fieldName, styleSheet.fieldIndex]:
        if getattr(obj, 'fontFamily') is None:
            setattr(obj, 'fontFamily', styleSheet.body.fontFamily)

        if getattr(obj, 'fontStyle') is None:
            setattr(obj, 'fontStyle', styleSheet.body.fontStyle)

        if getattr(obj, 'fontWeight') is None:
            setattr(obj, 'fontWeight', styleSheet.body.fontWeight)
        # !!!: Because fill attribute used for both text and rect with different semantics, using rect.stroke value for text.fill
        if getattr(obj, 'fill') is None:
            setattr(obj, 'fill', styleSheet.body.stroke)


def extractEnum(declaration, enumClass):
    value = None
    tokens = list(
        filter(lambda x: isinstance(x, tinycss2.ast.IdentToken), declaration.value))
    if len(tokens) == 0:
        # TODO: throw error
        pass
    token = tokens[0]
    if token.value in [x.value for x in list(enumClass)]:
        value = token.lower_value
    else:
        # TODO: throw error
        pass
    return enumClass[token.value]

def extractDimensionalValue(declaration):
    value = None
    tokens = list(
        filter(lambda x: (isinstance(x, tinycss2.ast.IdentToken) or
                          isinstance(x, tinycss2.ast.DimensionToken) or
                          isinstance(x, tinycss2.ast.NumberToken)),
                          declaration.value))
    if len(tokens) == 0:
        # TODO: throw error
        pass
    token = tokens[0]
    if isinstance(token, tinycss2.ast.IdentToken):
        value = token.lower_value
    elif isinstance(token, tinycss2.ast.DimensionToken):
        value = '{}{}'.format(token.value, token.lower_unit)
    elif isinstance(token, tinycss2.ast.NumberToken):
        value = str(token.value)
    return value

def extractColor(declaration):
    tokens = list(
        filter(lambda x: (isinstance(x, tinycss2.ast.IdentToken) or
                          isinstance(x, tinycss2.ast.HashToken)),
               declaration.value))
    if len(tokens) == 0:
        # TODO: throw error
        pass
    token = tokens[0]
    if isinstance(token, tinycss2.ast.IdentToken):
        value = token.lower_value
    else:
        value = '#{}'.format(token.value)
    return value

def extractFontSize(declaration):
    tokens = list(
        # TODO: handle just number
        filter(lambda x: isinstance(x, tinycss2.ast.DimensionToken), declaration.value))
    if len(tokens) == 0:
        # TODO: throw error
        pass
    token = tokens[0]
    value = '{}{}'.format(token.value, token.unit)
    return value

def extractFontFamily(declaration):
    tokens = filter(lambda x: isinstance(x, tinycss2.ast.IdentToken), declaration.value)
    return [x.value for x in tokens]

def filterDeclarationErrors(configFileName, declarations):
    parseErrors = filter(lambda x: isinstance(x, tinycss2.ast.ParseError), declarations)
    for parseError in parseErrors:
        message = 'ERROR: {}: line {}, col {}: {}\nExiting.\n'.format(configFileName,
                                                                      parseError.source_line,
                                                                      parseError.source_column,
                                                                      parseError.message)

        sys.stderr.write(message)
        sys.exit(1)