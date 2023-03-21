import unittest
import tassu_tutka.nmea as nmea
import sys

class TestNMEAMessages(unittest.TestCase):

    def setUp(self):
        self.test_string = """
        $GPGGA,194530.000,3051.8007,N,10035.9989,W,1,4,2.18,746.4,M,-22.2,M,,*6B
        $GPRMC,194530.000,A,3051.8007,N,10035.9989,W,1.49,111.67,310714,,,A*74
        """

    def test_sentence(self):
        for line in self.test_string.strip().splitlines():
            sentence = nmea.Sentence(line.strip())
            self.assertEqual(sentence["MSG_TIME"], "194530.000")
            if sentence["MSG_TYPE"] == "GPRMC":
                self.assertAlmostEqual(sentence["MSG_LATTITUDE"], 30.863345, delta=0.000002)
                self.assertAlmostEqual(sentence["MSG_LONGITUDE"], -100.5999817, delta=0.0000004)
                
            if sentence["MSG_TYPE"] == "GPGGA":
                self.assertAlmostEqual(sentence["MSG_LATTITUDE"], 30.863345, delta=0.000002)
                self.assertAlmostEqual(sentence["MSG_LONGITUDE"], -100.5999817, delta=0.0000004)
    

if __name__ == '__main__':
    unittest.main()
