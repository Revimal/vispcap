import asyncio
try:
    import aiofile
except ImportError:
    import typing
    from typing_extensions import Coroutine
    typing.Coroutine = Coroutine
    import aiofile
import ctypes
import io

from async_worker import SkelAsync
from flow_canvas import FlowCanvas
from file_logger import FileLogger

class PcapFileHeader(ctypes.Structure):
    _pack_ = 1
    _fields_ = [
        ("magic_number", ctypes.c_uint32),
        ("version_major", ctypes.c_uint16),
        ("version_minor", ctypes.c_uint16),
        ("thiszone", ctypes.c_int32),
        ("sigfigs", ctypes.c_uint32),
        ("snaplen", ctypes.c_uint32),
        ("network", ctypes.c_uint32)
    ]

class PcapRecordHeader(ctypes.Structure):
    _pack_ = 1
    _fields_ = [
        ("ts_sec", ctypes.c_uint32),
        ("ts_usec", ctypes.c_uint32),
        ("incl_len", ctypes.c_uint32),
        ("orig_len", ctypes.c_uint32)
    ]

class PcapParser(SkelAsync):
    def __init__(self, path, rdnum = 64):
        self.path = path
        self.rdnum = rdnum
        self.offset = 0
        self.fhdr = None
        self.rhdr = None
        self.buf = bytearray()

    async def parse(self):
        async with aiofile.AIOFile(self.path, "rb") as afp:
            while True:
                chunk = await afp.read(size = self.rdnum, offset = self.offset)

                if chunk is '':
                    break

                self.offset += self.rdnum
                self.buf.extend(chunk)

                if not self.fhdr:
                    fhsz = ctypes.sizeof(PcapFileHeader)

                    if len(self.buf) < fhsz:
                        continue

                    self.fhdr = PcapFileHeader.from_buffer(self.buf)
                    self.buf = self.buf[fhsz:]

                    if self.fhdr.magic_number != 0xa1b2c3d4:
                        FileLogger.instance().crit("WTF")
                        break

                    FileLogger.instance().info("magic_number: {:#x}".format(self.fhdr.magic_number))
                    FileLogger.instance().info("version_major: {:#d}".format(self.fhdr.version_major))
                    FileLogger.instance().info("magic_number: {:#d}".format(self.fhdr.version_minor))
                    FileLogger.instance().info("snaplen: {:#d}".format(self.fhdr.snaplen))
                    FileLogger.instance().info("network: {:#x}".format(self.fhdr.network))

                if not self.rhdr:
                    rhsz = ctypes.sizeof(PcapRecordHeader)

                    if len(self.buf) < rhsz:
                        continue

                    self.rhdr = PcapRecordHeader.from_buffer(self.buf)
                    self.buf = self.buf[rhsz:]

                    FileLogger.instance().info("pktsize: {:#d}/{:#d}".format(self.rhdr.incl_len, self.rhdr.orig_len))

                if len(self.buf) > self.rhdr.incl_len:
                        FlowCanvas.instance().test_draw()
                        self.buf = self.buf[self.rhdr.incl_len:]
                        self.rhdr = None