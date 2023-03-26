import platform
import threading
import signal
import functools
from typing import List
from tassu_tutka.api import ClientApi
from socketserver import TCPServer


def register_signal_handlers(
    socket_server: tuple[TCPServer, threading.Thread], should_quit: List[bool]
):
    if "windows" in platform.platform().lower():
        return  # Windows doesn't do unix signals.

    def signal_handler(
        socket_server: TCPServer,
        socket_server_t: threading.Thread,
        should_quit: List,
        sig,
        frame,
    ):
        should_quit.append(True)
        # Quit socket server.
        socket_server.shutdown()
        socket_server.server_close()
        socket_server_t.join()

        # Quit api server quit is handled by using context manager in server.py.

    signal_handler = functools.partial(
        signal_handler, socket_server[0], socket_server[1], should_quit
    )

    h0 = signal.signal(signal.SIGINT, signal_handler)
    if not "windows" in platform.platform().lower():
        h1 = signal.signal(signal.SIGHUP, signal_handler)
