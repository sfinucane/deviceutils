#!/usr/bin/env python
"""
"""
import socket
import io
import multiprocessing

from .mixin import IORateLimiterMixin
from deviceutils.error import IOTimeoutError


def receive_proc(return_queue, sock, count):
    try:
        return_queue.put_nowait(sock.recv(count))
    except Exception as e:
        return_queue.put_nowait(e)


class BasicTcpSocket(io.IOBase):
    """
    """
    def __init__(self, host, port, timeout=None, buffer_size=4096):
        super().__init__()
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host = host
        self.port = port
        self.timeout = timeout
        self._closed = True
        self.read_buffer_size = buffer_size
    
    def close(self):
        self._socket.shutdown(socket.SHUT_RDWR)
        self._socket.close()
        # re-instantiate so that the socket can be used again.
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._closed = True

    @property
    def closed(self):
        return self._closed

    def fileno(self):
        return self._socket.fileno(self)
        
    def flush(self):
        pass
    
    def readable(self):
        return not self._closed
        
    def read(self, size=None):
        if not size or size < 0:
            size = self.read_buffer_size

        receive_queue = multiprocessing.Queue()
        p_reader = multiprocessing.Process(target=receive_proc, args=(receive_queue, self._socket, size))
        p_reader.start()
        p_reader.join(timeout=self.timeout)
        if p_reader.is_alive():
            # the receive has timed out!
            p_reader.terminate()
            p_reader.join()
            raise IOTimeoutError('i/o timed out during read.')
        received = receive_queue.get_nowait()
        if isinstance(received, Exception):
            raise received
        return bytes(received)

    def writable(self):
        return not self._closed
        
    def write(self, b):
        return self._socket.send(b)
        
    def open(self):
        self._socket.connect((self.host, self.port))
        self._closed = False
        

class TcpSocket(IORateLimiterMixin, BasicTcpSocket):
    """
    """
    def __init__(self, *args, **kwargs):
        BasicTcpSocket.__init__(self, *args, **kwargs)
