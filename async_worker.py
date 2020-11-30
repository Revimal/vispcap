import asyncio
import threading

from skel_singleton import SkelSingleton

class SkelAsync:
    @classmethod
    def identifier(cls):
        return cls.__name__

class AsyncWorker(SkelSingleton):
    def __init__(self):
        super().__init__()
        self.async_dict = {}
        self.result_list = []
        self.current_pending = 0
        self.async_loop = asyncio.get_event_loop()

    async def _async_runner(self):
        finished, pending = await asyncio.wait(self.async_dict.values())
        self.result_list.append([task.result() for task in finished])
        self.current_pending = pending

    def add_async(self, name, callback):
        self.async_dict[name] = callback

    def del_async(self, name):
        del self.async_dict[name]

    def clear_results(self):
        self.result_list.clear()

    def do_async(self):
        self.async_loop.run_until_complete(self._async_runner())