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

class PcapParser(SkelAsync):
    def __init__(self, path):
        self.path = path

    async def parse(self):
        while True:
            await asyncio.sleep(0.01)
            FlowCanvas.instance().test_draw()