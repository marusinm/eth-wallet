from tkinter import Frame


class Page(Frame):
    def __init__(self, *args, **kwargs):
        Frame.__init__(self, *args, **kwargs)

    def show(self):
        self.lift()
        # todo try commented line
        # self.tkraise()
