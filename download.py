import os
import yt_dlp


def get_info(url):
    with yt_dlp.YoutubeDL({}) as ydl:
        return ydl.extract_info(url, download=False)


def build_menu(info):
    seen = set()
    menu = []

    for f in info['formats']:
        if f.get('vcodec') != 'none' and f.get('acodec') == 'none':
            h = f.get('height')
            if h and h not in seen:
                seen.add(h)
                size = f.get('filesize') or f.get('filsize_approx')
                size_str = format_size(size)
                menu.append({
                    'label': f"{h}p  (video only, will be merged with the audio)",
                    'selector': f"bestvideo[height<={h}]+bestaudio/best",
                })

    menu.append({
        'label': "audio only (best audio, m4a)",
        'selector': "bestaudio/best",
    })

    return menu

def download(url, selector, folder, container, progress_hook=None, subtitles=False, playlist=False):
    os.makedirs(folder, exist_ok=True)

    opts = {
        'format': selector,
        'outtmpl': f"{folder}/%(title)s.%(ext)s",
        "merge_output_format": container,
    }
    if progress_hook:
        opts['progress_hooks'] = [progress_hook]
    if subtitles:
        opts['writesubtitles'] = True
        opts['writeautomaticsub'] = True
        opts['subtitleslangs'] = ['ru', 'en']
    if playlist:
        opts['yes_playlist'] = True
    else:
        opts['noplaylist'] = True

    with yt_dlp.YoutubeDL(opts) as ydl:
        ydl.download([url])

def is_playlist(info):
    return info.get('_type') == 'playlist'

def playlist_entries(info):
    return info.get('entries', [])

def format_size(num_bytes):
    if not num_bytes:
        return "?"
    for unit in ('B', 'KB', 'MB', 'GB'):
        if num_bytes < 1024:
            return f"{num_bytes:.1f} {unit}"
        num_bytes /= 1024
    return f"{num_bytes:.1f} TB"



