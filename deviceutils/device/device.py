#!/usr/bin/env python
"""
"""
import time
import multiprocessing

from ..error import DeviceTimeoutError


def receive_proc(return_queue, io, count):
    return_queue.put_nowait(io.read(count))


class BasicDevice(object):
    """
    """

    DEFAULT_ENCODING = 'ascii'
    DEFAULT_RECV_COUNT = -1
    
    SEND_TERMINATION = '\n'
        
    def __init__(self, timeout=None):
        object.__init__(self)
        self._stdio = None
        
        self.timeout = timeout
        
    def send(self, message, encoding=DEFAULT_ENCODING):
        """
        """
        # TODO: store termination in bytes, then add to encoded message right before send.
        if not message.endswith(self.SEND_TERMINATION):
            message += self.SEND_TERMINATION
        if encoding:
            self.stdio.write(message.encode(encoding))
        else:
            self.stdio.write(message)
        
    def receive(self, count=DEFAULT_RECV_COUNT, encoding=DEFAULT_ENCODING):
        """
        """
        receive_queue = multiprocessing.Queue()
        t_reader = multiprocessing.Process(target=receive_proc, args=(receive_queue, self.stdio, count))
        t_reader.start()
        t_reader.join(timeout=self.timeout)
        if t_reader.is_alive():
            # the read timed out!
            t_reader.terminate()
            t_reader.join()
            raise DeviceTimeoutError('A timeout occurred while performing an device read.')

        received = receive_queue.get_nowait()
        if encoding:
            return received.decode(encoding=encoding)
        else:
            return bytes(received)
        
    @property
    def stdio(self):
        return self._stdio
        
    @stdio.setter
    def stdio(self, io):
        self._stdio = io


class Device(BasicDevice):
    """
    """
    def __init__(self, *args, uuid=None, name=None, make=None, model=None, version=None, **kwargs):
        BasicDevice.__init__(self, *args, **kwargs)
        self._uuid = uuid
        self.name = name
        self.make = make
        self.model = model
        self.version = version
