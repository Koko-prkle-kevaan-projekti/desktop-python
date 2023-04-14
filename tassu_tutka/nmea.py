from datetime import datetime
from typing import Literal, Any
import re


class UnknownSentence(Exception):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class Sentence:
    """Sentence is either a GGA or RMC sentence from GPS.

    If line isn't an understood sentence (GGA or RMC GPS sentence), an UnknownSentence
    exception is raised.

    Sentence can be subscripted like a dict, but doesn't support assignment.

    Valid keys are:
        MSG_TYPE
        MSG_TIME
        MSG_LATTITUDE_GPS
        MSG_LATTITUDAL_HEMISPEHERE
        MSG_LONGITUDE_GPS
        MSG_LONGITUDAL_HEMISPHERE
        MSG_IGNORED_FIELDS
        MSG_LONGITUDE (These are decimal, and don't have minutes like GPS coordinates)
        MSG_LATTITUDE

        RMC_SIGNAL_STATUS
        RMC_SPEED (In knots)
        RMC_SPEED_KMH
        RMC_HEADING
        RMC_DATE

        GGA_FIX
        GGA_NUM_SATELLITES
        GGA_HORIZONTAL_DILUTION
        GGA_ALTITUDE
    """

    _re = re.compile(
        r"""
            \$(?P<MSG_TYPE>GPRMC|GPGGA),
            (?P<MSG_TIME>\d{6}\.\d+),
            (?P<RMC_SIGNAL_STATUS>A|V)?,? # Only in RMC
            (?P<MSG_LATTITUDE_GPS>\d+\.\d+),
            (?P<MSG_LATTITUDAL_HEMISPHERE>N|S),
            (?P<MSG_LONGITUDE_GPS>\d+\.\d+),
            (?P<MSG_LONGITUDAL_HEMISPHERE>E|W),
            (
                (?P<RMC_SPEED>\d+\.\d+), # RMC
                (?P<RMC_HEADING>\d+\.\d*),
                (?P<RMC_DATE>\d{6}), # DDMMYY
                |
                (?P<GGA_FIX>\d), # GGA
                (?P<GGA_NUM_SATELLITES>\d+),
                (?P<GGA_HORIZONTAL_DILUTION>\d+\.\d*),
                (?P<GGA_ALTITUDE>\-?\d+\.\d*),
            )(?P<MSG_IGNORED_FIELDS>.*)$""",
        re.VERBOSE,
    )

    def __init__(self, raw_sentence: str):
        self.raw = raw_sentence.strip()
        self.sentence: dict | None = self._process(self.raw)

    def __str__(self):
        dt: datetime = self["MSG_DATETIME"]
        return f"{dt.day}.{dt.month}.{dt.year}  {dt.hour}:{dt.minute}:{dt.second}"

    def _convert_gps_degrees_to_decimal(
        self, degminsec: str, hemisphere: Literal["N", "E", "S", "W"]
    ) -> float:
        minutes = degminsec[degminsec.index(".") - 2 :]
        degrees = degminsec[: degminsec.index(".") - 2]

        # Convert to numeric and decimal.
        mp = -1 if hemisphere in "SW" else 1  # Multiplier to change sign.
        deg = int(degrees)
        deg += float(minutes) / 60
        deg *= mp
        return deg

    def _process(self, raw: str) -> dict | None:
        ret = self._re.match(raw)
        if not ret:
            raise UnknownSentence("Can't process sentence.")

        # Speed to km/h
        ret = ret.groupdict()
        if ret["MSG_TYPE"] == "GPRMC":
            speed_kmh = float(ret["RMC_SPEED"]) * 1.852
            ret["RMC_SPEED_KMH"] = speed_kmh

        # Minutes and seconds to decimal.
        ret["MSG_LONGITUDE"] = self._convert_gps_degrees_to_decimal(
            ret["MSG_LONGITUDE_GPS"], ret["MSG_LONGITUDAL_HEMISPHERE"]
        )
        ret["MSG_LATTITUDE"] = self._convert_gps_degrees_to_decimal(
            ret["MSG_LATTITUDE_GPS"], ret["MSG_LATTITUDAL_HEMISPHERE"]
        )

        # Time string to datetime
        from datetime import datetime, UTC

        date = ret["RMC_DATE"][:2]
        month = ret["RMC_DATE"][2:4]
        year = ret["RMC_DATE"][4:]

        hour = ret["MSG_TIME"][:2]
        minute = ret["MSG_TIME"][2:4]
        second = ret["MSG_TIME"][4:6]

        ret["MSG_DATETIME"] = datetime(
            int(year),
            int(month),
            int(date),
            int(hour),
            int(minute),
            int(second),
            tzinfo=UTC,
        )

        return ret

    def __getitem__(self, item) -> Any:
        return self.sentence[item]
