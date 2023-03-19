import argparse


def parse() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    subcommands = parser.add_subparsers(required=True)
    client_cmd = subcommands.add_parser("client", add_help=True, help="Client options.")
    exclusives = client_cmd.add_mutually_exclusive_group(required=True)
    exclusives.add_argument(
        "--gui", action="store_true", help="Launch graphical interface."
    )
    exclusives.add_argument("--ifile", action="store", help="Path to GPS .dat file.")
    server_cmd = subcommands.add_parser("server", add_help=True, help="Server options.")
    server_cmd.add_argument(
        "start",
        action="store",
        help="Start server. Supports .env file for loading env vars.",
    )
    server_cmd.add_argument(
        "--port",
        nargs=1,
        action="store",
        help="Port to listen to. Use environment variable TT_BIND_PORT if absent, or default to 65000",
        default=65000
    )
    server_cmd.add_argument(
        "--address",
        nargs=1,
        action="store",
        help="Address to bind to. Use environment variable TT_BIND_ADDRESS if absent, or default to 0.0.0.0",
        default="0.0.0.0"
    )
    client_cmd.add_argument(
        "--ofile",
        action="store",
        help="Path to GeoJSON output file. Optional. Defaults to stdout.",
    )
    return parser.parse_args()
