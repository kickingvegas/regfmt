import os
import sys

import tinycss2
from regfmtlib.cssstyles import *

def parseCSS(configFileName: str, styleSheet: StyleSheet):

    if configFileName is not None and os.path.exists(configFileName):
        with open(configFileName, 'r') as configFile:
            css = configFile.read()
            rules = tinycss2.parse_stylesheet(css, skip_comments=True, skip_whitespace=True)
            for rule in rules:
                className = rule.prelude[0].value

                if className not in ('body', 'register', 'field', 'register-name', 'field-name', 'field-index'):
                    continue

                elif className == 'body':
                    pass

                elif className in ('register', 'field'):
                    pass

                elif className in ('register-name', 'field-name', 'field-index'):
                    pass


                declarations = tinycss2.parse_declaration_list(rule.content,
                                                               skip_comments=True,
                                                               skip_whitespace=True)

                parseErrors = filter(lambda x: isinstance(x, tinycss2.ast.ParseError), declarations)
                for parseError in parseErrors:
                    message = 'ERROR: {}: line {}, col {}: {}\nExiting.\n'.format(configFileName,
                                                                  parseError.source_line,
                                                                  parseError.source_column,
                                                                  parseError.message)


                    sys.stderr.write(message)
                    sys.exit(1)


                for declaration in declarations:

                    try:
                        for value in declaration.value:
                            if isinstance(value, tinycss2.ast.DimensionToken):
                                print(value.value, value.unit)

                        print('   {0}: {1} {2}'.format(declaration.name, declaration.value,
                                                       tinycss2.serialize(declaration.value).strip()))

                    except:
                        # TODO: Need to handle all the exceptions.
                        print('hunh')
