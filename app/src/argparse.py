
import argparse

def parse() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("file", help="Path to GPS .dat file.")
    return parser.parse_args()
