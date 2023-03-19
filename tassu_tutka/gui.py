import tkinter
from tkinter import ttk
from tkinter.constants import *
import tkintermapview as tkm
from tkinter import filedialog
import io


def user_interface():
    tk = tkinter.Tk()
    tk.title("TassuTutka")
    mw = MainWindow(tk)
    tk.mainloop()


class MainWindow(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent, borderwidth=2, relief=RIDGE)
        self.grid()

        # Text showing selected file.
        self.file_name = tkinter.StringVar(self)
        self.file_name.set("Tiedostoa ei ole valittu")
        file_label = ttk.Label(self, textvariable=self.file_name, border=5)
        file_label.grid(column=0, row=0, columnspan=4)

        # File types for open file dialog.
        ft = (("GPS datatiedostot", "*.gdat"), ("Kaikki tiedostot", "*.*"))
        self._file: io.TextIOWrapper = None

        def read_file() -> None:
            if self.file:
                self.file.close()
            self.file = filedialog.askopenfile(
                title="Avaa tiedosto", initialdir="~", filetypes=ft
            )
            self.file_name.set(self.file.name) if self.file else self.file_name.set("Tiedostoa ei ole valittu")

        # Them buttons
        read_file = ttk.Button(
            self,
            text="Avaa tiedosto...",
            command=read_file,
        ).grid(column=0, row=1, sticky="ew")
        draw_route = ttk.Button(self, text="Piirrä reitti").grid(
            column=1, row=1, sticky="ew"
        )
        satellite_view = ttk.Button(
            self, text="Satelliittikartta", command=self.set_satellite_view
        ).grid(sticky="ew", column=2, row=1)
        satellite_view = ttk.Button(
            self, text="Open Street map", command=self.set_normal_view
        ).grid(column=3, row=1, sticky="ew")

        self.map = tkm.TkinterMapView(self, width=800, height=600, corner_radius=5)
        self.map.set_position(65.0612111, 25.4681883)
        self.map.grid(column=0, row=2, columnspan=4)

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
