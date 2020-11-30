import tkinter
import asyncio

from async_worker import SkelAsync
from skel_singleton import SkelSingleton

class FlowCanvas(SkelAsync, SkelSingleton):
    def __init__(self, wndname, width, height, refresh, middlebox):
        super().__init__()
        self.width = width
        self.height = height
        self.refresh = refresh
        self.middlebox = middlebox

        self.wcursor = 0
        self.hcursor = 0

        self.tk_root = tkinter.Tk()
        self.tk_root.title(wndname)
        self.tk_width = self.tk_root.winfo_screenwidth()
        self.tk_height = self.tk_root.winfo_screenheight()

        self.tk_frame = tkinter.Frame(self.tk_root,
            width = self.tk_width if self.width > self.tk_width else self.width,
            height = self.tk_height if self.height > self.tk_height else self.height)
        self.tk_frame.pack(expand = tkinter.YES, fill = tkinter.BOTH)

        self.tk_canvas = tkinter.Canvas(self.tk_frame,
            width = self.tk_width if self.width > self.tk_width else self.width,
            height = self.tk_height if self.height > self.tk_height else self.height,
            scrollregion = (0, 0, self.width, self.height))

        self.tk_hscroll = tkinter.Scrollbar(self.tk_frame, orient = tkinter.HORIZONTAL)
        self.tk_hscroll.pack(side = tkinter.BOTTOM, fill = tkinter.X)
        self.tk_hscroll.config(command = self.tk_canvas.xview)

        self.tk_vscroll = tkinter.Scrollbar(self.tk_frame, orient = tkinter.VERTICAL)
        self.tk_vscroll.pack(side = tkinter.RIGHT, fill = tkinter.Y)
        self.tk_vscroll.config(command = self.tk_canvas.yview)

        self.tk_canvas.config(xscrollcommand = self.tk_hscroll.set, yscrollcommand = self.tk_vscroll.set)
        self.tk_canvas.pack(side = tkinter.TOP, expand = tkinter.YES, fill = tkinter.BOTH)

    def _test_draw(self):
        self.wcursor += 2
        self.width += 2
        self.tk_canvas.create_line(self.wcursor, 0, self.wcursor, self.height)
        self.tk_canvas.config(scrollregion = (0, 0, self.width, self.height))

    def test_draw(self, count = 1):
        for _ in range(count):
            self._test_draw()

    async def render(self):
        while True:
            await asyncio.sleep(self.refresh)
            self.tk_root.update_idletasks()
            self.tk_root.update()