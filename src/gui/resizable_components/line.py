from resizable import Resizable

class ResizableLine(Resizable):
    def __init__(self, canvas, x0, y0, x1, y1, **kwargs):
        Resizable.__init__(self, canvas)
        self.object = canvas.create_line(x0, y0, x1, y1, **kwargs)