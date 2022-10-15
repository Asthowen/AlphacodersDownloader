# Author: James Spencer: http://stackoverflow.com/users/1375885/james-spencer
# Packager: Gijs Timers:  https://github.com/GijsTimmers

# Based on James Spencer's answer on StackOverflow:
# http://stackoverflow.com/q/5174810

import sys
import os

if os.name == "nt":
    import ctypes

    class _CursorInfo(ctypes.Structure):
        _fields_ = [("size", ctypes.c_int), ("visible", ctypes.c_byte)]


# pylint: disable=W0201
def hide(stream=sys.stdout):
    if os.name == "nt":
        cursor_info = _CursorInfo()
        handle = ctypes.windll.kernel32.GetStdHandle(-11)
        ctypes.windll.kernel32.GetConsoleCursorInfo(handle, ctypes.byref(cursor_info))
        cursor_info.visible = False
        ctypes.windll.kernel32.SetConsoleCursorInfo(handle, ctypes.byref(cursor_info))
    elif os.name == "posix":
        stream.write("\033[?25l")
        stream.flush()


# pylint: disable=W0201
def show(stream=sys.stdout):
    if os.name == "nt":
        cursor_info = _CursorInfo()
        handle = ctypes.windll.kernel32.GetStdHandle(-11)
        ctypes.windll.kernel32.GetConsoleCursorInfo(handle, ctypes.byref(cursor_info))
        cursor_info.visible = True
        ctypes.windll.kernel32.SetConsoleCursorInfo(handle, ctypes.byref(cursor_info))
    elif os.name == "posix":
        stream.write("\033[?25h")
        stream.flush()


class HiddenCursor:
    def __init__(self, stream=sys.stdout):
        self._stream = stream

    def __enter__(self):
        hide(stream=self._stream)

    def __exit__(self, exit_type, exit_value, exit_traceback):
        show(stream=self._stream)
