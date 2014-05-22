#!/usr/bin/env python
"""
"""
import socketserver
import threading

from deviceutils import Device
from deviceutils import SerialPort
from deviceutils import TcpSocket
from deviceutils import channel
from deviceutils import Query


class ThreadedTCPRequestHandler(socketserver.BaseRequestHandler):

    def handle(self):
        data = str(self.request.recv(1024), 'latin1')
        cur_thread = threading.current_thread()
        response = bytes("{}: {}".format(cur_thread.name, data), 'latin1')
        self.request.sendall(response)


class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass


if __name__ == '__main__':
    HOST, PORT = "localhost", 5028
    server = ThreadedTCPServer((HOST, PORT), ThreadedTCPRequestHandler)
    ip, port = server.server_address

    # Start a thread with the server -- that thread will then start one
    # more thread for each request
    server_thread = threading.Thread(target=server.serve_forever)
    # Exit the server thread when the main thread terminates
    server_thread.daemon = True
    server_thread.start()
    print("Server loop running in thread:", server_thread.name)

    # with channel(Device(), SerialPort(serial_port, timeout=6.0)) as dev:
    #     print(dev.stdio.closed)
    #     print(dev.stdio.io_min_delta)
    #     dev.stdio.io_min_delta = 3.0
    #     dev.send('Hello')
    #     print('Wrote ``Hello``.')
    #     dev.send('World!')
    #     print('Wrote ``World!``.')
    #     print('Attempting a read...')
    #     print(dev.receive(encoding=None))

    # the ``channel`` method
    with channel(Device(timeout=3.0), TcpSocket(HOST, PORT)) as dev:
        print(dev.stdio.closed)
        dev.send('Hello World!')
        # TODO: fix the following bug
        #print(dev.receive(32).strip())  # causes hang even with timeout set!
        print(dev.receive().strip())

    # the ``action`` method
    query0 = Query('Hello World!', device=Device(timeout=3.0), io=TcpSocket(HOST, PORT))
    query0()
    print(query0.value)

    import socket
    sss = socket.socket()
    sss.connect((HOST, PORT))
    query0 = Query('Hello World!', device=Device(timeout=3.0), io=sss.makefile())
    query0()
    print(query0.value)
