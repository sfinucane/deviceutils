#!/usr/bin/env python
"""
"""
import io


class DeviceError(Exception):
    """
    """
    def __init__(self, message='', uuid=None, name=None, make=None, model=None, version=None):
        self._uuid = uuid
        self.name = name
        self.make = make
        self.model = model
        self.version = version
        super().__init__(message)


class DeviceTimeoutError(DeviceError):
    pass


class DeviceIOError(IOError):
    pass


class IOTimeoutError(DeviceIOError):
    pass


class ProtocolError(Exception):
    """
    """
    pass
