#!/usr/bin/env python
"""
"""


class DeviceError(Exception):
    """
    """
    pass


class DeviceTimeoutError(DeviceError):
    pass


class IOError(Exception):
    pass


class IOTimeoutError(IOError):
    pass


class ProtocolError(Exception):
    """
    """
    pass
