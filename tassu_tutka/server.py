import os
import logging
import threading
import socketserver
from socketserver import BaseRequestHandler, BaseServer
import time
import functools
import platform
import pathlib
from functools import partialmethod
from typing import Any, Callable, Self

class PidFileHandlerFunctions :

    @staticmethod
    def _add_pid_to_pidfile(pid: int | None = None):
        if not pid:
            pid = os.getpid()
        home = os.getenv("HOME")
        with open(f"{home}/ttutka.pid", "w") as fh:
            fh.write(f"{pid}\n")

    @staticmethod
    def _remove_pid_from_pidfile(pid: int | None = None):
        if not pid:
            pid = os.getpid()
        home = os.getenv("HOME")
        with open(f"{home}/ttutka.pid", "r") as fh:
            pids = [x for x in fh.readlines() if x.strip() != str(pid)]
        with open(f"{home}/ttutka.pid", "w") as fh:
            fh.writelines(pids)

    @staticmethod
    def _get_pid_from_pidfile() -> int | None:
        """Returns process pid when found, otherwise None.
        """
        home = os.getenv("HOME")
        with open(f"{home}/ttutka.pid", "r") as fh:
            pids = fh.readline().strip()
        return pids


class MyTCPServer(socketserver.TCPServer):
    def __init__(
        self,
        server_address: tuple[str, int],
        RequestHandlerClass: Callable,
        bind_and_activate: bool = True,
        extra_args_for_handler: tuple[Any] | None = None,
    ) -> None:
        """Extended __init__() from TCPServer

        Args:
            server_address (tuple[str, int]): A tuple containing ip-address and port.
            RequestHandlerClass (Callable):
                    The handle must take as many extra args as the extra_args_for_handler
                    tuple has members.
            bind_and_activate (bool, optional): Same as superclass. Defaults to True.
            extra_args_for_handler (tuple[Any] | None, optional): _description_. Defaults to None.
        """
        super().__init__(
            server_address,
            RequestHandlerClass,
            bind_and_activate,
        )
        self._extra = extra_args_for_handler

    def finish_request(self, request, client_address) -> None:
        """Overridden version with extra args."""
        print(self._extra)
        self.RequestHandlerClass(request, client_address, self, *self._extra)


class RxHandler(socketserver.StreamRequestHandler):
    def __init__(
        self,
        request,
        client_address,
        server: BaseServer,
        extra: Callable[[str], None],
    ) -> None:
        self._line_cb = extra
        super().__init__(request, client_address, server)

    def handle(self) -> None:
        while True:
            line = self.rfile.readline().decode("utf-8")
            if line:
                print(self)
                self._line_cb(line)
            else:
                time.sleep(0.5)


def serve(options):
    import signal
    import tassu_tutka.api as tassapi

    if "windows" not in platform.platform().lower():
        PidFileHandlerFunctions._add_pid_to_pidfile()

    # Starting client api.
    logging.info("Starting client API.")
    api = tassapi.ClientApi(options)
    t_api = threading.Thread(group=None, target=api.run_forevaa)
    t_api.daemon = True
    t_api.start()

    # Starting socket server for GPS device.
    logging.info(
        f"Starting Rx server in port {options.gps_listener_port}. Waiting for a GPS device."
    )
    rx = MyTCPServer(
        (options.gps_listener_addr, int(options.gps_listener_port)),
        RxHandler,
        extra_args_for_handler=(api.push_to_queue,),
    )
    t_rx = threading.Thread(group=None, target=rx.serve_forever)
    t_rx.start()

    def quit_(
        a: socketserver.TCPServer,
        a_thread: threading.Thread,
        sig,
        frame,
    ):
        a.shutdown()
        a.server_close()
        PidFileHandlerFunctions._remove_pid_from_pidfile()

    quit_ = functools.partial(quit_, rx, t_rx)
    signal.signal(signal.SIGINT, quit_)
    if "windows" not in platform.platform().lower():
        signal.signal(signal.SIGHUP, quit_)
    logging.info("Use CTRL-C or send SIGHUP to terminate: `ttutka server stop`")
    t_api.join()
