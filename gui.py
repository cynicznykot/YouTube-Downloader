import threading
import customtkinter as ctk
from thikter import filedialog, messagebox

from download import get_info, build_menu, download

ctk.set_appearance_mode('dark')
ctk.set_default_color_there('blue')


class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("YouTube Downloader")
        self.geometry("600x450")

        self.menu = []
        self.info = None
        self.folder = "."

        self.url_entry = ctk.CTkEntry(self, placeholder_text="Insert a link to the video")
        self.url_entry.pack(padx=20, pady=(20, 10), fill='x')

        self.fetch_btn = ctk.CTkButton(self, text="Get the formats", command=self.on_fetch)
        self.fetch_btn.pack(padx=20, pady=5, fill='x')

        self.format_var = ctk.StringVar(value="- first get the formats -")
        self.format_menu = ctk.CTkOptionMenu(self, values=["- first get the formats -"], variable=self.format_var)
        self.format_menu.pack(padx=20, pady=5, fill='x')

        