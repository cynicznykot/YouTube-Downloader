import json
import os
import subprocess
import threading

import customtkinter as ctk
from tkinter import filedialog, messagebox

from download import get_info, build_menu, download, is_playlist, playlist_entries

ctk.set_appearance_mode('dark')
ctk.set_default_color_theme('blue')


class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("YouTube Downloader")
        self.geometry("600x700")

        self.config_path = "config.json"
        self.settings = {'folder': '.', 'container': 'mp4'}
        if os.path.exists(self.config_path):
            with open(self.config_path, encoding='utf=8') as f:
                self.settings.update(json.load(f))
        self.folder = self.settings['folder']

        self.menu = []
        self.info = None
        self.is_playlist = False
        self.folder = "."

        self.url_entry = ctk.CTkEntry(self, placeholder_text="Insert a link to the video")
        self.url_entry.pack(padx=20, pady=(20, 10), fill='x')

        self.fetch_btn = ctk.CTkButton(self, text="Get the formats", command=self.on_fetch)
        self.fetch_btn.pack(padx=20, pady=5, fill='x')

        self.format_var = ctk.StringVar(value="- first get the formats -")
        self.format_menu = ctk.CTkOptionMenu(self, values=["- first get the formats -"], variable=self.format_var)
        self.format_menu.pack(padx=20, pady=5, fill='x')

        self.container_var = ctk.StringVar(value=self.settings['container'])
        self.container_menu = ctk.CTkOptionMenu(self, values=['mp4', 'webm'], variable=self.container_var)
        self.container_menu.pack(padx=20, pady=5, fill='x')

        self.subtitles_var = ctk.BooleanVar(value=False)
        self.subtitles_check = ctk.CTkCheckBox(
            self, text="Download subtitles (ru/en)", variable=self.subtitles_var
        )
        self.subtitles_check.pack(padx=20, pady=5, fill='x')

        self.folder_label = ctk.CTkLabel(self, text=f"Folder: {self.folder}")
        self.folder_btn = ctk.CTkButton(self, text="Select a folder", command=self.on_choose_folder)
        self.folder_btn.pack(padx=20, pady=5, fill='x')
        self.folder_btn = ctk.CTkLabel(self, text="Folder: current")

        self.download_btn = ctk.CTkButton(self, text="Download", command=self.on_download, state='disabled')
        self.download_btn.pack(padx=20, pady=5, fill='x')

        self.progress = ctk.CTkProgressBar(self)
        self.progress.pack(padx=20, pady=5, fill='x')
        self.progress.set(0)

        self.status = ctk.CTkLabel(self, text="")
        self.status.pack(padx=20, pady=5)

        self.open_folder_btn = ctk.CTkButton(
            self, text="Open folder", command=self.on_open_folder, state='disabled'
        )
        self.open_folder_btn.pack(padx=20, pady=5, fill='x')

        self.queue_frame = ctk.CTkScrollableFrame(self, height=150)
        self.queue_frame.pack(padx=20, pady=5, fill='both', expand=False)

        self.queue_btn = ctk.CTkButton(self, text="Add to queue", command=self.on_add_to_queue)
        self.queue_btn.pack(padx=20, pady=5, fill='x')

        self.start_queue_btn = ctk.CTkButton(self, text="Download the queue", command=self.on_start_queue)
        self.start_queue_btn.pack(padx=20, pady=5, fill='x')

        self.log_box = ctk.CTkTextbox(self, height=120)
        self.log_box.pack(padx=20, pady=(0, 15), fill='both', expand=True)
        self.log_box.configure(state='disabled')

        self.protocol("WM_DELETE_WINDOW", self.on_close)

        self.config_path = "config.json"
        self.config = {'folder': '.', 'container': 'mp4'}
        if os.path.exists(self.config_path):
            with open(self.config_path, encoding='utf-8') as f:
                self.config.update(json.load(f))
        self.folder = self.config['folder']


    def log(self, text):
        self.log_box.configure(state='normal')
        self.log_box.insert('end', text + '\n')
        self.log_box.see('end')
        self.log_box.configure(state='disabled')

    def build_playlist_menu():
        return [
            {'label': "1080p (all playlist)", 'selector': "bestvideo[height<=1080]+bestaudio/best"},
            {'label': "720p (all playlist)", 'selector': "bestvideo[height<=720]+bestaudio/best"},
            {'label': "audio only (all playlist)", 'selector': "bestaudio/best"},
        ]

    def on_close(self):
        self.settings['folder'] = self.folder
        self.settings['container'] = self.container_var.get()
        with open(self.config_path, 'w', encoding='utf-8') as f:
            json.dump(self.settings, f, ensure_ascii=False, indent=2)
        self.destroy()
        
    def on_fetch(self):
        url = self.url_entry.get().strip()
        if not url:
            messagebox.showwarning("Error", "Insert a link")
            return

        self.log("Getting formats...")
        self.fetch_btn.configure(state='disabled')

        threading.Thread(target=self._fetch_worker, args=(url,), daemon=True).start()

    def _fetch_worker(self, url):
        try:
            self.info = get_info(url)
            if is_playlist(self.info):
                entries = playlist_entries(self.info)
                self.menu = build_menu(self.info)
                self.menu = build_playlist_menu()
                self.is_playlist = True
                self.status.configure(text=f"Playlist: {len(entries)} video")
            else:
                self.is_playlist = False
                self.menu = build_menu(self.info)
                labels = [item['label'] for item in self.menu]
                self.format_menu.configurate(values=labels)
                self.format_var.set(labels[0])
                self.log(f"Options found: {len(labels)}")
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

        self.open_folder_btn.configure(state='disabled')
        self.download_btn.configure(state='disabled')
        self.progress.set(0)
        self.log(f"Selected: {label}")
        self.log('Downloading...')

        threading.Thread(
            target=self._download_worker,
            args=(self.url_entry.get().strip(), choice['selector'], self.folder, self.container_var.get()),
            daemon=True,
        ).start()

    def _download_worker(self, url, selector, folder, container):
        def hook(d):
            if d['status'] == 'downloading':
                total = d.get('total_bytes') or d.get('total_bytes_estimate')
                if total:
                    pct = d.get('downloaded_bytes', 0) / total
                    self.progress.set(pct)
                    self.status.configure(text=f"{pct*100:.1f}%")
            elif d['status'] == 'finished':
                self.log("Downloaded, merging...")

        try:
            download(
                url, selector, folder, container,
                progress_hook=hook,
                subtitles=self.subtitles_var.get(),
                playlist=getattr(self, 'is_playlist', False)
            )
            self.status.configure(text='Done!')
            self.open_folder_btn.configure(state='normal')
        except Exception as e:
            self.log(f"Error: {e}")
            messagebox.showerror("Error", str(e))
        finally:
            self.download_btn.configure(state='normal')

    def on_open_folder(self):
        subprocess.Popen(["xdg-open", self.folder])

    def on_add_to_queue(self):
        url = self.url_entry.get().strip()
        if not url:
            messagebox.showwarning('Error', "Insert a link")
            return
        if not self.menu:
            messagebox.showwarning('Error', "First get the formats")
            return

        label = self.format_var.get()
        choice = next((item for item self.menu if item['label'] == label), None)
        if not choice:
            return

        task = {
            'url': url,
            'selector': choice['selector'],
            'container': self.container_var.get(),
            'status': 'waiting',
            'progress': 0.0,
        }
        self.queue.append(task)
        self.refresh_queue_view()
        self.log(f"Added to the queue: {url}")

    def refresh_queue_view(self):
        for w in self.queue_frame.winfo_children():
            w.destroy()

        for i, task in enumerate(self.queue, start=1):
            row = ctk.CTkFrame(self.queue_frame)
            row.pack(fill='x', pady=2)

            text = f"[{i}] {task['status']} {int(task['progress']*100)}% {task['url'][:50]}"
            ctk.CTkLabel(row, text=text, anchor='w').pack(side='left', fill='x', expand=True)

            bar = ctk.CTkProgressBar(row, width=120)
            bar.set(task['progress'])
            bar.pack(side='right', padx=5)

    def on_start_queue(self):
        if not self.queue:
            messagebox.showinfo('Queue', "Queue is empty")
            return
        self.start_queue_btn.configure(state='disabled')
        threading.Thread(target=self._queue_worker, daemon=True).start()

    def _queue_worker(self):
        try:
            for task in self.queue:
                if task['status'] != 'waiting':
                    continue
                task['status'] = 'downloading'
                self.refresh_queue_view()
                self.log(f"Downloading: {task['url']}")

                def hood(d, t=task):
                    if d['status'] == 'downloading':
                        total = d.get('total_bytes') or d.get('total_bytes_estimate')
                        if total:
                            t['progress'] = d.get('downloaded_bytes', 0) / total
                            self.refresh_queue_view()
                        elif d['status'] == 'finished':
                            t['progress'] = 1
                            self.refresh_queue_view()

                try:
                    download(
                        task['url'], task['selector'], self.folder, task['container'],
                        progress_hook=hook,
                        subtitles=self.subtitles_var.get(),
                        playlist=False,
                    )
                    task['status'] = 'done'
                except Exception as e:
                    task['status'] = 'error'
                    self.log(f"Error: {e}")

                self.refresh_queue_view()
            self.log("Queue completed")
        finally:
            self.start_queue_btn.configure(state='normal')


if __name__ == "__main__":
    App().mainloop()



