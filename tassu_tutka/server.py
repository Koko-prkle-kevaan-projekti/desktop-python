import selectors
import threading
import socket
import time

TX_PORT = 65000
RX_PORT = 64999

sel_tx = selectors.DefaultSelector()
BUF = ""
BUF_LOCK = threading.Lock()

def rx():
    global BUF, BUF_LOCK
    with socket.socket() as s:
        s.bind(("0.0.0.0", RX_PORT))
        s.listen()
        print(f"Listening waiting data to 0.0.0.0:{RX_PORT}")
        while True:
            conn, addr = s.accept()
            with conn:
                while True:
                    data = conn.recv(1024).decode()
                    if not data:
                        break
                    BUF_LOCK.acquire(blocking=True)
                    BUF += data
                    BUF_LOCK.release()

def tx():
    sel = selectors.DefaultSelector()
    with socket.socket() as s:
        s.bind(("0.0.0.0", TX_PORT))
        s.listen()
        break_flag = False
        while True:
            print(f"Listening at 0.0.0.0:{TX_PORT} and waiting to send data.")
            conn, addr = s.accept()
            conn.setblocking(False)
            with conn:
                print(f"tx: Connected by {addr}")
                while True:
                    line = readline()
                    if line:
                        try:
                            conn.send(line.encode("utf-8"))
                        except Exception as e:
                            print(e)
                            break

def readline() -> None | str:
    """Return a next line from buffer, or None if no new line is available."""
    global BUF, BUF_LOCK
    BUF_LOCK.acquire(blocking=True)
    if not BUF:
        BUF_LOCK.release()
        time.sleep(0.1)
        return None

    s = ""
    ret = None
    for index, ch in enumerate(BUF):
        if ch != "\n":
            s += ch
        else:
            ret = s + '\n'
            BUF = BUF[index+1:]
            break
    BUF_LOCK.release()
    return ret


def serve():
    rx_thread = threading.Thread(target=rx)
    tx_thread = threading.Thread(target=tx)

    print("launching rx thread.")
    rx_thread.start()
    print("launching tx thread.")
    tx_thread.start()
