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
                menu.append({
                    'label': f"{h}p  (video only, will be merged with the audio)",
                    'selector': f"bestvideo[height<={h}]+bestaudio/best",
                })

    menu.append({
        'label': "audio only (best audio, m4a)",
        'selector': "bestaudio/best",
    })

    return menu

def download(url, selector, folder, container, progress_hook=None):
    os.makedirs(folder, exist_ok=True)

    opts = {
        'format': choice['selector'],
        'outtmpl': "%(title)s.%(ext)s",
        "merge_output_format": 'mp4',
    }
    if progress_hook:
        opts['progress_hooks'] = [progress_hook]

    with yt_dlp.YoutubeDL(opts) as ydl:
        ydl.download([url])

