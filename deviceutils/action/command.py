#!/usr/bin/env python
"""
"""
from ..defaultencoding import DefaultEncoding
from ..import channel


class Command(object):
    """
    """
    def __init__(self, message, device=None, io=None, encoding=DefaultEncoding()):
        object.__init__(self)
        self.message = message
        self.device = device
        self.io = io
        self.encoding = encoding
    
    def __call__(self, *args, **kwargs):
        """Performs the command. The ``message`` is sent to the device using io.
        
        Any arguments and/or keyword arguments will be passed to ``format``,
        which is called on the command message before sending.
        """
        if isinstance(self.encoding, DefaultEncoding):
            with channel(self.device, self.io) as dev:
                dev.send(
                    self.message.format(*args, **kwargs))
        else:
            with channel(self.device, self.io) as dev:
                dev.send(
                    self.message.format(*args, **kwargs), encoding=self.encoding)
