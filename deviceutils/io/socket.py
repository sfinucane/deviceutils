#!/usr/bin/env python
"""
"""
import socket
import io

from .mixin import IORateLimiterMixin


class BasicTcpSocket(object):
    """
    """
    def __init__(self, host, port, timeout=30.0, buffer_size=4096):
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host = host
        self.port = port
        self.timeout = timeout
        self.closed = True
        self.buffer_size = buffer_size
    
    def close(self):
        self._socket.shutdown(socket.SHUT_RDWR)
        self._socket.close()
        # re-instantiate so that the socket can be used again.
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.closed = True
        
    def fileno(self):
        return self._socket.fileno(self)
        
    def flush(self):
        pass
    
    def readable(self):
        return not self.closed
        
    def read(self, size=-1):
        try:
            if not size or size < 0:
                return self._socket.recv(self.buffer_size)
            else:
                return self._socket.recv(size)
        except socket.timeout:
            return bytes([])
        except:
            raise
        
    def writable(self):
        return not self.closed
        
    def write(self, b):
        return self._socket.send(b)
        
    def open(self):
        self._socket.connect((self.host, self.port))
        self.closed = False
        

class TcpSocket(IORateLimiterMixin, BasicTcpSocket):
    """
    """
    def __init__(self, *args, **kwargs):
        BasicTcpSocket.__init__(self, *args, **kwargs)
