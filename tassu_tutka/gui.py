import datetime
import tkinter
from tkinter import ttk
from tkinter.constants import *
from tkinter import filedialog
import io
import tkintermapview as tkm


def user_interface():
    tk = tkinter.Tk()
    tk.title("TassuTutka")
    mw = MainWindow(tk)
    menu_bar = MenuBar(tk)
    tk.config(menu=menu_bar)
    tk.mainloop()


class InfoDialog(tkinter.Toplevel):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent)

        # self.geometry("400x300")
        self.title(kwargs.get("title") or "Info Dialog")
        text = tkinter.Text(
            self,
            border=0,
            padx=10,
            bg="#f0f0f0",
            width=90,
            height=kwargs.get("height", 10),
        )
        text.insert(
            tkinter.END,
            chars=kwargs.get("info_content", "PLACEHOLDER. SET info_content kwarg"),
        )
        text.grid(row=0, column=0, columnspan=3)

        close_btn = ttk.Button(self, text="Sulje", command=lambda: self.destroy())
        close_btn.grid(row=1, column=1)


class MenuBar(tkinter.Menu):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent)
        file_menu = tkinter.Menu(self, tearoff=0)
        file_menu.add_command(label="Tyhjennä merkinnät")
        file_menu.add_command(label="Lopeta", command=lambda: parent.destroy())
        self.add_cascade(label="Tiedosto", menu=file_menu)

        info_menu = tkinter.Menu(self, tearoff=0)
        info_menu.add_command(
            label="Epälisenssi",
            command=lambda: InfoDialog(
                parent,
                title="Epälisenssi",
                height=25,
                info_content="""
This is free and unencumbered software released into the public domain.

Anyone is free to copy, modify, publish, use, compile, sell, or distribute
this software, either in source code form or as a compiled binary, for any
purpose, commercial or non-commercial, and by any means.

In jurisdictions that recognize copyright laws, the author or authors of
this software dedicate any and all copyright interest in the software to the
public domain. We make this dedication for the benefit of the public at
large and to the detriment of our heirs and successors. We intend this
dedication to be an overt act of relinquishment in perpetuity of all present
and future rights to this software under copyright law.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN
ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

For more information, please refer to <http://unlicense.org/>
            """,
            ),
        )
        info_menu.add_command(
            label="Tietoa",
            command=lambda: InfoDialog(
                parent,
                title="Info",
                info_content="""
TassuTutka on neljän opiskelijan koira-GPS -projekti. Tämä ohjelma on projektin
työpöytäympäristöön tarkoitettu ohjelma, joka tulkitsee ja näyttää GPS-laitteelta
saatavaa dataa. Projektissa mukana: Mikko Kujala, Rebecca Soisenniemi, Nico Hertolin
sekä Pasi Puhakka.
            """,
                height=7,
            ),
        )
        self.add_cascade(label="Tietoa", menu=info_menu)


class MainWindow(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent, borderwidth=2, relief=RIDGE)

        # Text showing selected file.
        self.file_name = tkinter.StringVar(self)
        self.file_name.set("Tiedostoa ei ole valittu")
        file_label = ttk.Label(self, textvariable=self.file_name, border=5)
        file_label.grid(column=0, row=0, columnspan=5)

        # File types for open file dialog.
        ft = (("GPS datatiedostot", "*.gdat"), ("Kaikki tiedostot", "*.*"))
        self._file: io.TextIOWrapper | None = None

        def read_file() -> None:
            if self.file:
                self.file.close()
            self.file = filedialog.askopenfile(
                title="Avaa tiedosto", initialdir="~", filetypes=ft
            )
            self.file_name.set(self.file.name) if self.file else self.file_name.set(
                "Tiedostoa ei ole valittu"
            )

        # Them buttons
        # self.read_file = ttk.Button(self, text="Avaa tiedosto...", command=read_file)
        # self.read_file.grid(column=0, row=1, sticky="ew")
        # draw_route = ttk.Button(self, text="Piirrä reitti").grid(
        #    column=1, row=1, sticky="ew"
        # )
        satellite_view = ttk.Button(
            self, text="Satelliittikartta", command=self.set_satellite_view
        ).grid(sticky="ew", column=0, columnspan=2, row=1)
        openstreetmap_view = ttk.Button(
            self, text="Open Street map", command=self.set_normal_view
        ).grid(column=2, row=1, columnspan=2, sticky="ew")

        pause_or_cont = ttk.Button(self, text="Tauota tai jatka")
        pause_or_cont.grid(column=5, row=0, sticky="ew")
        chosen_file = ttk.Button(self, text="Valitse tiedosto")
        chosen_file.grid(column=5, row=1, sticky="ew")

        lb = tkinter.Listbox(self)
        lb.grid(column=5, row=2, rowspan=20, sticky="ns")

        lb.insert(0, str(datetime.datetime.now()))

        self.map = tkm.TkinterMapView(self, width=1200, height=900)
        self.map.set_position(65.0612111, 25.4681883)
        self.map.grid(column=0, row=2, rowspan=3, columnspan=4)
        self.grid()

    def set_normal_view(self):
        self.map.set_tile_server("https://a.tile.openstreetmap.org/{z}/{x}/{y}.png")

    def set_satellite_view(self):
        self.map.set_tile_server(
            "https://mt0.google.com/vt/lyrs=s&hl=en&x={x}&y={y}&z={z}&s=Ga", max_zoom=22
        )

    @property
    def file(self):
        return self._file

    @file.setter
    def file(self, val):
        self._file = val
