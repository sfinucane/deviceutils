#!/usr/bin/env python
"""
"""
import socketserver
import threading
import time

from deviceutils import Device
from deviceutils import SerialPort
from deviceutils import TcpSocket
from deviceutils import channel
from deviceutils import Query
from deviceutils.error import DeviceTimeoutError
from deviceutils.error import IOTimeoutError


class ThreadedTCPRequestHandler(socketserver.BaseRequestHandler):

    def handle(self):
        data = str(self.request.recv(1024), 'latin1')
        cur_thread = threading.current_thread()
        response = bytes("{}: {}".format(cur_thread.name, data), 'latin1')
        time.sleep(4.0)
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

    print('Available serial ports:', list(SerialPort.available_ports()))

    # the ``channel`` method
    try:
        with channel(Device(timeout=3.0), TcpSocket(HOST, PORT)) as dev:
            print(dev.stdio.closed)
            dev.send('Hello World!')
            # TODO: fix the following bug
            #print(dev.receive(32).strip())  # causes hang even with timeout set!
            print(dev.receive().strip())
    except DeviceTimeoutError as e:
        print(e)
    except IOTimeoutError as e:
        print(e)

    # the ``action`` method
    try:
        query0 = Query('Hello World!', device=Device(timeout=None), io=TcpSocket(HOST, PORT))
        query0()
        print(query0.value.strip())
    except DeviceTimeoutError as e:
        print(e)
    except IOTimeoutError as e:
        print(e)

    # the ``action`` method, with both IO and Device timeouts set
    try:
        query0 = Query('Hello World!', device=Device(timeout=None), io=TcpSocket(HOST, PORT, timeout=1.0))
        query0()
        print(query0.value.strip())
    except DeviceTimeoutError as e:
        print(e)
    except IOTimeoutError as e:
        print(e)
