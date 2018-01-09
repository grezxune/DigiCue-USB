from resizable import Resizable

class ResizableOval(Resizable):
    def __init__(self, canvas, x0, y0, x1, y1, **kwargs):
        Resizable.__init__(self, canvas)
        self.object = canvas.create_oval(x0, y0, x1, y1, **kwargs)