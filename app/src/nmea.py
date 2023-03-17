from datetime import datetime
from typing import Literal, Union
from abc import ABC
import re


class Sentence(dict):
    """Sentence is either a GGA or RMC sentence from GPS.
    """

    _re = re.compile(r"""
            \$(?P<MSG_TYPE>GPRMC|GPGGA),
            (?P<MSG_TIME>\d{6}\.\d{3}),
            (?P<MSG_SIGNAL_STATUS>A|V)?,? # Only in RMC
            (?P<MSG_LATTITUDE>\d+\.\d+),
            (?P<MSG_LATTITUDAL_HEMISPHERE>N|S),
            (?P<MSG_LONGITUDE>\d+\.\d+),
            (?P<MSG_LONGITUDAL_HEMISPHERE>E|W),
            (
                (?P<MSG_SPEED>\d+\.\d+), # RMC
                (?P<MSG_HEADING>\d+\.\d*),
                (?P<MSG_DATE>\d{6}), # DDMMYY
                |
                (?P<MSG_FIX>\d), # GGA
                (?P<MSG_NUM_SATELLITES>\d+),
                (?P<MSG_HORIZONTAL_DILUTION>\d+\.\d*),
                (?P<MSG_ALTITUDE>\-?\d+\.\d*),
            )(?P<MSG_IGNORED_FIELDS>.*)$""", re.VERBOSE)

    def __init__(self, raw_sentence: str):
        self.raw = raw_sentence
        self.sentence = self._process()
    
    def _process(self):
        self.sentence = _re.match(self.raw.strip())
