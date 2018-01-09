import sys

if sys.version_info[0] < 3:
    import Tkinter as Tk
    import ttk
else:
    import tkinter as Tk
    from tkinter import ttk

class Resizable(object):
    def __init__(self, canvas):
        self.canvas = canvas
        self.canvas_width_orig = canvas.width
        self.canvas_height_orig = canvas.height

    def redraw(self, x0, y0, x1, y1, **kwargs):
        self.ratio_width = self.canvas.width / float(self.canvas_width_orig)
        self.ratio_height = self.canvas.height / float(self.canvas_height_orig)
        a = x0 * self.ratio_width
        b = y0 * self.ratio_height
        c = x1 * self.ratio_width
        d = y1 * self.ratio_height
        self.canvas.coords(self.object, a, b, c, d, **kwargs)

    def itemconfig(self, **kwargs):
        self.canvas.itemconfig(self.object, **kwargs)