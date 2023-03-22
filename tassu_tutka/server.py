import threading
import socketserver
import time
import sys
import functools

TX_PORT = 65000
RX_PORT = 64999

BUF = ""
BUF_LOCK = threading.Lock()


class RxHandler(socketserver.StreamRequestHandler):

    def handle(self) -> None:
        global BUF
        while True:
            line = self.rfile.readline().decode("utf-8")
            BUF_LOCK.acquire(blocking=True)
            BUF += line
            BUF_LOCK.release()
        

class TxHandler(socketserver.StreamRequestHandler):

    def handle(self) -> None:
        global BUF
        line = ""
        while True:
            BUF_LOCK.acquire(blocking=True)
            for i, ch in enumerate(BUF):
                line += ch
                if ch == "\n":
                    BUF = BUF[i+1:]
                    break
            else: # A full line in buffer isn't available.
                BUF_LOCK.release()
                time.sleep(0.2)
                continue
            BUF_LOCK.release()
            self.wfile.write(line.encode("utf-8"))

def serve():
    import signal

    print("Starting Rx server in port 65000...")
    rx = socketserver.TCPServer(("0.0.0.0", 65000), RxHandler)
    t_rx = threading.Thread(group=None, target=rx.serve_forever)
    t_rx.start()


    print("Starting Tx server in port 64999...")
    tx = socketserver.TCPServer(("0.0.0.0", 64999), TxHandler)
    t_tx  = threading.Thread(group=None, target=tx.serve_forever)
    t_tx.start()

    def quit_(a: socketserver.TCPServer, b: socketserver.TCPServer, sig, frame):
        print("\nQuit requested.. Shutting down.\n")
        a.shutdown()
        b.shutdown()
    quit_ = functools.partial(quit_, tx, rx)
    signal.signal(signal.SIGINT, quit_)
    print("Server started. Press CTRL+C to quit.")
