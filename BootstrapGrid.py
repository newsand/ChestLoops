
from tkinter import ttk
try:
    import Tkinter as tk
except:
    import tkinter as tk

from io import BytesIO

import PIL
from PIL import Image
from PIL.ImageTk import PhotoImage

BGC = "#123456"


class ScrollableFrame(ttk.Frame):
    def __init__(self, container, *args, **kwargs):
        super().__init__(container, *args, **kwargs)
        canvas = tk.Canvas(self,bg=BGC)
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=canvas.yview)

        s = ttk.Style()
        s.configure('BGC.TFrame', background=BGC)
        self.scrollable_frame = ttk.Frame(canvas, style='BGC.TFrame')
        self.columns=0

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )

        self.bind('<Configure>', self.regrid)
        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    def regrid(self, event=None):
        grid_width = self.winfo_width()
        slaves = self.scrollable_frame.grid_slaves()
        slaves_width = slaves[1].winfo_width()
        cols = grid_width // slaves_width
        if (cols == self.columns) | (cols == 0):  # if the column number has not changed, abort
            return
        for i, slave in enumerate(reversed(slaves)):
            slave.grid_forget()
            slave.grid(row=i // cols, column=i % cols)
        self.columns = cols


class ImageCard(tk.Frame):
    def __init__(self, master=None, **kwargs):
        tk.Frame.__init__(self, master, bd=5, relief=tk.RAISED, **kwargs)

    def add_button(self, x):
        icon = generate_thumbnail(x[3])
        sound_btn = tk.Button(self, image=icon, relief=tk.FLAT, height=130, width=130, pady=2, padx=2,
                              command=lambda lan=x: stream_toImage(lan[3]).show())
        sound_btn.image = icon
        sound_btn.pack()
        return self

    def add_file_name(self, filename):
        tk.Label(self, text=filename).pack(pady=10)
        return self


def stream_toImage(stream) -> Image:
    stream = BytesIO(stream)
    im = Image.open(stream).convert("RGBA")
    stream.close()
    return im


def generate_thumbnail(xablau) -> PhotoImage:
    im = stream_toImage(xablau)
    im.thumbnail((128, 128), Image.ANTIALIAS)
    icon = PIL.ImageTk.PhotoImage(im)
    return icon
