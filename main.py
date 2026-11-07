import yt_dlp

url = "https://www.youtube.com/watch?v=LXb3EKWsInQ"

opts = {}

with yt_dlp.YoutubeDL(opts) as ydl:
    info = ydl.extract_info(url, download=False)

print(info['title'])
print(info['duration'])
print(info['uploader'])

print("\n--- All formats:", len(info['formats']), "---")
for f in info['formats']:
    print(f['format_id'], "|", f['ext'], "|", f.get('resolution'), "|",
          f.get('vcodec'), "|", f.get('acodec'))

