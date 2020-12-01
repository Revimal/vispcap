import asyncio
try:
    import aiofile
except ImportError:
    import typing
    from typing_extensions import Coroutine
    typing.Coroutine = Coroutine
    import aiofile
import datetime
import io

from async_worker import SkelAsync
from skel_singleton import SkelSingleton

class FileLogger(SkelAsync, SkelSingleton):
    _datefmts = {
        "$Y" : lambda x: str(x.year).zfill(4),
        "$M" : lambda x: str(x.month).zfill(2),
        "$D" : lambda x: str(x.day).zfill(2),
        "$h" : lambda x: str(x.hour).zfill(2),
        "$m" : lambda x: str(x.minute).zfill(2),
        "$s" : lambda x: str(x.second).zfill(2),
        "$u" : lambda x: str(x.microsecond).zfill(6)
    }

    @classmethod
    def _gdfmts(cls):
        return cls._datefmts

    def __init__(self, logpath = "/var/log/vispcap.log", fmtstr = "vispcap[$Y.$M.$D-$h:$m:$s.$u] $L:", conout = True, flush = 0.1):
        super().__init__()
        self.logpath = logpath
        self.fmtstr = fmtstr
        self.conout = conout
        self.flush = flush
        self.buffer = []

        if any(tok in fmtstr for tok in self._gdfmts().keys()):
            self.datetok = True
        else:
            self.datetok = False

        if "$L" in fmtstr:
            self.lvtok = True
        else:
            self.lvtok = False

    def _build_str(self, *args, **kwargs):
        slst = []

        sep = kwargs.pop("sep", None)
        if sep is not None:
            if not isinstance(sep, str):
                raise TypeError()
        else:
            sep = " "

        end = kwargs.pop("end", None)
        if end is not None:
            if not isinstance(end, str):
                raise TypeError()
        else:
            end = "\n"

        if kwargs:
            raise TypeError()

        for i, arg in enumerate(args):
            if i:
                slst.append(sep)
            slst.append(arg)
        slst.append(end)

        return ''.join(slst)

    def _do_log(self, level, msg, *args, **kwargs):
        fmtstr = self.fmtstr

        if self.datetok is True:
            dtime = datetime.datetime.now()
            for tok, fn in self._gdfmts().items():
                fmtstr = fmtstr.replace(tok, fn(dtime))

        if self.lvtok is True:
            fmtstr = fmtstr.replace("$L", level)

        output = self._build_str(fmtstr, msg, *args, **kwargs)

        self.buffer.append(output)

    def info(self, msg, *args, **kwargs):
        self._do_log("info", msg, *args, **kwargs)

    def warn(self, msg, *args, **kwargs):
        self._do_log("warn", msg, *args, **kwargs)

    def crit(self, msg, *args, **kwargs):
        self._do_log("crit", msg, *args, **kwargs)

    async def sync(self):
        async with aiofile.AIOFile(self.logpath, "a+") as afp:
            writer = aiofile.Writer(afp)

            while True:
                await asyncio.sleep(self.flush)

                while self.buffer:
                    buffered = self.buffer.pop(0)

                    if self.conout is True:
                        print(buffered, end='')

                    await writer(buffered)
                    await afp.fsync()