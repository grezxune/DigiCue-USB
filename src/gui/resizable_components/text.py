from resizable import Resizable

class ResizableText(Resizable):
    def __init__(self, canvas, x0, y0, **kwargs):
        Resizable.__init__(self, canvas)
        self.object = canvas.create_text(x0, y0, **kwargs)

    def redraw(self, x0, y0, **kwargs):
        self.ratio_width = self.canvas.width / float(self.canvas_width_orig)
        self.ratio_height = self.canvas.height / float(self.canvas_height_orig)
        a = x0 * self.ratio_width
        b = y0 * self.ratio_height
        self.canvas.coords(self.object, a, b, **kwargs)