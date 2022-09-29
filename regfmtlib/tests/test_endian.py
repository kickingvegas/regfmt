import unittest
from regfmtlib.ConfigurationFactory import Endian

class TestEndian(unittest.TestCase):
    def test_littleByte(self):
        self.assertEqual(Endian.littleByte.value, "littleByte")

    def test_bigByte(self):
        self.assertEqual(Endian.bigByte.value, "bigByte")
        
    def test_littleBit(self):
        self.assertEqual(Endian.littleBit.value, "littleBit")

    def test_bigBit(self):
        self.assertEqual(Endian.bigBit.value, "bigBit")


if __name__ == '__main__':
    unittest.main()
    
