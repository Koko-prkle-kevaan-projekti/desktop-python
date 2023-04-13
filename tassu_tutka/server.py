import logging
import threading
import socketserver
from socketserver import BaseRequestHandler, BaseServer
import time
from typing import Any, Callable

import tassu_tutka.api as tassapi
import tassu_tutka.signals as signals
from tassu_tutka import pidfile


class MyTCPServer(socketserver.ThreadingTCPServer):
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
                self._line_cb(line)
            else:
                time.sleep(0.5)


def serve(options):
    # Write process pid to the pid file.
    pidfile.PidFileHandlerFunctions.add_pid_to_pidfile()

    logging.info("Starting client API.")
    api = tassapi.ClientApi(options)  # api can thread itself.

    # Starting socket server for GPS device.
    logging.info(
        f"Starting Rx server in port {options.gps_listener_port}. Waiting for a GPS device."
    )
    rx = MyTCPServer(
        (options.gps_listener_addr, int(options.gps_listener_port)),
        RxHandler,
        extra_args_for_handler=(api.push_to_queue,),
    )
    rx_t = threading.Thread(group=None, target=rx.serve_forever)

    # Start the threads.
    rx_t.start()

    # Register signal handlers after starting threads.
    should_quit = []
    signals.register_signal_handlers((rx, rx_t), should_quit)

    logging.info("Use CTRL-C or send SIGHUP to terminate: `ttutka server stop`")
    with api.run_in_thread():
        while not should_quit:
            time.sleep(0.3)
        pidfile.PidFileHandlerFunctions.remove_pid_from_pidfile()
