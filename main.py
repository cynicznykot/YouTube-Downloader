import json
import yt_dlp

url = "https://www.youtube.com/watch?v=LXb3EKWsInQ"

opts = {}

with yt_dlp.YoutubeDL(opts) as ydl:
    info = ydl.extract_info(url, download=False)

print(info['title'])
print(info['duration'])
print(info['uploader'])


with open("info.json", "w", encoding="utf-8") as f:
    json.dump(info, f, ensure_ascii=False, indent=2)
print("\nSave in info.json")

print("\n--- All formats:", len(info['formats']), "---")
for f in info['formats']:
    print(f['format_id'], "|", f['ext'], "|", f.get('resolution'), "|",
          f.get('vcodec'), "|", f.get('acodec'))

print("\n--- Ready to download (video+audio) ---")
for f in info['formats']:
    if f.get('vcodec') != 'none' and f.get('acodec') != 'none':
        print(f['format_id'], "|", f['ext'], "|", f.get('resolution'))

print("\n--- Video only (no audio) ---")
for f in info['formats']:
    if f.get('vcodec') != 'none' and f.get('acodec') == 'none':
        print(f['format_id'], "|", f['ext'], "|", f.get('resolution'))

print("\n--- Audio only ---")
for f in info['formats']:
    if f.get('vcodec') == 'none' and f.get('acodec') != 'none':
        print(f['format_id'], "|", f['ext'], "|", f.get('resolution'))