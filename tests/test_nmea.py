import unittest
import app.src.nmea as nmea

class TestStringMethods(unittest.TestCase):

    def setUp(self):
        self.test_string = """
        $GPGGA,194530.000,3051.8007,N,10035.9989,W,1,4,2.18,746.4,M,-22.2,M,,*6B
        $GPRMC,194530.000,A,3051.8007,N,10035.9989,W,1.49,111.67,310714,,,A*74
        """

    def test_regex(self):
        for line in self.test_string.splitlines():
            try:
                print(nmea._re.match(line.strip()).groupdict())
            except AttributeError as e:
                pass

if __name__ == '__main__':
    unittest.main()
