import sys
import logging
import platform
import signal
import os
import argparse
import time
import pathlib
import multiprocessing as mp
import tassu_tutka.argparse as ap
import tassu_tutka.server as sr
import tassu_tutka.error as error


def start(options: argparse.Namespace):
    if options.daemon:
        if "windows" in platform.platform().lower():
            print("Windows does not have daemon processes.")
            return
        pid = os.fork()
        if pid:
            return
    sr.serve()


def stop():
    if "windows" in platform.platform().lower():
        raise error.WindowsError("This command is not usable in Windows.")
    try:
        pids = sr._get_pids_from_pidfile()
        pid = pids[0]
        print(f"Sending SIGHUP to {pid}")
        os.kill(int(pid), signal.SIGHUP)
    except (
        IndexError,
        FileNotFoundError,
    ) as e:  # reading pid can raise file not found.
        print("TassuTutka server isn't running..")
    except ProcessLookupError as e:
        print("TassuTutka server isn't running..")
        print("Removing stale pidfile.")
        pidfilep = pathlib.Path(f"{os.getenv('HOME')}/ttutka.pid")
        if pidfilep.is_file():
            os.unlink(pidfilep)


def restart(options: argparse.Namespace):
    try:
        stop()
        print("Sleeping 5secs... lol.")
        time.sleep(5)
        start(options)
    except error.WindowsError as e:
        print("Server restart isn't supported on Windows.")


def force_kill():
    """Kill a server with SIGKILL by force and remove pidfile."""
    try:
        home = os.getenv("HOME")
        with open(f"{home}/ttutka.pid", "r") as fh:
            pid = int(fh.read().strip())
            os.kill(pid, signal.SIGKILL)
            os.unlink(f"{home}/ttutka.pid")
    except FileNotFoundError as e:
        print("Can't kill. Pidfile doesn't exist.")
    except AttributeError as e:
        print("This feature has not been implemented for Windows.")


def main():
    options = ap.parse()
    print(options)

    # Client selected
    if "gui" in options.cmd:
        import tassu_tutka.gui as gui

        gui.user_interface()

    # Server selected
    elif "start" in options.cmd:
        start(options)
    elif "stop" in options.cmd:
        stop()
    elif "restart" in options.cmd:
        restart(options)
    elif "kill" in options.cmd:
        force_kill()


if __name__ == "__main__":
    main()
