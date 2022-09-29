import unittest

from regfmtlib import CommandLineParser

class TestCommandLineParser(unittest.TestCase):
    def test_version(self):
        clp = CommandLineParser()
        parsedArgs = clp.parser.parse_args(['-v'])
        self.assertTrue(parsedArgs.version)

    def test_arbitaryInput(self):
        control = 'inputHeyThere.yaml'
        clp = CommandLineParser()
        parsedArgs = clp.parser.parse_args([control])
        self.assertEqual(parsedArgs.input, control)

    def test_defaultInput(self):
        control = 'input.yaml'
        clp = CommandLineParser()
        parsedArgs = clp.parser.parse_args([])
        self.assertEqual(parsedArgs.input, control)
        
if __name__ == '__main__':
    unittest.main()
