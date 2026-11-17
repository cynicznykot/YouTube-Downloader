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

        