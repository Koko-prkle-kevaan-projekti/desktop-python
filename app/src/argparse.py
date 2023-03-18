
import argparse

def parse() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    exclusives = parser.add_mutually_exclusive_group()
    exclusives.required = True
    exclusives.add_argument("--gui", action="store_true", help="Launch graphical interface.")
    exclusives.add_argument("--ifile", action="store", help="Path to GPS .dat file.")
    parser.add_argument("--ofile", action="store", help="Path to GeoJSON output file. Optional. Defaults to stdout.")
    return parser.parse_args()
