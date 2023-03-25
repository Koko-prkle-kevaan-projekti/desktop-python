import argparse
import os
import logging
import threading
import socketserver
import time
import sys
import functools
import platform
import pathlib
import lock
import tassu_tutka.error as error

_TX_PORT = 65000


def _add_pid_to_pidfile(pid: int | None = None):
    if "windows" in platform.platform().lower():
        raise error.WindowsError("Wrong os")
    if not pid:
        pid = os.getpid()
    home = os.getenv("HOME")
    with open(f"{home}/ttutka.pid", "a+") as fh:
        fh.write(f"{pid}\n")


def _remove_pid_from_pidfile(pid: int | None = None):
    if not pid:
        pid = os.getpid()
    home = os.getenv("HOME")
    with open(f"{home}/ttutka.pid", "r") as fh:
        pids = [x for x in fh.readlines() if x.strip() != str(pid)]
    with open(f"{home}/ttutka.pid", "w") as fh:
        fh.writelines(pids)


def _get_pids_from_pidfile():
    home = os.getenv("HOME")
    with open(f"{home}/ttutka.pid", "r") as fh:
        pids = [x.strip() for x in fh.readlines()]
    return pids


class RxHandler(socketserver.StreamRequestHandler):
    buffer_file_path = pathlib.Path("/tmp/ttutka.tmp")

    def handle(self) -> None:
        if not self.buffer_file_path.exists():
            self.buffer_file_path.touch(mode=0o600, exist_ok=False)
        while True:
            # Write to locked file, if available.
            line = self.rfile.readline().decode("utf-8")
            if line:
                lock.lock(filepath=self.buffer_file_path)
                with self.buffer_file_path.open("a", encoding="utf-8") as fh:
                    fh.write(line)
                lock.unlock(self.buffer_file_path)
            else:
                time.sleep(0.5)


def serve(options):
    import signal
    import tassu_tutka.api as tassapi

    _add_pid_to_pidfile()

    # Starting socket server for GPS device.
    logging.info(f"Starting Rx server in port {options.gps_listener_port}. Waiting for a GPS device.")
    rx = socketserver.TCPServer(
        (options.gps_listener_addr, int(options.gps_listener_port)), RxHandler
    )
    t_rx = threading.Thread(group=None, target=rx.serve_forever)
    t_rx.start()

    # Starting client api.
    logging.info("Starting client API.")
    t_api = threading.Thread(group=None, target=tassapi.run, args=(options,))
    t_api.daemon = True
    t_api.start()

    def quit_(
        a: socketserver.TCPServer,
        a_thread: threading.Thread,
        sig,
        frame,
    ):
        a.shutdown()
        a.server_close()
        _remove_pid_from_pidfile()

    quit_ = functools.partial(quit_, rx, t_rx)
    signal.signal(signal.SIGINT, quit_)
    signal.signal(signal.SIGHUP, quit_)
    logging.info(
        "Use CTRL-C or send SIGHUP to terminate: `ttutka server stop`"
    )
    t_api.join()
