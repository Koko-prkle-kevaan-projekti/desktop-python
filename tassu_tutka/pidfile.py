import os


class PidFileHandlerFunctions:
    @staticmethod
    def add_pid_to_pidfile(pid: int | None = None):
        if not pid:
            pid = os.getpid()
        home = os.getenv("HOME")
        with open(f"{home}/ttutka.pid", "w") as fh:
            fh.write(f"{pid}\n")

    @staticmethod
    def remove_pid_from_pidfile(pid: int | None = None):
        if not pid:
            pid = os.getpid()
        home = os.getenv("HOME")
        with open(f"{home}/ttutka.pid", "r") as fh:
            pids = [x for x in fh.readlines() if x.strip() != str(pid)]
        with open(f"{home}/ttutka.pid", "w") as fh:
            fh.writelines(pids)

    @staticmethod
    def get_pid_from_pidfile() -> int | None:
        """Returns process pid when found, otherwise None."""
        home = os.getenv("HOME")
        with open(f"{home}/ttutka.pid", "r") as fh:
            try:
                pid = int(fh.readline().strip())
            except ValueError as e:
                pid = None
        return pid
