from collections import deque
from datetime import datetime, timedelta
import tkinter
from tkinter import ttk
from tkinter.constants import *
import tkintermapview as tkm

from tassu_tutka import client
from tassu_tutka.nmea import Sentence

UPDATE_INTERVAL = 1500

_RMC_MESSAGES = deque()
_LISTBOX_ITEMS: deque[Sentence] = deque()
_CLIENT = client.Requester()


def read_messages(main_window: "MainWindow"):
    _CLIENT.mkrequest()
    for coord in _CLIENT.get_responses():
        _RMC_MESSAGES.appendleft(coord)

    while _RMC_MESSAGES:
        msg = _RMC_MESSAGES.pop()
        _LISTBOX_ITEMS.appendleft(msg)
        entry: datetime = msg["MSG_DATETIME"]
        str_entry = (
            f"{entry.day}.{entry.month}. {entry.hour}:{entry.minute}:{entry.second}"
        )
        main_window.add_lb_entry(str(str_entry))
    main_window.after(UPDATE_INTERVAL, read_messages, main_window)


def user_interface():
    tk = tkinter.Tk()
    tk.title("TussuTutka")
    mw = MainWindow(tk)
    menu_bar = MenuBar(tk)
    tk.config(menu=menu_bar)
    tk.after(UPDATE_INTERVAL, read_messages, mw)
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
                info_content="""Jeejee!
                Tee mitä haluat tällä ohjelmalla! :D""",
            ),
        )
        info_menu.add_command(
            label="Tietoa",
            command=lambda: InfoDialog(
                parent,
                title="Info",
                info_content="""
TassuTutka on neljän pippelin koira-GPS -projekti. Tämä ohjelma on projektin
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

        satellite_view = ttk.Button(
            self, text="Satelliittikartta", command=self.set_satellite_view
        )
        satellite_view.grid(sticky="ew", column=0, columnspan=2, row=1, ipadx=10, ipady=10)
        openstreetmap_view = ttk.Button(
            self, text="Open Street map", command=self.set_normal_view
        )
        openstreetmap_view.grid(column=2, row=1, columnspan=2, sticky="ew", ipadx=10, ipady=10)

        center_latest = ttk.Button(
            self, text="Keskitä viimeisimpään", command=self.center_map_to_last_position
        )
        center_latest.grid(column=5, row=0, sticky="ew", rowspan=2, ipadx=10, ipady=10)

        self.listbox = tkinter.Listbox(self, selectmode=SINGLE)
        self.listbox.bind('<<ListboxSelect>>', self.set_map_position_listbox_cb)
        for i, item in enumerate(_RMC_MESSAGES):
            self.listbox.insert(i, str(item))
        self.listbox.grid(column=5, row=2, rowspan=20, sticky="ns")

        self.map = tkm.TkinterMapView(self, width=1200, height=900)
        self.map.set_position(65.0612111, 25.4681883)
        self.map.grid(column=0, row=2, rowspan=3, columnspan=4)
        self.grid()

    def set_map_position_listbox_cb(self, event):
        print(event)
        print(dir(event))
        selection = self.listbox.curselection()
        sentence = _LISTBOX_ITEMS[selection[0]]
        self.set_map_position(
            sentence.sentence["MSG_LATTITUDE"],
            sentence.sentence["MSG_LONGITUDE"],
            "",
            True
        )

    def center_map_to_last_position(self):
        """Callback for the button to center map.

        Do nothing, if no data has been received.
        """
        try:
            self.set_map_position(
                _LISTBOX_ITEMS[0]["MSG_LATTITUDE"],
                _LISTBOX_ITEMS[0]["MSG_LONGITUDE"],
                "Viimeisin",
                True,
            )
        except IndexError as e:
            pass

    def set_map_position_with_time_given(self, time: datetime, td: timedelta = timedelta(seconds=1)):
        """Set map position to first item in _LISTBOX_ITEMS which is within the threshold of td.
        """
        for item in _LISTBOX_ITEMS:
            if not (time - td < item.sentence["MSG_DATETIME"] < time + td):
                self.set_map_position(
                    item.sentence["MSG_LATTITUDE"],
                    item.sentence["MSG_LONGITUDE"],
                    text=time,
                    marker=True
                )

    def set_map_position(self, deg_x, deg_y, text=None, marker=True):
        self.map.set_position(deg_x, deg_y, text, marker)

    def add_lb_entry(self, entry):
        self.listbox.insert(self.listbox.size() + 1, str(entry))

    def clear_listbox(self):
        self.listbox.delete(1, self.listbox.size() + 1)

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
