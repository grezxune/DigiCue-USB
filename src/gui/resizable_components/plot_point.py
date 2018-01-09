import sys

from resizable import Resizable

if sys.version_info[0] < 3:
    import Tkinter as Tk
    import ttk
else:
    import tkinter as Tk
    from tkinter import ttk

class ResizablePlotPoint(Resizable):
    def __init__(self, canvas, x0, y0, mag, **kwargs):
        Resizable.__init__(self, canvas)
        self.x0 = x0
        self.y0 = y0
        self.mag = mag
        self.size = 3
        self.object = canvas.create_oval(
            x0 - self.size,
            y0 - self.size,
            x0 + self.size,
            y0 + self.size,
            **kwargs)

    def redraw(self, **kwargs):
        self.ratio_width = self.canvas.width / float(self.canvas_width_orig)
        self.ratio_height = self.canvas.height / float(self.canvas_height_orig)
        a = self.x0 * self.ratio_width
        b = self.y0 * self.ratio_height
        self.canvas.coords(
            self.object,
            a - self.size,
            b - self.size,
            a + self.size,
            b + self.size,
            **kwargs)