import sys
import tassu_tutka.argparse as ap

def main():
    options = ap.parse()
    print(options)
    if hasattr(options, "gui") and options.gui:
        import tassu_tutka.gui as gui
        gui.user_interface()
        return
    elif hasattr(options, "start") and options.start == "start":
        import tassu_tutka.server as sr
        import multiprocessing as mp
        import os
        if options.daemon:
            sys.stdin.close()
            sys.stdin = sys.stderr
            pid = os.fork()
            if pid:
                return
        sr.serve()
    elif hasattr(options, "start") and options.start == "stop":
        import tassu_tutka.server as sr
        import signal, os
        pids = sr._get_pids_from_pidfile()
        try:
            pid = pids[0] # Only fork to damonize
            print(f"Sending SIGHUP to {pid}")
            os.kill(int(pid), signal.SIGHUP)
        except IndexError as e:
            print("TassuTutka server isn't running..")
        

        

if __name__ == "__main__":
    main()
