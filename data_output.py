"""Data output manager module."""
import abc
import typing


class Writer(abc.ABC):
    """Abstract class for output manager"""

    def __call__(self, *args, **kwargs):
        raise NotImplementedError

    def write(self, *args, **kwargs):
        self(*args, **kwargs)


class FileWriter(Writer):
    """Writes data into file. (Or file-like object)"""

    def __init__(self, file: typing.IO):
        self.file = file

    def __call__(self, *args, **kwargs):
        if self.file and not self.file.closed:
            self.file.write(*args, **kwargs)

    def __enter__(self):
        return self.file

    def __exit__(self, exc_type, exc_val, exc_tb):
        try:
            if self.file and not self.file.closed:
                self.file.close()
        except AttributeError:
            pass

    def __del__(self):
        try:
            if self.file and not self.file.closed:
                self.file.close()
        except AttributeError:
            pass


class StdPrintWriter(Writer):
    """Prints data into default stdout or stream by print function"""

    def __call__(self, *args, **kwargs):
        print(*args, **kwargs)
