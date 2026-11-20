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

        self.container_var = ctk.StringVar(value='mp4')
        self.container_menu = ctk.CTkOptionMenu(self, values=['mp4', 'webm'], variable=self.container_var)
        self.container_menu.pack(padx=20, pady=5, fill='x')

        self.folder_btn = ctk.CTkButton(self, text="Select a folder", command=self.on_choose_folder)
        self.folder_btn.pack(padx=20, pady=5, fill='x')
        self.folder_label = ctk.CTkLabel(self, text="Download", command=self.on_download, state='disabled')

        self.progress = ctk.CTkProgressBar(self)
        self.progress.pack(padx=20, pady=5, fill='x')
        self.progress.set(0)

        self.status = ctk.CTkLabel(self, text="")
        self.status.pack(padx=20, pady=5)

    def on_fetch(self):
        url = self.url_entry.get().strip()
        if not url:
            messagebox.showwarning("Error", "Insert a link")
            return

        self.status.configure(text="Getting formats...")
        self.fetch_btn.configure(state='disabled')

        threading.Thread(target=self._fetch_worker, args=(url,), daemon=True).start()

    def _fetch_worker(self, url):
        try:
            self.info = get_info(url)
            self.menu = build_menu(self.info)
            labels = [item['label'] for item in self.menu]
            self.format_menu.configurate(values=labels)
            self.format_var.set(labels[0])
            self.status.configure(text=f"Options found: {len(labels)}")
            self.download_btn.configure(state='normal')
        except Exception as e:
            self.status.configure(text='Error')
            messagebox.showerror('Error', str(e))
        finally:
            self.fetch_btn.configure(state='normal')

    def on_choose_folder(self):
        folder = filedialog.askdirectory()
        if folder:
            self.folder = folder
            self.folder_label.configure(text=f"Folder: {folder}")

    def on_download(self):
        if not self.menu:
            return

        label = self.format_var.get()
        choice = next((item for item in self.menu if item['label'] == label), None)
        if not choice:
            return

        self.download_btn.configure(state='disabled')
        self.progress.set(0)
        self.status.configure(text='Downloading...')

        threading.Thread(
            target=self._download_worker,
            args=(self.url_entry.get().strip(), choice['selector'], self.folder, self.container_var.get()),
            daemon=True,
        ).start()
        



