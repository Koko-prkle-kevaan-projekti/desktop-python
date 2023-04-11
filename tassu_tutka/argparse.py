import argparse


def parse() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    subcommands = parser.add_subparsers(required=True)

    # Client stuff
    client_cmd = subcommands.add_parser("client", add_help=True, help="Client options.")
    client_cmd.add_argument(
        "cmd",
        action="store",
        nargs=1,
        choices=("gui", "mkrequest"),
        help="Launch user interface or make an api request.",
    )
    client_cmd.add_argument("--server-address", action="store", help="Server address will be saved to ~/.ttutka.dotenv")
    client_cmd.add_argument("--server-port", action="store", help="Server port will be saved to ~/.ttutka.dotenv")

    # Server stuff
    server_cmd = subcommands.add_parser("server", add_help=True, help="Server options.")
    server_cmd.add_argument(
        "cmd",
        action="store",
        nargs=1,
        choices=("start", "stop", "restart", "kill"),
        help=(
            "Start, stop, restart or kill a server. Note that restart doesn't inherit"
            + " options of previous process."
        ),
    )
    server_cmd.add_argument(
        "--daemon",
        action="store_true",
        help="Daemonize the server",
    )

    # Logging related opts
    logging_ = server_cmd.add_argument_group("Logging")
    logging_.add_argument(
        "--log-level",
        choices=("debug", "info", "warning", "error", "critical"),
        action="store",
        help="Set the server logging level. Default=warning",
        default="warning",
        dest="log_level",
    )
    logging_.add_argument(
        "--log-file",
        nargs=1,
        action="store",
        help="Path to the log file",
        default="/var/log/ttutka.log",
        dest="log_file",
    )

    # Socket binding related opts.
    server_sock = server_cmd.add_argument_group("Address and port configuration")
    server_sock.add_argument(
        "--gps-listener-addr",
        action="store",
        default="0.0.0.0",
        help="Address to listen to. Default=0.0.0.0",
    )
    server_sock.add_argument(
        "--gps-listener-port",
        action="store",
        default=65000,
        help="TCP port to listen",
    )
    server_sock.add_argument(
        "--api-addr",
        action="store",
        default="0.0.0.0",
        help="API service address. Default=0.0.0.0",
    )
    server_sock.add_argument(
        "--api-port",
        action="store",
        default="8000",
        help="API service port. Default=8000",
    )

    return parser.parse_args()
