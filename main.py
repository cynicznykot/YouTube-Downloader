import yt_dlp

url = "https://www.youtube.com/watch?v=LXb3EKWsInQ"

opts = {}

with yt_dlp.YoutubeDL(opts) as ydl:
    info = ydl.extract_info(url, download=False)

print(info['title'])
print(info['duration'])
print(info['uploader'])

