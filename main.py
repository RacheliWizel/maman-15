import os
import helper
import selectors
import socket
from request import Request

HOST = ""

sel = selectors.DefaultSelector()

def accept(sock, mask):
     conn, addr = sock.accept() # Should be ready
     print('accepted', conn, 'from', addr)
     conn.setblocking(False)
     sel.register(conn, selectors.EVENT_READ, read)

def read(conn, mask):
    data = conn.recv(1024) # Should be ready
    if data:
         print('echoing', repr(data), 'to', conn)
         request = Request(data)
         request.handel_request()
    else:
         print('closing', conn )
         sel.unregister(conn)
         conn.close()

def main():
    port = helper.get_port()
    helper.init_data_base()
    sock = socket.socket()
    sock.bind((HOST, port))
    sock.listen(100)#todo check func parameter
    sock.setblocking(False)
    sel.register(sock, selectors.EVENT_READ, accept)
    while True:
        events = sel.select()
        for key, mask in events:
            callback = key.data
            callback(key.fileobj, mask)


if __name__ == '__main__':
    main()
