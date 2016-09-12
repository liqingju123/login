# -*- coding: utf-8 -*-

from Tkinter import *
from ttk import *

# http://tkinter.unpythonic.net/wiki/VerticalScrolledFrame

class VerticalScrolledFrame(Frame):
    def __init__(self, parent, *args, **kw):
        Frame.__init__(self, parent,*args , **kw)            
#         Frame.size(1000,1000)
        # create a canvas object and a vertical scrollbar for scrolling it
        vscrollbar = Scrollbar(self, orient=VERTICAL)
        vscrollbar.pack(fill=Y, side=RIGHT, expand=FALSE)
        canvas = Canvas(self, bd=0, highlightthickness=0,
                        yscrollcommand=vscrollbar.set)
        canvas.pack(side=LEFT, fill=BOTH, expand=TRUE)
        vscrollbar.config(command=canvas.yview)

        # reset the view
        canvas.xview_moveto(0)
        canvas.yview_moveto(0)
        # create a frame inside the canvas which will be scrolled with it
        self.interior = interior = Frame(canvas)
        interior_id = canvas.create_window(0, 0, window=interior,
                                           anchor=NW)

        # track changes to the canvas and frame width and sync them,
        # also updating the scrollbar
        def _configure_interior(event):
            # update the scrollbars to match the size of the inner frame
            size = (interior.winfo_reqwidth(), interior.winfo_reqheight())
            canvas.config(scrollregion="0 0 %s %s"% size)
            if interior.winfo_reqwidth() != canvas.winfo_width():
                # update the canvas's width to fit the inner frame
                canvas.config(width=interior.winfo_reqwidth())
        interior.bind('<Configure>', _configure_interior)

        def _configure_canvas(event):
            if interior.winfo_reqwidth() != canvas.winfo_width():
                # update the inner frame's width to fill the canvas
                canvas.itemconfigure(interior_id, width=canvas.winfo_width())
        canvas.bind('<Configure>', _configure_canvas)


if __name__ == "__main__":

    class SampleApp(Tk):
        def __init__(self, *args, **kwargs):
            root = Tk.__init__(self, *args, **kwargs)
            f1=Frame(root);
            f1.pack() 
            Label(f1,text="姓名").pack(side=LEFT)
#             f1.title('表情')
            self.frame = VerticalScrolledFrame(root)
            self.frame.pack()
            self.title('医生搜索')
            buttons=[]
            for j in range(30):
                for i in range(5):
                    buttons.append(Button(self.frame.interior, text="Button 111111111111111" + str(i)))
                    buttons[-1].grid(row=j, column=i)




    app = SampleApp()
    app.minsize(800, 500)
    app.mainloop()
