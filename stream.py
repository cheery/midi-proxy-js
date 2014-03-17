from greenlet import getcurrent
from asyncio import schedule
from select import select
import os

def open(path):
    fd = os.open(path, os.O_RDONLY | os.O_NONBLOCK)
    return Stream(fd, streams)

class FileSelect(object):
    def __init__(self, timeout=0.01):
        self.timeout = timeout
        self.main = getcurrent()
        self.reading = []

    @property
    def tasks(self):
        return len(self.reading)

    def read(self, stream):
        stream.reading_greenlet = getcurrent()
        self.reading.append(stream)
        self.main.switch()

    def step(self):
        readable, writable, error = select(self.reading, [], [], self.timeout)
        
        for stream in readable:
            self.switchReading(stream)

        for stream in error:
            self.throw(stream, StreamError('error during select'))

    def switchReading(self, stream):
        greenlet = stream.reading_greenlet
        stream.reading_greenlet = None
        self.reading.remove(stream)
        greenlet.switch()

    def throw(self, stream, error):
        if stream in self.reading:
            greenlet = stream.reading_greenlet
            stream.reading_greenlet = None
            self.reading.remove(socket)
            greenlet.throw(error)

class Stream(object):
    def __init__(self, fd, strategy):
        self.fd = fd
        self.strategy = strategy

    def fileno(self):
        return self.fd
        
    def read(self, count):
        self.strategy.read(self)
        return os.read(self.fd, count)

class StreamError(Exception): pass

streams = FileSelect()
schedule.strategies.append(streams)
