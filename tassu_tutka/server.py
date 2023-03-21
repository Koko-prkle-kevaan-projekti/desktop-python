import selectors
import threading
import socket

sel = selectors.DefaultSelector()

def accept(sock, mask):
    conn, addr = sock.accept()  # Should be ready
    print('accepted', conn, 'from', addr)
    conn.setblocking(False)
    sel.register(conn, selectors.EVENT_READ, read)

def read(conn, mask):
    data = conn.recv(1000)  # Should be ready
    if data:
        print('echoing', repr(data), 'to', conn)
        conn.send(data)  # Hope it won't block
    else:
        print('closing', conn)
        sel.unregister(conn)
        conn.close()

def start_server(addr, port):
    sock = socket.socket()
    sock.bind((addr, port))
    sock.listen(5)
    sock.setblocking(False)
    sel.register(sock, selectors.EVENT_READ, accept)
    print(f"Listening to {addr}:{port} ...")

    while True:
        events = sel.select()
        for key, mask in events:
            print(key)
            callback = key.data
            callback(key.fileobj, mask)

